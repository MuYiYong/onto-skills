# 标准优先与证据方法

先读 sources.json 固定 SPDX2.3、CSAF2.0、CVSS4.0 的适用范围，再读 domain.json 的条目定位和本地缺口。原始标准定位、项目解释、图设计和业务结论分别交付；基础工作可离线使用包内知识。

| 问题 | 建模与复核 |
| --- | --- |
| 两个 SPDXRef 同名 | 用 document_namespace + spdx_id；更新SPDX文档版本使用新namespace，不得跨文档直接合并 |
| 通告 product_id 同名 | 以publisher.namespace作为发布者键，按 publisher + tracking_id + revision + product_id；保留精确版本与修订绑定的映射证据 |
| 最新通告与历史判断 | 先过滤 released_at ≤ as_of 与 observed_at ≤ known_as_of，再按声明的修订规则选择；同修订异文按payload_hash保留独立原始记录，并按发布者/通告/修订分组报告冲突 |
| 状态与理由 | 保留 known_affected / known_not_affected / fixed / under_investigation；未评估保留 unknown，否定状态保留 impact_statement，affected 保留 action_statement |
| 依赖、严重度和补丁 | 依赖是声明关系；CVSS 为严重度输入；修复产品版本与资产已安装修复分别举证 |

CSAF 还有 first_affected、first_fixed、last_affected、recommended 等字段；不能静默压成四类。SPDX 文件/许可证/校验和、完整 CSAF 产品树/组/范围及信任验证在示例中未全部展开。图规格记录损失和待决项，不能声称通过完整标准校验。

合成投影的 final-only、正整数修订、精确版本、知识截点与冲突处理均为项目政策。真实任务先确定发布者信任、原始语义版本排序、适用产品范围和证据有效性；不要把示例政策说成规范全文。保留CSAF/VEX来源理由，不能以缺记录推导安全，也不能因新补丁关闭全部发现。CVSS4.0独立来源不得伪装为CSAF2.0内建CVSS4字段。

输出：范围/两类截点；组件、部署、通告修订、漏洞与状态断言；映射证据/冲突；标准定位和缺口；正常反例；待决项。只在显式部署证据与匹配状态同时成立时列受影响资产候选；无数据支持的被利用与已修复结论保持未知。
