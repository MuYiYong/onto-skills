# 工作示例：一笔交付，两段运输

输入：买方要求两托盘LU-1/LU-2共同交付，货主单号SH-100；货代先以C-FEEDER-10运至新加坡，换承运方以C-SEA-20继续；BK-20已确认、DOC-20已签发。只有LU-1在SG-PORT的卸货和装载扫描。所有号均为合成内部身份，未提供GS1获配证据。

交付：Shipment=(SHIPPER-A,SH-100)；LogisticUnit=(SHIPPER-A,LU-1/LU-2)；两个Consignment保留不同provider范围；Leg分别记录CN→SG与SG→NL；Booking与TransportDocument独立关联C-SEA-20。单元的Consignment成员关系使用有效区间，不能修改原Shipment身份。

证据判断：单证签发和订舱确认支持运输安排；SG扫描支持中转处理；仍缺LU-2轨迹、最终目的地实际到达和交接责任凭证。因此输出delivery=unconfirmed，handover=unconfirmed，而不是推断丢失或已交付。

反例：将SH-100、C-SEA-20和LU-1合成一个“运单节点”会失去两托盘交付完整性和换段责任；将计划NL到达写成actual会无证据关闭异常。需要哪一项推断都必须另交证据和适用政策。
