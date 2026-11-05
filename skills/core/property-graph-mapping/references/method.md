# OWL → 属性图决策

这是本项目自主映射解释；OWL 语义参照 [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)（2012-12-11），不构成数据库语法或自动推理器。

| 源项 | 候选表达 | 需保留的区别 |
| --- | --- | --- |
| Class | 节点类型/标签/分类属性 | 类和实例不同；抽象类无需实例节点 |
| Object Property | 有方向边/关联实体 | 多方角色、关系身份、逆属性不可静默丢失 |
| Datatype Property | 逻辑类型属性 | datatype、语言标记、单位、多值和空值需说明 |
| Domain / Range | 端点类型与来源注释 | OWL 用于类型推断；不是封闭世界校验。多个 domain 通常形成交集语义，不是任选一个 |
| SubClassOf | 展平父类字段、标签或显式类型关系 | 展平保留含义但不自动执行继承推理；区分 is-a 和 part-of |
| someValuesFrom | 应用检查/推理备注 | 存在量词不授权虚构一个缺失节点；开放世界下缺记录不等于矛盾 |
| allValuesFrom | 范围限制备注/封闭世界检查 | 全称限制不蕴含至少有一个值 |
| min/max/exact cardinality | 按类作用域的规则 | 区分 qualified cardinality 与所有值基数；缺失值不等同本体不一致 |
| Functional / inverse functional | 合并/唯一性候选与规则 | 可能推断 sameAs；不同 IRI 不自动不同实体；不能机械当唯一索引 |
| union / intersection / disjoint | 类型规则/显式损失 | 无等价表达时写 unmapped，并列影响的业务问题 |
| property chain / transitive | 派生关系规则 | 物化边需标来源、时效与刷新；不假称数据库原生蕴含 |

多值属性可用有序集合、边或值节点；OWL 集合通常无顺序，数据字段若有顺序要保留。事件节点要求独立身份、参与方及生命周期，不能只凭时间字段判断。

业务闭世界校验与 OWL 开放世界推理是两个不同证据层次。建议 constraint.enforcement 使用 application/review，只有目标环境证据充分才使用 database。

