# Semantica调研与本库采用点

核查日期2026-11-06；[semantica-agi/semantica](https://github.com/semantica-agi/semantica)默认分支main，实际读取修订[`c0ec77be3d163d2bcccfc50781bb04372180aadd`](https://github.com/semantica-agi/semantica/tree/c0ec77be3d163d2bcccfc50781bb04372180aadd)，该修订[LICENSE](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/LICENSE)为MIT。以下为源码审阅，未安装运行、未测试性能或宣称集成兼容。

| 实际读取的源码 | 观察 | 本库采用及调整 |
| --- | --- | --- |
| [provenance/schemas.py](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/provenance/schemas.py) | ProvenanceEntry包含source_document/location、checksum、时间和agent；previous_version_id与derived_from_id分列，并有失效字段 | 六个新包附原创evidence-review.md；三个图模型显式SourceRecord、定位/散列、supersedes与derived_from，避免把更正和推导混成一条血缘；不实现其存储/哈希链。 |
| [kg/entity_resolver.py](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/kg/entity_resolver.py) | resolve_entities先检测候选组，再交给entity_merger合并，配置包含匹配策略/阈值 | 借鉴候选发现与处置分步。本库要求范围和证据成立才确认身份，不采用自动模糊合并；跨模型/服务/发行者及同ID冲突都有反例。 |
| [ontology/quality_gate.py](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/ontology/quality_gate.py) | QualityIssue有code/severity/element/details，报告把阈值失败和问题列表分开 | 新包交付可定位质量问题，关键证据失败阻断结论；不让平均分或confidence覆盖身份、时间、单位、内容绑定条件。 |
| [ontology/competency_questions.py](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/ontology/competency_questions.py) | CompetencyQuestion记录trace_to_elements；所读trace_to_elements实现采用问题词与类/属性名匹配 | 采用问题→模型→验收案例的显式追踪。三个cq-trace.json绑定手工预期和反例；不把词匹配覆盖率当作语义正确率。 |

落地位置：[建筑示例](../examples/built-environment/scenario-guide.md)、[环境监测示例](../examples/environmental-monitoring/scenario-guide.md)、[教育示例](../examples/education/scenario-guide.md)。每个场景对应完整图模型、正反例、包内证据复核表；六项新技能离线使用不依赖Semantica或其他技能。

Semantica是工程参考，不是IFC、OGC或教育标准的发布者。本轮行业定义仍引用正式标准。仅借鉴上述设计并原创编写指导，未复制源代码、运行时、CLI、服务或UI。其源码中的PROV-O兼容描述属于上游声明；本库未做完整PROV-O语义验证，因此不复述为本库认证结论。
