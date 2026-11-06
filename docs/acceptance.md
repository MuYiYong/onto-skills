# 初始13项交付验收记录

> 本页保留首版历史验收。最终27项/227文件、21项当前代理应用与本轮CLI429限制见[原生记录](../tests/compatibility/standards-first-native/README.md)；逐项标准依据与非标准范围见[核验报告](standards-verification.md)。历史原始记录未重写。


本页保留已发布首版13项的历史验收。当前25项及五个新增行业/金融场景的范围见[扩展记录](multi-industry-expansion.md)，不能将以下原生结果自动外推。

按用户开发提示词第 1–20 节及最终 21 条标准逐项核对。本记录涵盖首版资产和发布前验证；提交、Release 与 CI 的实时状态以 GitHub 仓库记录为准。无法实际运行的检查依提示词 14.3 明确列为未验证，不用静态证据代替。

| 要求 | 当前资产/证据 | 结论与边界 |
| --- | --- | --- |
| 1 独立开源项目 | LICENSE、README、AGENTS、独立目录 | 原创 MIT；无 OINX 依赖，独立仓库与普通 ZIP 分发 |
| 2 无独立 CLI/Installer/Registry | 仅 Markdown/JSON 资产、两个开发测试入口和 validator | 没有面向用户的管理程序/服务 |
| 3 Agent Skills 标准 | 13 个 SKILL.md，YAML/name/description/目录验证 | 本地格式通过 |
| 4 每项独立安装 | tests/test_distribution.py 逐项复制到临时无关目录 | 13 项资源闭包通过 |
| 5 每项独立使用 | 本地方法、知识、示例、许可；独立内容审查 | 全部内容审查、两项独立 Agent 试用；后续四项原生 CLI 实际调用通过，非 13 项模型量化评测 |
| 6 可组合 | Pack、来源/概念/关系/图规格/质量交付接口 | 无强制未安装技能文件依赖 |
| 7 Pack 选择安装 | 金融 Pack、逐项安装表、cc-switch-native/ | 两项金融选择 ZIP、单项与13项原生安装/共存通过；Pack 不是专用管理格式 |
| 8 行业与方法分离 | core / finance / scenarios / knowledge | Core 用设备例子，金融标准知识在金融资产 |
| 9 知识随包分发 | references、examples、LICENSE、snapshots.json | 不使用仓库外相对路径/服务依赖；知识副本一致 |
| 10 Codex 发现和使用 | codex-native.json、codex-execution/、cc-switch-native/ | 0.166.0 两种目录/单项/13项发现，四项 CLI 实际调用通过；真实同步后13项发现无错误；隐式触发未测 |
| 11 CC-Switch 现有机制 | 安装指南、cc-switch-native/、上游源码观察 | 官方4.0.25 Linux 原生 ZIP 安装/同步/开关/卸载通过，84文件匹配；仓库配置成功，发布后安装/远程升级与 macOS 未验 |
| 12 无 OINX 依赖 | 资产与开发依赖清单 | 独立知识/方法，无运行时连接 |
| 13 数据库中立 | Graph Model Specification 逻辑类型，target unspecified | 外部示例另选 NebulaGraph 5.3.0，不改变 Core |
| 14 金融首试点 | 四项 Finance、两项场景、金融 Pack | 其他行业无假库存 |
| 15 FIBO 首重点标准 | 模块索引、Loan 固定来源/哈希/版本/父类/限制 | 只做合法索引与原创解释；未分发完整本体/未跑 imports 推理 |
| 16 合理属性图辅助 | 决策方法、贷款与欺诈模型、正反例、审查 | 有界专家式内容审查与 Agent 示例；不替代真实业务确认 |
| 17 完整图规格 | JSON Schema、两个 Core 例子、金融融合/标准草案/欺诈模型 | 属性/键/端点/方向/约束/来源/损失/未决项完整；草案与 ready 有区别 |
| 18 外部 GQL 交接 | 本地手册、金融交接请求、generated/ receipt 与原生记录 | 外部 query Skill 生成 DQL/lint，后续 5.3.2 固定 DDL 与查询原生通过；外部完整 DDL 覆盖仍单独标记未证实 |
| 19 不维护重复 GQL 语法 | 没有外部文件副本；只保留具体示例和来源哈希 | 不建设通用 GQL 生成器，不锁长期外部版本 |
| 20 知识来源可追溯 | sources.json，重要资产/条目来源与分类 | 官方/通用/原创/推断区分；来源版本与检索日期分别记录 |
| 21 模型质量验证 | ontology-validation，JSON Schema 与语义负例 | 静态身份/类型/端点/时间/约束引用/来源验证；业务/推理/实现分层 |

## 提示词的其他明确交付

- 七项 Core、四项 Finance、两个 Scenario 完整目录见 [库存](../README.md)。关联交易当时属于后续范围，本次已新增 `related-party-transaction-modeling`，按扩展记录另验。
- 八份要求文档：architecture、skill-specification、knowledge-specification、pack-specification、installation-guide、contribution-guide、roadmap，以及独立 Graph Model Specification 文档均存在；README、CONTRIBUTING、CHANGELOG、LICENSE 齐备。
- 两条建模路径及融合：[输入、模型与完整流程](../examples/finance/README.md)。标准裁剪草案含未决项，会被 ready 门槛拒绝；关键语义损失明确保留。
- 外部核查：当前上游 README、两个 SKILL、Release、查询语法目录均已查看；本地已装 query Skill 的适用资源和 lint 实际使用，未复制其文件。
- macOS/Ubuntu：Ubuntu 复制、原生发现/实际调用、CC-Switch 原生本地管理已验；macOS 仅静态目录审查，CI matrix 覆盖 macOS 离线检查，其结果以对应提交为准，不替代原生应用验收。发布后仓库安装/远程升级、外部 Skill 的完整 DDL 覆盖仍未验证；5.3.2 数据库的固定 DDL、39 节点/51 边样例与查询原生通过，见 [记录](../tests/compatibility/native-yueshu/README.md)。

## 质量与审查

本地命令：`.venv/bin/python scripts/validate.py` 与 `.venv/bin/python -m unittest discover -s tests -v`。发布前本地结果为资产验证 PASS、46/46 测试 PASS；证据范围见 [测试说明](../tests/README.md)，远端 CI 状态以对应提交为准。

独立审查报告见 [review.md](../tests/content-validation/review.md)；重要发现均修复：引用式/HTML/带空格路径和源根软链接不能绕过检查；欺诈简单转账明确一发一收并排除未拆分批次，观测与证据保留匹配方法/置信说明。两项独立试用及修复说明见 [forward-test](../tests/content-validation/forward-test/README.md)。

后续外部验收按 [兼容报告](compatibility.md) 的明确步骤进行；不声称所有平台和数据库已通过。后续行业扩展、关联交易及其他 Agent 专门适配见 [路线图](roadmap.md)。
