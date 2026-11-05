# 医疗数据知识核对方法

本方法是原创建模建议。官方来源见 [来源目录](sources.json)，版本固定为发布版 HL7® FHIR® R4 4.0.1；不采用 build.fhir.org 开发定义。当地实施指南、术语和授权政策由任务另行指定。

## 从问题到最少概念

先问“要解释哪一条数据事实”：请求是否存在、执行是否有记录、结果何时可用、某条断言是否仍可用，属于不同问题。患者有不同机构的资源记录；一次就诊可关联多个请求、执行和结果。尽量用属性保留简单字段；只有生命周期、独立身份或证据需要时再建节点。

可直接填写以下概念行，不需要外部模板：

| 字段 | 必填含义 |
| --- | --- |
| concept_id / local_name | 稳定的项目概念 ID 与业务名称，不伪造标准 IRI |
| definition / excluded_inferences | 概念描述与该事实不能证明什么 |
| identity_scope / key | 来源服务器、资源类型、业务/记录 id、患者映射范围及版本策略 |
| status / times | 状态来源、未知处理，以及各时间的事件意义、精度和时区 |
| source_ids / classification | 明确使用本包来源 ID；official-standard、project-curated 或 model-inference |
| mapping / loss / validation | preserved/approximated/unmapped、未表达语义与验收反例 |

## 需要明确判断的边界

1. **身份。** FHIR resourceType/id 与服务器 base URL 共同定位资源；meta.versionId 定位记录版本。Patient.identifier 是业务标识，患者假名是项目范围的映射结果，四者不可互换。相同姓名、出生信息或共享联系信息只能形成待核实候选，不能授权合并。缺失版本时先提出单独的 intake-snapshot 策略，不把 ingest timestamp 伪造成 FHIR versionId。
2. **生命周期。** ServiceRequest.intent 与 status 描述请求；Procedure.status 描述活动记录。R4 revoked 表示被撤销请求，但独立完成的活动可能已经发生。completed Procedure 是本示例“有完成记录”口径；它不证明疗效，也不能仅凭一个完成请求推导。
3. **结果。** entered-in-error 在官方 Observation 语义中使该记录无效；unknown、无值、无结果和未完成各自保留。官方 obs-6 不允许根 value[x] 与 dataAbsentReason 并存。项目 quantitative view 另要求 current final/amended/corrected 数值、完整 coding 和 coded unit；这是保守的数据使用政策，不是临床有效性标准。
4. **断言。** Condition 的 clinicalStatus 与 verificationStatus 独立。unconfirmed 不等于 confirmed；不能从数值或别的资源推导确诊。对明确涉及的 con-4/con-5 做局部约束核对，不能宣称全量 FHIR 验证。
5. **时间。** 保留 authoredOn、occurrence[x]、performed[x]、effective[x]、issued、onset[x]、recordedDate、Provenance.recorded、meta.lastUpdated 与项目入库时间各自意义。部分日期和 Age/Range/string 等 choice 类型保持原型；不填午夜或用报告时间代替测量时间。
6. **代码和单位。** 保留所有 Coding.system/version/code 和源显示值；缺版本为未知。Quantity 保留 value、comparator、unit、system、code 与原精度。可比较性需明确同一术语意义、数量维度及获批转换；本包默认不转换。ICD/LOINC/SNOMED 需来源、版本、许可和任务核实，本包不分发其代码表。
7. **证据和授权。** Provenance 表达记录来源和变更过程，不是一次医疗执行，不授予读取/披露权限。撤回有效视图要有可验证的授权、精确版本及原因；历史按获批保留策略处理，不能因撤回恢复旧结果。图模型本身不实现授权、同意、匿名化或合规。

## 输出证据与未知

每个交付结论写出：结论、证据字段、来源版本、分类、适用范围、反例和未决条件。保留本地术语与原标准概念的对应关系，不把项目图模型称为官方医疗本体。原始 JSON 保存只提供审计线索，不代表理解了扩展、修饰扩展、实施指南、签名和术语绑定。

若后续需要数据库语句，提供中立模型、目标数据库/版本及不允许改变的语义，交给另行获得的数据库工具；本包不提供 GQL 语法或数据库执行器。

请求否定修饰也必须保留：ServiceRequest.doNotPerform=true 表示禁止该服务，不能把其 code 当作正向执行指令。R4 缺失时的默认含义是正向请求；保存原字段缺失与语义解释的区别。未识别的 modifierExtension 应先隔离/评审，不能因保留原 JSON 就进入已理解的事实视图。
