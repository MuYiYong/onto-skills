# BIM属性变更与空间影响候选：投影与验收

标准基线：IFC 4.3.2.0（IFC4X3_ADD2）。三个文件分别是[合成输入](input.json)、[数据库中立图规格](graph-model.json)、[手工预期](acceptance.json)。共有12个手工期望案例，开发侧参考计算消费投影字段；没有原生IFC/完整SensorThings/签名凭证校验。

图规格为设计草案，未选数据库版本，有明确unresolved。JSON结构通过不代表部署就绪。图模型是可复用设计；input.json只覆盖下面明确列出的案例投影，未构造所有SourceRecord、属性断言与边实例，不声称做过完整入库往返。

## 原始字段到本地投影

| 本地字段 | 标准字段或来源 | 取舍与损失 |
| --- | --- | --- |
| objects[].global_id / types[].global_id | IfcRoot.GlobalId | 模型谱系和快照由本地补充；示例省略完整STEP序列化。 |
| objects[].type_id | IfcRelDefinesByType.RelatedObjects / RelatingType | 以有向关系投影；完整关系实体和逆属性由源定位保留。 |
| primary_spaces / referenced_spaces | IfcRelContainedInSpatialStructure / IfcRelReferencedInSpatialStructure | 示例空间只用ID；正式模型需ObjectSnapshot端点，不能丢失两种语义。 |
| properties[].value / measure_type / unit | IfcPropertySingleValue.NominalValue / Unit | 例子用十进制字符串；省略单值之外的属性类型，未运行IFC解析。 |
| project_length_unit | IfcProject.UnitsInContext解析结果 | 已经过量纲解析的长度单位投影；不是完整IfcUnitAssignment。 |
| lineage / revision / delivery_id / complete_scope | 本地交付契约 | 不把OwnerHistory当全量历史。所选自定义属性Project_Clearance.RequiredGap不是标准Pset。 |

## 能力问题与反例

| 问题 | 关键模型元素 | case_id |
| --- | --- | --- |
| 哪个实例的所选属性发生可比变化，类型变更被哪些实例覆盖？ | PropertyAssertion / HAS_TYPE / ChangeAssessment | type-change, null-value, equivalent-unit, unknown-unit, project-unit, missing-type |
| 变化涉及哪些主包含或引用空间，证据来自哪个修订？ | CONTAINED_IN / REFERENCED_IN / CANDIDATE_SPACE | multiple-containment, missing-space |
| 哪些对象因身份、单位或缺失数据不能比较？ | ModelRevision / ObjectSnapshot / SourceRecord | different-lineage, partial-delivery, duplicate-receipt, conflicting-object |

结果必须带可定位的源版本、标准支持范围、本地政策和不足。名称相似度或一个质量总分不能绕过必需证据。对未支持的原生字段或不完整输入给出补证要求，不静默丢弃。
