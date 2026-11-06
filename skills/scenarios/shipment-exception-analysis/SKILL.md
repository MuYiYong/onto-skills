---
name: shipment-exception-analysis
description: 为运输延误、转运与交付异常设计Shipment/Consignment/物流单元及计划、估计、实际事件的时序证据图。用于ETA比较、晚到乱序、消息重放、部分交付和交接追踪；不把订舱或计划到达当作实际签收。
license: MIT
---

# 运输异常与交付证据建模

## 定位、适用与边界

将用户业务问题和源数据转成可解释的本体/属性图交付物以及有证据的场景判定。适用于场景设计、规则澄清和既有模型审查；不执行生产变更、自动业务操作或标准认证。本包直接安装后自足，无需预装其他技能或联网读取知识。

## 输入

最小输入：shipment与必需物流单元身份、目的地点/里程碑、带偏移时间的事件记录、source_system+event_id、issued_at/observed_at、评价as_of与known_as_of。ETA判定另需计划基线、用户延误阈值和来源优先级。可选：路段、订舱/单证版本、交接双方证据和已核实GS1标识。

数据缺失时先列影响、待确认项与可继续部分；不能把未知当0或补造事实。

## 工作流程

1. 固定范围与参数，列清shipment、consignment、unit、leg及booking/document的不同身份。
2. 阅读[本地领域知识](references/domain.json)和[来源](references/sources.json)，依[方法](references/method.md)区分三类事件与四种时间，建立可追溯键。
3. 对重复、冲突、时区、未发生actual及证据截点执行校验；每项保留原记录引用和拒绝原因。
4. 建模转运成员关系和交接证据；按目标地点/里程碑选择当前有效ETA并比较用户基线，分别输出部分单元和完整交付结论。
5. 按[图规格](references/graph-model-specification.md)交付节点、边、键、时间、约束、映射损失与来源；参考[完整模型](examples/graph-model.json)，target未选定写unspecified。
6. 使用[输入](examples/input.json)、[工作示例](examples/worked-example.md)和[验收](examples/acceptance.json)复核正反例；缺证据保留未知，不关闭异常。

## 输出

范围与用户参数；概念/关系/生命周期；Graph Model Specification1.0（目标未定保持数据库中立）；身份/时间/单位与来源字段；应用层约束和标准映射损失；场景结论、具体数量/时间/证据键、反证及未知；验收结果与执行证据限制。

## 资源

[本地方法](references/method.md)、[领域JSON](references/domain.json)、[来源JSON](references/sources.json)、[图规格](references/graph-model-specification.md)、[本地Schema](references/graph-model.schema.json)、[工作示例](examples/worked-example.md)、[输入](examples/input.json)、[模型](examples/graph-model.json)、[验收](examples/acceptance.json)和[许可证](LICENSE)全部随包提供。外部来源链接只作可选核实。

## 质量检查与约束

每个结论能回到来源键与评价/证据时点；正常业务反例不误报。核对来源许可、身份范围、时间/单位、事件完整性与冲突处理。标准背景与项目政策分别标注，用户阈值不冒称行业规定；静态有效不证明真实数据完整、标准合规或数据库执行。需要GQL时交接完整规格、目标与确切版本给外部已验证生成能力，并复核返回语义；本包不提供GQL语法或执行工具。

## 标准依据与缺口

先核实包内来源与知识条目的standard_basis：固定发布机构、版次、具体定位和支持范围，再形成项目解释。standard_gap保留未核实映射、本地政策和补证路径；本地键、阈值或判定公式不因引用标准就成为官方定义。任务缺少适用版本或来源时交付不依赖缺口的部分，并明确待核实项。

交付时读取条目的standard_status：standard-backed仅表示standard_basis.scope内有已核实标准依据，其他本地规则仍按standard_gap保留；nonstandard-modeling明确标为“非标准建模”，标准未取得或精确映射未核实的原因一并列出。不得把背景页、目录或来源分类当成条目符合性。
