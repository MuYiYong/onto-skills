# 医疗健康本体知识与照护路径数据建模组合

此目录是文档组合指南，不是安装器、解析器、registry 或运行时。两个可直接安装且互不依赖的 Skill：

- [healthcare-domain-knowledge](../../skills/industries/healthcare-domain-knowledge/SKILL.md)：厘清医疗数据概念、状态/时间/标识、固定版本标准与映射损失。
- [healthcare-care-pathway-modeling](../../skills/scenarios/healthcare-care-pathway-modeling/SKILL.md)：按具体问题交付完整数据库中立图模型和正反例；照护路径指事实血缘，不是治疗方案。

可选组合时，前者交付概念/来源/映射/未知表，后者以显式输入继续建模；不依赖另一个包路径或隐式上下文。首次即可仅安装任意一个并使用包内资源。[中心合成例](../../examples/healthcare/README.md) 展示撤销、未执行、结果纠正、录入错误、未知/缺失、重复就诊、身份与单位边界。

知识基线为发布版 HL7® FHIR® R4 4.0.1，明确不是最新发布版；不混用 R5/开发构建。保留 source server/type/id/versionId，与患者假名/术语版本分开。无真实患者数据、第三方标准副本或临床术语表，不输出诊疗建议，不声明医学、法规或完整 FHIR 符合性。

需要数据库语句时，另行向数据库能力交付中立模型、目标版本及不可变语义；本组合不提供 GQL 语法、连接数据库或运行临床决策。每个包附项目 MIT LICENSE，第三方来源按其原条款；HL7/FHIR 为 Health Level Seven International 的注册商标，本项目不获其背书。
