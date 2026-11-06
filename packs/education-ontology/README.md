# 教育与学习凭证 Ontology Pack

供数据治理、本体设计和业务复核人员使用，围绕学习成就凭证证据核对。基线：1EdTech Open Badges 3.0 文档1.4.5；W3C VC Data Model 2.0，本地规则逐项标明。Pack只有组合说明，每个Skill可单独安装，不存在运行依赖。

| 推荐步骤 | Skill | 交付 |
| --- | --- | --- |
| 理清行业 | [education-domain-knowledge](../../skills/industries/education-domain-knowledge/SKILL.md) | 概念/字段/标准依据与缺口 |
| 细化场景 | [learning-credential-verification](../../skills/scenarios/learning-credential-verification/SKILL.md) | 完整证据图与正反例 |
| 按需建模 | [ontology-modeling](../../skills/core/ontology-modeling/SKILL.md)、[property-graph-mapping](../../skills/core/property-graph-mapping/SKILL.md) | 概念边界、映射损失 |
| 按需复核 | [ontology-validation](../../skills/core/ontology-validation/SKILL.md) | 约束、证据和待决项 |

可从任何一步开始，仅安装当前需要的目录。端到端输入、图模型、手工预期见[完整例子](../../examples/education/README.md)。需要数据库实现时，另选目标与版本并使用已验证外部能力；例如[nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)，具体安装和能力核实见[安装说明](../../docs/installation-guide.md)。本包不复制外部语法资源。
