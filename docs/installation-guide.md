# 安装与更新

安装单元是含 SKILL.md 的完整目录；不能只复制入口文件。当前版本 `v26.11.06_Build0721` 包含全部25项。从 [GitHub 仓库](https://github.com/MuYiYong/onto-skills) 或 [最新 Release](https://github.com/MuYiYong/onto-skills/releases/latest) 获取资产；Release 提供25个单技能 ZIP、全量 ZIP 和八项金融/场景组合 ZIP，均使用普通目录并附 SHA-256。

## Codex CLI

官方 [Skills 文档](https://learn.chatgpt.com/docs/build-skills) 推荐用户级 `~/.agents/skills/<name>/`，项目级 `<project>/.agents/skills/<name>/`。当前 Codex 0.166.0 也实测发现 `$CODEX_HOME/skills/<name>/`，默认对应 `~/.codex/skills`，这是 CC-Switch 当前使用的同步目标。优先选一种管理方式，避免同名重复安装。

从本地仓库安装单个 Skill，例：

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/ontology-modeling" && cp -R skills/core/ontology-modeling "$HOME/.agents/skills/"
```

若目标已存在，先检查由谁管理以及是否有本地修改，再用原管理工具更新；上述命令不覆盖现有目录。若只需项目级，改目标为 `.agents/skills/`。macOS/Ubuntu 都使用上述普通目录结构；macOS 原生运行尚未验收。

没有本地仓库时，可从 GitHub Download ZIP 得到仓库副本后只保留所选 Skill 完整目录，也可用 Codex 现有 skill-installer 按 GitHub 子路径获取单个 Skill。本项目不提供下载/安装脚本；安装后可以删除下载的仓库副本。

启动 Codex，使用 `/skills` 或输入 `$ontology-modeling` 检查并调用。未显示时重新发现/重启；不要把 `skills/core/` 分类目录原样当成一个 Skill。明确选择目标目录可避免名称冲突。

所有独立路径如下；每行均可把其最后一级目录单独复制到用户或项目 Skills 根目录：

| Skill | 源目录 |
| --- | --- |
| ontology-modeling | skills/core/ontology-modeling |
| industry-knowledge-discovery | skills/core/industry-knowledge-discovery |
| entity-relationship-modeling | skills/core/entity-relationship-modeling |
| property-graph-mapping | skills/core/property-graph-mapping |
| ontology-validation | skills/core/ontology-validation |
| ontology-documentation | skills/core/ontology-documentation |
| ontology-evolution | skills/core/ontology-evolution |
| finance-domain-knowledge | skills/finance/finance-domain-knowledge |
| fibo-ontology | skills/finance/fibo-ontology |
| banking-business-model | skills/finance/banking-business-model |
| credit-risk-knowledge | skills/finance/credit-risk-knowledge |
| multi-lending-detection | skills/scenarios/multi-lending-detection |
| fraud-network-modeling | skills/scenarios/fraud-network-modeling |

本次新增技能的独立安装目录：

| Skill | 源目录 |
| --- | --- |
| electric-power-domain-knowledge | skills/industries/electric-power-domain-knowledge |
| power-outage-impact-analysis | skills/scenarios/power-outage-impact-analysis |
| manufacturing-domain-knowledge | skills/industries/manufacturing-domain-knowledge |
| manufacturing-quality-traceability | skills/scenarios/manufacturing-quality-traceability |
| logistics-domain-knowledge | skills/industries/logistics-domain-knowledge |
| shipment-exception-analysis | skills/scenarios/shipment-exception-analysis |
| healthcare-domain-knowledge | skills/industries/healthcare-domain-knowledge |
| healthcare-care-pathway-modeling | skills/scenarios/healthcare-care-pathway-modeling |
| retail-domain-knowledge | skills/industries/retail-domain-knowledge |
| retail-inventory-replenishment | skills/scenarios/retail-inventory-replenishment |
| financial-regulatory-reporting | skills/scenarios/financial-regulatory-reporting |
| related-party-transaction-modeling | skills/scenarios/related-party-transaction-modeling |

## CC-Switch

官方 Linux 4.0.25 已在隔离账户中通过原生界面验收；用户自己的安装版本仍未确认。以下注明实际菜单和需单独验收的仓库流程，见 [兼容报告](compatibility.md)。

1. 打开 Skills → 顶部 ⋯ → Manage repositories。
2. 4.0.25 的 Repository URL 填 `https://github.com/MuYiYong/onto-skills`，Branch 填 `main`。此界面没有子目录字段，不能填写 `tree/main/skills` URL，实测会拒绝。若旧版本有独立子目录字段，填 `skills`。
3. 重新读取/刷新仓库。上游扫描器递归识别 `skills/core/<name>`、`skills/finance/<name>`、`skills/industries/<name>`、`skills/scenarios/<name>`。发布前原生验收时该配置显示 0 项；该历史结果只证明配置可添加。发布后的仓库安装仍需单独验证。
4. 在发现页选择安装目标 Codex，只安装需要的 Skill。已安装页可调整各应用开关；多项选择按当前版本批量启用。
5. 确认 SKILL.md、references、examples、LICENSE 都安装成功，且 Codex 可发现。存储主副本默认 `~/.cc-switch/skills/`，Codex 目标默认 `~/.codex/skills/`，实际配置可修改。

本地资产使用 Skills → Add Skill → Install from ZIP。将所选完整 Skill 目录放进普通 ZIP；已实测单项、两项选择包和包含 `skills/<category>/<name>/` 的 13 项包。`Import from this computer` 扫描已安装应用的 Skills，不是任意本地目录选择器。不支持 ZIP 的旧版本可先按 Codex 手动方式安装，再用其已有导入功能。Pack 是组合说明，不是 CC-Switch 专用包格式。

发布仓库来源的更新使用现有 Check Updates/卡片操作；改变远端版本后的升级尚未验证。本地 ZIP 重复导入会跳过同名目录，不覆盖更新；需要替换时先检查本地修改和备份，再通过已有卸载/导入操作完成。已实测单项卸载保留其他项、选择后批量卸载、Codex 开关和原生发现；CC-Switch 会在卸载前备份。不要用本项目脚本替代 CC-Switch 管理。

## 可选外部 nebula-gql-skills

官方仓库：[MuYiYong/nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills)。仅本体设计不需要安装。

- CC-Switch 4.0.25：添加仓库根 URL `https://github.com/MuYiYong/nebula-gql-skills`、分支 `main`，递归发现后选择 gql-query-generator 或 gql-procedure-generator；有独立子目录字段的旧版可填 `src`。外部仓库的实际安装/升级未纳入本次本地 ZIP 验收。
- Codex 手动：从 [最新 Release](https://github.com/MuYiYong/nebula-gql-skills/releases/latest) 下载所需单 Skill 或组合包，解压后将完整 `gql-query-generator/` 或 `gql-procedure-generator/` 放入 `~/.agents/skills/`；保持目录名不变，检查发现后调用。
- 检查/更新：每次 GQL 任务先读当前已安装入口与相应参考，按目标版本核实能力；更新由 CC-Switch 或原有安装方式完成。日期化观测 release 不等于长期版本锁定。

查询/支持的 DML 使用 query 技能，过程定义/管理和算法使用 procedure 技能。Graph Type/其他 DDL 须核实当前技能是否覆盖；若未来有专用技能优先采用。缺技能时报告具体名称和上方官方安装方式；有技能但不具备所需能力时保留图规格并报告能力缺口，不冒称完成语法生成。
