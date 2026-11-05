# 架构

Onto Skills 将行业知识和业务需求转化为可审查、数据库中立的属性图本体。

```text
业务描述/Schema → 行业理解 → 概念/实体关系 → 属性图 → 质量复核
标准 RDF/OWL → 版本与范围 → 裁剪/扩展 ──────────┘
                                  ↓
                      Graph Model Specification
                                  ↓ 可选
                  当前安装的 nebula-gql-skills → GQL
```

- Core：通用本体工程方法，独立于行业、OINX 和图数据库。
- Industry：金融/FIBO与电力、制造、物流、医疗、零售知识；各有来源目录和随包最小知识，行业事实不放入 Core。
- Scenario：多头借贷、欺诈、监管报送、关联交易，以及五个新行业的具体场景；模型/输入/反例随包，使用本地最小知识即可独立执行。
- Knowledge：有来源、版本、许可、证据分类的行业资产。
- Packs：说明如何选择、排序和组合 Skills，不是程序或强制依赖清单。

skills/<category>/<name> 是直接分发单元。每个目录有 SKILL.md、本地资源、示例和 LICENSE；不引用仓库其他目录。knowledge 的选用子集随 Skill 保存，开发检查追踪副本一致性，不运行发布时依赖解析。

组合通过交付物传递：来源清单 → 概念目录 → 实体关系表 → 图规格 → 质量报告。用户可从任一步开始，不要求安装全部技能。完整 JSON 交接格式见 [图规格](graph-model-specification.md)。

GQL 的 DDL/DML/DQL/Procedure 表达由独立的 [nebula-gql-skills](https://github.com/MuYiYong/nebula-gql-skills) 负责。每次任务检查当前已安装能力；Graph Type 语义仍由本项目设计。当前入口是否支持目标 DDL 要从其当前资源核实，不能因名称为 query 就假定支持完整 DDL。缺失能力时保留图规格并指出缺口。

本项目没有应用运行时、数据库连接、网络知识服务、安装器、Registry、Resolver、同步服务或 Web 界面。scripts 只服务仓库开发检查。
