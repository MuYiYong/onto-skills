# Onto Skills

面向行业知识理解与本体工程的可组合 AI Skills 资产库。

将业务需求、数据 Schema 与行业标准转化为有来源、可验证、数据库中立的属性图本体。覆盖金融、电力、制造、物流、医疗、零售、网络安全、建筑、环境监测和教育的行业知识与业务场景，使用 Codex CLI 与 CC-Switch 现有安装机制；FIBO 是金融重点标准。

## 设计与架构

Skills 提供方法，Knowledge 提供行业知识，Packs 说明组合。每个 Skill 可单独获取、安装、离线使用给定材料；必要知识、示例和许可随目录分发。通用建模方法与行业知识分层，模型设计保持数据库中立。

支持自下而上的业务/数据建模，以及自上而下的 RDF/OWL 标准裁剪、业务扩展与图映射，二者可以融合。继承、Domain/Range 和 Restriction 无法完全表达时明确标注损失。

```text
skills/core/       通用方法
skills/finance/    金融知识、标准与业务建模
skills/industries/ 行业知识
skills/scenarios/  业务场景
knowledge/         分行业、分专项的有来源知识资产
packs/             推荐组合说明
docs/              规范、安装和兼容性
schemas/           图规格交付格式
examples/          完整业务示例
tests/ + scripts/  仅开发验证
```

## Skills

共 33 项：7 项通用方法、26 项行业技能。按金融、电力、制造、物流、医疗、零售、网络安全、建筑、环境监测和教育十个行业，将相关知识、标准本体与业务场景集中列出；每项均可独立安装，也可按任务组合使用。

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

### 金融（Finance）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [finance-domain-knowledge](skills/finance/finance-domain-knowledge/SKILL.md) | 金融概念及角色边界 |
| 标准本体 | [fibo-ontology](skills/finance/fibo-ontology/SKILL.md) | FIBO 裁剪、扩展、映射与版本 |
| 业务建模 | [banking-business-model](skills/finance/banking-business-model/SKILL.md) | 银行业务流程和实体关系 |
| 风险知识 | [credit-risk-knowledge](skills/finance/credit-risk-knowledge/SKILL.md) | 信用风险口径与时序关联 |
| 业务场景 | [multi-lending-detection](skills/scenarios/multi-lending-detection/SKILL.md) | 多机构有效贷款与共债关联 |
| 业务场景 | [fraud-network-modeling](skills/scenarios/fraud-network-modeling/SKILL.md) | 证据网络、风险链路与复核假设 |
| 业务场景 | [financial-regulatory-reporting](skills/scenarios/financial-regulatory-reporting/SKILL.md) | 监管报送、指标血缘与更正回执 |
| 业务场景 | [related-party-transaction-modeling](skills/scenarios/related-party-transaction-modeling/SKILL.md) | 关联交易控制证据与口径审查 |

### 电力（Electric Power）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [electric-power-domain-knowledge](skills/industries/electric-power-domain-knowledge/SKILL.md) | 设备、端子、连通性与拓扑版本 |
| 业务场景 | [power-outage-impact-analysis](skills/scenarios/power-outage-impact-analysis/SKILL.md) | 停电影响与恢复分段 |

### 制造（Manufacturing）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [manufacturing-domain-knowledge](skills/industries/manufacturing-domain-knowledge/SKILL.md) | 产品、批次、生产事件与资源 |
| 业务场景 | [manufacturing-quality-traceability](skills/scenarios/manufacturing-quality-traceability/SKILL.md) | 批次质量与拆分、合并、返工追溯 |

### 物流（Logistics）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [logistics-domain-knowledge](skills/industries/logistics-domain-knowledge/SKILL.md) | 货运、物流单元、交接与运输事件 |
| 业务场景 | [shipment-exception-analysis](skills/scenarios/shipment-exception-analysis/SKILL.md) | 运输异常、交接与事件时序 |

### 医疗（Healthcare）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [healthcare-domain-knowledge](skills/industries/healthcare-domain-knowledge/SKILL.md) | 照护记录、资源身份与版本 |
| 业务场景 | [healthcare-care-pathway-modeling](skills/scenarios/healthcare-care-pathway-modeling/SKILL.md) | 照护事实、医嘱与执行、结果版本 |

### 零售（Retail）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [retail-domain-knowledge](skills/industries/retail-domain-knowledge/SKILL.md) | 产品、地点、库存与销售事件 |
| 业务场景 | [retail-inventory-replenishment](skills/scenarios/retail-inventory-replenishment/SKILL.md) | 库存、预留与补货候选 |

### 网络安全（Cybersecurity）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [cybersecurity-domain-knowledge](skills/industries/cybersecurity-domain-knowledge/SKILL.md) | 软件组件、通告产品、漏洞状态与部署证据 |
| 业务场景 | [software-vulnerability-impact](skills/scenarios/software-vulnerability-impact/SKILL.md) | SBOM、漏洞适用性、通告修订与修复证据 |

### 建筑与设施（Built Environment）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [built-environment-domain-knowledge](skills/industries/built-environment-domain-knowledge/SKILL.md) | 建筑与设施身份、角色与标准语义 |
| 业务场景 | [bim-change-impact](skills/scenarios/bim-change-impact/SKILL.md) | BIM属性变更与空间影响候选 |

### 环境监测（Environmental Monitoring）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [environmental-monitoring-domain-knowledge](skills/industries/environmental-monitoring-domain-knowledge/SKILL.md) | 环境监测身份、角色与标准语义 |
| 业务场景 | [observation-quality-assessment](skills/scenarios/observation-quality-assessment/SKILL.md) | 环境观测质量与阈值候选 |

### 教育与学习凭证（Education）

| 类型 | Skill | 职责 |
| --- | --- | --- |
| 行业知识 | [education-domain-knowledge](skills/industries/education-domain-knowledge/SKILL.md) | 教育与学习凭证身份、角色与标准语义 |
| 业务场景 | [learning-credential-verification](skills/scenarios/learning-credential-verification/SKILL.md) | 学习成就凭证证据核对 |

## 标准依据

知识优先核实发布机构的正式标准、版本和具体条目，再形成项目解释与图设计。每条知识记录标准定位和适用范围；无直接规范支持、未取得正文或精确映射未核实的内容明确标为“非标准建模”，并说明缺口。标准依据只覆盖所列scope，本地策略仍单列。引用官方标准不会把项目解释变成官方定义。

| 知识范围 | 选定标准与官方来源 | 应用边界与知识索引 |
| --- | --- | --- |
| 本体方法 | [W3C OWL 2](https://www.w3.org/TR/2012/REC-owl2-syntax-20121211/)，2012-12-11 Recommendation | 语义解释；图设计方法为项目整理 |
| 金融 | [FIBO](https://spec.edmcouncil.org/fibo/)，固定仓库修订；[Basel CRE36](https://www.bis.org/committees/bcbs/basel-framework/standard/cre/36/inforce/2023-01-01/published/2022-12-08) | 类/属性及信贷背景；[来源](knowledge/finance/standards/sources.json)，各本体版本分开记录 |
| 监管报送 | [监管统计管理办法](https://www.nfra.gov.cn/cn/view/pages/governmentDetail.html?docId=1089714&itemId=861&generaltype=1)，2022年第10号；[BCBS239](https://www.bis.org/publ/bcbs239.htm)，2013；[XBRL2.1](https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31%2Bcorrected-errata-2013-02-20.html) | 制度/质量/事实语义；[来源](knowledge/finance/regulatory/standards/sources.json)，具体模板另定 |
| 关联交易 | [2025年关联交易管理办法修正](https://www.nfra.gov.cn/cn/view/pages/ItemDetail.html?docId=1209888&generaltype=0&itemId=928)；[企业会计准则第36号](https://kjs.mof.gov.cn/zt/kjzzss/kuaijizhunzeshishi/200806/t20080618_46245.htm) | 监管和会计口径分开；[来源](knowledge/finance/related-parties/standards/sources.json) |
| 电力 | [IEC61970-301:2020](https://webstore.iec.ch/en/publication/62698) / AMD1:2022；[CGMES3.0](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/) | 已取得CGMES3正式RDFS/SHACL，核对类/字段/基数；IEC付费正文未取得，客户/停电政策为非标准建模；[来源](knowledge/electric-power/standards/sources.json) |
| 制造 | [OPC10030 v1.00 / ISA-95](https://reference.opcfoundation.org/specs/OPC-10030/full)；[EPCIS2.0.1](https://ref.gs1.org/standards/epcis/2.0.1/) | 物料/设备/检验与转化事件；[来源](knowledge/manufacturing/standards/sources.json)，本地质量阈值另定 |
| 物流 | [GS1 Architecture12.0.0](https://ref.gs1.org/architecture/system-architecture/12.0.0/)；[EPCIS2.0.0](https://ref.gs1.org/standards/epcis/2.0.0/) / [CBV2.0.0](https://ref.gs1.org/standards/cbv/2.0.0/)；[DCSA2024.4](https://models.dcsa.org/2024Q4/EARoot/EA5/EA2/EA6/EA7/EA1/EA1/EA2575.htm) | 身份与事件分类；[来源](knowledge/logistics/standards/sources.json)，延误政策另定 |
| 医疗 | [HL7 FHIR R4 4.0.1](https://hl7.org/fhir/R4/) | 固定R4基线，资源身份/版本/状态/量；[来源](knowledge/healthcare/standards/sources.json)，非完整FHIR认证 |
| 零售 | GS1 Architecture12.0.0、EPCIS2.0.0、CBV2.0.0；[Traceability2.0](https://ref.gs1.org/standards/global-traceability/2.0.0/) | 商品/地点/追溯背景；[来源](knowledge/retail/standards/sources.json)，库存预留与补货公式另定 |
| 网络安全 | [SPDX2.3](https://github.com/spdx/spdx-spec/tree/v2.3)；[OASIS CSAF2.0](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html)；[FIRST CVSS4.0](https://www.first.org/cvss/v4.0/specification-document) | 组件身份、产品状态与严重度分层；[来源](knowledge/cybersecurity/standards/sources.json)，不从依赖或补丁发布推断已修复 |
| 建筑与设施 | [IFC4.3.2.0 / IFC4X3_ADD2](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/)，固定官方RELEASE快照 | 对象、类型/实例属性、主包含/引用与单位；[来源](knowledge/built-environment/standards/sources.json)，无几何或结构安全结论 |
| 环境监测 | [OGC SensorThings API1.1 /18-088](https://docs.ogc.org/is/18-088/18-088.html)，2021-08-04 | 观测、质量、时间与被测对象；[来源](knowledge/environmental-monitoring/standards/sources.json)，阈值为本地政策，非环境法规 |
| 教育与学习凭证 | [Open Badges3.0](https://www.imsglobal.org/spec/ob/v3p0/) 文档1.4.5；[W3C VC2.0](https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/) | 成就/凭证/发行者与核查证据；[来源](knowledge/education/standards/sources.json)，不自动验签或认可学历能力 |

条目级定位、实质知识补强、标准映射损失与缺口处理见[标准优先知识说明](docs/standards-first-knowledge.md)。固定版次是建模基线，检索日期不代表标准版本；法律、机构和行业Profile的适用性仍按具体任务核实。

## 安装与使用

单个 Skill 的安装单位是其完整目录。例如在仓库根目录将 `skills/core/ontology-modeling/` 复制到 Codex 用户 `~/.agents/skills/`，保留 references、examples 和 LICENSE，然后用 `$ontology-modeling` 调用。目录已存在时先检查管理方式和本地修改；项目级可放 `.agents/skills/`。

CC-Switch 使用 Skills → Add Skill → Install from ZIP 导入本地包并同步到 Codex；Linux 4.0.25 的既有原生验收覆盖此前27项包的安装、同步、开关与卸载；新增六项尚未做原生验收。在 ⋯ → Manage repositories 可添加仓库根 URL `https://github.com/MuYiYong/onto-skills`、分支 main；仓库 GUI 安装/升级尚未单独验证。逐项路径、更新、卸载与版本差异见 [安装指南](docs/installation-guide.md)。

[Release](https://github.com/MuYiYong/onto-skills/releases/latest) 提供独立 ZIP、组合 ZIP、发布清单和 SHA-256；具体包含项以该版本发布清单为准。上表每项均可从仓库复制完整目录使用，解压后仍是普通 Skill 目录。

## 行业组合与示例

Pack 提供选用顺序和交付物衔接说明，可按任务选择其中的技能。

| 行业 | 组合指南 | 示例 |
| --- | --- | --- |
| 金融 | [Finance Ontology Pack](packs/finance-ontology/README.md) | [业务 + Schema → 双路径本体 → 图规格](examples/finance/README.md)、[监管报送](examples/finance/regulatory-reporting/README.md)、[关联交易](examples/finance/related-party/README.md) |
| 电力 | [Electric Power Ontology Pack](packs/electric-power-ontology/README.md) | [故障线路、未知联络与 DER](examples/electric-power/README.md) |
| 制造 | [Manufacturing Ontology Pack](packs/manufacturing-ontology/README.md) | [批次质量与谱系追溯](examples/manufacturing/README.md) |
| 物流 | [Logistics Ontology Pack](packs/logistics-ontology/README.md) | [运输异常与交接事件](examples/logistics/README.md) |
| 医疗 | [Healthcare Ontology Pack](packs/healthcare-ontology/README.md) | [照护路径数据与版本](examples/healthcare/README.md) |
| 零售 | [Retail Ontology Pack](packs/retail-ontology/README.md) | [库存、预留与补货](examples/retail/README.md) |
| 网络安全 | [Cybersecurity Ontology Pack](packs/cybersecurity-ontology/README.md) | [组件、漏洞与通告修订证据](examples/cybersecurity/README.md) |
| 建筑与设施 | [建筑与设施 Pack](packs/built-environment-ontology/README.md) | [BIM属性变更与空间影响候选](examples/built-environment/README.md) |
| 环境监测 | [环境监测 Pack](packs/environmental-monitoring-ontology/README.md) | [环境观测质量与阈值候选](examples/environmental-monitoring/README.md) |
| 教育与学习凭证 | [教育与学习凭证 Pack](packs/education-ontology/README.md) | [学习成就凭证证据核对](examples/education/README.md) |

行业与金融专项示例包含图模型、合成输入和具体正反例；知识来源、设计取舍及验证范围见 [多行业知识与业务场景](docs/multi-industry-expansion.md)。

本轮新增三行业、六项技能、41个正反例及条目级标准核查，见[扩展说明](docs/standards-industry-expansion.md)。[Semantica调研与采用点](docs/semantica-review.md)记录固定源码版本，以及来源追踪、身份候选和质量问题设计。

## 建模交付

交付物包括业务语义、概念与角色、实体关系、属性与稳定身份、时间与来源、约束、映射损失及待决问题。结构化输出采用 [Graph Model Specification](docs/graph-model-specification.md)，便于审查、复用和后续实现。

模型设计与数据库实现分开。需要落地时，再按任务选定的目标系统和版本适配具体语法、存储约束与验证方式。

## 验证、贡献与许可

| 验证层次 | 已记录的范围 |
| --- | --- |
| 离线检查 | 资产格式、独立资源闭包、知识副本、图模型结构及合成示例正反例 |
| Codex 原生发现 | Linux Codex0.166.0，两种布局发现此前27项并读取227文件；该次CLI推理因429未产生结果 |
| Codex代理应用 | 此前代理运行时完成21项修改/新增技能的有界任务；与CLI证据分开记录 |
| CC-Switch 原生 | Linux4.0.25，此前27项ZIP安装/同步、227文件哈希、Codex开关和全量卸载通过 |
| 标准核验 | 现有173个知识对象逐项标明依据与缺口；原149项及标准工具证据见[报告](docs/standards-verification.md)，新增24项见[扩展核查](docs/standards-industry-expansion.md) |

发布前另对全部33项做了[技能审查](docs/skill-review-2026-11-06.md)，修正4项既有技能的输出契约或语义说明；这些修改尚未重新做原生验收。

新增六项仅有本轮离线资产检查与合成案例验证，尚无原生应用或独立模型调用证据。具体来源与限制见 [兼容报告](docs/compatibility.md) 和 [验收说明](docs/acceptance.md)。原生记录以[冻结源码和日期化证据](tests/compatibility/standards-first-native/README.md)为准，代理应用包含两项独立先导和共享审阅上下文的其余任务。macOS 原生应用、远程安装/升级、隐式触发准确率与性能尚未验证；格式检查和有界合成任务不证明完整行业标准符合性或生产部署效果。开发校验命令见 [测试说明](tests/README.md)。

贡献见 [CONTRIBUTING](CONTRIBUTING.md)；规范见 [Skill](docs/skill-specification.md)、[Knowledge](docs/knowledge-specification.md)、[Pack](docs/pack-specification.md)，未来范围见 [路线图](docs/roadmap.md)。

原创资产采用 [MIT](LICENSE)。第三方来源许可单独记录；不打包完整 FIBO。本项目只交付资产，不提供独立 CLI、安装器、Registry、知识服务或 Web 管理系统。
