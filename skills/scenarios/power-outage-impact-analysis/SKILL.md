---
name: power-outage-impact-analysis
description: 为停电影响候选分析建立带版本的设备/端子/连接点、开关/电源状态、供电点/客户/回路和恢复分段图模型。用于计划或实际停电的范围、未知反送电和时长证据分析；不生成倒闸指令或证明安全供电。
license: MIT
---

# power-outage-impact-analysis

## 定位、适用与边界

从台账、拓扑和观测资料交付可复核的停电候选范围及数据库中立图规格。适用于业务建模、数据质量检查、证据追溯；不替代潮流/保护/相别仿真、现场确认、调度许可或客户停电认定。本包自带最小知识，不依赖其他 Skill。

## 输入

最低：utility_id 范围的设备/端子/连接点、拓扑版本及有效/接收时间、开关和电源状态、待分析设备停电、供电点/回路/客户绑定、event_as_of 和 knowledge_cutoff。增强：DER/边界电源、服务观测、恢复分段及相别/量纲信息。缺状态输出 unknown；无唯一兼容版本不能给出确定影响名单。

## 工作流程

1. 固定计划/实际模式、事件与观测截止时间、报告回路及边界。读 [领域知识](references/domain.json)、[来源](references/sources.json) 和 [方法](references/method.md)。
2. 以 utility_id 限定稳定身份；按 event_as_of 选择有效且已知的单一拓扑。端子归属/连接、服务绑定和状态必须兼容同一版本，不能拼接未来资料。
3. 将台账、正常设计状态与实际观测分开；保留 source key、event_time/valid interval、observed_at、证据质量。冲突状态不按最后写入静默覆盖。
4. 移除指定不可用设备，分别建确定连接和可能连接。closed/open 是确定证据；unknown/缺状态只影响可能连接。DER/边界电源未知状态也保留可能供电。
5. 从已知电源求确定可达，从确定/可能电源和可能边求可能可达。无确定但有可能路径标 uncertain；两者皆无标 disconnected_candidate。已知可达只标拓扑筛查未失去路径，不能证明实际带电。
6. 报告范围按供电点/回路筛选，但保留跨范围边界路径；客户按有效绑定去重。计划仅输出投影，不计实际停电；客户实际中断需服务证据。
7. 恢复分析仅使用已知的实际中断分段；同供电点求区间并集，保留重复停电，未知恢复终点不补成已恢复。
8. 按 [图规格](references/graph-model-specification.md) 输出模型/映射/限制，通过 [完整示例](examples/worked-example.md) 与 [机器验收](examples/acceptance.json) 的正反例。数据库语法按 [外部交接](references/handoff.md) 单独核实。

## 输出契约

范围与双时间参数；唯一拓扑/状态来源；完整 Graph Model Specification；每个供电点的 disconnected_candidate/uncertain/unaffected_by_topology 分类、证据路径及未知原因；去重客户/回路范围；计划/实际区分；观测恢复段、已证实时长与未关闭段；未决事项、来源适用性及验证层级。机器结果字段见 [输入/验收约定](references/fixture-contract.md)。

## 质量检查

验证未知开关不被当作 open/closed、晚到状态未提前参与、跨回路已知电源未截断、DER 未知未被忽略、客户不重复计数及恢复重叠不重复累计。容量/相别/保护/孤岛和现场安全未验证时明示边界；不发出操作性切换命令。CIM/CGMES 来源不赋予本地模型标准认证。
