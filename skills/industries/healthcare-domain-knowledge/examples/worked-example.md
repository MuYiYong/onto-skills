# 合成例：请求、活动与结果不能互相替代

输入：一个教学系统导出以下部分字段。所有标识和数值均为虚构，无真实患者；代码 `assay-A` 属于本地 `https://onto-skills.example.invalid/codes/training` 的 `training-1` 版本，不是标准检验术语。

| 记录 | 已提供事实 | 可支持的数据结论 |
| --- | --- | --- |
| Patient/pa，server A，v1 | 被授权的 crosswalk-a → synthetic-p-001 | 在 offline-training 范围建立身份关联；pa 本身不是全球患者身份 |
| Encounter/enc-1 与 enc-2 | 同一患者的两次独立就诊 | 保留两个就诊，不按患者/日期近邻折叠 |
| ServiceRequest/ord-1 | completed、intent=order | 请求的状态；仍需独立 Procedure 证明活动记录 |
| Procedure/proc-1 | completed、basedOn ord-1 | 此项目“有完成记录”口径计 1；不推断疗效 |
| ServiceRequest/ord-2 | revoked | R4 撤销请求；不能建立一个 completed Procedure |
| Procedure/proc-cancelled | not-done、basedOn ord-2 | 有未执行文档；完成数为 0 |
| Observation/obs-1 v1 → v2 | final 5 mg/L → corrected 6 mg/L | 保存两版本；权威 current=v2 时当前值为 6，不求和为 11 |
| Observation/obs-error | entered-in-error，value=99 | 保留无效版本供审计，不进可用数值视图 |
| Observation/obs-unknown | final，dataAbsentReason=unknown，无值 | 未知值；不判正常、阴性或 0 |
| ServiceRequest/ord-3 | active，无结果资源 | 结果缺失；不等于阴性 |
| Observation/obs-unit | 同代码，0.5 g/L | 与 mg/L 的合计被阻断；未获批转换不自行换算 |
| Condition/concern-1 | verificationStatus=unconfirmed | 记录未确认问题；不提升为确诊 |

判断中“请求/观测/活动资源及状态”来自 [固定版本来源](../references/sources.json)；跨系统 crosswalk、数值使用门槛和聚合政策是 [项目方法](../references/method.md)。若 B 系统 Patient/pb 与 pa 仅共享虚构联系方式，保持 synthetic-p-002 独立，输出“缺少经授权身份交叉证据”。

交付样例：概念表列出 PatientRecord、PatientPseudonym、Encounter、RequestedAct、DocumentedActivity、VersionedObservation、RecordedConcern 和 Provenance；每行记录源字段、身份和时间。映射表将 Patient→患者假名标 approximated，将未实现的 modifierExtension、完整术语绑定和签名标 unmapped。既不从检验值推出 Condition，也不声称该表完成了 FHIR 符合性认证。
