# 🚀 快速上手（新手向）

不懂命令行也没关系。这份指南教你用**最省事**的方式跑起来。

---

## 先搞懂一件事：你需要一个「AI Agent」

这个工具本身**不含 AI**，它需要一个 **AI Agent** 来帮你「提炼灵感」和「跑流程」。

**什么是 AI Agent？** 就是那种能帮你读文件、敲命令、自己跑完一连串操作的 AI 工具，比如：

- **WorkBuddy 自动化**
- **Codex**
- **Claude Code**
- **Cursor / Cline**

普通网页版 ChatGPT 不行 —— 它只能陪你聊天，不能自己动手操作你的电脑。

---

## 最简路径：让 Agent 帮你做

如果你有上面任意一个 AI Agent，**这是最快的方式**：

> 把下面这句话（连同本仓库链接）发给你的 AI Agent：

```
帮我把这个项目 clone 到本地并按 README 跑通：
https://github.com/wangxianda941030/idea-inbox-feishu

我要用它把我和 AI 聊出的灵感自动整理进飞书多维表格。
请依次帮我：
1. clone 项目
2. 指导我安装并授权飞书 CLI（需要我在浏览器操作的步骤请告诉我）
3. 运行 setup-base 建好飞书表
4. 以后我把灵感文件丢进 inbox/，你帮我 scan → 提炼 → push → archive
```

Agent 会一步步带你做，需要你在浏览器点授权的地方，它会提示你。

---

## 你唯一必须亲自做的事

无论用哪个 Agent，有**一件事只能你本人做**：

### 授权飞书（把写表权限给工具）

因为要写进**你自己的**飞书表，需要你登录授权一次：

1. 装飞书 CLI：`npm install -g @larksuite/cli`（需要先装 [Node.js](https://nodejs.org/)）
2. `lark-cli config init --new` → 浏览器里建个飞书应用
3. `lark-cli auth login --recommend` → 浏览器里授权，**记得勾选多维表格权限**

详细图文见 [docs/feishu-setup.md](./docs/feishu-setup.md)。这步做完，Agent 就能帮你把选题写进飞书了。

---

## 日常怎么用（配置好之后）

1. 和 AI 聊出好想法 → 复制，存成 txt/md 丢进 `inbox/` 文件夹（格式随意）
2. 跟你的 Agent 说一句：「处理一下灵感投递箱」
3. 打开飞书，选题已经整理好躺在表里了 ✅

就这么简单。你只负责「产生想法 + 丢进文件夹」，其余交给 Agent。

---

## 常见疑问

**Q：我要不要花钱买 API？**
用 Agent 手动跑 —— **不用**，Agent 自己会提炼。只有你想做成"每天定时全自动、完全不管"，才需要自己接一个 LLM API（见 [docs/automation.md](./docs/automation.md)）。

**Q：我的灵感会不会被传到 GitHub？**
不会。`inbox/` 里的内容和你的飞书 token 都被 `.gitignore` 保护，只留在你自己电脑上。

**Q：一定要用飞书吗？**
默认写飞书。想换 Notion / Excel，可以让 Agent 帮你改，或看 [CONTRIBUTING.md](./CONTRIBUTING.md)。
