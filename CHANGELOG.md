# Changelog

## [Unreleased]

## [v26.11.06_Build2157] - 2026-11-06

### Added

- 建筑、环境监测、教育三个行业的知识与配套场景，共六项独立技能；当前共33项技能、十个行业。
- IFC4.3.2.0、OGC SensorThings1.1、Open Badges3.0/VC2.0的条目级依据，三个完整图模型、41个正反例和24个新增知识对象；累计173个知识对象明确标准范围及缺口。
- 固定源码版本的Semantica调研，以及随包的来源定位、身份复核、质量问题和能力问题追踪方法。
- 全部33项技能的发布前源码审查报告；33项格式检查、资产校验及149项离线测试通过。

### Changed

- README按十个行业集中呈现知识和场景，更新标准矩阵、独立安装路径、行业Pack及验证范围。

### Fixed

- 行业知识发现技能补齐standard_status、standards_policy、来源kind/uri等输出契约及对应示例。
- 电力知识入口区分已核实CGMES3直接依据、IEC目录背景和本地规则。
- 制造知识和质量追溯明确返工的新输出键属于本地示例约定；真实源沿用批号时保留原号并要求版本/状态模型扩展。

### Limits

- 新增六项及本轮修订的四项既有技能未重新做原生应用或独立模型调用验收；旧原生收据绑定冻结源码，保持原范围。
- 两路独立审查代理因HTTP429未产生结果；本轮内容审阅由主代理完成，不冒称独立审查通过。
- 合成场景与模拟核查报告不证明完整行业标准符合性、真实凭证验签、生产部署或业务认可。

## [v26.11.06_Build1906] - 2026-11-06

### Added

- 网络安全知识与软件漏洞影响2项独立技能；当前共27项、七个行业，附标准格式SPDX/CSAF/CVSS样例、证据图和正反例。
- 全部149个知识对象的条目级标准状态、具体定位、适用范围及非标准缺口；取得公开CGMES3配置及规范性OWL2来源。
- 最终27包227文件的两布局Codex原生发现、Linux CC-Switch全量安装/同步/开关/卸载，以及21项当前Codex代理有界应用证据。
- 实际SPDX/CSAF/CVSS工具校验与EPCIS纠错身份证据；135项离线检查，原历史源码/结果冻结保留。

### Fixed

- 修正CSAF Remediations条款、CVSS完整向量与分数、EPCIS同ID合法纠错边界、FinancialProduct定义范围及CAS36过时获取说明。
- 校验器拒绝缺少标准状态、背景冒充直接依据和无解释的非标准项；知识副本保持同步。

### Limits

- 本轮CLI推理5次终态HTTP429失败，未产生模型结果；21项代理应用与CLI/版本证据分开记录，含共享审阅上下文。
- 未取得IEC付费完整正文；本地政策、未核实语义明确标非标准建模。未宣称完整标准认证、macOS原生、远程升级或新增数据库执行。

## [v26.11.06_Build0721] - 2026-11-06

### Added

- 新增电力、制造、物流、医疗、零售5项行业知识及5项配套业务场景，附来源、独立知识、图模型和具体正反例。
- 新增中国监管优先的金融监管报送血缘和关联交易2场景。
- 开发校验支持行业/金融专项最近来源目录，保留原13项原生证据的准确边界。
- 七个场景共90项具体正反例；全部25项Codex原生发现及12项新增技能独立CLI试用，附最终源码哈希与有界语义复核。

## [v26.11.05_Build2200] - 2026-11-05

### Added

- 新建七项 Core、四项 Finance、两项 Scenario Skills。
- 金融知识来源索引、FIBO/OWL 映射方法、Graph Model Specification 1.0。
- 金融 Pack 与双路径、融合模型及外部 GQL 交接示例。
- 轻量资产/模型验证、隔离安装测试、Codex 原生发现探针与兼容性记录。
- 四项 Codex CLI 实际调用、CC-Switch 4.0.25 Linux 原生 ZIP 安装/同步/卸载证据及准确菜单说明。
- 5.3.2 原生数据库的完整模型/合成样例/查询验收与已清理证据。
- 46 项离线验证，以及带 SHA-256 的单技能、全量和金融选择 ZIP 发布包。

版本采用 `vYY.MM.DD_BuildHHMM`，日期与时间为 Asia/Shanghai；原生验收范围和未验证项见[兼容报告](docs/compatibility.md)。

[v26.11.05_Build2200]: https://github.com/MuYiYong/onto-skills/releases/tag/v26.11.05_Build2200

[v26.11.06_Build0721]: https://github.com/MuYiYong/onto-skills/compare/v26.11.05_Build2200...v26.11.06_Build0721

[v26.11.06_Build1906]: https://github.com/MuYiYong/onto-skills/compare/v26.11.06_Build0721...v26.11.06_Build1906

[v26.11.06_Build2157]: https://github.com/MuYiYong/onto-skills/compare/v26.11.06_Build1906...v26.11.06_Build2157
