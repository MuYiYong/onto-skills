# Logistics Ontology Pack

面向本体工程师和行业业务图设计者的文档组合，不含安装器、运行时或隐式依赖。

- [行业知识技能](../../skills/industries/logistics-domain-knowledge/SKILL.md)：独立完成术语、身份、生命周期、字段与来源梳理。
- [场景技能](../../skills/scenarios/shipment-exception-analysis/SKILL.md)：独立完成运输异常与交付证据建模、完整图规格、参数与反例验收。已自带最小行业知识，无需先安装行业技能。
- [知识](../../knowledge/logistics/README.md)和[端到端示例](../../examples/logistics/README.md)：便于维护和审查，不是安装后运行依赖。

按任务选择任一完整skill目录；可先以行业知识产生范围/概念/来源表，再把这个显式交付物交给场景技能。外部GQL能力为可选后续交接，须另核目标及版本，本包没有数据库语法、生产写入或自动业务操作。

标准来源提供对象与追溯背景，图模型、判断政策和阈值均为项目整理或用户输入。检索日期与源版本、法律/合同适用性分开。静态/离线验收不证明标准认证、真实数据完整或数据库执行；不涉及CC-Switch GUI或macOS验证。
