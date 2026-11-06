# 开发验证

本目录只做资产质量和兼容性测试，不提供 Skills 安装管理功能。

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

test_validation.py 检查 YAML、名称、资源路径/缺文件/软链接、知识来源/分类、图模型结构与语义交叉引用。test_distribution.py 检查独立复制、选择性共存与示例状态。content-validation 保存知识副本映射、独立内容审查和试用证据；compatibility 保存 opt-in 原生 Codex app-server 探针及来源记录。

原生发现检查：`python3 tests/compatibility/codex_probe.py`。只启动本地 Codex app-server，不调用模型、不访问业务数据库、不改变用户已安装 Skills，产物在临时目录中清理。原始结果可由调用方重定向到证据文件。

test_native_evidence.py 离线检查 [5.3.2 原生验收记录](compatibility/native-yueshu/README.md) 的哈希、实际返回值、DDL 回读与清理证据；不在 CI 自动连接数据库。普通格式测试通过仍不等于做了新的原生运行。

后续 [四项原生 CLI 实际调用](compatibility/codex-execution/README.md) 保存独立输入、输出、资源命令及语义复核；[CC-Switch Linux 原生验收](compatibility/cc-switch-native/README.md) 保存真实界面操作、13 项同步哈希、Codex 发现和清理证据。test_compatibility_evidence.py 只校验这些日期化证据的来源绑定、结果和管理状态，不启动应用、不调用模型，也不将离线 CI 当成新的原生验收。

通过不代表：真实领域事实正确、完整 OWL 一致性、macOS 原生兼容、发布后远程安装/升级或大规模性能。当前证据见 [兼容报告](../docs/compatibility.md)。

多行业扩展：`test_multi_industry_assets.py` 检查所有指定行业的知识/场景覆盖、就近来源、完整独立副本及安装路径；`test_*_examples.py` 中的行业/金融样例模块复算合成输入→expected并加入身份、时间、单位、状态和版本反例。它们是开发侧有界参考计算，不随Skill作为生产运行时分发，也不证明完整行业标准、临床/法律或原生数据库符合性。原13项与当时25项源码的历史证据分别记录。

[日期化多行业原生记录](compatibility/multi-industry-native/README.md)保存全部25项发现和12项独立CLI试用；[金融独立试用](content-validation/multi-industry-finance/README.md)保留原始17项检查、四个实际缺口及修复后的21项有界复核。`test_multi_industry_evidence.py` 只离线核对这些记录与冻结源码的哈希、实际结果、schema和已复核预期，不调用模型、应用或数据库。

标准优先与网络安全：`test_standards_grounding.py`检查所有中心知识的条目覆盖及伪标准/空定位/越域来源负例；`test_cybersecurity_examples.py`复算15个手工期望投影，并检查重放、时区、库存过期、身份冲突与严重度/补丁反例。见[范围](../docs/standards-first-knowledge.md)。

历史证据测试读取[冻结源码](compatibility/source-baselines/README.md)，校验归档哈希、199个源文件与原始收据的对应；不再将历史25项的发现/模型调用结果绑定到修改后的27项源码。原始收据、输出与GUI证据保持不变。当前资产继续由全量分发/来源/模型/副本测试独立检查；不得把历史完整性PASS称为新的原生验收。

[标准优先原生记录](compatibility/standards-first-native/README.md)绑定最终27包227文件：实际Codex两布局发现、Linux CC-Switch全量管理，以及与CLI失败分开保存的21项当前代理应用。`test_standards_first_native_evidence.py`只做冻结来源/读取/输出/终态的离线完整性复核。

[逐项标准核验](../docs/standards-verification.md)明确149个对象的依据和非标准范围；`test_standard_document_evidence.py`复核实际SPDX/CSAF/CVSS工具收据及EPCIS同ID纠错语义，CI不会重新下载标准或调用外部校验器。

建筑/环境监测/教育扩展：`test_standards_expansion_examples.py`复算41个手工预期及附加边界，`test_expansion_traceability.py`检查问题→模型→案例和新增知识账本的闭合。所有新案例为原创投影，教育报告明确模拟，不运行完整IFC/OGC/凭证处理器。见[说明](../docs/standards-industry-expansion.md)。
