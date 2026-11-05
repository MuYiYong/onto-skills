---
name: logistics-domain-knowledge
description: 为物流本体或业务图整理Shipment、Consignment、物流单元、路段、订舱单证与可见性事件的身份、时间和来源边界。用于物流术语澄清、数据字典对齐和概念建模；不从计划事件推断实际交付。
license: MIT
---

# 物流领域知识

## 定位与适用范围

将用户材料整理成可追溯、可组合的行业概念与关系交付物，支持本体和业务图设计。适用于术语对齐、范围澄清和模型裁剪；不执行业务操作、认证标准符合性或写生产数据。本包独立可用，不要求安装其他技能。

## 输入

最小输入：业务问题、运输参与方及命名空间、原始字段或脱敏样例、来源与时间口径。可选：GSIN/GINC/SSCC/GLN 的获配证据、订舱/单证版本、交接凭证及原代码词典。

身份、时间、单位或政策缺失先列未决项，继续交付不依赖缺口的部分。

## 工作流程

1. 固定分析范围：端到端交付、某段运输服务或单元追踪，列出关键业务问题与 as_of/known_as_of。
2. 按[领域记录](references/domain.json)区分 Shipment、Consignment、LogisticUnit；逐个声明命名空间，标识证据未知则保留内部号。
3. 分别列商业/文档事实和物理观测：订舱确认、单证签发、装载、卸货、交接与交付不互为替代证据。
4. 按[方法](references/method.md)拆分计划、估计、实际及 event_time/issued_at/record_time/observed_at，保留原始时区偏移。
5. 为转运重组的成员关系建有效区间，为消息建来源事件键；重放、冲突与真实复扫分别处理。
6. 输出概念、关系、生命周期、来源与缺口，并用[工作示例](examples/worked-example.md)中的误合并/误交付反例复核。

## 输出

- 范围、业务问题、评价时点及假设。
- 概念/角色表：name、business meaning、identity scope、lifecycle、source_ids、classification。
- 关系表：端点/方向、含义、基数条件、时间、来源和不确定项。
- 字段映射与损失；证据支持/反证；未决项、确认办法和质量结果。

## 资源与约束

[领域JSON](references/domain.json)、[来源JSON](references/sources.json)、[本地方法](references/method.md)、[完整示例](examples/worked-example.md)与[许可证](LICENSE)均随包提供。已有输入的基本工作可离线完成，外链仅供可选核实。

## 质量检查

区分官方对象背景和项目建模建议；所有概念有来源与分类，不把模型选择称为官方定义。检查同名异义、身份范围、重复/晚到记录、时间与单位、正常反例。报告模型静态审查与实际运行的不同证据层级，不从缺失数据得出肯定业务结论。
