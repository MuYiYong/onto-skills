# 2026-11-06 标准优先资产原生记录

本次冻结27个独立包、227个文件，完整原始包字节见 [source-packages.tar.gz](source-packages.tar.gz)，哈希见 [manifest.json](manifest.json) 和 [source-files.json](source-files.json)。证据按运行层次分别记录，不能相互替代。

| 层次 | 实际结果 | 证据 |
| --- | --- | --- |
| Codex CLI0.166.0 原生发现 | project及legacy-codex-home两种布局，单项/全部27项，227文件读取及源哈希通过 | [discovery.json](discovery.json)，无模型调用 |
| CC-Switch4.0.25 Linux原生GUI | 隔离Ubuntu24.04真实GTK/WebKit桌面，全27项ZIP安装/SSOT及Codex同步；227文件逐字节哈希一致；场景Codex开关关闭保留其余26项、恢复27项；全量卸载终态为零 | [desktop](desktop/)，安装/卸载截图、实际原生Codex发现、路径及哈希；测试容器未挂载宿主用户配置 |
| 当前Codex代理运行时应用 | 21个修改/新增技能完成有界合成任务；逐个完整自足包隔离，实际读取资源、输出schema及根代理语义复核通过 | [review.json](agent-application/review.json)，每项保存请求/schema/结果/读取收据及全部包文件清单 |
| 本地CLI推理 | 5次任务均退出1、turn.failed，内建重试后HTTP429，没有模型结果 | [cli-failures](cli-failures/)，保留默认及显式模型路由失败；不计为试用通过 |

代理运行时的两项先导任务使用独立代理，其余任务共享一个审阅代理上下文；目录仅安装自身，禁止读取示例/答案/验收资源。完整包文件哈希由根代理另行验证，审阅代理只声明实际消费文件，不能把清单当作实际读取证明。这不是21个独立CLI进程、CLI版本兼容性或隐式触发准确率证明。

关联交易原试用发现CAS36获取说明过时，原输出与旧方法留在[superseded-related-party](superseded-related-party/)，不计入最终21项；修正后在新目录重新应用、读取和复核。历史25项/13项证据也保持原字节，不用修改后的源码回填旧结果。

macOS原生应用、远程安装/升级、完整标准认证和生产数据库均未在本轮运行。CI仅离线复核上述证据的完整性及有界结果，不重新调用服务或GUI。标准范围另见[核验报告](../../../docs/standards-verification.md)。
