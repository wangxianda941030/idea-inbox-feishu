# 每天自动运行

灵感的"提炼"需要 AI 判断，所以自动化有两种模式：

## 模式 A：AI Agent 全自动（推荐）

如果你在用支持定时任务的 AI 助手，让它每天定时执行完整流程：

> 「扫描灵感投递箱 → 你亲自把每条灵感提炼成选题（一条可拆多个，太碎的跳过）→ 写进飞书研究素材库和内容生产库 → 归档已处理文件。」

AI 负责提炼这一步，这是最省心、覆盖最全的方式。本项目最初就是这么用的。

## 模式 B：脚本定时 + LLM API 提炼

`scan` 和 `push`/`archive` 可脚本化，中间的提炼调用你选的 LLM API：

### Linux / macOS cron

```cron
0 21 * * * cd /path/to/idea-inbox-feishu && ./run_daily.sh >> out/cron.log 2>&1
```

`run_daily.sh` 大致逻辑：
```bash
python -m ideainbox scan > out/scan.json
python your_llm_refine.py out/scan.json   # 调 LLM，产出 out/research.json 和 out/content.json
python -m ideainbox push --table research --input out/research.json
python -m ideainbox push --table content  --input out/content.json
# 归档（文件名可从 scan.json 里解析）
```

### Windows 任务计划程序

新建每天 21:00 的任务，动作为上面这串命令。

## 关于飞书授权过期

lark-cli 的授权 token 有有效期。若写入报鉴权错误，重新执行一次 `lark-cli auth login --recommend` 即可。
