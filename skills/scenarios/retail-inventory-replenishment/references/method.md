# 库存与补货判定方法

以下规则是示例输入显式给定的项目政策，不是GS1官方库存算法。结合[概念](domain.json)和[来源](sources.json)阅读。

1. 固定stock_scope、as_of、known_as_of、基础单位、快照覆盖边界和运动完整性声明。示例只算一个merchant/sku/location/lot_issuer/lot/unit，sellable与damaged各有快照；未知批次或无锚粒度不能当0。
2. 对每个condition取event_time<=as_of且observed_at<=known_as_of的最新快照。该快照明确覆盖event_time<=快照时点的运动。多张快照不累加；同截面冲突先隔离/对账，不能任选。
3. StockMovement按source_system+event_id作原子键，以排除observed_at的完整语义负载辨重。相同负载重放一次，冲突负载整键隔离。每条posting带精确十进制quantity_delta和完整库存粒度；无转换的单位混合导致整事件零posting生效。
4. 按event_time/来源键确定性处理已知且已发生的事件。damage在相同SKU/地点/lot/unit内sellable减少和damaged增加等量；receipt/return正向、sale/disposal负向。reversal必须引用此前有效的非reversal原事件，逐条精确反向且最多冲正一次，部分/未知/重复冲正整事件拒绝。先验证全事件，再应用任何posting。
5. 对目标粒度，仅在posting.event_time>该condition快照时点时累加。之前/等于锚的晚到消息列pre_anchor_event_keys用于对账，不再叠加。跨lot/地点的posting不进入本粒度；在途与商业单据不作为posting。
6. 预留按source_system+reservation_id选known_as_of可见且valid_from<=as_of的最高revision，检查无冲突、同粒度、非负数量和有效区间[valid_from,valid_to)，null明确为未结束。仅active扣减；released/fulfilled/cancelled不扣。冲突版本使available未知，不能按最后一行选择。
7. 用户给定available_rule=sellable_on_hand_minus_active_reserved时才计算available；保留负值并提示。用户给定同单位target>=reorder_point>=0，available严格小于reorder_point才输出signal，suggested_quantity=target-available；等于阈值不触发。在途outstanding_quantity单列且不自动抵扣建议。无规则输出policy_required与null结论。

[验收](../examples/acceptance.json)输出status、on_hand_by_condition、reserved、available、in_transit、restock_signal、suggested_quantity、order_created=false、duplicate_receipts、rejected_event_keys、pre_anchor_event_keys、warnings。数量是十进制字符串，未知是null，金额不参与计算。拒绝/不足证据须另列原因，不声称已对全量库存审计。

[输入](../examples/input.json)是有界源投影，商业行、预留状态和实际postings分别提供，并不是全量Graph Model导入。完整模型还声明了外键、边身份和来源定位字段，缺失时不补造。快照与运动相互完整性的假设必须交给业务确认。

EPCIS适配边界：标准7.4.1.2允许错误声明重发原事件，eventID保持相同，除errorDeclaration/recordTime外事件内容不变。先识别并验证这一合法配对，再应用本地同键异文冲突规则；保留原始记录、声明与独立ID的更正事件。错误声明不等于物理库存冲正。包内自定义投影不冒称实现EPCIS捕获/查询接口。
