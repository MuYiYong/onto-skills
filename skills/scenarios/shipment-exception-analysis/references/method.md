# 运输异常判定方法

以下均为项目原创政策，来源边界见[知识](domain.json)和[来源](sources.json)。

1. 记录shipment、必需单元集合、delivery_location、里程碑、planned_arrival、用户延误分钟阈值、source_priority、业务as_of和证据known_as_of。时间输入必须带偏移，比较前转UTC。缺基线、单位身份或来源优先级则输出未知项，不猜测。
2. 以(source_system,event_id)分组。observed_at是传输观察时间，不参与语义负载指纹；其他字段不一致为冲突，整键隔离。相同负载重放只留一个事实且保留最早observed_at；不同event_id的复扫不按端点折叠。
3. 首先只使用observed_at与issued_at均<=known_as_of的记录，再校验classifier/时间/valid。actual未来于as_of属于错误证据；无时区拒绝。record_time单列，只用于来源记录审计，不决定实际轨迹或ETA新旧。
4. 轨迹仅取valid actual，以event_time选最新，晚到旧扫描不覆盖新扫描；同一最新时间有多条实际证据时全部返回。转运arrival与最终delivery_location不同，不能完成交付。订舱、单证和卸货/装载不能替代交接方凭证。
5. ETA候选限定同shipment、最终地点和arrival里程碑的estimated；取issued_at最大，再按用户source_priority取最高优先级。并列优先级与发布时间的多个不同ETA输出ambiguous_eta，不做first/last选择。planned仅为计划证据，不能充当预测。
6. delay_minutes=(ETA UTC-planned_arrival UTC)/60，仅严格大于给定阈值为eta_delay，其他为on_schedule。缺预测输出insufficient_evidence。保留ETA证据及计划基线，不把延误候选宣称合同违约。
7. 每个必需单元必须有正确shipment、最终地点与arrival里程碑的已发生actual证据，才delivery_confirmed=true。只有部分单元返回delivered_unit_ids，完整交付不确认。全部确认时status=delivered，预测字段若存在仍明确是预测。

输出字段与[验收](../examples/acceptance.json)一致：status、selected_eta_event_id、latest_eta(UTC)、delay_minutes、delivery_confirmed、delivered_unit_ids、latest_actual_event_ids、actual_event_count、duplicate_receipts、rejected_event_keys。未知值为null，不用0代替。复核报告另列来源记录时间、原因、冲突和需要的证据。

[输入](../examples/input.json)是有界源投影，不是全量Graph Model导入文件。context声明9类模型实体及缺失证据；events只投影本次判定需要的字段。关系实例和GS1号不可从未提供字段补造。

EPCIS适配边界：标准7.4.1.2允许错误声明重发原事件，eventID保持相同，除errorDeclaration/recordTime外事件内容不变。先识别并验证这一合法配对，再应用本地同键异文冲突规则；保留原始记录、声明与独立ID的更正事件。错误声明不等于物理库存冲正。包内自定义投影不冒称实现EPCIS捕获/查询接口。
