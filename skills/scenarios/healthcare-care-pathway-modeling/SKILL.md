---
name: healthcare-care-pathway-modeling
description: 为医疗照护路径的数据追踪设计数据库中立图模型，区分患者身份、重复就诊、医嘱请求、实际执行记录、观测结果版本、健康问题断言和证据来源。用于 FHIR R4 数据血缘、撤销请求/录入错误/缺失结果/单位不一致及版本纠正建模；不输出临床治疗路径、自动诊断、完整 FHIR 认证或生产操作。
license: MIT
---

# healthcare-care-pathway-modeling

## 定位与问题

将脱敏医疗业务数据组织为“谁、哪次就诊、请求了什么、实际记录了什么、结果哪个版本、证据在哪里”的可审计模型。这里的照护路径指数据事实与血缘，不生成临床诊疗方案。基线是明确固定的 HL7® FHIR® R4 4.0.1；它不是最新 FHIR 发布版，不混用 R5 或开发构建。HL7 与 FHIR 是 Health Level Seven International 的注册商标，使用不表示其背书。

本包独立可用，方法、知识、Schema、例子与来源均在包内。未安装其他技能或无网络不会阻断基于已有材料的基本设计。

## 输入

最少：数据问题、允许使用的脱敏/合成字段与来源范围。为可核验模型提供：FHIR 版本、来源 server/type/id/versionId、患者映射证据、就诊和 basedOn 引用、状态、原始时间、coding/version、quantity/unit、版本 current 依据及授权目的。未知项进入 unresolved，不静默补齐。可选：本地实施指南、术语映射、获批单位转换、保留/撤回与披露政策。

## 工作流程

1. 固定范围、as_of、目的与允许的输入；不读取患者系统或请求真实身份秘密。明确交付数据模型而非医疗决定。
2. 读 [领域知识](references/domain.json) 及 [来源](references/sources.json)，按 [建模和验收方法](references/method.md) 区分官方约束、项目图映射与当地政策。
3. 为源资源和不可排序的 versionId 设计稳定身份；另建目的范围内患者假名和带证据 identity link。重复就诊、重复真实事件、纠正版本保留；精确重放幂等，冲突快照拒绝。
4. 设计 Patient、PatientIdentityLink、ResourceVersion、Encounter、Order、Observation、Procedure、Condition、Provenance；按业务需要减少或扩展，说明差异。只根据明确引用建立 subject/encounter/basedOn/provenance 边，解析到精确版本并记录证据。
5. 写状态、时间和使用规则：撤销请求不变成执行；not-done 不计完成；entered-in-error 不作有效测量；无值/无结果不判阴性或正常。独立记录 authored/requested/performed/effective/issued/source recorded/lastUpdated/intake 时间。
6. 保留 coding system/version/code、单位和 comparator；仅在获批规则下比较/转换。Condition 保留断言状态，不能从观测数值推导诊断。精确版本撤回不得误删历史或回退到旧有效值。
7. 依据 [规格说明](references/graph-model-specification.md) 与 [Schema](references/graph-model.schema.json) 输出完整 Graph Model Specification；逐项说明 preserved/approximated/unmapped 及风险，保留 unresolved。
8. 用 [合成输入](examples/input.json)、[可核验模型](examples/graph-model.json) 和 [正反例](examples/acceptance.json) 检查身份、请求/执行、结果版本、单位、授权与撤回，形成可独立审阅的证据；见 [完整示例](examples/worked-example.md)。静态检查与真实运行证据分开报告。

## 输出

范围/目的/as_of/版本与假设；概念、节点/边、属性、身份、时间与来源；完整图规格；状态与 current-view 使用口径；字段映射及损失；引用解析证据；正反例输入及具体预期 ID/计数；未决事项与验证范围。没有足够证据时明确输出 missing、unknown、unresolved 或 rejected，不伪造事实。

## 质量检查与限制

资源 id 不当患者假名，版本不按字典序选最新，源状态不被视图政策覆盖。每条关系能还原源字段与解析版本。每个重要判断带来源 ID 与分类；图规格的官方来源不把项目建模决策变成规范。保留原始数据并不实现 FHIR 扩展、实施指南、术语绑定、授权/同意或签名语义。

本包不运行医疗决策、不写数据库、不提供 GQL 方言、无合规认证。若用户另要数据库语句，交付中立规格、目标数据库/版本、原始语义及不可变约束，转给外部数据库能力进行核实；不要求其他 Skill 作为基本依赖。原始资产见 [MIT 许可证](LICENSE)；第三方标准与商标保留原条款。

## 标准依据与缺口

先核实包内来源与知识条目的standard_basis：固定发布机构、版次、具体定位和支持范围，再形成项目解释。standard_gap保留未核实映射、本地政策和补证路径；本地键、阈值或判定公式不因引用标准就成为官方定义。任务缺少适用版本或来源时交付不依赖缺口的部分，并明确待核实项。

交付时读取条目的standard_status：standard-backed仅表示standard_basis.scope内有已核实标准依据，其他本地规则仍按standard_gap保留；nonstandard-modeling明确标为“非标准建模”，标准未取得或精确映射未核实的原因一并列出。不得把背景页、目录或来源分类当成条目符合性。
