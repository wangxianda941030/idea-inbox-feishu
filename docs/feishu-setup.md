# 飞书 CLI 安装与授权

本项目通过官方 **飞书 CLI（lark-cli）** 写入多维表格，鉴权完全交给它，本项目不碰你的密钥。

## 1. 安装

需要先有 [Node.js](https://nodejs.org/)（含 npm）。

```bash
npm install -g @larksuite/cli
lark-cli --version   # 出现版本号即安装成功
```

## 2. 创建飞书应用（配置凭证）

```bash
lark-cli config init --new
```

- 命令会输出一个链接（和一个二维码）。**在浏览器打开**，登录飞书，按引导**创建一个自建应用**（名字随意，如「内容中台助手」），确认授权。
- 完成后终端会显示 `应用配置成功! App ID: cli_xxx`。

## 3. 登录授权

```bash
lark-cli auth login --recommend
```

- 同样会给一个授权链接 / 二维码，浏览器打开或飞书扫码。
- 授权时**务必勾选多维表格相关权限**（base:app、base:table、base:field、base:record 的读写）。
- 成功后显示 `授权成功! 用户: <你的名字>`。

## 4. 验证

```bash
lark-cli auth status
```

能看到你的账号和已授予的 scopes 即可。

## 常见问题

- **子命令报 `unknown subcommand`**：base 的子命令要带 `+` 前缀，如 `lark-cli base +table-list`。本项目已在代码里处理好。
- **写入报 `missing scope`**：授权时漏勾了权限，重新 `lark-cli auth login --scope "base:record:create ..."`。
- **授权链接失效**：device code 有时效（约 10 分钟），过期就重新执行登录命令。
- **想生成二维码**：`lark-cli auth qrcode "<授权URL>" --output qr.png`（URL 是位置参数，输出用相对路径）。

## 安全说明

- 凭证由 lark-cli 存在你本机的用户目录，**不在本项目仓库内**，不会被 git 提交。
- 本项目 `config.json`（含表 token）已被 `.gitignore` 忽略。
