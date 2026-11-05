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

多行业扩展：`test_multi_industry_assets.py` 检查所有指定行业的知识/场景覆盖、就近来源、完整独立副本及安装路径；`test_*_examples.py` 中的7个行业/金融样例模块复算合成输入→expected并加入身份、时间、单位、状态和版本反例。它们是开发侧有界参考计算，不随Skill作为生产运行时分发，也不证明完整行业标准、临床/法律或原生数据库符合性。原13项历史证据与当前25项源码分开记录。

[当前多行业原生记录](compatibility/multi-industry-native/README.md)保存全部25项发现和12项独立CLI试用；[金融独立试用](content-validation/multi-industry-finance/README.md)保留原始17项检查、四个实际缺口及修复后的21项有界复核。`test_multi_industry_evidence.py` 只离线核对这些记录与当前包的哈希、实际结果、schema和已复核预期，不调用模型、应用或数据库。
