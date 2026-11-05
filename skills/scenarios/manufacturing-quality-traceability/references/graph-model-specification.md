# Graph Model Specification 1.0

本包包含 [JSON Schema](graph-model.schema.json) 和 [完整模型](../examples/graph-model.json)。它们描述数据库中立交付物，不是 DDL。

顶层必须有 spec_version/model_id/version/graph_type/description/target/source_catalog/node_types/edge_types/constraints/mappings/assumptions/unresolved/competency_questions。target 未选定时 database/version 都是 unspecified。

每种节点记录业务意义、identity_scope、primary_key、properties 和 source_ids。属性有 logical_type、nullable、multivalued、business_meaning 和 source_ids；键必须是存在、非空、单值的标量。类型是 string/identifier/integer/decimal/boolean/date/datetime/json；精度、单位和时区约束另列。

边另有 from/to、direction=outgoing、cardinality 和 temporal。关系记录有独立 identity_scope/键，重复事件不能只按端点折叠。temporal.kind 为 none/event_time/valid_time/bitemporal，字段引用真实 datetime 属性。bitemporal 在此只保证业务有效区间和 observed_at，完整系统有效历史还需另建记录终止时间及修订策略。

constraints 的 subject 指向 model、node:Name、edge:Name 或 property:Type.field，enforcement 指明 application/review/database/unresolved。声称数据库执行须有实际证据。mappings 记录来源词、目标、preserved/approximated/unmapped 与解释、约束引用；unmapped 的 target=null。来源的官方地位不使本地图映射变成官方公理。

完整来源目录列 id/name/uri/version/publisher/license/retrieved_at/scope/authority/kind。草案允许 unresolved；下游执行前应处理阻塞项并核实目标版本。结构有效不证明业务正确，应运行正反例并保留不确定性。
