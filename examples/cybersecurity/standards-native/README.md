# 标准原生文档与显式投影

这些文档为项目原创合成数据，原始事实与上级input.json的关系见[投影说明](projection-map.json)。A/B文档命名空间与简写别名显式映射，不通过同名组件猜测等价。部署与observed_at来自独立本地证据，不能从SBOM或通告补造。

- [SPDX A](sbom-a.spdx.json)、[SPDX B](sbom-b.spdx.json)：SPDX2.3文档、包和声明依赖。
- [通告修订1](advisory-1.csaf.json)、[修订2](advisory-2.csaf.json)：CSAF2.0 VEX格式，含产品范围及行动/影响说明。
- [CVSS4.0](cvss-4.0.json)：完整Base向量与10.0分；独立于CSAF2.0的v2/v3分数字段。FIRST参考实现与另一实现交叉计算。
- negative目录保留错误影响说明/矛盾产品状态、重复SPDX身份及不一致分数反例。分数字段符合JSON类型仍可能与向量计算不符，因此不能只用schema判断CVSS有效。

这些格式/语义检查只证明对应合成文档，不证明Skills已经实现完整标准处理器、真实漏洞事实或全部七行业标准符合性。原始例子及解释适用项目MIT许可；所用外部规范/校验器另按其来源许可，未复制校验器或规范全文。
