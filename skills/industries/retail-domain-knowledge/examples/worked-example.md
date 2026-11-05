# 工作示例：受损退货不等于可销售库存

输入：商家MERCHANT-A在STORE-A有SKU-OAT-1/LOT-20261101，单位EA。8Z盘点sellable20、damaged2；9Z售出7，10Z实际收货5，10:30有同一原子damage事件将sellable3转damaged3；9:30发生的受损退货2到11:30才看到。有效预留4，在途12。销售行金额62.30CNY另列。

截至12Z且证据截点12Z：sellable=20-7+5-3=15；damaged=2+3+2=7；用户明确available=sellable-active_reserved，因此available=11EA。在途12、订单5和62.30CNY都不加减这个库存算式。

用户政策为available<12时补至30：建议19EA，order_created=false。该建议是可解释的复核信号，未创建采购单。

反例：将受损退货加到sellable会得出13并漏报；将同一sale事件重放再扣7会误报更大缺口；把在途加到on-hand会掩盖当前缺货；将商业销售行与库存movement各扣一次同样错误。证据截点若为10Z，则晚到退货尚未进入当时已知damaged余额。
