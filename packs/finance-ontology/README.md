# Finance Ontology Pack

为金融知识工程师、图模型设计者和需要金融业务理解的 Agent 提供从需求到属性图本体的组合说明。适用于信贷、账户、授信、贷款、担保及风险网络建模；Pack 是文档，没有安装或管理逻辑。

## 内部 Skills 与建议顺序

| 步骤 | Skill | 职责 |
| --- | --- | --- |
| 1 | [industry-knowledge-discovery](../../skills/core/industry-knowledge-discovery/SKILL.md) | 术语/来源/缺口 |
| 2 | [finance-domain-knowledge](../../skills/finance/finance-domain-knowledge/SKILL.md) | 金融概念与角色 |
| 3 | [banking-business-model](../../skills/finance/banking-business-model/SKILL.md) | 银行业务流程/实体 |
| 4 | [credit-risk-knowledge](../../skills/finance/credit-risk-knowledge/SKILL.md) | 风险口径与时效 |
| 5 | [ontology-modeling](../../skills/core/ontology-modeling/SKILL.md) | 概念模型与边界 |
| 6 | [entity-relationship-modeling](../../skills/core/entity-relationship-modeling/SKILL.md) | 身份/关系/基数 |
| 7 | [fibo-ontology](../../skills/finance/fibo-ontology/SKILL.md) | 标准裁剪与业务扩展 |
| 8 | [property-graph-mapping](../../skills/core/property-graph-mapping/SKILL.md) | 属性图与图规格 |
| 9 | [ontology-validation](../../skills/core/ontology-validation/SKILL.md) | 语义与结构复核 |
| 按需 | [multi-lending-detection](../../skills/scenarios/multi-lending-detection/SKILL.md) | 多机构有效负债与关联 |
| 按需 | [fraud-network-modeling](../../skills/scenarios/fraud-network-modeling/SKILL.md) | 调查证据网络/风险子图 |
| 收尾 | [ontology-documentation](../../skills/core/ontology-documentation/SKILL.md) | 设计文档 |
| 后续 | [ontology-evolution](../../skills/core/ontology-evolution/SKILL.md) | 差异/兼容/演进 |

以上顺序可按已有输入跳过。只整理术语可只装 finance-domain-knowledge；概念模型转图可只装 property-graph-mapping；审查已有模型可只装 ontology-validation；单个场景 Skill 自带最小知识。

## 安装与组合

按 [逐项安装指南](../../docs/installation-guide.md) 将各自完整目录装入 Codex，或在 CC-Switch 的 onto-skills 发现页选择需要的项目。没有原生 Pack 导入时逐个安装即可。

交付物连接步骤：来源/术语 → 概念与角色 → 实体关系 → FIBO 对齐 → 图规格/损失 → 质量结果。Agent 按任务选择技能，不必加载全部。

## 可选外部 Skills

来源：[nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。gql-query-generator 处理查询、支持的 DML 与已有签名调用；gql-procedure-generator 处理过程定义/管理和算法。Graph Type/Schema DDL 检查当前安装能力，未来专门技能优先复用。

CC-Switch 添加该仓库 main/src；Codex 下载上游最新 Release，将所需完整目录放用户 Skills 根目录。更新使用原工具，任务读取当前安装版本，两项目独立升级。日期化兼容情况见 [报告](../../docs/compatibility.md)，不固定永久外部版本，不复制外部资源。

## 完整示例

> 结合业务描述和 Schema 设计信贷风险本体。固定观察时点、独立机构粒度与有效贷款口径；对齐 FIBO 并说明损失；输出 Graph Model Specification 与质量报告。要求 GQL 时再检查目标版本和外部能力并交接。

完整输入、双路径、融合输出和语义复核见 [端到端示例](../../examples/finance/README.md)。GQL 部分是可提交的请求，不是已运行证据。
