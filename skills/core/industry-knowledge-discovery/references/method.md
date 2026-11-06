建议记录结构：id、name、definition、aliases、classification、source_ids、source_locator、scope、standard_status、standard_basis/standard_gap、open_questions。confidence可选，不能替代来源或标准状态。

证据分为 official-standard（正式标准及其版本）、industry-common（有来源的行业通用解释）、project-curated（项目自主整理）、model-inference（AI/建模推断）。发布机构网站的一般介绍不自动是规范性标准；来源元数据与知识项分类可以不同。

来源索引的sources条目必须包含name、id、uri、version、publisher、license、retrieved_at、scope、authority、kind；uri使用小写字段名。kind区分official-standard、industry-common、project-curated、model-inference。缺少许可写unknown并只存索引与原创摘要，不据此复制原文。记录原文位置不意味着可以重新分发全部原文。

冲突示例：同一个“客户”在签约系统指合同当事人，在营销系统指潜客；先保留两个有范围的定义，不能因为字段同名直接合并。

本说明为项目自主知识工程方法。

标准优先交付顺序：适用范围/版次 → 发布机构与具体定位 → 原定义范围 → 原创解释 → 图设计 → 缺口及补证。standard_basis的supports只表示该具体范围有正式标准支持；background用于摘要或通用背景。standard_gap说明未核实、无通用标准规则或需用户决策的部分。每条来源都应服务于具体知识，避免仅列网站入口作为依据。

JSON知识资产另带id、name、version、license、updated_at、scope、authority、classification、source_ids及standards_policy="standards-first-v1"。所有有id的知识对象，包括集合和导航对象，都应有standard_status及相应依据/缺口。standard-backed只支持standard_basis列明的范围；nonstandard-modeling必须说明缺口。标准支持与本地缺口可并存；来源目录自身不要求这套知识条目状态。源版本未知应原样写未知，检索日期不能填作源版本。
