# 医疗照护路径数据建模与离线验收方法

本方法是项目原创图映射建议；[来源目录](sources.json) 索引发布版 HL7® FHIR® R4 4.0.1。资源及官方选定规则见 [领域摘要](domain.json)。R5 或开发版本须另做差异分析。下面的 quantitative/completed/retraction/authorization 口径均是本例本地政策，不能写成临床/法律要求。

## 一、业务事实、身份与版本

| 概念 | 独立身份和关键区别 |
| --- | --- |
| Patient | `namespace + patient_key` 为目的范围内的合成假名，不是全球患者 ID |
| PatientIdentityLink | 独立 decision id；记录 source Patient logical URL、evidence、decision 与 purpose authorization |
| ResourceVersion | canonical source server + resourceType + id + opaque meta.versionId；携带原始快照/hash、current authority、lastUpdated 与 intake recorded_at |
| Encounter | 某源 Encounter 版本的就诊上下文；重复就诊不折叠，finished 不等于所有请求已完成 |
| Order | 某 ServiceRequest 版本，status/intent/authoredOn/occurrence 与已执行事件分开 |
| Observation | 某结果版本，status、原始 coding/value/dataAbsentReason、effective 与 issued 独立 |
| Procedure | 某活动记录版本，包括 not-done；仅 completed 进入本例完成视图 |
| Condition | 某问题断言版本；clinicalStatus 与 verificationStatus 分离，无自动诊断 |
| Provenance | 某证据记录版本；target 精确到源版本，recorded 不等于临床发生/患者授权 |

源 base URL 在 intake 时按系统清单固定；不可任意小写 URL path、删改业务 id 或跨服务器合并相同 id。例子的 version key 是规范 source base 加 `/ResourceType/id/_history/versionId`，逻辑 key 不含 `/_history/...`。真实系统必须验证 FHIR id/versionId 与引用语法；缺版本不可用占位字符串冒充。

每个 typed 资源节点都对应同 key 的 ResourceVersion；Patient 是特意分开的假名。只为 accepted、有非空获批 evidence 且 authorized_for_purpose 的 crosswalk 建 Patient 关联。demographics/contact 不能证明患者相同。版本快照不可覆盖：相同 key、相同 canonical payload 重放幂等；相同 key、不同 payload 拒绝。新版本不新增一次临床事件；不同真实资源 id 不能因内容相似而去重。

current 由有证据的源声明确定。每 logical key 至多一个 current；无法确定时不选数值最大/最新入库的 versionId。`v2` 在示例恰是 current，不代表这个字符串可排序。元数据 FHIR release、记录版本与术语版本是三个不同维度。

## 二、引用和边

subject、encounter、basedOn 和 provenance target 均从显式源引用产生；无字段不推导。绝对 versioned 引用使用精确快照；相对 versionless 引用以 envelope source_server 为 base，选本次 as_of/intake 时源权威 current，并在边保存 source_path、original_reference、resolved_version_key、recorded_at。跨服务器引用必须有明确 base；未知目标不创建事实边。多次引用与重复事件的边键含源版本/字段/index/目标，不能只按端点去重。

同一个患者或时间接近不证明 encounter 或 basedOn 关系。版本到 typed 节点的边只是项目投影；FHIR 不要求该属性图结构。原始 Patient 资源保存在 ResourceVersion，PatientIdentityLink 才把它关联到项目 Patient 假名。

## 三、状态、时间和数量

- R4 ServiceRequest 的取消状态是 `revoked`。Order 不制造 Procedure；Procedure `not-done` 仍是可审计记录，完成数为 0。已经有独立 completed Procedure 时，之后撤销请求不会抹去已发生的记录。完成统计只表达“源文档记录完成”，不推断效果。
- Observation `entered-in-error` 是官方无效边界。本例 quantitative policy 还要求 current 且 final/amended/corrected、数值 valueQuantity、无 comparator、一组明确选定的已知 coding system/version/code、已知 unit system/code。被排除的记录仍可在审计历史中存在。若本地允许初步结果另行显示，必须另定视图，不能悄悄改此政策。
- 无 Observation → missing-result；有 Observation 但 dataAbsentReason unknown → unknown-value；unknown status → unknown-status；preliminary → provisional。上述均不代表阴性、正常、0 或“未患病”。根 value[x] 加 dataAbsentReason 违反官方选定 obs-6，隔离并报错，不修复数据。
- 保留 authoredOn、occurrence[x]、performed[x]、effective[x]、issued、Condition onset/recordedDate、Provenance.recorded、meta.lastUpdated、项目 recorded_at。原始 choice/精度/时区用 raw 字段保存。示例 Condition onset 是 `2026-10-01`，保持日期精度，不生成午夜。标准 datetime 属性只用于源中确有完整瞬时值的字段。
- 比较必须同 Coding.system/version/code 与 Quantity.system/code。空/未知版本阻止比较；不同 unit/code 阻止聚合，未开启单位转换。离线参考计算只处理单个完整 coding；多 coding 未给出选择证据时阻止比较，不能任取第一个。单位显示文本不作为等价证据。比较器 `<` 等不能当精确数值，原始 comparator 保留。本例 6 mg/L + 7 mg/L = 13 是合成数据算术，不给出临床正常范围或解释。
- Condition 的 unconfirmed 保持未确认；con-4/con-5 局部核对不能冒充全量资源验证。Observation 不能自动生成 Condition。

## 四、证据、撤回与授权

Provenance 说明资源版本如何产生/修订，不等于 Procedure，也不代表数据主体同意或系统访问授权。源 entered-in-error 自动进入本例无效分类；另行 view retraction 要 authorized=true、非空 evidence_id 和确切存在的 version key 才应用。撤回保留被授权保留的历史，不回退旧版本作 current。versionless 撤回或未授权指令拒绝，不能因新增一条 Provenance 就改临床事实。

本例 purpose_approved=true 只针对离线合成建模；disclosure_approved=false 时输出 released_record_count=0。实际部署必须另选目的、授权、最小化、保留和披露治理；本包没有权限引擎，也不声称匿名化、医学质量或法规符合。

## 五、验收文件契约 operations-v1

[验收 JSON](../examples/acceptance.json) 每个 case 包含 id/classification/source_ids/input/expected/reason。每例从 [input.json](../examples/input.json) 的全新副本执行；`fixture` 只指同目录文件。`mutations` 用 resource_type/resource_id 与点路径 `set` 覆盖当前资源字段（数字路径用于数组）。它们是受控反例，不是新认证的源版本。`replay_version_key` 重放相同 envelope；`conflicting_replay` 重放同 key 不同 payload。测试计算只是离线例子验证，不是发布的医疗/知识 runtime。

| operation | 输入选择 | 具体 expected 含义 |
| --- | --- | --- |
| completed_procedures | order_id，默认 server A；可覆写 order 状态 | current Procedure 有 basedOn 指定 ServiceRequest 且 status=completed 的 version keys 与 count；有 not-done 时另列 documented_not_done_keys；不根据 Order 状态制造/删除完成 |
| observation_state | observation_id，默认 server A | 权威 current version_key、state、quantitative_eligible、normality 恒为 not-assessed；entered-in-error 优先于 value 分类 |
| order_result_state | order_id | 当前 Observation 的明确 basedOn 引用集合；空集合 state=missing-result、negative_result=null |
| identity_inventory | 可精确 replay | 去重后的资源版本数、logical 资源数、Patient 假名数、Encounter id 集、Observation 全版本/current 数及 obs-1 历史/current key |
| identity_decision | attempt_id | 无 approved crosswalk evidence 的 shared-contact 候选 merge_authorized=false，两个患者假名不合并 |
| compare_observations | 两个 observation_ids | current version keys；先判 eligibility，再判 coding tuple，再判 unit tuple；通过才给 aggregate_value。coding/unit mismatch 为可核验 reason_code；不计算转换或医学解释 |
| validate_intake | mutations/conflicting replay | accepted 与 error_codes，检查冲突 version payload、obs-6 及 source current 冲突；不宣称全量 FHIR 验证 |
| retraction_decision | instruction.target_version_key/authorized/evidence_id | 仅 authorized + evidence + exact existing version 才 applied；excluded keys、保留全部历史 keys 与 fallback_to_prior_version=false |
| disclosure_decision | fixture.authorization | 独立披露授权与目的均成立才可披露；默认 false，released_record_count=0 |

expected 中的 null 表示未作该结论，不是 false/0；ID 列表按字典序排序用于稳定比较。已知的 primary-source 约束与本地策略分别由案例 reason/source_ids 说明。完整模型包含 unresolved，因此本例是完整结构的设计草案，不是 ready-to-deploy 认证。真实目标数据库/版本、运行检查、术语/扩展和安全策略须另行验证。

请求否定修饰也必须保留：ServiceRequest.doNotPerform=true 表示禁止该服务，不能把其 code 当作正向执行指令。R4 缺失时的默认含义是正向请求；保存原字段缺失与语义解释的区别。未识别的 modifierExtension 应先隔离/评审，不能因保留原 JSON 就进入已理解的事实视图。
