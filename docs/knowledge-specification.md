# 知识资产规范

各行业知识置于 `knowledge/<industry>/`，按 terminology、concepts、relationships、standards、examples 组织；无需为不存在的内容建空目录。金融专项可以使用 `knowledge/finance/<topic>/`。按内容选择 Markdown、JSON、YAML、CSV、Turtle 或 OWL，不强制一种格式；第一阶段主要采用有元数据的 JSON，示例用 Markdown/JSON。

每个重要资产记录 id、name、version、source_ids、license、updated_at、scope、authority、classification。source_ids 指向 sources.json 内的来源：id、name、uri、version、publisher、license、retrieved_at、scope、authority、kind。知识条目也记录自己的来源与分类，不能仅给整个文档贴“官方”标签。

classification/kind：official-standard（有明确版本的规范定义）、industry-common（有来源的通用知识）、project-curated（原创整理）、model-inference（AI/建模建议）。转述、裁剪策略和属性图建议属于项目整理或推断，即使参考了官方标准，也不能变成官方定义。

版本变更记录新增概念、来源版本变化、定义变化及废弃 ID；ID 不复用。原标准 IRI 与本项目概念 ID 分开。未知版本写明未知，不编造发布日期。检索日期不是源版本。

许可证：本项目原创摘要与例子为 MIT；不把第三方规范自动改成 MIT。仅保存标准索引、来源与自主解释；复制原文/本体前核查精确文件及其许可。unknown 表示未确认，不授权重新分发。FIBO 仓库 LICENSE 为 MIT，但链接的出版物与商标各自适用，当前不打包 FIBO 本体。

同步：修改中心资产后显式更新 tests/content-validation/snapshots.json 指定的包内副本；差异检查会阻止遗漏。禁止通过 ../../knowledge 运行时访问。每个包单独复制后必须保有来源索引和基本知识。

标准优先：先确定地区、适用日期、标准发布机构和正式版次，核实具体条目，再形成原创解释。所有非来源目录的JSON知识资产声明 `standards_policy: standards-first-v1`。每个含id的知识项（含集合、模块和变更记录）给出 `standard_basis` 或非空 `standard_gap`；集合组织方式、原创例子和本地政策也可直接说明其非标准性质。

standard_basis是数组，每项含source_id、locator、relation和scope。source_id必须在该条目的source_ids及本地来源目录内；locator为具体条文、字段、IRI或文件位置，scope说明只支持哪部分。relation为supports时仅能引用official-standard；background可引用官方标准的公开摘要或有来源的行业介绍。只查到付费标准目录不能声称读取了正文或验证了类级公理。official-standard知识项必须有直接supports，但机械通过仍需人工核对实质含义。

standard_gap说明无直接依据、未核实的精确映射或必须由用户提供的政策；不能以一个官方链接替代缺口。basis与gap可并存，以区分背景语义和项目规则。未知版本、阈值、范围与许可继续保持未知，注明补证路径。具体行业见[标准优先知识说明](standards-first-knowledge.md)。

每个知识范围有自己的 `standards/sources.json`。开发校验从当前资产向上选择最近的来源目录，并要求它位于knowledge树内；缺失、畸形或软链接越界均报错，不回退到另一行业的金融来源。包内仅携带自己的来源和所需知识副本，不运行该查找逻辑。

每条知识另有standard_status：standard-backed仅对已核实supports范围表示有标准依据；nonstandard-modeling明确表示非标准建模，必须附standard_gap说明本地政策、无直接规范或标准未核实的原因。仅有background不能标为standard-backed；两类状态都不自动变成标准认证。
