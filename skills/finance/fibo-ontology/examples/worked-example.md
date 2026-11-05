# FIBO Loan 有界对齐

来源为 references/fibo-index.json 记录的官方固定 revision，实际解析 LOAN/LoansGeneral/Loans.rdf；这是原创说明，不分发原本体。未递归取得 imports，未运行推理。

输入：业务仅需按期偿付贷款的机构和有效期分析，已有 loan_id、principal_amount、currency。

1. 标准入口为 `https://spec.edmcouncil.org/fibo/ontology/LOAN/LoansGeneral/Loans/Loan`。观察到直接父类 CreditAgreementRepaidPeriodically 与 DebtInstrument，不能静默丢失。
2. 观察到 hasPrincipalAmount some MonetaryAmount。企业 amount/currency 扁平化会失去量值对象的身份与相关推理；记录 approximated 和 application 检查，而非宣称完全等价。
3. hasGuarantor 的 qualified minimum 0 不是必须存在保证人的限制。本范围不处理担保，不构造缺失保证人。
4. 企业 loan_id 属于扩展命名空间，不冒充 FIBO 的标准主键。父类不单建类型，但 mappings 保留 URI、含义与未实施推理的损失。
5. 未展开 imports、其他限制和复杂偿付计划。交付“有界候选”，需用户接受损失与业务范围才能用于最终模型。

输出项：版本/来源表；选中类/必要父类/属性/限制；裁剪排除项；业务扩展；图映射及损失；imports 状态。若任务要求完整标准语义，先取得确切版本和闭包再继续，不能用这个局部示例代替解析。
