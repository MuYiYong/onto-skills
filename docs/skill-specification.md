# Skill 资产规范

遵守 [Agent Skills 规范](https://agentskills.io/specification) 与 [Codex 文档](https://learn.chatgpt.com/docs/build-skills)。

每个 skills/<category>/<name>/ 必须包含 SKILL.md，文件以 YAML frontmatter 开始。name 为 1–64 字符的小写字母、数字、单连字符，不以连字符开头/结尾、不连续，且等于目录名；description 是 1–1024 字符的具体调用条件。避免泛称“帮助处理任何本体任务”。本仓库原创内容用 license: MIT，包内附 LICENSE。

正文需说明定位、解决的问题、适用/不适用、输入、工作流程、输出、资源、质量检查、约束及示例。基础方法在入口，细节在 references；只读当前任务需要的资源。不能仅写行业介绍。

输入注明最小材料和可选增强。输出注明字段、业务含义、来源、假设和未知项，前后步骤靠这些交付物组合，不用隐式上下文。每个 Skill 应能直接从用户材料完成其声明的基本任务。

资源只用包内相对路径；不使用父目录逃逸、绝对路径、软链接或另一个未安装 Skill 的文件。外链用于可选核实与来源索引，已有材料的基本工作不依赖联网。随包知识同步表见 tests/content-validation/snapshots.json，只供开发核对。

评审：描述是否能正确触发、方法是否具体、示例能否体现关键取舍、是否过度建模、标准与推断是否分开、输出可否被下游独立理解。格式检查不能证明方法专业质量；运行 [验证说明](../tests/README.md) 并做人工/行为评估。
