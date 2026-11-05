# Graph Model Specification 1.0

这是一份数据库中立的模型交付物，不是数据库 DDL。完整机器可读定义为 [JSON Schema](../schemas/graph-model.schema.json)，完成示例为 [金融模型](../examples/finance/graph-model.json)。

顶层字段：spec_version、model_id、version、graph_type、description、target、source_catalog、node_types、edge_types、constraints、mappings、assumptions、unresolved、competency_questions。

target.database/version 是任务目标及版本；未选定写 unspecified，不把逻辑类型当成物理类型。property.logical_type 是 string、identifier、integer、decimal、boolean、date、datetime、json；精度、时区、货币/单位等放进约束。数据库适配必须核实转换和执行能力。

节点：name、business_meaning、identity_scope、primary_key、properties、source_ids。每个属性有 name、logical_type、nullable、multivalued、business_meaning、source_ids。键字段必须存在、非空、单值且有稳定的业务范围，不能用名称/电话替代身份。

边：同样记录身份和属性，另含 from/to、direction=outgoing、cardinality.per_source/per_target，以及 temporal.kind/start/end/observed_at。边键表达实例身份；是否在端点/类型内唯一需写 identity_scope。重复发生不能被端点键折叠。基数含时间与条件语义，不自动编译成数据库约束。

时间采用 UTC datetime；区间默认 [start,end)，end 为空含义需明确。kind 为 none/event_time/valid_time/bitemporal；bitemporal 的 observed_at 只记录观测时刻，若要完整系统有效区间，应另加 recorded_to 并说明更新历史策略。时间字段必须对应真实属性，时间范围规则放 constraints。

constraints 每项：id、subject、rule、enforcement、source_ids。subject 为 model、node:Name、edge:Name 或 property:Type.field；执行位置为 database/application/review/unresolved。database 需额外运行证据，不能根据标准语义猜测已支持。

mappings 每项：id、source_id、source_term（标准 IRI/源字段/公理表达）、target（同 subject 格式或 null）、status（preserved/approximated/unmapped）、explanation、constraint_ids。unmapped 的 target 必须 null；每项均解释差异及影响，无法映射的语义不得静默丢弃。

source_catalog 包含来源 URI、精确版本、机构、许可、范围、权威性、日期与类型。标准来源并不意味着图映射是标准定义。unresolved 列尚未确定的事项及确认办法；assumptions 为已显式说明的建模假设。

结构有效与可交接有区别：草案可含 unresolved；ready 要求关键设计已定、约束执行位置已定、损失已获业务接受。开发验证器 validate_model(model, ready=True) 检查机器可判定部分；领域合理性仍需业务问题/反例验收。

GQL 请求应同时带上原规格、目标版本、业务问题、限制和不允许改变的语义。回传 DDL 后核对元素、键、类型、端点/方向、时间与约束；未运行数据库就标“语义复核，执行未验证”。
