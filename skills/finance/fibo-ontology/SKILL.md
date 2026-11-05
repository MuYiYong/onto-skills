---
name: fibo-ontology
description: 解析并裁剪 FIBO 模块、Class、Object/Datatype Property、Domain/Range、SubClass 和 OWL Restriction，对齐业务扩展并记录属性图映射损失。用于 FIBO 标准驱动建模与版本差异；不分发完整 FIBO、不生成 GQL。
license: MIT
---

# fibo-ontology

## 定位与解决的问题

将标准语义与企业业务范围对齐，产生可追溯的裁剪、扩展与图映射建议。

## 适用与不适用

用于上述金融行业知识与建模任务。只处理请求范围，不能将项目解释当成标准原意；不负责 GQL 语法、生产数据操作或自动作出不利业务决定。

## 输入

业务范围、FIBO 版本或用户提供的 RDF/OWL/Turtle、imports 可用性及业务数据。只有索引时只能做候选对齐，不能宣称解析了完整标准。

## 工作流程

1. 先读 [模块索引](references/fibo-index.json) 和 [来源](references/sources.json)，区分当前发布/开发材料、版本 IRI 与稳定术语 IRI。
2. 用户给本体时列 ontology/imports 闭包、Class、Object Property、Datatype Property、Domain/Range、继承、Restriction；资源缺失要登记。
3. 用业务问题选概念，沿必要父类、属性、限制及导入依赖扩展最小子集；明确保留、排除和未获取三类。
4. 以 IRI/定义/约束匹配业务概念；不靠同名或中文译名判等。借款人等角色与主体身份分开。
5. 参考 [语义映射方法](references/method.md) 设计属性图；标出推理与闭世界规则的区别，不把所有 OWL 类都变节点。
6. 将企业扩展放独立命名空间，不改写标准 IRI 的原定义。每个保留/近似/未映射项记录理由、信息损失及受影响业务问题。
7. 比较不同版本时检查实体/公理、弃用、IRI、imports 和业务扩展冲突；不得把检索时间当源版本。
8. 输出裁剪/扩展目录和图映射；本地 [精确示例](examples/worked-example.md) 演示贷款概念的有界对齐。需要 GQL 时读 [交接](references/gql-handoff.md)。

## 输出

来源/版本与 imports 状态、标准子集、业务扩展目录、IRI 对齐表、图设计、限制执行位置、映射损失、未决项和版本差异。

## 资源

先读 [方法](references/method.md)，按流程读取所需 JSON，需演示时读 [工作示例](examples/worked-example.md)。来源和基本知识随本 Skill 分发；仅在用户要求最新标准或缺少必要原文时再检索，离线可使用给定材料并明确缺口。

## 质量检查与约束

核对术语、身份范围、角色、时间和来源；保留标准/通用/整理/推断的分类。未知阈值不杜撰，示例阈值不推广为监管要求。单独安装可完成本职工作；其他 Core、Finance 或 Scenario 技能是可选组合。

## 示例

将 FIBO Loan 对齐业务 LoanContract 时保留其两个父类及贷款金额相关限制的映射说明；业务字段 loan_id 是企业扩展，不声称是标准定义的主键。
