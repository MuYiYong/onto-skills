---
name: financial-regulatory-reporting
description: 设计中国金融监管报送的制度版本、指标上下文、源数据到报表血缘、勾稽质量、更正提交与监管回执图模型。用于监管统计数据治理、报送差错追溯和影响分析；不代替正式报表模板、法律适用确认或自动报送。
license: MIT
---

# 金融监管报送与指标血缘

## 输入与范围

中国监管机关、机构类型、制度/报表/指标定义版本、单体或合并范围、报告时点/期间、known_at、源Schema/脱敏样例、币种单位/转换、质量规则、提交和回执。缺少正式模板/指标时可完成有界血缘草案，不能编造实际表号、公式、阈值、截止或“已合规”。基本任务不依赖其他Skill或联网。

## 工作流程

1. 阅读[领域知识](references/domain.json)、[来源](references/sources.json)和[方法](references/method.md)，明确中国本地要求与国际数据语义的边界。
2. 为ReportingEntity、ReportDefinition、MetricDefinition、ReportContext、SourceRecord、TransformationRun、ReportedFact、Submission、ValidationCheck、Receipt、Evidence建立身份、关系和版本；用[完整模型](examples/graph-model.json)作可审查参考，不盲目照搬其粒度。
3. 将主体/范围/时点或期间/维度/单位写入事实上下文，明确存量/流量、时区、汇率与舍入。未知值保留nil原因，口径不匹配或无转换时报告阻断。
4. 固定as_of与known_at，逐源事件版本去重/冲突检测；构建源版本→转换运行→事实→报送修订→回执的血缘和逐条贡献，保留人工调节及责任角色。
5. 将格式、本地业务校验、勾稽/跨表一致性、复核与监管回执分开。更正关联旧提交，明确已发送/已收到/已拒绝/已接受，不能用本地通过推定监管接受。
6. 依据[合成输入](examples/input.json)和[正反例](examples/acceptance.json)验证重放、晚到、更正、错版本、混币种、缺失和回执；报告实际验证层次。
7. 输出中立图规格、差异定位、证据/版本、影响范围和未决事项。需要GQL时按[外部交接](references/gql-handoff.md)交给当前已安装外部能力，不能自行补语法或执行真实报送。

## 输出

选定制度/版本与范围；完整图规格；事实/上下文/单位及逐层来源表；质量问题定位与复核责任；运行/提交/更正/回执状态链；正反例和适用性缺口。规范化结构参考[图规格](references/graph-model-specification.md)及[Schema](references/graph-model.schema.json)。

## 质量与示例

核对源版本身份、上下文/单位、双时钟、不可覆盖历史和回执性质。项目模型不等同于XBRL或监管接口一致性验证；BCBS239及2026信息性通讯不替代中国模板。见[工作示例](examples/worked-example.md)。
