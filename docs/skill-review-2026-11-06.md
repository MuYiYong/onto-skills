# 33项Skill发布前审查（2026-11-06）

本轮逐项审阅33项技能的入口、触发范围、工作方法、关键示例及标准/来源边界，并检查12份中心图模型的身份、业务问题和映射损失。结果是有界源码审查，不能证明所有真实业务输入正确、模型触发准确率、完整行业认证或新一轮原生应用兼容。

## 发现与修正

| 问题 | 影响 | 修正 |
| --- | --- | --- |
| R01 知识发现输出缺少标准状态契约 | 下游JSON知识资产可能缺standard_status，来源条目字段不完整 | 补齐standard_status、supports/gap条件、standards_policy及来源kind/uri；用双角色例子明确非标准输出 |
| R02 电力入口的标准范围说明过时 | 将已有CGMES3直接依据统称为背景，与知识条目不一致 | 区分已核实CGMES3类/字段/基数、IEC目录背景和本地规则 |
| R03 制造返工身份说明过度概括 | 可能把示例的新输出键误用成源系统必须重编物理批号 | 明确为本地示例约定；沿用批号的输入须保留原号并扩展版本/状态模型，现有示例先报告不支持 |

这三类修正涉及4项既有技能：industry-knowledge-discovery、electric-power-domain-knowledge、manufacturing-domain-knowledge、manufacturing-quality-traceability。历史源码及原生收据保持不变，不能把它们当作这4项修改后版本的原生通过证据。新增六项同样没有本轮原生或独立模型应用结果。

## 逐项覆盖

| Skill | 本轮审查重点 |
| --- | --- |
| [entity-relationship-modeling](../skills/core/entity-relationship-modeling/SKILL.md) | 命名空间、复合键、多次关系和时点基数 |
| [industry-knowledge-discovery](../skills/core/industry-knowledge-discovery/SKILL.md) | 来源/知识分类、标准状态与JSON输出契约；R01已修正 |
| [ontology-documentation](../skills/core/ontology-documentation/SKILL.md) | 文档对应模型版本、主键、映射和证据层次 |
| [ontology-evolution](../skills/core/ontology-evolution/SKILL.md) | 身份变更、不可逆映射、消费者兼容和回滚 |
| [ontology-modeling](../skills/core/ontology-modeling/SKILL.md) | 继承/组成/角色/事件区别与身份生命周期 |
| [ontology-validation](../skills/core/ontology-validation/SKILL.md) | 开放世界、闭世界约束、草案与验证证据 |
| [property-graph-mapping](../skills/core/property-graph-mapping/SKILL.md) | OWL限制、多domain、qualified cardinality与映射损失 |
| [banking-business-model](../skills/finance/banking-business-model/SKILL.md) | 授信/贷款/放款、计划与执行、多方角色及币种时间 |
| [credit-risk-knowledge](../skills/finance/credit-risk-knowledge/SKILL.md) | 实际负债与申请查询、机构粒度、共享标识边界 |
| [fibo-ontology](../skills/finance/fibo-ontology/SKILL.md) | 固定Loan来源、imports边界、存在/全称/零基数限制 |
| [finance-domain-knowledge](../skills/finance/finance-domain-knowledge/SKILL.md) | 产品定义、合同账户、余额与角色分层 |
| [built-environment-domain-knowledge](../skills/industries/built-environment-domain-knowledge/SKILL.md) | IFC正式版本、主包含/引用、属性覆盖和单位 |
| [cybersecurity-domain-knowledge](../skills/industries/cybersecurity-domain-knowledge/SKILL.md) | SPDX身份、CSAF修订、CVSS与部署修复证据 |
| [education-domain-knowledge](../skills/industries/education-domain-knowledge/SKILL.md) | OB/VC版次、发行者/创建者/接收者及有效期 |
| [electric-power-domain-knowledge](../skills/industries/electric-power-domain-knowledge/SKILL.md) | CGMES直接依据与IEC背景、未知状态和实际停电证据；R02已修正 |
| [environmental-monitoring-domain-knowledge](../skills/industries/environmental-monitoring-domain-knowledge/SKILL.md) | 服务范围身份、被测对象、时间质量与本地阈值 |
| [healthcare-domain-knowledge](../skills/industries/healthcare-domain-knowledge/SKILL.md) | FHIR R4版本、患者交叉映射、状态、修饰字段和量值 |
| [logistics-domain-knowledge](../skills/industries/logistics-domain-knowledge/SKILL.md) | Shipment/Consignment/物流单元、单证与实物、GS1身份范围 |
| [manufacturing-domain-knowledge](../skills/industries/manufacturing-domain-knowledge/SKILL.md) | 物料血缘、共享设备、数量基础与源批号保留；R03已修正 |
| [retail-domain-knowledge](../skills/industries/retail-domain-knowledge/SKILL.md) | 库存粒度、实际运动、商业单据与在途/状态/单位 |
| [bim-change-impact](../skills/scenarios/bim-change-impact/SKILL.md) | 快照/类型/实例、空值覆盖、单位和前后空间候选 |
| [financial-regulatory-reporting](../skills/scenarios/financial-regulatory-reporting/SKILL.md) | 指标上下文、源版本、币种/nil、传输与业务回执 |
| [fraud-network-modeling](../skills/scenarios/fraud-network-modeling/SKILL.md) | 有向时序资金链、证据独立性与公共节点反证 |
| [healthcare-care-pathway-modeling](../skills/scenarios/healthcare-care-pathway-modeling/SKILL.md) | 不透明版本、显式引用、修饰字段、量值和授权限制 |
| [learning-credential-verification](../skills/scenarios/learning-credential-verification/SKILL.md) | 报告内容绑定、状态与时效、接收者和模拟验证边界 |
| [manufacturing-quality-traceability](../skills/scenarios/manufacturing-quality-traceability/SKILL.md) | 拆分合并返工、数量与终端暴露、保留源标识；R03已修正 |
| [multi-lending-detection](../skills/scenarios/multi-lending-detection/SKILL.md) | 同刻重叠与窗口出现、机构去重和共享标识反证 |
| [observation-quality-assessment](../skills/scenarios/observation-quality-assessment/SKILL.md) | 观测/元数据已知时点、质量、有限数值、单位和FOI |
| [power-outage-impact-analysis](../skills/scenarios/power-outage-impact-analysis/SKILL.md) | 确定/可能可达、边界电源、客户去重与实际恢复区间 |
| [related-party-transaction-modeling](../skills/scenarios/related-party-transaction-modeling/SKILL.md) | 持股/控制、制度时点、多路径去重、更正与补偿 |
| [retail-inventory-replenishment](../skills/scenarios/retail-inventory-replenishment/SKILL.md) | 快照锚点、原子posting/冲正、预留与本地补货规则 |
| [shipment-exception-analysis](../skills/scenarios/shipment-exception-analysis/SKILL.md) | ETA发布与事件时间、部分交付、重放和EPCIS错误声明 |
| [software-vulnerability-impact](../skills/scenarios/software-vulnerability-impact/SKILL.md) | 版本/修订绑定、冲突载荷、影响候选与补丁反证 |

## 验证与限制

发布前执行资产校验、全量单元测试以及33项独立Skill格式检查；发布包还需从精确提交构建并解压校验每个包的资源闭包。标准条目沿用固定版本及其已有逐项核验记录，本轮没有重新获取全部标准全文。

两路独立审查代理均因HTTP429终止，未产生报告，因此这里的内容审阅由主代理完成，不称为独立审查通过。合成案例参考计算、静态来源/模型检查与历史原生证据分别记录；不能由格式通过推出专业正确性或当前生产行为。完整标准、OWL推理、真实密码学、macOS原生、远程升级和生产执行按已有说明保持未验证。
