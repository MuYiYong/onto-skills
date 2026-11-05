---
name: retail-inventory-replenishment
description: 为SKU/地点/批次/单位粒度的库存、预留和补货建议设计证据图与规则。用于快照加原子运动、晚到退货、受损库存、冲正和用户阈值分析；不把在途、订单或销售金额当作实存，不自动创建采购单。
license: MIT
---

# 零售库存与补货证据建模

## 定位、适用与边界

将用户业务问题和源数据转成可解释的本体/属性图交付物以及有证据的场景判定。适用于场景设计、规则澄清和既有模型审查；不执行生产变更、自动业务操作或标准认证。本包直接安装后自足，无需预装其他技能或联网读取知识。

## 输入

最小输入：stock grain、带覆盖边界的快照、原子运动事件及全部postings、source_system+event_id、带偏移event_time/observed_at、as_of与known_as_of。可用量/补货另需预留状态版本、明确available政策、同单位reorder_point和target。可选：在途、订单/销售/退货单据、金额币种、GTIN/GLN映射与单位转换证据。

数据缺失时先列影响、待确认项与可继续部分；不能把未知当0或补造事实。

## 工作流程

1. 固定SKU/地点/lot_issuer/lot/condition/unit及时间截点，声明快照和后续运动完整性，缺lot不并入已知批次。
2. 阅读[领域知识](references/domain.json)与[来源](references/sources.json)，按[方法](references/method.md)区分测量、运动、预留状态和商业单据。
3. 校验原子事件键、全部postings、单位与冲正；重放幂等，任一posting失败整事件不纳入，不修改已接受历史。
4. 每个库存状态取最新有效快照，仅加快照后的实际运动；处理晚到证据、受损退货、预留版本与区间。
5. 用户政策明确时计算可用量与阈值信号，保留负数和在途单列；输出解释及order_created=false，不执行采购。
6. 按[图规格](references/graph-model-specification.md)交付[完整模型](examples/graph-model.json)，用[输入](examples/input.json)、[工作示例](examples/worked-example.md)和[验收](examples/acceptance.json)核对具体正反例。

## 输出

范围与用户参数；概念/关系/生命周期；Graph Model Specification1.0（目标未定保持数据库中立）；身份/时间/单位与来源字段；应用层约束和标准映射损失；场景结论、具体数量/时间/证据键、反证及未知；验收结果与执行证据限制。

## 资源

[本地方法](references/method.md)、[领域JSON](references/domain.json)、[来源JSON](references/sources.json)、[图规格](references/graph-model-specification.md)、[本地Schema](references/graph-model.schema.json)、[工作示例](examples/worked-example.md)、[输入](examples/input.json)、[模型](examples/graph-model.json)、[验收](examples/acceptance.json)和[许可证](LICENSE)全部随包提供。外部来源链接只作可选核实。

## 质量检查与约束

每个结论能回到来源键与评价/证据时点；正常业务反例不误报。核对来源许可、身份范围、时间/单位、事件完整性与冲突处理。标准背景与项目政策分别标注，用户阈值不冒称行业规定；静态有效不证明真实数据完整、标准合规或数据库执行。需要GQL时交接完整规格、目标与确切版本给外部已验证生成能力，并复核返回语义；本包不提供GQL语法或执行工具。
