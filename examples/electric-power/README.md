# 故障线路、未知联络与 DER

输入：[input.json](input.json)；规格：[graph-model.json](graph-model.json)；正反例：[acceptance.json](acceptance.json)。数据全为虚构，不是运行系统或 IEC 示例。

U1/TV1 的主电源 SRC-A 经闭合 SW-A 到 N1，再经 LINE-B 到 N2；备用 SRC-B 在 N3，SW-TIE 连接 N2/N3 但状态 unknown，DER-1 在 N2 也为 unknown。C1 有 SP1/N1 和 SP2/N2，C2 有 SP3/N3。分析10:20已知10:11接收的实际 LINE-B 不可用事件。

先固定 TV1 和双时间，再移除 LINE-B。SP1 有已知主电源路径，SP2 只有可能的联络/DER 路径，因此输出 uncertain_service_points=[SP2]、customer_candidates=[CUS2]，不是“SP2已停电”。SP3 不在报告回路，但它的备用电源路径不能从图中裁掉。

反例：SW-TIE=open 且 DER unavailable，SP2 才成为 disconnected_candidate；SW-TIE=closed 则 SP2 有确定路径，依然不证明允许或能够实际反送电。closed 观测若10:25才到，10:20回溯中只能视为缺状态。把事件改成 planned 只得到投影，actual_outage_count=0。

两条服务观测分别记录 SP2 在10:10–10:30和10:40–11:00中断，截止12:00合计40分钟；第二条11:10才接收，10:50已知视图只能计第一段20分钟。另一个10:20–10:35重叠证据加入后应并成45分钟，不能算55。恢复证据与拓扑候选是不同事实。

交付结论保留事件、版本、源记录、未知开关/DER及边界电源。相别、容量、保护、孤岛、电气可行性、现场验证及任何操作命令均无本例证据。

输入覆盖/patch约定见场景包内的 fixture-contract.md；机器用例可离线复核，不需要外部服务。
