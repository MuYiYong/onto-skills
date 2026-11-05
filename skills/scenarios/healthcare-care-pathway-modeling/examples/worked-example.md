# 完整示例：两次就诊的请求、活动与结果版本

此例只使用虚构数据及 `.example.invalid` 来源地址。局部代码 `assay-A` 和 `training-concern-A` 不映射到 ICD、LOINC 或 SNOMED CT，无临床诊断、检验解释或治疗建议。

## 输入和问题

读取 [合成导出](input.json)：两个机构的 Patient 资源通过各自已批准的合成 crosswalk 映射为两个患者假名；它们仅共享一个虚构 household signature 时仍不合并。A 的患者有 enc-1、enc-2 两次就诊。资源总计 20 个版本、19 个 logical resources，包含 2 个 Patient、2 个 Encounter、5 个 ServiceRequest、6 个 Observation 版本、2 个 Procedure、1 个 Condition、2 个 Provenance。

问题是“哪些请求有明确完成文档、哪些结果可用于本地数值视图、纠正和无效记录如何保留证据”。[图规格](graph-model.json) 给出 9 类节点、20 类关系、12 条约束和逐项映射损失。target 未选数据库；unresolved 保留真实部署需要的版本、授权、扩展/术语及治理决策。

## 关键结果

| 场景 | 预期结果与理由 |
| --- | --- |
| ord-1 + proc-1 completed | 有明确完成文档 count=1；basedOn 来自源引用 |
| ord-2 revoked + proc-cancelled not-done | 完成 count=0；未执行文档仍保留，不造 completed Procedure |
| 把 ord-1 改为 revoked 的反例 | proc-1 仍是独立完成记录，count=1；不删除已记录事实 |
| obs-1 v1=5 → current v2 corrected=6 mg/L | 两个版本保留，当前只选 v2；不把 5+6 当两次测量 |
| obs-error entered-in-error=99 | quantitative_eligible=false；保留审计，不作测量 |
| ord-3 无 Observation | missing-result，negative_result=null |
| obs-unknown final、无值、dataAbsentReason unknown | unknown-value，normality=not-assessed |
| obs-unit=0.5 g/L 与 obs-1=6 mg/L | unit-mismatch，aggregate_value=null；不默换单位 |
| obs-repeat=7 mg/L 与 obs-1=6 mg/L | 同 coding/version/unit 时离线算术=13；无临床解释 |
| 改 obs-repeat coding.version | coding-mismatch，阻止合计 |
| 重放 obs-1 v2 | 仍为 20 版本；相同 key 不同 payload 则拒绝 |
| obs-repeat 同时有值和 dataAbsentReason | 拒绝，error=obs-6-value-and-absent-reason，不修复 |
| 已授权、精确 v2 撤回 | 排除 v2，保留 v1/v2 历史，不回退 v1 为当前 |
| 未授权撤回或独立披露未批准 | 不应用撤回；不释放记录 |

## 时间、边和损失

obs-1 v2 的 effectiveDateTime 是 2026-10-01 09:00Z，issued 是 2026-10-02 10:00Z，入库是 2026-10-04 12:00Z，不能用报告/入库时间重排生理事件。Condition.onsetDateTime 只给 `2026-10-01`，不补午夜；verificationStatus=unconfirmed，不标确诊。

每个 basedOn/encounter/subject 引用解析都应保存源路径、原引用、选定版本和入库时刻。Provenance 的 revision target 指向具体版本，只表达文档修订。Patient→患者假名是 approximated；完整 profile、modifierExtension、术语绑定、签名、安全/同意属于 unmapped，原始快照不补齐这些语义。

[17 个验收案例](acceptance.json) 的 expected 给出精确 ID/计数，由 [方法契约](../references/method.md) 定义操作。它们验证离线输入的有限语义；不证明医学正确性、完整 FHIR 符合性、数据库执行、CC-Switch GUI 或 macOS 行为。
