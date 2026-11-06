# 来源、身份和质量复核

这是原创审阅约定，可在离线材料上填写。设计参考[Semantica的ProvenanceEntry](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/provenance/schemas.py)、[质量报告](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/ontology/quality_gate.py)与[问题追踪](https://github.com/semantica-agi/semantica/blob/c0ec77be3d163d2bcccfc50781bb04372180aadd/semantica/ontology/competency_questions.py)，该版本MIT。本包未复制代码、未依赖运行时，也不把源码设计当作行业标准。

| 记录 | 必填内容 | 复核问题 |
| --- | --- | --- |
| 标准依据 | 发布者、版次、条目、支持范围、未支持部分 | 该条文真的支持当前语义还是只有背景相关？ |
| 源断言 | source_record、source_locator、原始身份/值、载荷散列、源时间、接收时间 | 可否定位到原始内容？散列只验证完整性，不证明真实或可信。 |
| 派生断言 | used_records、转换方法/版本、参数、输出及不确定性 | 与源断言是否分开？previous_version和derived_from不可混为一条关系。 |
| 身份候选 | 两侧源身份、匹配/反证、范围、审阅结论、审阅依据 | 名称相似只能提候选；冲突和撤回保留，不抹掉原断言。 |
| 能力问题 | 问题、模型元素、输入、手工期望、正反例case_id | 有字段不等于能回答；必须用结果和反例证明有界能力。 |
| 质量问题 | code、severity、element、source_locator、reason、补证动作 | 阻断错误与已知缺口分别呈现，不用总分抹掉关键失败。 |

本包质量口径：身份/载荷冲突或缺少必需证据阻断相关结论；不支持的标准结构列unknown及补证路径；非关键展示缺失可为warning。任何confidence均不能覆盖硬性条件。不要把“未发现反例”写成“标准符合”。需要修正时保留旧断言、修正来源和理由，缺少正式替代证据不自行选最新。
