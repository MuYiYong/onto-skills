# 工作示例：可用11EA，建议复核补货19EA

[输入](input.json)给出SKU-OAT-1/STORE-A/LOT-20261101，所有内部身份为合成数据，单位EA。8Z快照sellable20、damaged2；9Zsale-1减7，重放不再扣；10Zreceipt-1加5；10:30damage-1以同一原子事件将sellable3转damaged3；9:30实际发生的受损退货2到11:30Z才看到。

截至12Z且证据截点12Z：sellable_on_hand=20-7+5-3=15，damaged_on_hand=2+3+2=7。预留reserve-1当前有效4，用户明确sellable_on_hand_minus_active_reserved政策，所以available=11EA。在途12另列，订单5和销售62.30CNY不进入库存算式。

用户阈值available<12，目标30，输出status=signal、suggested_quantity=19EA、order_created=false。结论引用快照、4个有效运动身份、原子损坏转移和预留版本，不宣称已下单或已做库存审计。

[模型](graph-model.json)将商业行(kind区分订单/销售/退货)、快照、原子事件、预留版本和信号分别建模，Posting边记录粒度与数量。缺单位转换时不能把CASE混入EA；任一posting无效时整笔damage零生效。

[验收](acceptance.json)还覆盖多快照锚、不同真实销售、完整/重复冲正、单位混合整笔拒绝、晚到受损退货、当时未知证据、快照前退回对账、已履行预留、缺政策、超额预留负可用、其他批次和阈值相等。仅为有界离线语义证据，不是原生数据库或标准认证。
