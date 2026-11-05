# Onto Skills

面向行业知识理解与本体工程的可组合 AI Skills 资产库。

将业务需求、数据 Schema 与行业标准转化为有来源、可验证、数据库中立的属性图本体。第一阶段支持 Codex CLI 与 CC-Switch，金融为首个行业，FIBO 为重点标准。

## 设计与架构

Skills 提供方法，Knowledge 提供行业知识，Packs 说明组合。每个 Skill 可单独获取、安装、离线使用给定材料；必要知识、示例和许可随目录分发。通用建模与行业知识分层，不依赖 OINX 或特定数据库。

支持自下而上的业务/数据建模，以及自上而下的 RDF/OWL 标准裁剪、业务扩展与图映射，二者可以融合。继承、Domain/Range 和 Restriction 无法完全表达时明确标注损失。

```text
skills/core/       通用方法
skills/finance/    金融知识与标准
skills/scenarios/  业务场景
knowledge/finance/ 有来源知识资产
packs/             推荐组合说明
docs/              规范、安装和兼容性
schemas/           图规格交付格式
examples/          完整业务示例
tests/ + scripts/  仅开发验证
```

## 当前 Skills

| 分类 | Skill | 职责 |
| --- | --- | --- |
| Core | [ontology-modeling](skills/core/ontology-modeling/SKILL.md) | 概念、边界、身份与生命周期 |
| Core | [industry-knowledge-discovery](skills/core/industry-knowledge-discovery/SKILL.md) | 术语、标准、来源与缺口 |
| Core | [entity-relationship-modeling](skills/core/entity-relationship-modeling/SKILL.md) | 实体、关系、基数、稳定键 |
| Core | [property-graph-mapping](skills/core/property-graph-mapping/SKILL.md) | OWL/概念到图规格与损失 |
| Core | [ontology-validation](skills/core/ontology-validation/SKILL.md) | 业务、结构、图设计与实现边界 |
| Core | [ontology-documentation](skills/core/ontology-documentation/SKILL.md) | 可审查的设计文档 |
| Core | [ontology-evolution](skills/core/ontology-evolution/SKILL.md) | 变更、兼容、迁移与回滚规划 |
| Finance | [finance-domain-knowledge](skills/finance/finance-domain-knowledge/SKILL.md) | 金融概念及角色边界 |
| Finance | [fibo-ontology](skills/finance/fibo-ontology/SKILL.md) | FIBO 裁剪/扩展/映射与版本 |
| Finance | [banking-business-model](skills/finance/banking-business-model/SKILL.md) | 银行业务流程和实体关系 |
| Finance | [credit-risk-knowledge](skills/finance/credit-risk-knowledge/SKILL.md) | 信用风险口径与时序关联 |
| Scenario | [multi-lending-detection](skills/scenarios/multi-lending-detection/SKILL.md) | 多机构有效贷款与共债关联 |
| Scenario | [fraud-network-modeling](skills/scenarios/fraud-network-modeling/SKILL.md) | 证据网络、风险链路与复核假设 |

## 安装与使用

单个 Skill 的安装单位是其完整目录。例如在仓库根目录将 `skills/core/ontology-modeling/` 复制到 Codex 用户 `~/.agents/skills/`，保留 references、examples 和 LICENSE，然后用 `$ontology-modeling` 调用。目录已存在时先检查管理方式和本地修改；项目级可放 `.agents/skills/`。

CC-Switch 4.0.25 的 Skills → Add Skill → Install from ZIP 已实测支持单项、选择组合和全量本地包，并同步到 Codex。在 ⋯ → Manage repositories 可添加仓库根 URL `https://github.com/MuYiYong/onto-skills`、分支 main；仓库 GUI 安装/升级尚未单独验证。逐项路径、更新、卸载与版本差异见 [安装指南](docs/installation-guide.md)。

[最新 Release](https://github.com/MuYiYong/onto-skills/releases/latest) 提供13个独立 ZIP、全量 ZIP、六项金融/场景选择 ZIP 和 SHA-256；解压后每项仍是普通完整 Skill 目录。

金融组合见 [Finance Ontology Pack](packs/finance-ontology/README.md)，可只选择部分技能，不必装齐。完整案例见 [业务 + Schema → 双路径本体 → 图规格 → GQL 交接](examples/finance/README.md)。

## 外部 GQL Skills

本项目负责业务语义、Node/Edge/属性/身份/约束设计。NebulaGraph DDL、DML、DQL 和 Procedure 的具体表达复用独立的 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。查询使用 gql-query-generator，过程/算法使用 gql-procedure-generator；Graph Type DDL 须检查其当前资源/未来专门技能的实际覆盖。

先形成 [Graph Model Specification](docs/graph-model-specification.md)，再交接当前已安装能力；缺技能或能力时说明缺口和官方安装方式。仅本体设计无需该外部项目。这里不复制其语法、资源或长期固定其版本。

## 验证、贡献与许可

[兼容报告](docs/compatibility.md) 区分真实 Codex 发现与四项实际调用、离线闭包、5.3.2 数据库原生验收、CC-Switch Linux 原生操作和 macOS/远程升级未验证项；[逐项验收](docs/acceptance.md) 对照原始要求；[测试说明](tests/README.md) 提供开发命令。格式通过不等于行业语义或数据库运行通过。

贡献见 [CONTRIBUTING](CONTRIBUTING.md)；规范见 [Skill](docs/skill-specification.md)、[Knowledge](docs/knowledge-specification.md)、[Pack](docs/pack-specification.md)，未来范围见 [路线图](docs/roadmap.md)。

原创资产采用 [MIT](LICENSE)。第三方来源许可单独记录；不打包完整 FIBO 或外部 GQL 技能。本项目只交付资产，不提供独立 CLI、安装器、Registry、知识服务或 Web 管理系统。
