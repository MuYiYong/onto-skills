# 贡献指南

先选明确边界的能力或知识缺口，说明真实输入和预期输出。新增 Skill 必须有具体 description、独立资源、工作方法、可检验例子与许可；不要把行业知识放入 Core。

知识贡献记录来源、版本、发布方、许可、范围与证据分类。提交原创解释与索引；若要带入第三方原文/本体，先核实许可证与归属声明。AI 建议标 model-inference，不能写成标准事实。

新增 Pack 仅写组合说明，列当前真实存在的技能。未来行业放 roadmap，不创建貌似可用的空 Skill。

开发环境：Python 3.10+；在自己的虚拟环境安装 requirements-dev.txt。运行 `python3 scripts/validate.py` 与 `python3 -m unittest discover -s tests -v`；修改知识副本时同步 snapshots.json 指定文件。原生 Codex 检查可用 `python3 tests/compatibility/codex_probe.py`，不要求 CI 有 Codex。

评审同时检查职责、专业内容、输入输出、映射损失、示例、来源、资源闭包和未验证项。测试只匹配标题不能代替内容评审。任何新代码仅供开发验证，不能扩展成安装/管理产品。

PR 描述给出变化与理由、验证命令和真实结果、来源许可变化、兼容性限制。不要提交真实客户数据、机器私有配置或访问凭据。
