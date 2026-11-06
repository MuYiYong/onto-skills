# 环境观测质量与阈值候选：投影与验收

标准基线：OGC SensorThings API Part 1: Sensing 1.1（18-088）。三个文件分别是[合成输入](input.json)、[数据库中立图规格](graph-model.json)、[手工预期](acceptance.json)。共有14个手工期望案例，开发侧参考计算消费投影字段；没有原生IFC/完整SensorThings/签名凭证校验。

图规格为设计草案，未选数据库版本，有明确unresolved。JSON结构通过不代表部署就绪。图模型是可复用设计；input.json只覆盖下面明确列出的案例投影，未构造所有SourceRecord、属性断言与边实例，不声称做过完整入库往返。

## 原始字段到本地投影

| 本地字段 | 标准字段或来源 | 取舍与损失 |
| --- | --- | --- |
| service / id | 服务根及资源路径 / @iot.id | 示例字符串ID是显式投影；实体集合由数组语境提供，真实ID类型或完整URI须保留。 |
| stream_id / foi_id | Observation.Datastream / FeatureOfInterest | 导航关系展开为源范围标识，不把Location替代FOI。 |
| observed_property / unit_definition | Datastream.ObservedProperty.definition / unitOfMeasurement.definition | 省略单位name/symbol，不支持按展示名换算；urn:example的指标/单位为合成标识。 |
| phenomenonTime / resultTime / resultQuality | Observation同名字段（Table18） | 原始质量结构保留；result用十进制字符串投影，不宣称原生JSON序列化通过。 |
| quality_decision / observed_at | 本地质量审核 / 观测及元数据接收时间 | 不是OGC字段或枚举；已知时点与测量时间独立。 |
| policy / expected.status | 本地阈值与复核输出 | 没有采用任何法定环境限值；区间、validTime、其他测量类型另需政策。 |

## 能力问题与反例

| 问题 | 关键模型元素 | case_id |
| --- | --- | --- |
| 哪些观测在指定被测对象、时间与质量条件下超过本地阈值？ | ObservationAssessment / ThresholdPolicy / OBSERVES_FEATURE | above-local-threshold, equal-threshold, other-foi, window-boundary, wrong-property |
| 同一局部ID跨服务或同ID不同载荷如何保留？ | ObservationRecord / DatastreamSnapshot / SourceRecord | duplicate-observation, conflicting-result, other-service-id |
| 区间结果、缺质量、单位不符和晚到记录为何不能直接判断？ | ObservationRecord / ObservationAssessment | missing-result, quality-unknown, wrong-unit, late-known, time-interval, null-result-time |

结果必须带可定位的源版本、标准支持范围、本地政策和不足。名称相似度或一个质量总分不能绕过必需证据。对未支持的原生字段或不完整输入给出补证要求，不静默丢弃。
