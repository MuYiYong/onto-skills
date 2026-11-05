---
name: ontology-validation
description: 审查概念本体与属性图模型的业务完整性、身份、关系、类型、冗余及标准映射损失。用于模型质量验收和 Graph Model Specification 复核；不宣称静态检查等于 OWL 推理或数据库运行验证。
license: MIT
---

# ontology-validation

## 定位与解决的问题

交付可定位、可修复且分证据等级的模型质量报告。

## 适用与不适用

在用户请求上述建模工作时使用。仅加载与当前问题相关的材料；不强制调用其他 Skill。不用于具体行业标准定义的替代、GQL 语法生成或未经授权的数据库操作。

## 输入

概念/图模型、业务问题、来源/映射、规则和目标环境；允许不完整模型，但必须显式指出缺失项。独立使用时从输入重建审查表。

## 工作流程

1. 建立业务问题覆盖表，检查概念、流程和关键关系是否足以回答需求。
2. 按 [审查规则](references/method.md) 检查身份范围、空键/复合键、多重边身份、类型、单位和必填语义。
3. 检查方向、每端基数、有效区间和可选关系；用正反例看是否丢事件或误合并主体。
4. 检查冗余、循环继承、过度拆分节点与相同事实多处存储的冲突策略。
5. 对源本体逐项核对 Domain/Range、继承和 Restriction；不能以缺失数据代替 OWL 不一致证明。
6. 把问题分为 business-semantic、ontology-structure、property-graph-design、target-implementation；记录严重性、路径、证据和修复建议。
7. 图模型按 [规格说明与随包 Schema](references/graph-model-specification.md) 审查；unresolved 非空或关键约束执行位置未知，交付状态为 draft；语法/执行未跑则写未验证，不盖“已通过”。
8. 给出 issue 列表与复核后结论；有 GQL 结果时按 [外部交接](references/gql-handoff.md) 核对语义，具体语法校验交由外部技能。

## 输出

检查范围；业务问题覆盖；issues（id/category/severity/location/evidence/impact/remediation）；来源覆盖；映射损失；证据等级与 draft/ready 结论；未验证项。

## 资源

开始工作时读 [方法与决策](references/method.md)，需要完整演示时读 [示例](examples/worked-example.md)。资源均随本 Skill 分发；外链仅用于来源核实，不是基本功能的在线依赖。

## 质量检查与约束

用业务正反例检验输出是否覆盖需求、身份和来源。明确区分已知事实、项目方法和模型推断；缺少证据的结论标待确认。用户明确要求优先于本技能建议。静态模型审查不能冒充领域专家确认、OWL 推理或数据库原生运行结果。

需要组合时把本次输出作为下一步输入；其他技能是可选增强，基本流程独立可执行。

## 示例

“同一设备可在重叠时段借给两人”的样例与排他保管规则冲突。报告 business-semantic/error，定位 ASSIGNED_TO 的区间规则；静态 JSON 校验通过仍不能标业务通过。
