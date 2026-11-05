# Onto Skills

面向行业知识理解与本体工程的可组合 AI Skills 资产库。

将业务需求、数据 Schema 与行业标准转化为有来源、可验证、数据库中立的属性图本体。覆盖金融、电力、制造、物流、医疗和零售的行业知识与业务场景，使用 Codex CLI 与 CC-Switch 现有安装机制；FIBO 是金融重点标准。

## 设计与架构

Skills 提供方法，Knowledge 提供行业知识，Packs 说明组合。每个 Skill 可单独获取、安装、离线使用给定材料；必要知识、示例和许可随目录分发。通用建模与行业知识分层，不依赖 OINX 或特定数据库。

支持自下而上的业务/数据建模，以及自上而下的 RDF/OWL 标准裁剪、业务扩展与图映射，二者可以融合。继承、Domain/Range 和 Restriction 无法完全表达时明确标注损失。

```text
skills/core/       通用方法
skills/finance/    金融知识与标准
skills/industries/ 五项其他行业知识
skills/scenarios/  业务场景
knowledge/         分行业、分专项的有来源知识资产
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

### 本次新增行业与场景

当前源码共25项：7项Core、4项Finance、5项行业知识、9项Scenario。以下12项随本次扩展加入；[当前版本 `v26.11.06_Build0721`](https://github.com/MuYiYong/onto-skills/releases/tag/v26.11.06_Build0721) 提供全部25项。`v26.11.05_Build2200` 为原13项的历史版本。

| 分类 | Skill | 职责 |
| --- | --- | --- |
| 电力知识 | [electric-power-domain-knowledge](skills/industries/electric-power-domain-knowledge/SKILL.md) | 电力概念、身份、事件/状态、来源与映射边界 |
| 电力场景 | [power-outage-impact-analysis](skills/scenarios/power-outage-impact-analysis/SKILL.md) | 停电影响与恢复分段 |
| 制造知识 | [manufacturing-domain-knowledge](skills/industries/manufacturing-domain-knowledge/SKILL.md) | 制造概念、身份、事件/状态、来源与映射边界 |
| 制造场景 | [manufacturing-quality-traceability](skills/scenarios/manufacturing-quality-traceability/SKILL.md) | 批次质量与拆分/合并/返工追溯 |
| 物流知识 | [logistics-domain-knowledge](skills/industries/logistics-domain-knowledge/SKILL.md) | 物流概念、身份、事件/状态、来源与映射边界 |
| 物流场景 | [shipment-exception-analysis](skills/scenarios/shipment-exception-analysis/SKILL.md) | 运输异常、交接与事件时序 |
| 医疗知识 | [healthcare-domain-knowledge](skills/industries/healthcare-domain-knowledge/SKILL.md) | 医疗概念、身份、事件/状态、来源与映射边界 |
| 医疗场景 | [healthcare-care-pathway-modeling](skills/scenarios/healthcare-care-pathway-modeling/SKILL.md) | 照护事实、医嘱/执行与结果版本 |
| 零售知识 | [retail-domain-knowledge](skills/industries/retail-domain-knowledge/SKILL.md) | 零售概念、身份、事件/状态、来源与映射边界 |
| 零售场景 | [retail-inventory-replenishment](skills/scenarios/retail-inventory-replenishment/SKILL.md) | 库存、预留与补货候选 |
| 金融场景 | [financial-regulatory-reporting](skills/scenarios/financial-regulatory-reporting/SKILL.md) | 监管报送、指标血缘与更正回执 |
| 金融场景 | [related-party-transaction-modeling](skills/scenarios/related-party-transaction-modeling/SKILL.md) | 关联交易控制证据与口径审查 |

行业组合见 [电力](packs/electric-power-ontology/README.md)、[制造](packs/manufacturing-ontology/README.md)、[物流](packs/logistics-ontology/README.md)、[医疗](packs/healthcare-ontology/README.md)、[零售](packs/retail-ontology/README.md)；[新增能力与验证范围](docs/multi-industry-expansion.md)列出模型、输入和反例。

## 安装与使用

单个 Skill 的安装单位是其完整目录。例如在仓库根目录将 `skills/core/ontology-modeling/` 复制到 Codex 用户 `~/.agents/skills/`，保留 references、examples 和 LICENSE，然后用 `$ontology-modeling` 调用。目录已存在时先检查管理方式和本地修改；项目级可放 `.agents/skills/`。

CC-Switch 4.0.25 的 Skills → Add Skill → Install from ZIP 已实测支持单项、选择组合和全量本地包，并同步到 Codex。在 ⋯ → Manage repositories 可添加仓库根 URL `https://github.com/MuYiYong/onto-skills`、分支 main；仓库 GUI 安装/升级尚未单独验证。逐项路径、更新、卸载与版本差异见 [安装指南](docs/installation-guide.md)。

[当前发布版](https://github.com/MuYiYong/onto-skills/releases/tag/v26.11.06_Build0721) 提供25个独立 ZIP、全量 ZIP、八项金融/场景组合 ZIP、发布清单和 SHA-256；解压后每项仍是普通完整 Skill 目录。

金融组合见 [Finance Ontology Pack](packs/finance-ontology/README.md)，可只选择部分技能，不必装齐。完整案例见 [业务 + Schema → 双路径本体 → 图规格 → GQL 交接](examples/finance/README.md)。

## 外部 GQL Skills

本项目负责业务语义、Node/Edge/属性/身份/约束设计。NebulaGraph DDL、DML、DQL 和 Procedure 的具体表达复用独立的 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。查询使用 gql-query-generator，过程/算法使用 gql-procedure-generator；Graph Type DDL 须检查其当前资源/未来专门技能的实际覆盖。

先形成 [Graph Model Specification](docs/graph-model-specification.md)，再交接当前已安装能力；缺技能或能力时说明缺口和官方安装方式。仅本体设计无需该外部项目。这里不复制其语法、资源或长期固定其版本。

## 验证、贡献与许可

[兼容报告](docs/compatibility.md) 区分当前25项Codex发现与12项新增独立调用、原13项中的四项历史调用、离线闭包、5.3.2数据库原生验收、CC-Switch Linux原生操作和macOS/远程升级未验证项；[逐项验收](docs/acceptance.md) 对照首版要求；[扩展验收](docs/multi-industry-expansion.md)覆盖本次新增范围；[测试说明](tests/README.md) 提供开发命令。格式通过不等于行业语义或数据库运行通过。

贡献见 [CONTRIBUTING](CONTRIBUTING.md)；规范见 [Skill](docs/skill-specification.md)、[Knowledge](docs/knowledge-specification.md)、[Pack](docs/pack-specification.md)，未来范围见 [路线图](docs/roadmap.md)。

原创资产采用 [MIT](LICENSE)。第三方来源许可单独记录；不打包完整 FIBO 或外部 GQL 技能。本项目只交付资产，不提供独立 CLI、安装器、Registry、知识服务或 Web 管理系统。
