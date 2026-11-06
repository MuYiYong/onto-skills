# 物流概念裁剪方法

项目原创，知识来源与版本见 [来源索引](sources.json)。只读与当前问题有关的[概念记录](domain.json)。

先问业务对象：买卖双方约定交付的一组货物、运输服务承运的一组单元、可独立处理的物理单元分别给稳定身份。订舱、单证和箱体资产不能替代这些身份。用字段映射表记录 source field、namespace、concept、identity evidence、loss/unknown。没有正式分配证据时，不把内部号改写成GS1号。

示例裁剪：只需托盘运输异常时保留Shipment/Consignment/LogisticUnit/Leg/Event即可，商品种类和批次作为未知内容，不无证据展开。需要召回时再加入产品/lot内容与其成员区间。GLN按用途区分物理地点和主体；GTIN不是物流单元标识。

每个事件保留来源键和不可变语义负载。计划与估计不会变成实际；修订需要新的事件身份或明确更正引用。actual按发生时点形成轨迹，ETA按来源发布时间选当前预测，本系统observed_at仅决定当时是否已知。中转arrival不是最终目的地arrival，实际交接还需前后保管方证据。

输出关系至少写端点、含义、基数/条件、键、有效区间、证据与执行位置。bitemporal只有observed_at时并不代表完整系统时间历史。标准对象范围只是对齐背景，关系裁剪、阈值与预测策略都标project-curated或model-inference。

EPCIS适配边界：标准7.4.1.2允许错误声明重发原事件，eventID保持相同，除errorDeclaration/recordTime外事件内容不变。先识别并验证这一合法配对，再应用本地同键异文冲突规则；保留原始记录、声明与独立ID的更正事件。错误声明不等于物理库存冲正。包内自定义投影不冒称实现EPCIS捕获/查询接口。
