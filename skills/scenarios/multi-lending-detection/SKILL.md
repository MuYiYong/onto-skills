---
name: multi-lending-detection
description: 为多头借贷识别设计借款人、机构、授信、申请、放款、征信、手机与收款账户的时序图模型及风险口径。用于多机构重叠负债、行为顺序和共债关联建模；不把查询/申请或共享标识直接视为借贷事实。
license: MIT
---

# multi-lending-detection

## 定位与解决的问题

将具体风险问题转成可解释、有时间和证据的业务图模型。

## 适用与不适用

用于请求的风险场景建模与图语义设计，不直接运行风控审批或写生产数据。不需要预装其他本体/金融技能。

## 输入

业务问题、时间窗口、脱敏 Schema/样例、主体/事件标识、来源和规则参数。缺失机构粒度、身份或时间口径时先列未决项；可交付不依赖缺口的模型草案。

## 工作流程

1. 固定风险问题、as_of、窗口、机构粒度与用户阈值。示例阈值仅为演示，不是监管或机构审批规则。
2. 读 [领域最小知识](references/domain.md) 和 [来源](references/sources.json)，提取 Borrower、Lender、LoanApplication、CreditFacility、Loan、Disbursement、Repayment、CreditInquiry、Phone 与 Account。
3. 明确主体身份与匹配证据；手机号/账户共享不自动等于同一人。只有关系分析有需要才将标识建节点，其他简单字段保持属性。
4. 将申请、查询、授信、放款、还款作为不同业务事实；事件有独立来源编号与参与方，不用同一条无类型“申请记录”替代全部。
5. 为主体-手机号/账户绑定设计 valid_from/valid_to/observed_at，为业务事件设计 event_time/observed_at；支持重复发生、晚到、冲正与关系失效。
6. 对当前有效贷款按机构身份去重，再计算重叠负债与时间窗口；遵循 [时序与风险规则](references/method.md)。缺失结束/余额口径时给出不确定结论。
7. 识别跨主体共享证据、集团/共债关系和行为先后；每个候选保留原始事实、时点、匹配方式、反证与待复核项。
8. 输出完整模型与规则；按 [示例](examples/worked-example.md) 的正反例验收。若需 GQL 走 [外部交接](references/gql-handoff.md)，不在本技能补语法。

## 输出

范围/参数与假设；概念和时序关系表；属性图规格或 Graph Model Specification；窗口与机构去重规则；风险候选/证据路径；正反例；知识缺口及质量结果。

## 资源

流程中链接的知识、来源、决策方法和示例均在本包内。需要完整规范化交付时参考 [图规格](references/graph-model-specification.md)；联网仅用于可选来源核实。

## 质量检查与约束

用正常业务反例测试误合并和误报，核对身份、时效、来源与规则的执行位置。推断标 model-inference；示例不是监管阈值。静态建模与实际数据库运行分别报告。Core/Finance 的组合是可选增强，只传递交付物，不依赖其他包文件。

## 示例

见 [完整工作示例](examples/worked-example.md)。
