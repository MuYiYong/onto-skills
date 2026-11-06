# 学习成就凭证证据核对：投影与验收

标准基线：1EdTech Open Badges 3.0 文档1.4.5；W3C VC Data Model 2.0。三个文件分别是[合成输入](input.json)、[数据库中立图规格](graph-model.json)、[手工预期](acceptance.json)。共有15个手工期望案例，开发侧参考计算消费投影字段；没有原生IFC/完整SensorThings/签名凭证校验。

图规格为设计草案，未选数据库版本，有明确unresolved。JSON结构通过不代表部署就绪。图模型是可复用设计；input.json只覆盖下面明确列出的案例投影，未构造所有SourceRecord、属性断言与边实例，不声称做过完整入库往返。

## 原始字段到本地投影

| 本地字段 | 标准字段或来源 | 取舍与损失 |
| --- | --- | --- |
| id / issuer_id / subject_id | AchievementCredential.id / issuer.id / credentialSubject.id | 固定VC2子集，不支持所有identifier与holder证明。 |
| achievement_id / creator_id / evidence | credentialSubject.achievement.id / achievement.creator.id / evidence | 原始成就、条件和证据完整内容见源；例子仅引用，未核实URL内容。 |
| validFrom / validUntil | VC2 §4.9 / OB B.1.2 | 不从旧issuanceDate直接补写；本例半开边界为明确本地政策。 |
| credential_status_id | credentialStatus.id | 只保留机制入口；无状态查询/列表解码。 |
| reports[].credential_content / artifact | 本地报告的内容绑定 | 合成例子直接比较投影内容；实际必须绑定原始签名字节的散列/标识和校验方法。 |
| reports[].schema / proof / status / simulated | 外部验证报告投影 | 所有报告为模拟，未运行任何真实签名/标准校验；pass不能被转述为已验签。 |
| policy / candidate_for_review | 本地信任、时点、新鲜度和机构复核 | 不代表事实真伪、当前能力或学分学历认可。 |

## 能力问题与反例

| 问题 | 关键模型元素 | case_id |
| --- | --- | --- |
| 哪些明确学习者的凭证有内容绑定且足够新鲜的核查报告？ | CredentialRecord / VerificationReport / REPORT_FOR | reported-checks-pass, no-report, changed-payload, wrong-status-target, late-report, stale-status |
| 未知、撤销、过期或同ID冲突时为何不能声称验证通过？ | RecognitionReview / CredentialRecord / SourceRecord | revoked, unknown-status, proof-failed, expired, future-validity, conflicting-credential, duplicate-receipt |
| 成就创建者、凭证发行者、证据来源与机构认可如何区分？ | Issuer / LearnerIdentity / AchievementDefinition | wrong-subject, untrusted-issuer |

结果必须带可定位的源版本、标准支持范围、本地政策和不足。名称相似度或一个质量总分不能绕过必需证据。对未支持的原生字段或不完整输入给出补证要求，不静默丢弃。
