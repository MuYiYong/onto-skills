# 输入和验收约定

[input.json](../examples/input.json) 是脱敏的合成源数据，不是标准交换消息或数据库导入文件。模型字段与源记录并非一一同名：源系统/公用事业命名空间、稳定键和记录位置提供 source_record；外键展开为图关系，关系实例需保留源记录键。缺失必需事实必须先补全，不能为真实数据编造值。

[acceptance.json](../examples/acceptance.json) 每个 case.input 先深复制 fixture=input.json，然后覆盖 query 中列出的字段、依次应用 patches、最后向 append 指定的数组追加记录。patch.path 用 / 分隔；数组记录选择器为 version_id/state_id/outage_id/event_id/segment_id/lot_id 等已存在的完整键值，数字选择器仅用于已选记录内部的数量参与数组。路径找不到或匹配不唯一应报错。测试中的外部批次身份由 source_system/site_id/lot_id 完整限定，不能以 lot_id 跨工厂选取模糊记录。

expected 是该有界参考计算的完整结果对象，不是自然语言通过条件。所有输出数组按字典序排序，数量为十进制字符串。用例只证明这些离线数据和约定，不证明标准符合性、实际业务正确性、数据库执行、CC-Switch GUI 或 macOS 行为。
