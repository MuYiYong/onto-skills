# GQL 交接请求与语义验收

输入为 [FinanceCreditRisk 规格](graph-model.json)。下列文本是交给 Agent 的请求，不是已调用记录。

> 使用当前已安装的 nebula-gql-skills，先检查是否具备目标 Graph Type DDL 能力。目标 NebulaGraph 版本由用户确认；当前模型 target 为 unspecified，先完成目标版本决定。按图规格生成定义，保留所有名称、键、属性类型/空值/多值、端点和方向。区分数据库可执行约束与应用/审查规则；无法支持的类型或约束逐项返回，不静默删除。若需查询，以 2026-02-01 的有效区间计算独立机构数量，示例阈值为 2，不计申请/征信。算法/Procedure 按实际请求加载过程技能。

如果没有 gql-query-generator/gql-procedure-generator，说明缺哪个并指向 [官方仓库](https://github.com/MuYiYong/nebula-gql-skills)；CC-Switch 添加该仓库 main/src，或下载其最新 Release 单技能包并复制到 Codex 用户 Skills 目录。已安装但不覆盖 DDL 时报告能力缺口，不自行补维护语法。

返回复核清单：

- 10 个 Node Types、14 个 Edge Types 与规格逐项对齐，事件不被折叠为属性。
- 所有主键、Account 复合身份及多重边身份保留，空键/缺端点有明确处理。
- 逻辑 decimal、datetime、标识及空值的目标物理类型有依据；币种和 UTC 口径不变。
- BORROWS/PROVIDES 等方向、时效字段和每端基数与原规格一致。
- FIBO 近似和 unmapped 项仍有说明；OWL 存在限制不被冒称为数据库推理。
- 当前有效机构按 Lender 身份去重，历史已结清/征信查询/同机构多放款正反例正确。
- 记录外部 Skill 的实际名称/版本、目标数据库版本、静态检查和原生执行分别有哪些证据。

当前状态：主模型保持目标中立；外部查询 Skill 以 5.3.0 兼容基线生成 DQL 并运行随包 lint。后续用户授权的实际服务端为 5.3.2，已完成 [固定 DDL、合成数据和查询原生验收](../../tests/compatibility/native-yueshu/README.md)。原查询分号失败被保留，删除唯一终止分号后复验通过。当前外部 Skill 的完整 DDL 覆盖仍未建立证据，测试 DDL 用实际版本官方文档核对；没有复制资源、实现通用生成器或声称 Procedure/性能已验证。
