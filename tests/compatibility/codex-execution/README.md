# Codex CLI 实际调用验收

2026-11-05，Ubuntu，原生 Codex 0.166.0，4 个终态成功用例。每个用例只将单一完整 Skill 复制到无关临时项目 `.agents/skills/<name>/`；显式调用，read-only/ephemeral，使用 CLI 原有认证，未读取或复制凭据。

[receipt.json](receipt.json) 记录终态退出码、schema 检查、源文件和输出哈希；各子目录保存实际 prompt、JSON schema、result 和真实资源读取命令。命令输出只存哈希，未保留推理日志或用户配置。[review.json](review.json) 逐条记录人工语义复核依据。FIBO 输入为项目原创的有界 Turtle 表达，不是完整官方本体。

覆盖关系身份、FIBO 标准裁剪与语义损失、多头借贷反例、版本演化与回滚；没有发现需修改正文的缺陷。4 个有界成功案例不是全部 13 项的量化评测，也不证明自动触发、完整 OWL 推理或 macOS。已有 13 项静态独立性与原生发现证据继续单独保留。

复现时将相应单包复制到临时项目，保存本目录的 prompt/schema（FIBO 同时保存 input.ttl），在该目录运行 receipt 中的 argv 并人工复核结果；需要可用的正常 Codex 认证，会产生模型调用费用。不要将有界结果当作生产事实。
