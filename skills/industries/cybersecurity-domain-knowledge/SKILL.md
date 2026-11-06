---
name: cybersecurity-domain-knowledge
description: 用于软件供应链与漏洞本体建模，厘清SPDX文档/组件身份、CSAF产品通告与版本、CVSS严重度和部署修复证据；适用于SBOM字段对齐和状态口径审查，不推断实际入侵或自动修复。
license: MIT
---

# 网络安全领域知识

## 定位与输入

独立使用给定材料建立数据库中立的概念与证据模型。最小输入：业务范围、SBOM文档命名空间/组件ID/版本、来源及评价/知识时点。场景判断另需通告发布者、文档ID/修订/产品状态、版本映射依据和部署记录；缺失项保持未知并列确认方法。

## 工作流程

1. 读取[标准来源](references/sources.json)和[领域记录](references/domain.json)，固定标准版次与适用范围；每项写标准定位与解释或本地政策缺口。
2. 依[方法](references/method.md)区分组件、文档、资产、产品、漏洞和通告断言；同名及同SPDXRef不自动合并。
3. 保留发布和知识时间、原始修订及载荷证据；显式选择修订策略，冲突不任意覆盖。
4. 用受信版本映射连接产品断言与组件，保持四类状态及缺评估的区别；保留影响/行动理由，列未支持的范围/组/状态及损失。
5. 分别交付依赖、部署、影响候选、严重度和实际修复证据；不把补丁存在、分数或依赖当作已安装修复或被利用。
6. 依据[工作示例](examples/worked-example.md)复核正常反例、未知、来源和待决项；仅使用任务提供或包内材料即可完成基本工作。

## 输出与质量

范围、标准版本/定位、概念关系、身份与时间表、映射来源、冲突与未决问题、证据支持的候选结论及限制。项目解释维持project-curated，未实际执行的标准校验、数据库运行和生产修复不作完成声明。用户明确约束优先，其他技能均为可选。

## 资源

[方法](references/method.md)、[知识](references/domain.json)、[来源](references/sources.json)、[示例](examples/worked-example.md)和[许可证](LICENSE)均包内自足；官方链接用于可选核实，不是运行依赖。

交付时读取条目的standard_status：standard-backed仅表示standard_basis.scope内有已核实标准依据，其他本地规则仍按standard_gap保留；nonstandard-modeling明确标为“非标准建模”，标准未取得或精确映射未核实的原因一并列出。不得把背景页、目录或来源分类当成条目符合性。
