# 从“回路停电”到明确的知识边界

输入：“C1回路有两个供电点，LINE-B故障，SP2是否停电？联络开关状态未到，现场有DER。”

将“回路”解释为报告范围，将物理连接解释为版本化端子/连接点关系。要求 LINE-B、开关、DER 与供电点身份及拓扑版本；用有效时间查业务状态，用 observed_at 判断当时是否已知。

输出概念包括 Equipment、Terminal、ConnectivityNode、TopologyVersion、StateObservation、Circuit、ServicePoint、Customer、OutageEvent、RestorationSegment。关系把状态与台账、客户与供电点分开。即使 LINE-B 已不可用，未知开关和 DER 仍可能供电，因此只能列不确定候选；需要服务证据确认实际中断。

正例：确认联络 open 且 DER unavailable 后可列无路径候选。反例：仅因同回路就断言全部客户停电，或把迟到的 closed 观测用于过去已知视图，均不成立。来源为包内 CIM/CGMES 索引，具体三值规则是本项目整理，不是官方操作规程。
