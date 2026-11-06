---
name: related-party-transaction-modeling
description: 设计金融关联交易的主体、持股、控制/任职证据、交易版本、时点路径、去重金额和复核模型。用于中国银行保险监管与财务披露口径对照、关联候选和反证分析；不以共享标识或持股比例自动认定关联、违法或审批通过。
license: MIT
---

# 关联交易证据与审查模型

## 输入与范围

机构类型、监管/会计制度及版本、单体/合并范围、法律主体标识、股权/任职/控制证据与有效期、交易/合同/冲正/版本、known_at、币种和业务金额口径。缺少关键身份、适用规则或证据时列明缺口，可完成模型草案。基本任务不依赖其他Skill或外部服务。

## 工作流程

1. 阅读[专项知识](references/domain.json)、[来源](references/sources.json)和[证据方法](references/method.md)，选择中国监管或财务披露制度；显式保留2025修正及后续会计解释的适用边界。
2. 从来源建立Party、OwnershipPosition、ControlAssessment、RoleAssignment、Transaction、Contract、RuleSet、RelatedPartyAssessment、RelationshipEvidence、ReviewDecision。按[完整模型](examples/graph-model.json)核对身份和来源，避免把角色固化为不同人或把股权当控制结论。
3. 对每笔交易的业务时点和已知证据截止筛选控制/任职，保留待定/撤回、过期、晚到及矛盾来源。共享电话/地址仅为线索，主体合并需独立证据。
4. 在用户明确的规则中找直接、间接或共同控制等候选路径；记录visited集合和路径证据，循环/多路径不能重复累计同一交易。无法证明只标not_demonstrated/unknown，不作法律否定。
5. 按源事件版本去重并检测载荷冲突，真实重复交易分别保留；按币种和合同/发生额/余额口径分别计算。合并披露调整不自动变成监管豁免。
6. 将候选、人工审查、批准/拒绝与实际报告分开。具体重大交易阈值、家属/任职范围、2025治理程序和时限需用户正式规则；不从演示金额推断审批结果。
7. 用[输入](examples/input.json)、[正反例](examples/acceptance.json)和[工作示例](examples/worked-example.md)检验弱线索、过期/晚到、共同国家持股、重复事件/循环路径及合并边界；按[外部交接](references/gql-handoff.md)处理另行请求的数据库表达。

## 输出

制度/时点/范围与假设；主体/关系/事件/证据模型和[图规格](references/graph-model-specification.md)（[Schema](references/graph-model.schema.json)）；候选及证据/反证；原币去重金额与调整；待复核流程、未知与正反例。候选不构成法律认定或自动审批/报送。

## 标准依据与缺口

先核实包内来源与知识条目的standard_basis：固定发布机构、版次、具体定位和支持范围，再形成项目解释。standard_gap保留未核实映射、本地政策和补证路径；本地键、阈值或判定公式不因引用标准就成为官方定义。任务缺少适用版本或来源时交付不依赖缺口的部分，并明确待核实项。

交付时读取条目的standard_status：standard-backed仅表示standard_basis.scope内有已核实标准依据，其他本地规则仍按standard_gap保留；nonstandard-modeling明确标为“非标准建模”，标准未取得或精确映射未核实的原因一并列出。不得把背景页、目录或来源分类当成条目符合性。
