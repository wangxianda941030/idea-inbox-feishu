"""飞书多维表格封装（基于官方 lark-cli 命令行）。

鉴权完全交给 lark-cli，本模块只用 subprocess 调用，不直接碰 token。
安装与授权见 docs/feishu-setup.md。
"""
import json
import subprocess


def _run(args):
    cmd = ["lark-cli"] + args + ["--as", "user", "--format", "json"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    out = (p.stdout or "").strip()
    try:
        data = json.loads(out)
    except Exception:
        raise RuntimeError(f"lark-cli 输出无法解析: {out[:300]} | stderr: {p.stderr[:200]}")
    if not data.get("ok", False):
        e = data.get("error", {})
        raise RuntimeError(f"lark-cli 报错: {e.get('type')}/{e.get('subtype')} - {e.get('message')}")
    return data


def check_auth():
    try:
        p = subprocess.run(["lark-cli", "auth", "status"],
                           capture_output=True, text=True, encoding="utf-8")
        return p.returncode == 0
    except FileNotFoundError:
        raise RuntimeError("未找到 lark-cli，请先安装：npm install -g @larksuite/cli")


def create_base(name, time_zone="Asia/Shanghai"):
    d = _run(["base", "+base-create", "--name", name, "--time-zone", time_zone])
    b = d["data"]["base"]
    return b["base_token"], b["url"]


def create_table(base_token, name, fields):
    """用 table-create 一次性建表+字段。返回 table_id。"""
    d = _run(["base", "+table-create", "--base-token", base_token,
              "--name", name, "--fields", json.dumps(fields, ensure_ascii=False)])
    data = d.get("data", {})
    # 兼容不同返回结构
    return (data.get("table_id") or data.get("table", {}).get("table_id")
            or data.get("table", {}).get("id"))


def list_tables(base_token):
    d = _run(["base", "+table-list", "--base-token", base_token])
    return d["data"]["tables"]


def delete_table(base_token, table_id):
    return _run(["base", "+table-delete", "--base-token", base_token,
                 "--table-id", table_id, "--yes"])


def batch_create(base_token, table_id, batch_relpath):
    d = _run(["base", "+record-batch-create", "--base-token", base_token,
              "--table-id", table_id, "--json", f"@{batch_relpath}"])
    return len(d["data"].get("data", []))


def existing_titles(base_token, table_id, limit=200):
    """读表内已有记录的长文本单元，用于去重。"""
    d = _run(["base", "+record-list", "--base-token", base_token,
              "--table-id", table_id, "--limit", str(limit)])
    rows = d["data"].get("data", [])
    titles = []
    for r in rows:
        cand = [x for x in r if isinstance(x, str) and len(x) > 6]
        if cand:
            titles.append(cand[0])
    return titles
