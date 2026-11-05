模块层次为 FIBO → Domain → Module → Ontology → Class/Property。FND 提供基础，BE/FBC 提供主体与金融商务，LOAN/SEC/DER 等承载专项语义，IND/MD 关注指标和市场数据；索引不是成熟度或完整性声明。

Class 是概念集合；Object Property 关联个体，Datatype Property 指向数据值。Domain/Range 可推断类型，多 domain 通常是交集；不能当作关系允许类型的并集。SubClass 表达实例包含，既非 part-of，也非“该类使用另一类”。

OWL someValuesFrom 表达存在限制，allValuesFrom 不蕴含存在；qualified cardinality 仅计算指定类的值。开放世界与无唯一名称假设意味着缺少记录不一定违反本体，同名/不同 IRI 也不自动证明相同/不同主体。Functional 属性可能引出个体相等，而不是直接数据库唯一冲突。

映射策略：Class 选择节点/分类/标签；Object Property 选择带方向边/关联实体；Datatype Property 选择逻辑属性。继承展开保留来源映射；Restriction 写应用检查/推理备注；无法表达的公理写 unmapped。不假称关系数据库/属性图原生执行 OWL 推理。

裁剪闭包要列选中 IRI、必要父类/限制/属性/进口依赖；未知 imports 不用相似概念补造。已确认抽取的标准只是局部样例，完整业务建模仍须对实际输入版本复核。

参考官方 FIBO 与 W3C 的来源见 sources.json；本文为原创方法。
