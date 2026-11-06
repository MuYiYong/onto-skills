# 标准优先的知识与场景

先核实适用地区/时期、发布机构、正式版次和具体条目，再形成业务解释与数据库中立模型。选择公开可读且可定位的标准；不能访问的正文、未核实的映射和本地业务政策保留缺口。此流程适用于金融、电力、制造、物流、医疗、零售及网络安全，Core仅保留通用方法。

## 知识如何记录依据

每个非来源目录JSON资产声明`standards_policy: standards-first-v1`。每个知识项声明`standard_status`并提供`standard_basis`或`standard_gap`，包括集合与模块导航。basis保存source_id、locator、relation、scope；来源版本、发布机构、许可和检索日期在对应sources.json中。`supports`是正式标准对具体范围的支持，`background`是摘要或行业介绍，不能由此推出未经访问的正文内容。

来源分类与知识分类分别维护。下列情况保持project-curated或model-inference：标准转述、业务裁剪、图键和关系方向选择、历史获知截点、风险/延误阈值、库存公式、质量界限和合成例子。没有通用标准规则时，gap说明依据为何不足、哪些材料可补证；已有标准背景也不能遮盖本地政策缺口。

校验器拒绝缺少政策或条目覆盖、未知/未附着来源、空定位/范围，以及把项目来源当正式标准支持的情况。它验证记录结构，不判断一个引用是否在语义上足以支持结论；仍需按条目阅读标准并用业务反例复核。

## 各行业的核查与补强

| 范围 | 具体依据和补强 | 仍需业务材料或专项验证 |
| --- | --- | --- |
| 金融 | 固定FIBO修订的Class/Property与各自versionIRI；区分贷款、授信、合同角色、还款计划和实际支付；保留精确映射缺口 | 不根据中文术语猜造IRI，不把图基数当OWL公理；集团/风险口径按地区制度确定 |
| 监管报送 | 监管统计办法条文、BCBS239治理/质量原则、XBRL2.1事实上下文和单位；2026通讯仅作信息背景 | 实际报表制度、指标、公式、时限和回执协议由正式材料确定 |
| 关联交易 | 2025修正后的监管规则与CAS36会计范围分开；关联交易披露金额、未结算项目与条款保留独立信息 | 多路径不能重复计量；本地交易键、控制路径及最终判断需复核，不自动审批 |
| 电力 | 已取得CGMES3正式RDFS/SHACL，核对Terminal关系、Switch状态及Header时钟；CIM/Profile/快照身份分别记录 | IEC付费全文仍未取得；客户/停电策略为非标准建模，不从公开Profile推导电气可行性或调度权限 |
| 制造 | OPC10030的物料定义/批次、设备角色、检验规范/结果；EPCIS转化事件和错误声明 | 共享设备不产生物料谱系；数量守恒基础、检验限值和召回决定由本地规则确定 |
| 物流 | GS1商品/物流单元/Shipment/Consignment身份；EPCIS读点与业务地点、时间/交接；DCSA2024.4含ACT/PLN/EST/REQ | 场景三类事件投影不是完整DCSA枚举；REQ不证明实际发生。ETA阈值、完送定义为本地政策 |
| 医疗 | FHIR R4 4.0.1资源身份/版本、Identifier与Quantity字段；请求与执行、状态错误及缺失语义 | `<5`之类带comparator的量不当精确5；代码/单位转换及患者跨源匹配需证据，不提供诊疗 |
| 零售 | GS1标识层级、可见性事件、追溯关键数据；CBV标识预留与库存预留分开 | 库存快照边界、原子运动/冲正、可销售退货和补货公式不由这些标准直接规定 |
| 网络安全 | SPDX2.3文档内组件身份、CSAF2.0通告修订/产品状态、CVSS4.0严重度分层；有界漏洞影响示例 | 映射、发布者信任、版本范围、部署/实际修复证据分别确认；不以缺通告判安全 |

README的[标准矩阵](../README.md#标准依据)链接各范围来源目录。2026-11-06核查发现并修正的访问与版本问题包括：旧BIS CRE36链接跳到通用目录、NFRA网页只返回脚本壳、CAS36原页此前超时但本次可读，以及GS1浮动链接不能固定选定版次。NFRA正文可由同机构公开JSON读取：[统计办法](https://www.nfra.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId=1089714.json)、[2025修正及重刊](https://www.nfra.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId=1209888.json)。法规适用性仍按真实任务复核，页面可访问不等于所有业务结论已经证实。

可复查的具体定位包括[OPC物料检验结果8.4.2.1](https://reference.opcfoundation.org/specs/OPC-10030/8.4.2.1)、[FHIR Quantity](https://hl7.org/fhir/R4/datatypes.html#Quantity)、[DCSA事件分类](https://models.dcsa.org/2024Q4/EARoot/EA5/EA2/EA6/EA7/EA1/EA1/EA2575.htm)。EPCIS的recordTime是仓库捕获时间，不能替代本地首次获知时间；各时钟应分栏保留。

## 软件物料清单与漏洞场景

[网络安全知识](../knowledge/cybersecurity/README.md)和[场景示例](../examples/cybersecurity/README.md)提供两个独立Skill、一份文档Pack、完整图规格及15个合成正反例。组件键保留文档命名空间，通告产品ID保留发布者与文档范围；依赖、部署、适用性、严重度和实际修复分开举证。

[SPDX2.3](https://github.com/spdx/spdx-spec/tree/v2.3)采用固定tag；其浮动文档页重定向到2.3.1，不把重定向后的内容称为原2.3原文。[CSAF2.0](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html)选2022-11-18 OASIS Standard，定位产品ID、tracking、product_status及VEX证据；[CVSS4.0](https://www.first.org/cvss/v4.0/specification-document)仅作独立严重度来源，不塞进CSAF2.0的v2/v3分数字段。

输入是原创的有界源投影，不是原始SPDX或CSAF序列化。人工精确版本映射、正整数修订和final-only策略属于示例政策。更完整的产品树/组、版本范围、语义修订、数字签名、许可证和Profile校验均不能由此推定完成。模型含部署前待决问题，target未定；不能把结构验证通过称为部署就绪。

## 分发与证据边界

中心知识和包内副本通过显式snapshot映射同步；每个Skill独立复制后仍含知识、来源、例子与许可，不依赖其他技能或仓库目录。仅保存原创解释与索引，不重新授权第三方标准全文。

[测试说明](../tests/README.md)列出资产/来源/模型/副本和合成参考计算。历史Codex/CC-Switch记录保留原字节，并对照[冻结的25项源码](../tests/compatibility/source-baselines/README.md)核验，避免把修改后的知识误称为通过了历史原生测试。最终27项源码的[日期化原生记录](../tests/compatibility/standards-first-native/README.md)另行保存：两种布局发现、全量GUI安装/同步/卸载以及21项当前代理有界任务；CLI推理429失败保留，不写成通过。独立闭包与离线案例不证明完整标准符合性、macOS原生或数据库执行。完整知识依据、真实标准格式样例校验及非标准范围见[核验报告](standards-verification.md)。

标准状态按条目区分：standard-backed仅限已核实条文和scope；nonstandard-modeling明确标注非标准建模及原因。CGMES3公开配置已经取得，不能再把其具体类/字段说成只查过目录；但未取得的IEC完整条款和本地规则也不能借此升级为标准定义。标准原生合成文档的实际工具校验见[记录](../tests/standards/cybersecurity/README.md)。
