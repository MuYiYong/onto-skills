# 建筑、环境监测与教育行业扩展

本轮从七个行业27项技能扩展到十个行业33项：新增三项行业知识和三项业务场景，每项独立分发；每个行业另有来源、概念、Pack、完整图模型及正反例。保留之前金融、电力、制造、物流、医疗、零售、网络安全的源资产和原生证据。

| 行业与场景 | 正式标准基线及定位 | 本地规则与未覆盖范围 |
| --- | --- | --- |
| 建筑：BIM属性变化与空间候选 | buildingSMART IFC4.3.2.0 / IFC4X3_ADD2，IfcRoot、IfcRelDefinesByType、IfcRelContainedInSpatialStructure、IfcRelReferencedInSpatialStructure、IfcPropertySingleValue | 修订谱系、完整性、自定义Project_Clearance属性及影响政策为原创；无几何、结构安全、EXPRESS全量校验。 |
| 环境监测：观测质量与阈值候选 | OGC SensorThings API Part1 Sensing1.1 /18-088，§8.1、8.2.4、8.2.7、8.2.8与9.1 | OGC只规定数据语义；例子阈值3mg/L、质量准入和瞬时时窗均为合成政策，不是环境法规。 |
| 教育：学习凭证证据核对 | 1EdTech Open Badges3.0文档1.4.5（2026-06-29），§2.4.1、8–10、B.1.1–3/6/9/14/16；W3C VC2.0 Recommendation2025-05-15 §4.9/4.10 | 固定VC2/context3.0.3路径；报告均为模拟，不提供真实验签或学历/能力认可；新鲜度和半开有效区间为本地政策。 |

## 来源核查与版次

IFC官方站点直接访问返回403，实际读取发布机构[Standards-builds的RELEASE快照](https://github.com/buildingSMART/Standards-builds/tree/aac6189946c9f3116198b03ee482152dd3981c76/IFC/RELEASE/IFC4_3/HTML)。该快照明确为4.3.2.0正式版；排除了DEV中的工作草案。官方发布索引：[IFC4_3](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/)。最终IFC许可为CC BY-ND4.0；本库仅提供来源和自主摘要，不分发规范正文/修改版。

实际读取[OGC18-088](https://docs.ogc.org/is/18-088/18-088.html)、[Open Badges3.0](https://www.imsglobal.org/spec/ob/v3p0/)和[VC2.0固定Recommendation](https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/)。Open Badges的v3p0链接包含后续文档修订，故记录文档版次和获取内容SHA256。其9.1兼容注记对旧字段的VC版本标签存在歧义；本轮使用B.1.2与VC2.0正式§4.9字段，不把该注记当转换依据。获取日期不代替规范版次。

新增21条实质概念：18条具有具体范围的标准支持，3条本地政策明确非标准；加上3个集合组织对象，共24个知识对象。全部原创解释仍为project-curated，不标成官方定义。逐项来源与获取摘要见[增量审阅账本](../tests/standards/knowledge-review/expansion-ledger.json)，此前149对象账本保持原样。

## 交付与验证范围

- [建筑](../examples/built-environment/README.md)：12个手工预期案例，实例覆盖、单位、空间、版本、缺失与冲突。
- [环境监测](../examples/environmental-monitoring/README.md)：14个案例，结果/质量/单位、FOI、乱序时点、区间和重复冲突。
- [教育](../examples/education/README.md)：15个案例，报告内容绑定、proof/状态分离、身份、时效和模拟边界。

开发测试复算41个合成投影和附加反例，静态检查独立包闭包、来源、模型结构、快照同步及问题追踪。它们不执行完整标准解析或原生数据库运行。输入字段到标准的映射和损失随场景包分发；模型中未决项阻止声称部署就绪。原27项的Codex/CC-Switch原生记录仍绑定冻结源码，不延伸到新增六项。

[Semantica审阅](semantica-review.md)记录固定源码、实际观察及采用点。新场景显式区分源记录、派生/更正、匹配候选与质量问题，问题覆盖由手工预期支持；未引入外部运行时或执行产品。
