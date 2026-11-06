# 工作示例：保留两个“使用人”口径

输入：一份合成资产台账将申请人记在requested_by，交接记录将实际保管人记在custodian_id；两者在界面都显示为“使用人”。没有机构规则或标准原文证明这两个角色等价。

来源目录将这份用户材料记作source_id=training-register、kind=project-curated，保留材料版本、字段位置、适用范围与未知许可。不能因为它来自业务系统，就标成official-standard。

输出两个知识项：

| id | 定义与来源定位 | classification | standard_status | standard_gap |
| --- | --- | --- | --- | --- |
| requester-role | 提出申请的人；requested_by | project-curated | nonstandard-modeling | 仅有用户字段含义，无标准支持，不证明实际保管 |
| custodian-role | 交接记录中的保管人；custodian_id | project-curated | nonstandard-modeling | 保管生效与结束时间、申请人兼任条件尚需业务证据 |

两项source_ids均包含training-register；不伪造standard_basis。集合对象本身也注明nonstandard-modeling及“原创术语组织”的缺口。JSON交付另按方法补齐资产元数据与standards_policy。

若后来取得正式标准，只给该标准确实支持的范围添加source_id、locator、relation=supports和scope；仍保留本地字段到标准的映射缺口，classification仍为project-curated。一个标准网站入口不能把两项自动标为standard-backed。

验收：同一人同时承担两角色是可能情况，不能据此合并角色定义；申请人和保管人不同也不构成数据矛盾。来源与条目分类、标准状态、缺口均可由下游独立读取。
