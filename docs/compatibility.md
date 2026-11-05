# 兼容性与证据边界

原13项证据保持历史范围。当前25项源码的新增证据与限制见[多行业扩展](multi-industry-expansion.md)；下表中的13项/84文件、四项CLI与CC-Switch/数据库运行不能当作新增内容已通过同类原生验收。

原生证据采集日期：2026-11-05。以下原生检查在首版发布前完成，当时远端尚无 refs；保留该历史边界。当前源码/下载包见 [GitHub 仓库](https://github.com/MuYiYong/onto-skills) 和 [Releases](https://github.com/MuYiYong/onto-skills/releases)。发布资产不自动证明仓库 GUI 安装或远程升级已验。

| 验收项 | 当前结果 | 证据范围 |
| --- | --- | --- |
| Agent Skills 格式 | 本地检查通过 | YAML、名称、目录、引用、许可 |
| 单 Skill 独立复制 | 13 项逐个通过 | 临时目录资源闭包/模型结构检查，非模型调用 |
| 选择安装/多 Skill 共存 | 本地检查通过 | 2 项选择复制及 13 项完整布局，无名称碰撞 |
| Codex CLI 原生发现 | 0.166.0，Ubuntu，通过 | 真实 app-server initialize → skills/list；项目 .agents/skills 与临时 CODEX_HOME/skills，单项/13 项 |
| 发现后的资源访问 | 通过 | 从原生 API 返回路径读取 84 个文件，不依赖仓库相对路径 |
| Codex CLI 实际调用 | 4 项有界用例通过 | 0.166.0，独立单包，实际资源读取、模型输出、schema/语义复核和终态退出 0 |
| Codex 自动触发 | 未验证 | 实际调用使用显式技能名称，不外推隐式选择准确率 |
| CC-Switch 测试版本 | 官方 Linux 4.0.25 | 隔离 Ubuntu 24.04 原生桌面；用户已有安装版本仍未确认 |
| CC-Switch 仓库发现/安装/更新/同步逻辑 | 上游源码/手册复核 | 4.0.25，revision cc4ce03860b5987e4928dcbee76f17b29eec20e6；不是 GUI 实测 |
| CC-Switch GUI 本地安装/卸载/Codex 开关 | 原生通过 | 单项/两项/13 项 ZIP、84 文件哈希、开关、单项/批量卸载、真实同步后 Codex 发现 |
| CC-Switch 仓库安装/远程升级 | 未验证 | 仓库根 URL/main 配置成功；资产尚未发布，0 项可发现；本地更新提示不能证明远程升级 |
| Ubuntu 目录兼容 | 本地复制与原生发现通过 | 当前 Linux 主机 |
| macOS 目录/原生运行 | 目录静态可移植；原生未验证 | 无软链接资源或硬编码绝对包路径；CI matrix 覆盖 macOS 离线检查，结果以对应提交为准，不证明原生应用运行 |
| 外部 GQL Skills 独立更新 | 上游结构/文档复核 | 单技能/组合 Release 与 CC-Switch main/src；本项目没有复制内容或固定依赖版本 |
| GQL DQL 生成与外部静态 lint | 已完成有界示例 | 实际应用当前已安装 gql-query-generator；输入/输出/入口哈希和 lint 结果有记录 |
| Graph Type DDL 与数据库执行 | 5.3.2 原生通过 | 完整信贷/欺诈模型回读、39 节点/51 边合成数据、查询正反例与清理；32 项验收通过 |
| Procedure、规模与性能 | 未运行 | 本项目没有提供待测 Procedure；小规模功能验收不外推性能 |

## 当前25项源码的新增原生验证

2026-11-06的[独立记录](../tests/compatibility/multi-industry-native/README.md)使用Codex0.166.0，原生app-server在project/legacy-codex-home两种布局均完成单项及全部25项发现，共199个包内文件可读。随后12个新增技能分别在仅安装自身的临时项目中实际显式调用，全部turn.completed、退出0；五项知识输出和七项场景结果经语义复核，提示、schema、结果、命令与全部包文件哈希均保存。监管报送包最终模型变更后的补跑已替换计数中的旧试用；旧试用单独保留而不冒充当前源码。

这是本次新增范围的有界合成任务证据，不是隐式触发率或完整标准符合性评测。关联交易试用的一次可选搜索未匹配，以及缺少python别名后改用python3的恢复过程均保留。新增包未进行CC-Switch GUI、macOS原生、远程安装升级或数据库验收；下方原13项GUI和数据库证据仍保持历史范围。

## 原13项原生 Codex 证据

[原始结果](../tests/compatibility/codex-native.json)，复现：`python3 tests/compatibility/codex_probe.py`。探针每次使用新临时目录，不改用户现有安装；仅使用本地 app-server，未调用模型或数据库。scope=legacy-codex-home 对应 CC-Switch 默认 Codex 同步目录的格式，但不证明 CC-Switch 本身执行成功。

后续 [CLI 实际调用](../tests/compatibility/codex-execution/README.md) 在四个独立临时项目中分别运行 entity-relationship-modeling、fibo-ontology、multi-lending-detection、ontology-evolution。全部终态退出 0，JSON schema 和语义复核通过，原生读取命令及源文件哈希可回查。覆盖重复关系身份、OWL 限制/映射损失、多头借贷反例、破坏性版本演化；没有完整 imports 推理或隐式触发评估，不等于 13 项量化评测。

## CC-Switch 来源

[官方源码](https://github.com/farion1231/cc-switch/blob/cc4ce03860b5987e4928dcbee76f17b29eec20e6/src-tauri/src/services/skill.rs) 的 scan_dir_recursive/scan_skills_recursive 递归寻找 SKILL.md，找到后停止进入其子目录，能够识别 skills/<category>/<name>。resolve_skill_source_dir 有嵌套目录处理。手册记录默认主副本 .cc-switch/skills，Codex .codex/skills，可选通用 .agents/skills，支持复制/软链接与更新检测。版本来自该 revision 的 Cargo.toml，不是本机已安装版本。

[原生 GUI 补验](../tests/compatibility/cc-switch-native/README.md) 使用官方 4.0.25 安装包，在未挂载真实用户配置的专用容器中运行。单项、两项选择及全量嵌套 ZIP 导入成功；13 项 84 文件在主副本与同步目标哈希一致。默认 Codex 同步为软链接，关闭/重新启用和单项卸载均保留其他项目；Codex 原生 app-server 发现全部 13 项且无错误。全量及选择卸载均达到终态，测试容器已删除。

实测修正：Install from ZIP 才是任意本地包入口，Import from this computer 扫描已有安装；重复 ZIP 跳过同名目录。Manage repositories 接受仓库根 URL 和分支，没有子目录字段，拒绝 tree URL。Check Updates 对本地包提示最新，不能证明尚未发布仓库的远程更新。发布后还需真实仓库发现、安装和改变版本后的升级；macOS 原生仍需对应平台。

## 外部与标准观察

日期化 [上游观察](../tests/compatibility/upstream-observations.json) 记录精确 revision、文件哈希和能力范围，不是依赖锁。GQL [README](https://github.com/MuYiYong/nebula-gql-skills) 当前列两项技能，观测 release 为 v26.10.25_Build142；每次任务优先读当前安装内容。当前入口/索引未建立完整 Graph Type DDL 支持证据，使用前必须核实，不在本库补建语法。

FIBO [Loans.rdf](https://github.com/edmcouncil/fibo/blob/33a92cd34285d532c158da97bb42add089f135d3/LOAN/LoansGeneral/Loans.rdf) 的具体 versionIRI 为 LOAN/20251201/LoansGeneral/Loans；AboutFIBOProd 的 20261001 是聚合本体版本，两者不能混淆。只解析了有界文件，未取得完整 imports 或运行推理。许可证查自官方仓库，当前仅分发原创索引与解释。

## 用户授权的原生数据库补验

后续使用用户提供的私有连接完成 [原生验收](../tests/compatibility/native-yueshu/README.md)。SHOW VERSION 确认为 5.3.2，使用官方 SDK nebula5_python 5.3.0。完整信贷与欺诈 Graph Type、所有属性/空值/键/方向、全部类型的样例数据、查询结果及预期错误均有原生状态码与来源哈希。

原查询末尾的分号在该原生 API 返回 42001；保留原字节与失败记录，仅删终止分号后五组同源查询通过。验证脚本显式调用 raise_on_error，不能以 SDK 返回空行判定成功。两个 Graph 与两个 Graph Type 已清理并回查不存在。连接地址、账户与密码未保存。

本次固定 DDL 用实际版本的官方文档核对，不代表当前外部查询 Skill 已覆盖所有 DDL；没有新增语法生成器或复制外部文件。该结果只证明 5.3.2 的有界功能，5.3.0 原生执行、Procedure、性能、完整 OWL 推理、macOS 与远程升级仍各自保持未验证。
