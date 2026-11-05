---
name: property-graph-mapping
description: 把概念模型或 RDF/OWL 标准本体裁剪并映射为数据库中立属性图及 Graph Model Specification。用于 Class/Property/继承/Restriction 的保真与损失分析；不生成 NebulaGraph GQL 语法。
license: MIT
---

# property-graph-mapping

## 定位与解决的问题

从概念/标准本体形成显式保留语义、可交付的属性图规格。

## 适用与不适用

在用户请求上述建模工作时使用。仅加载与当前问题相关的材料；不强制调用其他 Skill。不用于具体行业标准定义的替代、GQL 语法生成或未经授权的数据库操作。

## 输入

概念模型或用户提供的 RDF/OWL/Turtle、业务范围、目标平台及版本（未知则写 unspecified）。标准路径还需来源版本和可用的 imports 闭包；无法获得的导入标缺失。

## 工作流程

1. 先写业务问题和选择范围。业务路径从概念/字段识别身份；标准路径盘点 IRI、imports、Class、Property、SubClass 与 Restriction。
2. 按 [映射规则](references/method.md) 筛选标准子集，保留被选类的必要父类、属性及限制依赖。裁剪时记录每个保留、排除与缺失项。
3. Class 仅在独立身份/生命周期/关系意义成立时映射节点；抽象类可成为标签、分类或文档中的父类，不机械一类一节点。
4. Object Property 映射有方向关系或关联实体；Datatype Property 映射逻辑类型属性；保存 Domain/Range 的推断语义及多域解释。
5. 对继承、等价、逆关系、限制、多值及复杂关系逐项决定保留、近似或未映射；每项提供解释和约束执行位置。
6. 按 [规格格式](references/graph-model-specification.md) 形成 Graph Model Specification，填完整主键、属性类型、端点、方向、约束、来源和未决事项。
7. 按业务问题检查映射完整性；把未表达语义写进 mappings，未知设计写进 unresolved。若需 GQL，读 [外部交接](references/gql-handoff.md)。

## 输出

裁剪/扩展本体清单；属性图规格；概念/字段/IRI 到图元素的映射表；信息损失与执行位置；Graph Model Specification；待决事项和业务问题验证。

## 资源

开始工作时读 [方法与决策](references/method.md)，需要完整演示时读 [示例](examples/worked-example.md)。资源均随本 Skill 分发；外链仅用于来源核实，不是基本功能的在线依赖。

## 质量检查与约束

用业务正反例检验输出是否覆盖需求、身份和来源。明确区分已知事实、项目方法和模型推断；缺少证据的结论标待确认。用户明确要求优先于本技能建议。静态模型审查不能冒充领域专家确认、OWL 推理或数据库原生运行结果。

需要组合时把本次输出作为下一步输入；其他技能是可选增强，基本流程独立可执行。

## 示例

Equipment 的某父类拥有 identifier；映射后展开 identifier 并保留 SubClassOf 的 mapping。若标准要求至少一个 custodian，但数据缺失，输出待补证据及应用检查，不虚构保管人，也不宣称本体不一致。
