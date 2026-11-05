# 金融端到端示例

所有数据与企业规则均为虚构；这是完整的建模/交接演示，不是已运行的数据库应用。

输入见 [业务与 Schema](input.json)：指定时点判断哪些主体存在多机构有效贷款，解释共享手机/收款账户关联，同时区分申请、授信、征信、放款和还款。输出见 [融合图规格](graph-model.json)、[标准裁剪草案](top-down-graph-model.json)、[欺诈调查模型](fraud-graph-model.json)。

## 自下而上

1. industry-knowledge-discovery 从输入提取术语和知识缺口；finance-domain-knowledge 澄清授信不是放款、查询不是负债。
2. ontology-modeling 识别借款主体、机构、贷款、事件和上下文角色。账户/电话只有需要跨主体时序分析才建节点；产品状态/目的留属性。
3. entity-relationship-modeling 定义稳定主体 ID、机构粒度和事件来源键。借款/提供方向是 Borrower/Lender → Loan，端点相同的两笔贷款不能合并。Account 使用机构/标识/体系的复合键。
4. banking-business-model 与 credit-risk-knowledge 检查流程、金额口径和业务边界：额度、放款、余额不可重复相加；示例暂排除联合借款、银团贷款、担保与集团暴露。
5. multi-lending-detection 明确 as_of、UTC 半开区间、观测时间、机构去重和例外。示例阈值为 2；B1 有两家有效机构，B2 两笔同机构只计一家，B3 已结清加征信查询不算当前多头。

概念模型：主体参与贷款合同，机构提供贷款；申请/查询/放款/还款是分别可追踪的事件；授信是额度安排；电话/账户是有时间证据的关联对象。主键和生命周期见 JSON。

## 自上而下

使用 FIBO 官方来源的固定 revision `33a92cd34285d532c158da97bb42add089f135d3`，本地保存原创摘要与 URI，不重分发本体。已读取 Loans.rdf 的 Loan 类、直接父类和部分限制；未递归加载 imports，未运行 OWL 推理。

- Loan 类 IRI：`https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/Loans/Loan`。
- 直接父类 CreditAgreementRepaidPeriodically、DebtInstrument：保留映射解释，当前例子不单建父类类型或实现继承推理。
- hasPrincipalAmount some MonetaryAmount：以 principal_amount/currency 近似；损失 MonetaryAmount 对象身份与相关推理，增加应用检查。
- hasGuarantor qualified minimum 0：不能解释成“每笔必须有保证人”。担保不在当前业务范围，不伪造保证人。
- 生产/开发与 imports 要按实际版本重新核对。这里只是有界标准对齐，不声称完整 FIBO 合规。

[标准裁剪草案](top-down-graph-model.json) 保留未决项，因此不是 ready。企业 loan_id/机构代码和事件字段均为业务扩展，没有复用/重定义标准 IRI。

## 融合与验证

property-graph-mapping 将业务角色/时效与上述标准对齐合并为 [图规格](graph-model.json)。它包含 10 种节点、14 种边、完整属性/主键/方向/每端基数、约束执行位置、来源、5 项映射以及明确损失。示例假设接受有界损失，真实应用需业务确认。

ontology-validation 的结构检查发现端点、键、类型及来源闭合；示例反例覆盖同机构多笔、历史已结清与查询不等于负债。后续已在用户授权的 5.3.2 数据库完成完整模型 DDL/样例数据和查询正反例的 [有界原生验收](../../tests/compatibility/native-yueshu/README.md)。真实业务专家签认、完整 OWL 推理、金额暴露和机构合并口径仍不由这些合成数据证明。

ontology-documentation 可据模型生成设计说明；ontology-evolution 可在将 Loan 键改为复合来源键、加入联合借款或升级 FIBO 时给出兼容/回填/回滚计划。

## 可选 GQL 交接

用户要求 NebulaGraph 输出时，使用 [交接请求与复核清单](gql-handoff.md)。开发中实际应用已安装 gql-query-generator，形成了 [有界查询输出及 lint 记录](generated/README.md)；它是具体示例，未复制外部资源或语法库。仅本体设计在以上步骤即可完成；GQL 执行需要目标环境。

完整链路：业务+Schema → 金融理解 → 概念/实体关系 → FIBO 有界对齐 → 属性图规格 → 外部查询生成 → 语义复核与原生验收。当前已完成查询生成/lint，以及 5.3.2 的固定 DDL、合成数据和查询执行；Procedure、真实业务与规模性能未验，具体边界见交接与原生记录。
