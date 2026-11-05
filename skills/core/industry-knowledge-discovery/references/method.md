建议记录结构：id、name、definition、aliases、classification、source_ids、source_locator、scope、confidence、open_questions。

证据分为 official-standard（正式标准及其版本）、industry-common（有来源的行业通用解释）、project-curated（项目自主整理）、model-inference（AI/建模推断）。发布机构网站的一般介绍不自动是规范性标准；来源元数据与知识项分类可以不同。

来源索引必须包含 name、id、URI、version、publisher、license、retrieved_at、scope、authority。缺少许可写 unknown 并只存索引与原创摘要，不据此复制原文。记录原文位置不意味着可以重新分发全部原文。

冲突示例：同一个“客户”在签约系统指合同当事人，在营销系统指潜客；先保留两个有范围的定义，不能因为字段同名直接合并。

本说明为项目自主知识工程方法。
