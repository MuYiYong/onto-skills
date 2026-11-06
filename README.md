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

## Skills

共 25 项：7 项通用方法、4 项金融知识与标准、5 项行业知识、9 项业务场景。每项均可独立安装，也可按任务组合使用。

### 通用方法（Core）

| Skill | 职责 |
| --- | --- |
| [ontology-modeling](skills/core/ontology-modeling/SKILL.md) | 概念、边界、身份与生命周期 |
| [industry-knowledge-discovery](skills/core/industry-knowledge-discovery/SKILL.md) | 术语、标准、来源与缺口 |
| [entity-relationship-modeling](skills/core/entity-relationship-modeling/SKILL.md) | 实体、关系、基数、稳定键 |
| [property-graph-mapping](skills/core/property-graph-mapping/SKILL.md) | OWL/概念到图规格与映射损失 |
| [ontology-validation](skills/core/ontology-validation/SKILL.md) | 业务、结构、图设计与实现边界 |
| [ontology-documentation](skills/core/ontology-documentation/SKILL.md) | 可审查的设计文档 |
| [ontology-evolution](skills/core/ontology-evolution/SKILL.md) | 变更、兼容、迁移与回滚规划 |

### 金融知识与标准（Finance）

| Skill | 职责 |
| --- | --- |
| [finance-domain-knowledge](skills/finance/finance-domain-knowledge/SKILL.md) | 金融概念及角色边界 |
| [fibo-ontology](skills/finance/fibo-ontology/SKILL.md) | FIBO 裁剪、扩展、映射与版本 |
| [banking-business-model](skills/finance/banking-business-model/SKILL.md) | 银行业务流程和实体关系 |
| [credit-risk-knowledge](skills/finance/credit-risk-knowledge/SKILL.md) | 信用风险口径与时序关联 |

### 行业知识（Industries）

| 行业 | Skill | 职责 |
| --- | --- | --- |
| 电力 | [electric-power-domain-knowledge](skills/industries/electric-power-domain-knowledge/SKILL.md) | 设备、端子、连通性与拓扑版本 |
| 制造 | [manufacturing-domain-knowledge](skills/industries/manufacturing-domain-knowledge/SKILL.md) | 产品、批次、生产事件与资源 |
| 物流 | [logistics-domain-knowledge](skills/industries/logistics-domain-knowledge/SKILL.md) | 货运、物流单元、交接与运输事件 |
| 医疗 | [healthcare-domain-knowledge](skills/industries/healthcare-domain-knowledge/SKILL.md) | 照护记录、资源身份与版本 |
| 零售 | [retail-domain-knowledge](skills/industries/retail-domain-knowledge/SKILL.md) | 产品、地点、库存与销售事件 |

### 业务场景（Scenarios）

| 行业 | Skill | 职责 |
| --- | --- | --- |
| 金融 | [multi-lending-detection](skills/scenarios/multi-lending-detection/SKILL.md) | 多机构有效贷款与共债关联 |
| 金融 | [fraud-network-modeling](skills/scenarios/fraud-network-modeling/SKILL.md) | 证据网络、风险链路与复核假设 |
| 金融 | [financial-regulatory-reporting](skills/scenarios/financial-regulatory-reporting/SKILL.md) | 监管报送、指标血缘与更正回执 |
| 金融 | [related-party-transaction-modeling](skills/scenarios/related-party-transaction-modeling/SKILL.md) | 关联交易控制证据与口径审查 |
| 电力 | [power-outage-impact-analysis](skills/scenarios/power-outage-impact-analysis/SKILL.md) | 停电影响与恢复分段 |
| 制造 | [manufacturing-quality-traceability](skills/scenarios/manufacturing-quality-traceability/SKILL.md) | 批次质量与拆分、合并、返工追溯 |
| 物流 | [shipment-exception-analysis](skills/scenarios/shipment-exception-analysis/SKILL.md) | 运输异常、交接与事件时序 |
| 医疗 | [healthcare-care-pathway-modeling](skills/scenarios/healthcare-care-pathway-modeling/SKILL.md) | 照护事实、医嘱与执行、结果版本 |
| 零售 | [retail-inventory-replenishment](skills/scenarios/retail-inventory-replenishment/SKILL.md) | 库存、预留与补货候选 |

## 安装与使用

单个 Skill 的安装单位是其完整目录。例如在仓库根目录将 `skills/core/ontology-modeling/` 复制到 Codex 用户 `~/.agents/skills/`，保留 references、examples 和 LICENSE，然后用 `$ontology-modeling` 调用。目录已存在时先检查管理方式和本地修改；项目级可放 `.agents/skills/`。

CC-Switch 使用 Skills → Add Skill → Install from ZIP 导入本地包并同步到 Codex；Linux 4.0.25 已完成单项、两项组合及 13 项包的原生验收。在 ⋯ → Manage repositories 可添加仓库根 URL `https://github.com/MuYiYong/onto-skills`、分支 main；仓库 GUI 安装/升级尚未单独验证。逐项路径、更新、卸载与版本差异见 [安装指南](docs/installation-guide.md)。

[最新 Release](https://github.com/MuYiYong/onto-skills/releases/latest) 提供 25 个独立 ZIP、全量 ZIP、八项金融/场景组合 ZIP、发布清单和 SHA-256；解压后每项仍是普通完整 Skill 目录。

## 行业组合与示例

Pack 提供选用顺序和交付物衔接说明，可按任务选择其中的技能。

| 行业 | 组合指南 | 示例 |
| --- | --- | --- |
| 金融 | [Finance Ontology Pack](packs/finance-ontology/README.md) | [业务 + Schema → 双路径本体 → 图规格 → GQL 交接](examples/finance/README.md)、[监管报送](examples/finance/regulatory-reporting/README.md)、[关联交易](examples/finance/related-party/README.md) |
| 电力 | [Electric Power Ontology Pack](packs/electric-power-ontology/README.md) | [故障线路、未知联络与 DER](examples/electric-power/README.md) |
| 制造 | [Manufacturing Ontology Pack](packs/manufacturing-ontology/README.md) | [批次质量与谱系追溯](examples/manufacturing/README.md) |
| 物流 | [Logistics Ontology Pack](packs/logistics-ontology/README.md) | [运输异常与交接事件](examples/logistics/README.md) |
| 医疗 | [Healthcare Ontology Pack](packs/healthcare-ontology/README.md) | [照护路径数据与版本](examples/healthcare/README.md) |
| 零售 | [Retail Ontology Pack](packs/retail-ontology/README.md) | [库存、预留与补货](examples/retail/README.md) |

行业与金融专项示例包含图模型、合成输入和具体正反例；知识来源、设计取舍及验证范围见 [多行业知识与业务场景](docs/multi-industry-expansion.md)。

## 外部 GQL Skills

本项目负责业务语义、Node/Edge/属性/身份/约束设计。NebulaGraph DDL、DML、DQL 和 Procedure 的具体表达复用独立的 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。查询使用 gql-query-generator，过程/算法使用 gql-procedure-generator；Graph Type DDL 须检查已安装资源或专门技能的实际覆盖。

先形成 [Graph Model Specification](docs/graph-model-specification.md)，再根据目标数据库版本交接已安装能力；缺技能或能力时说明缺口和官方安装方式。仅本体设计无需该外部项目。这里不复制其语法、资源或长期固定其版本。

## 验证、贡献与许可

| 验证层次 | 已记录的范围 |
| --- | --- |
| 离线检查 | 资产格式、独立资源闭包、知识副本、图模型结构及合成示例正反例 |
| Codex 原生 | Linux Codex 0.166.0 发现全部 25 项，读取 199 个包内文件；独立单包显式调用与有界语义复核 |
| CC-Switch 原生 | Linux 4.0.25 的单项、两项组合及 13 项 ZIP 安装、同步、卸载和 Codex 开关 |
| 数据库原生 | 5.3.2 的信贷与欺诈模型、合成数据、查询正反例、模型回读及清理 |

具体来源与限制见 [兼容报告](docs/compatibility.md) 和 [验收说明](docs/acceptance.md)。macOS 原生应用、远程安装/升级、隐式触发准确率、Procedure 与性能尚未验证；格式检查和有界合成任务不证明完整行业标准符合性或所有模型的数据库执行。开发校验命令见 [测试说明](tests/README.md)。

贡献见 [CONTRIBUTING](CONTRIBUTING.md)；规范见 [Skill](docs/skill-specification.md)、[Knowledge](docs/knowledge-specification.md)、[Pack](docs/pack-specification.md)，未来范围见 [路线图](docs/roadmap.md)。

原创资产采用 [MIT](LICENSE)。第三方来源许可单独记录；不打包完整 FIBO 或外部 GQL 技能。本项目只交付资产，不提供独立 CLI、安装器、Registry、知识服务或 Web 管理系统。
