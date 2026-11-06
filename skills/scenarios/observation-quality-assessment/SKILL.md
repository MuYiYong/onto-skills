---
name: observation-quality-assessment
description: 为环境监测设计基于观测质量、被测对象、时间、单位和用户阈值的证据图。用于SensorThings1.1观测异常复核、乱序重放与缺失分析；不输出法定超标结论。
license: MIT
---

# 环境观测质量与阈值候选

## 任务与输入

独立完成给定材料的数据库中立建模。最小材料：监测对象、服务/资源标识、Datastream与Observation字段及来源。阈值场景另需FeatureOfInterest、单位定义、质量证据、评价/已知时点和明确本地政策。 未给材料列待补证，仍可交付有依据的概念和字段设计。标准基线为OGC SensorThings API Part 1: Sensing 1.1（18-088），适用Profile与业务政策由当前任务明确。

## 工作流程

1. 读取[来源](references/sources.json)与[知识](references/domain.json)中相关条目。区分standard_basis的具体支持范围与standard_gap；project-curated摘要不冒充官方定义。
2. 先固定问题、范围、输入粒度及政策，再依方法形成可审查的节点/边/身份/时间和证据链。对每个判断保留输入与反证，冲突不能靠默认值消除。
3. 依[方法](references/method.md)处理领域身份、时间、关系和特殊值；原始记录、标准解释、推断和本地政策分层。
4. 按[证据复核](references/evidence-review.md)记录源定位、内容绑定、修订/派生关系和身份候选。只有实际证据支持的范围可下结论。
5. 用[工作例子](examples/worked-example.md)检查区别、未知和反例；交付标准定位、模型/语义、字段来源、假设、缺口与质量问题。

## 交付与质量

输出可被独立审查的术语/角色和实体关系表、稳定身份、时间与来源表、标准映射及损失、本地政策和待决问题。表格中给出字段名、业务含义、标准位置、证据及不能推出的结论。可从包内材料完成基本工作，无需另一Skill或联网。未运行的工具、真实验证与生产效果保持未验证。

所有解释以用户给定范围为准；不执行生产写入。需要数据库实现时交接完整图规格及选定目标版本给外部已验证能力，本包不生成GQL。包内原创内容见[许可](LICENSE)，第三方标准保持其各自许可。

## 场景规格与验收

按[图规格](references/graph-model-specification.md)和[Schema](references/graph-model.schema.json)交付，参考[完整模型](examples/graph-model.json)、[合成输入](examples/input.json)和[手工预期](examples/acceptance.json)。字段投影和问题到反例的对应见[示例说明](examples/scenario-guide.md)。target未选择、unresolved未解决时保持草案状态。测试预期仅描述合成案例，不是完整标准符合性、真实验签或部署证明。
