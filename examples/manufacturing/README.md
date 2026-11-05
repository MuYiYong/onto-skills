# 合并、拆分、返工和召回候选

输入：[input.json](input.json)；模型：[graph-model.json](graph-model.json)；机器用例：[acceptance.json](acceptance.json)。全部是原创合成数据，不是 EPCIS 消息、ISA-95 实现或质量批准记录。

E1 合并 RAW-100的100kg 与 ADD-10的10kg，产出 MIX-110的110kg。E2 拆成 FG-60的60kg 与 RW-50的50kg；E3 返工 RW-50，产出 FG-48的48kg 和 SCRAP-2的2kg。质量守恒基础在此明确为 mass。E4 用同一 MIXER-1 处理独立 RAW-U30 → FG-U30的30kg。

种子 RAW-100 沿材料路径到 FG-60、RW-50、FG-48和SCRAP-2。仅选择终端 released/shipped：FG-60 + FG-48 =108kg。MIX-110/RW-50是中间批次，不再相加；SCRAP-2非候选状态；FG-U30只是共用设备，不能加入血缘。

本地虚构规格 LOCAL-CONTAMINANT/v1 用0.10mg/kg上限演示：I1=0.20是fail，I2=0.05是pass。两个批次仍有相同上游血缘，I2 pass 不自动撤销召回候选。限值和采样策略均不是 EPCIS/ISA-95 规定。

E1 虽在11月1日08:00发生，却在11月2日09:00才接收。11月1日23:00的已知视图不能沿 E1 追溯 RAW-100，此时空候选只表示尚未找到路径。缺 FG-48 数量时仍输出候选，但合计 unknown；混合 lb/kg 且无批准换算、111kg拆分产出、报废重复列入损耗或冲突事件键均拒绝。相同批次标签在 P2 不与 P1 合并。

输出保留完整来源事件、角色和数量证据。受控离线测试不能证明真实工厂行为、标准消息符合性、数据库约束或召回法律适用。

输入覆盖/patch约定见场景包内的 fixture-contract.md；机器用例可离线复核，不需要外部服务。
