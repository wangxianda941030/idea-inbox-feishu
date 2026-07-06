# 💡 Idea Inbox → Feishu · 灵感投递箱

> 把你和 AI 聊出来的灵感、随手记下的想法，**自动整理成结构化选题，沉淀进飞书多维表格**。
> 不用记录格式、不用手动填表 —— 你只管把灵感丢进一个文件夹，剩下交给 AI。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

---

## 这个工具解决什么问题

你有没有过这种时刻：**和 ChatGPT 聊着聊着，突然碰撞出一个特别好的想法/选题** —— 然后聊天窗口一关，它就再也找不回来了。

好想法不该随聊天记录流走。这个工具帮你：

```
随手把灵感丢进文件夹  →  AI 读懂并提炼成选题  →  自动存进飞书表格
```

之后你打开飞书，就有一个**越攒越厚的选题库**，能筛选、能追踪"拍了没 / 发了没"、能回看自己积累了哪些判断。

> 💡 特别适合：内容创作者、自媒体、研究者、任何"经常和 AI 聊出好东西"的人。

---

## 它的设计哲学（重要）

**生成交给 AI，管理交给飞书，机械活交给脚本。** 三者分工：

| 角色 | 负责 |
|---|---|
| 🤖 **AI** | 读懂你那段乱糟糟的灵感，提炼成选题、写脚本 —— 这是 AI 最擅长的 |
| 🗂️ **飞书多维表格** | 沉淀、检索、状态追踪（待制作→已拍→已发布）、数据回流 |
| ⚙️ **本工具（脚本）** | 扫描文件夹、结构化写入飞书、归档已处理文件 |

**所以你投递的内容完全不需要格式**：一句话、一大段对话、一篇研究纪要都行。"从乱到结构"正是 AI 的价值。

---

## 三张表：一个内容生产系统

`setup-base` 会帮你建好一个 Base + 三张表，构成 **研究 → 内容 → 复盘** 的闭环：

1. **研究素材库** — 存判断和证据（研究主题 / 核心判断 / 证据 / 来源 / 反方观点…）
2. **内容生产库** — 存可拍的成品（选题 / 钩子 / 抖音脚本 / 小红书正文 / 状态…）
3. **发布复盘库** — 存数据回流（曝光 / 完播率 / 点赞 / 结论…）

字段都可在 `config/tables.json` 里自定义。

---

## 🚀 快速开始

### 0. 前置

- Python 3.9+（纯标准库，无需 pip 装包）
- 飞书账号 + 飞书 CLI（用于写表，见 [docs/feishu-setup.md](./docs/feishu-setup.md)）

### 1. 克隆

```bash
git clone https://github.com/wangxianda941030/idea-inbox-feishu.git
cd idea-inbox-feishu
```

### 2. 装并授权飞书 CLI

```bash
npm install -g @larksuite/cli
lark-cli config init --new       # 浏览器建应用
lark-cli auth login --recommend  # 浏览器授权（勾选多维表格权限）
```

### 3. 配置

```bash
cp config/config.example.json config/config.json
```

打开 `config.json`，把 `persona`（你的人设与风格）改成你自己的。其余先留空。

### 4. 一键建表

```bash
python -m ideainbox setup-base --name "我的内容中台"
```

自动创建 Base + 三张表，并把 token / table_id 回填进 `config.json`。跑完给你一个飞书链接。

### 5. 日常使用

```bash
# ① 把灵感存进 inbox/ 文件夹（txt/md，格式随意）

# ② 扫描待处理内容
python -m ideainbox scan

# ③ 让 AI 读扫描结果，提炼成 records JSON（见下方「AI 提炼」）

# ④ 写入飞书
python -m ideainbox push --table research --input out/research.json
python -m ideainbox push --table content  --input out/content.json

# ⑤ 归档已处理文件
python -m ideainbox archive --files 你的文件名.txt
```

---

## 🧠 AI 提炼这一步怎么做

`scan` 会输出待处理内容的 JSON。把它连同下面的提示词发给任意 AI：

<details>
<summary>点开：提炼提示词模板</summary>

```
下面是我随手记的灵感/和AI的聊天。请你：
1. 判断里面有几个值得做的选题（一段内容可能含多个，也可能都不值得——太碎就跳过并说明，不要硬凑）。
2. 保持我的风格：结论先行、抓"预期差"、带反方观点、不落身份刻板印象、锋利但克制。
3. 每个选题产出两部分，分别对应飞书两张表的字段顺序，输出为 push 能用的 JSON：

研究素材（research.json）：
{"fields":["研究主题","核心判断","证据","来源","来源链接","来源等级","反方观点","研究日期"],
 "rows":[[...]]}

内容成品（content.json）：
{"fields":["选题","核心钩子","抖音30秒","抖音90秒","小红书标题","小红书正文","封面文案","关联研究","状态","日期"],
 "rows":[[...]]}

规则：不编造证据/数据/来源链接，原文没有就留空；信息不足以写完整脚本时，先写选题+钩子+核心判断，脚本字段留空；状态填"待制作"，日期填今天。
```
</details>

> 如果你用的是**支持定时任务的 AI 助手**，可以让它每天自动跑完整个流程（scan → 提炼 → push → archive），真正全自动。见 [docs/automation.md](./docs/automation.md)。

---

## 📋 命令一览

| 命令 | 作用 |
|---|---|
| `python -m ideainbox setup-base` | 一键建 Base + 三张表 |
| `python -m ideainbox scan` | 扫描灵感文件箱，输出待处理内容 |
| `python -m ideainbox push --table <research/content/review> --input x.json` | 写入某张表（自动去重） |
| `python -m ideainbox archive --files a.txt b.md` | 归档已入库文件到 processed/ |

---

## ⚙️ 自定义

- **人设 / 风格**：`config/config.json` 的 `persona`
- **表字段**：`config/tables.json`（改字段后需与提炼 JSON 对应）
- **投递箱位置**：`config/config.json` 的 `inbox_dir`

---

## 📁 项目结构

```
idea-inbox-feishu/
├── ideainbox/            # 核心包（纯标准库）
│   ├── __main__.py       #   CLI: setup-base/scan/push/archive
│   ├── config.py         #   配置加载
│   ├── scanner.py        #   扫描/归档
│   ├── feishu.py         #   飞书 lark-cli 封装
│   └── setup_base.py     #   一键建表
├── config/
│   ├── config.example.json  # 配置模板（复制成 config.json）
│   └── tables.json          # 三张表字段定义
├── inbox/                # 灵感投递箱（内容不进 git）
├── docs/                 # 详细文档
└── README.md
```

---

## ❓ FAQ

**Q：为什么不做成"聊完自动抓取"，还要我手动丢文件？**
因为你和 AI 的对话在对方平台的"围墙花园"里，外部程序无权自动读取。把对话"交出来"这一步只能你做 —— 本工具把它压缩到最小：**复制粘贴进一个文件夹**，其余全自动。

**Q：一定要用飞书吗？**
写入目标是飞书多维表格（它的状态流转 / 筛选 / 三表关联很适合内容管理）。但 `feishu.py` 是独立模块，欢迎 PR 适配 Notion / Airtable 等。

**Q：我的灵感隐私安全吗？**
`inbox/` 里的内容和 `config.json`（含 token）都已被 `.gitignore` 忽略，不会提交到仓库。

**Q：AI 会瞎编吗？**
提示词已明确要求"不编造证据/数据/来源，没有就留空"。提炼保留你的判断风格，不注水。

---

## 🤝 贡献

欢迎 PR：其他输出后端（Notion 等）、更多提炼模板、多语言。见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📜 License

[MIT](./LICENSE)
