# 知识资产规范

金融知识按 terminology、concepts、relationships、standards、examples 组织。按内容选择 Markdown、JSON、YAML、CSV、Turtle 或 OWL，不强制一种格式；第一阶段主要采用有元数据的 JSON，示例用 Markdown/JSON。

每个重要资产记录 id、name、version、source_ids、license、updated_at、scope、authority、classification。source_ids 指向 sources.json 内的来源：id、name、uri、version、publisher、license、retrieved_at、scope、authority、kind。知识条目也记录自己的来源与分类，不能仅给整个文档贴“官方”标签。

classification/kind：official-standard（有明确版本的规范定义）、industry-common（有来源的通用知识）、project-curated（原创整理）、model-inference（AI/建模建议）。转述、裁剪策略和属性图建议属于项目整理或推断，即使参考了官方标准，也不能变成官方定义。

版本变更记录新增概念、来源版本变化、定义变化及废弃 ID；ID 不复用。原标准 IRI 与本项目概念 ID 分开。未知版本写明未知，不编造发布日期。检索日期不是源版本。

许可证：本项目原创摘要与例子为 MIT；不把第三方规范自动改成 MIT。仅保存标准索引、来源与自主解释；复制原文/本体前核查精确文件及其许可。unknown 表示未确认，不授权重新分发。FIBO 仓库 LICENSE 为 MIT，但链接的出版物与商标各自适用，当前不打包 FIBO 本体。

同步：修改中心资产后显式更新 tests/content-validation/snapshots.json 指定的包内副本；差异检查会阻止遗漏。禁止通过 ../../knowledge 运行时访问。每个包单独复制后必须保有来源索引和基本知识。
