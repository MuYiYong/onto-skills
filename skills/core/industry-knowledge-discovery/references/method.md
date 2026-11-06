建议记录结构：id、name、definition、aliases、classification、source_ids、source_locator、scope、confidence、open_questions。

证据分为 official-standard（正式标准及其版本）、industry-common（有来源的行业通用解释）、project-curated（项目自主整理）、model-inference（AI/建模推断）。发布机构网站的一般介绍不自动是规范性标准；来源元数据与知识项分类可以不同。

来源索引必须包含 name、id、URI、version、publisher、license、retrieved_at、scope、authority。缺少许可写 unknown 并只存索引与原创摘要，不据此复制原文。记录原文位置不意味着可以重新分发全部原文。

冲突示例：同一个“客户”在签约系统指合同当事人，在营销系统指潜客；先保留两个有范围的定义，不能因为字段同名直接合并。

本说明为项目自主知识工程方法。

标准优先交付顺序：适用范围/版次 → 发布机构与具体定位 → 原定义范围 → 原创解释 → 图设计 → 缺口及补证。standard_basis的supports只表示该具体范围有正式标准支持；background用于摘要或通用背景。standard_gap说明未核实、无通用标准规则或需用户决策的部分。每条来源都应服务于具体知识，避免仅列网站入口作为依据。
