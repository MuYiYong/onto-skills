# EPCIS 纠错身份证据

2026-11-06，以 GS1 发布的 EPCIS 2.0.1 JSON Schema 实际校验三份原创合成文档，均通过结构验证；版本、来源、校验器及 SHA-256 见 [receipt.json](receipt.json)。不复制第三方标准正文或官方示例。

[原记录](original.jsonld)与[纠错声明及更正事件](declaration-and-corrective.jsonld)满足 §7.4.1.2 的关键身份规则：声明重用原 eventID，除 errorDeclaration 和 recordTime 外保持原事件内容相同；更正事件使用另一个 eventID。声明不是新的实物流转。

[反例](negative-changed-original.jsonld)在重用 eventID 时修改了原商品内容。它仍符合 JSON Schema，但不满足上述跨文档内容相等规则。这证明仅做结构校验不足以识别该错误。离线证据测试独立检查这两种情况；未运行 EPCIS 服务接口、完整 JSON-LD/SHACL 验证或认证。
