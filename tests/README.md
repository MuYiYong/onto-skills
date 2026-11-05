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
