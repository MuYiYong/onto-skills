# 工作示例：ETA晚到与转运扫描

[原始输入](input.json)给出SH-100的两个必需单元、三段运输和已确认订舱/已签发单证。当前业务与证据时点均为2026-11-05T12:00Z。计划到达15:00+01=14:00Z，用户延误阈值60分钟。

10Z发布的eta-new指向18:00+01=17:00Z；08Z发布的eta-old指向16:00+01=15:00Z，却到11Z才看到。依据issued_at取eta-new，delay_minutes=180，status=eta_delay。不能因旧消息更晚接收而改成60分钟。

scan-new实际发生2026-11-05T09:00+01=08Z，地点NL-PORT；scan-old是2026-10-12T12:00+08=04Z在SG-PORT的历史卸货消息，到11月5日11:05Z才补传。因此当前最新实际事件仍为scan-new。SG至NL的海运跨约24天，NL港区与最终NL-DC分别建地点和末端公路路段；两条都不能证明NL-DC交付，LU-2亦无目的地证据，所以delivery_confirmed=false、delivered_unit_ids=[]。BK-20/DOC-20不改变这个结论。

输出是[数据库中立图模型](graph-model.json)和带源事件键的异常证据。中转装卸不足以证明交接前后保管责任，context中的handover保持unconfirmed。

[验收](acceptance.json)另覆盖同ID重放与不同ID复扫、冲突ID、两个单元完整到达、只有一单元到达、时区同一时刻、当时尚未知证据、未来actual、并列冲突ETA和无时区拒绝。仅为有界离线语义证据，未运行数据库或标准合规测试。
