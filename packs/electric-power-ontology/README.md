# Electric Power Ontology Pack

这是文档组合，不是安装器或运行时。可只安装 [领域知识](../../skills/industries/electric-power-domain-knowledge/SKILL.md)，也可只安装 [业务场景](../../skills/scenarios/power-outage-impact-analysis/SKILL.md)；两者均自带来源、知识、方法、例子和许可证，不要求同时安装。

建议交付顺序：术语/来源与身份边界 → 事件/时序/数量关系 → 数据库中立图规格 → 反例与未决项。根据已有材料跳过步骤，无隐式共享上下文。图规格与原始证据是步骤间契约。

场景输入、完整图模型和具体预期见 [端到端示例](../../examples/electric-power/README.md)。中心原创知识见 [知识目录](../../knowledge/electric-power/README.md)。来源版本为检索时观察，不代表任一现场版本适用或标准符合性；第三方标准正文不随包分发。

若需 NebulaGraph GQL，明确目标版本后交接到经核实可用的外部 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills) 能力。这里仅维护业务语义和模型，没有数据库执行或生产操作证明。
