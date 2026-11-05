# 外部 GQL 交接

本技能交付业务语义和 Graph Model Specification。语法生成使用当前 Agent 已安装的 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。不要复制该项目文件、语法库或固定旧版本。

1. 先完成模型与语义检查，明确目标 NebulaGraph 版本及未决事项。
2. 检查 Agent 当前已安装技能及其声明/相关资源：查询和受支持 DML 路由 gql-query-generator，定义/管理过程和图算法路由 gql-procedure-generator。不要因出现 CALL 就加载全部技能。
3. Graph Type/其他 DDL：检查当前已安装版本是否确有对应能力；若新增专用 Skill 优先使用。不能假定 query 入口必然支持完整 DDL，也不能靠旧知识补语法。
4. 缺技能时明确说缺少哪个能力及 Skill；给出上方官方仓库。CC-Switch：Skills → 仓库管理 → 添加 MuYiYong/nebula-gql-skills，分支 main、子目录 src，刷新并安装所需项。Codex：从上游最新 Release 获取单 Skill 或组合包，将所需完整目录复制到 ~/.agents/skills/<name>/（CC-Switch 可能同步到 ~/.codex/skills）；重新发现。用户目录命令由宿主环境解析，不是本包资源路径。
5. 如果已安装版本不覆盖目标 DDL，交付模型并说明实际能力缺口，检查上游最新 README/Release；不冒称已调用、已生成或已验证。
6. 交接模型、业务问题、来源与损失、目标版本、约束执行位置；回传后核对元素/类型/键/端点/方向/时效/约束。静态语义复核与真实数据库执行分别记录。

安装、检查更新、升级与卸载用现有 Agent/CC-Switch；两个项目独立更新。仅本体设计无需安装外部技能。
