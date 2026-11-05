# 有界工作示例

输入（虚构）：P1/P2 在同日观测到设备 token-D；P1 账户向 P2 账户转账 T1，P2 在后续向 P3 转账 T2；P4 只与 P1 共用公司公共 IP。

输出：Party、Account、DeviceObservation、Transaction、EvidenceRecord、InvestigationHypothesis，账户所有关系与转账事件分开。候选包含 P1/P2/P3 的 T1→T2 时序路径与 token-D 观测；P4 不能仅凭公共 IP 自动进入团伙结论。

验收反例：T2 在 T1 之前时不满足该连续流转顺序；重复导入 T1 不增加独立证据数；撤销交易保留历史且退出当前有效链；过期设备关联不作为当前共享证据。所有人均保持待复核状态，没有自动欺诈结论。
