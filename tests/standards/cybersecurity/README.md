# 标准原生合成文档验证

[receipt.json](receipt.json)绑定[原始文档](../../../examples/cybersecurity/standards-native/README.md)及实际校验结果。来源/章节更正、本地策略与标准未核实部分分别报告，不把资产格式测试称为标准认证。

实际执行：SPDX-tools0.8.5的SPDX2.3解析/语义校验；Secvisogram CSAF-validator-lib3.0.2全部full与mandatory导出函数（每份75项）；FIRST官方CVSS4.0 Revision2 JSON schema、固定FIRST参考实现与cvss3.6交叉计算。

两份SPDX文档与两份CSAF2.0/VEX通告通过强制错误检查，重复SPDX身份、矛盾产品状态、缺少影响说明被拒绝。CSAF可选项的8条警告逐份保留；isValid=true不表示所有SHOULD项满足。CVSS4.0完整Base向量计算10.0，字段schema不能单独发现向量与9.8不一致，因此另做分值计算。

外部工具仅作开发验证，未复制到Skill或引入运行时依赖。完整标准原文、校验器和FIRST实现均按上游条款获取；仅原始合成例子与结果随仓库分发。普通CI只验证冻结证据完整性和源绑定，不冒充新的外部校验器运行。
