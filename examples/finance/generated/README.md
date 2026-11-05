# 外部 Skill 生成的具体示例

[multi-lending.gql](multi-lending.gql) 是开发验收时实际读取并应用当前已安装 gql-query-generator 后生成的单个输出，不是本项目的语法知识库或通用生成程序。目标为 NebulaGraph 5.3.0 Database，主图规格保持数据库中立。

[生成与检查记录](generation-receipt.json) 绑定安装入口/所读资源、输入模型和输出哈希；实际运行了外部随包 lint。lint 只报告其静态检查能力；后续 [原生验收](../../../tests/compatibility/native-yueshu/README.md) 单独记录了实际 5.3.2 服务端结果。

运行前需已有与模型一致的图和 Node/Edge Types、确认贷款/机构口径，以及 `$as_of` 的目标原生时间类型和 `$min_lenders` 整数参数。没有提供图名，所以此示例要求调用者选好当前图；不伪造数据库资源。

语义走查：Borrower → Loan ← Lender，过滤指定时点有效贷款，按 lender_id 去重；同机构多笔、查询/申请、历史贷款和手机共享不增加当前机构计数。原生运行确认指定时点仅 B1 计数 2，同时验证起点包含、终点排除、同机构去重和征信不当作负债。

当前查询文件仅修复最后一个分号：在已测原生 API 中，该分号触发 42001；原字节、失败与修复哈希都保留，全部业务子句不变。SDK 结果必须检查 status_code 或调用 raise_on_error，否则错误可能被误看作空结果。

两个完整 Graph Type 的固定测试 DDL 已在 5.3.2 原生创建、回读和清理。它们用匹配实际版本的官方文档核对，不是外部查询 Skill 完整 DDL 覆盖的证明，也不是本项目的通用生成能力。5.3.0 原生执行、Procedure 和性能仍未验证。
