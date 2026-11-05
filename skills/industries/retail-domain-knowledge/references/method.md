# 零售概念裁剪方法

这是项目原创业务方法；标准只提供标识、可见性与追溯背景，确切范围见[来源](sources.json)和[概念](domain.json)。

先固定stock grain=(merchant,sku,location,lot_issuer,lot,condition,unit)。SKU是内部管理身份，GTIN可选且有包装级别；lot不能脱离SKU/分配方使用。GLN用途和地点层级须核实。缺lot可单独保留unknown范围，不并入已知lot。

将输入分成不同业务含义：StockSnapshot是截面测量，StockMovement是有符号运动，Reservation是有效版本状态，CommerceLine.kind保留订单/销售/退货差别，在途是待收货证据。仅StockMovement实际posting改变实存。快照不是进货，订单不是扣库，商业销售行和对应运动不能扣两次。

运动键为source_system+event_id，postings共用原子边界。任一posting有单位、引用或数量缺陷，整事件不纳入；完整冲正逐条反向引用原事件，不覆盖历史。受损退回只增加damaged；合格状态转移需要可追溯的平衡postings。

输出先报告实存与预留，再依据明确available政策计算；不把在途或未知转换加入。数量保留十进制和单位，金额单列currency与期间。没有阈值就交付待确认参数，不臆造采购量。CBV中的reserving/reserved是标识分配语境，不能冒称零售库存预留的标准定义。
