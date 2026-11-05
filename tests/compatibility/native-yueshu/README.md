# YueShu / NebulaGraph 原生验收

本次使用用户授权的私有连接与独立随机资源名，实际服务端为 **5.3.2**（build 2026-09-21），Python SDK 为 nebula5_python 5.3.0。地址、账户与密码不保存在这些资产中。

[终态验收](receipt.json) 包含 32 项通过的检查、源文件哈希和清理证明；[原生记录](native-records.json) 包含 54 条最终状态检查后的语句/结果。4 个错误是明确保留的预期反例：原查询终止分号与最小分号诊断为 42001、重复主键 NR205、空主键 ND008。其余语句状态均为 00000。

- 完整 lending 模型：10 Node Types、14 Edge Types，19 个合成节点、26 条边。
- 完整 fraud 模型：6 Node Types、8 Edge Types，20 个合成节点、25 条边。
- 每个声明类型都有记录；SHOW CREATE GRAPH TYPE 与原模型逐属性/空值/键/端点方向比较。Account 复合键、边 MULTIEDGE KEY、DECIMAL(18,2)、UTC ZONED DATETIME 均有原生证据。
- 五组原模型查询验证机构去重、起点包含和终点排除；B1 在指定时点计两家机构，B2 同机构多笔仍计一家，历史已结清和征信不计当前贷款。另检验手机号过期、同贷款多次放款、简单转账时间顺序/撤销过滤与待复核状态。
- 清理仅涉及 [资源清单](resources.json) 中的两个 Graph、两个 Graph Type；drop 状态通过，回查无剩余同前缀资源，目录总数恢复到原值。没有查询或修改现有业务图的数据。

Graph Type 与 Graph DDL、节点/边 DML 和场景查询均为此处的固定测试用例，不是通用语法生成器。DDL 根据与实际版本匹配的 [官方规范](https://dev-docs.nebula-graph.io/v5.3.2/database-gql-reference/ddl/graph-type/create/) 编写；查询/DML 同时使用当前安装的外部 GQL Skill。没有复制该 Skill 的文件或语法库。当前外部 Skill 的完整 DDL 覆盖仍需独立核实，原生数据库支持 DDL 不等于该 Skill 已声明该能力。

## 失败与修复

[原查询](pre-repair-multi-lending.gql) 最后有分号。原生 API 返回 42001，而初版测试脚本只迭代结果行、没有调用 SDK 的 raise_on_error，错误被误看作空结果。最终验证已明确记录 status_code/message 并调用 raise_on_error；重连后重跑全部业务查询和错误反例，结果见 native-records.json。原始 [setup-observations](setup-observations.json) 保留其状态检查局限，不作为 SQL 成功状态依据；最终模型回读/类型计数独立证明创建及导入状态。

当前 [查询文件](../../../examples/finance/generated/multi-lending.gql) 只删除了最后一个分号，所有业务子句不变。所有最终信贷验收均执行当前文件的相同字节，哈希已绑定。该结论限定本次 SDK/服务端原生 API；没有推广为所有客户端禁止分号。

## 复现边界

普通 CI 只通过 test_native_evidence.py 检查已记录证据与当前源文件的一致性，不自动连接数据库。

重新做原生验收时使用现有官方 SDK 或 ngql：选择新的唯一资源名前缀、确认不存在；按固定 DDL/DML 建立自己的测试资源；设置当前图和 typed SESSION SET VALUE 参数后执行查询；逐条检查状态而不只看结果行；最后只删除自己创建的图和类型并回查。密码用 getpass/工具现有密码提示输入，不放命令行、文件或报告。SDK execute_py 是模板渲染，不能假定它直接绑定 `$as_of`。

这些小规模合成数据不证明生产语义、吞吐、性能、全部版本兼容、完整 FIBO/OWL 推理、Procedure 或 CC-Switch/macOS 行为。
