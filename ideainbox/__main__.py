"""ideainbox 命令行入口。

设计：提炼灵感→选题这一步需要"读懂内容"，交给 AI 完成；本 CLI 负责机械环节。

子命令：
  setup-base   一键创建飞书 Base + 三张表（首次用）
  scan         扫描灵感文件箱，输出待处理内容（JSON，交给 AI 提炼）
  push         把 AI 产出的 records JSON 写入指定表（自动去重）
  archive      把已入库的灵感文件归档到 processed/

典型流程（人 + AI 协作）：
  1. python -m ideainbox scan            # 得到待处理内容
  2. （AI 读内容，提炼成 research/content 的 records JSON）
  3. python -m ideainbox push --table research --input out/research.json
     python -m ideainbox push --table content  --input out/content.json
  4. python -m ideainbox archive --files 已处理的文件名
"""
import argparse
import json
import os
import sys

from . import scanner, feishu
from .config import load_config, load_tables, resolve_inbox, ROOT


def cmd_setup_base(args):
    from . import setup_base
    setup_base.run(name=args.name)


def cmd_scan(args):
    cfg = load_config()
    inbox = resolve_inbox(cfg)
    items = scanner.scan(inbox)
    print(json.dumps({"inbox": inbox, "count": len(items), "items": items},
                     ensure_ascii=False, indent=2))


def cmd_push(args):
    cfg = load_config()
    fs = cfg["feishu"]
    if not fs.get("base_token"):
        sys.exit("config.json 缺 base_token，请先运行 setup-base。")
    tbl = fs["tables"].get(args.table)
    if not tbl or not tbl.get("table_id"):
        sys.exit(f"未找到表 '{args.table}' 的 table_id，检查 config.json。")

    with open(args.input, "r", encoding="utf-8") as f:
        batch = json.load(f)
    fields, rows = batch["fields"], batch["rows"]

    # 去重：按第一个文本字段（通常是标题/研究主题/选题）
    if not args.no_dedup:
        existing = feishu.existing_titles(fs["base_token"], tbl["table_id"])
        def dup(r):
            key = str(r[0])
            return any(key[:12] in e or e[:12] in key for e in existing)
        new_rows = [r for r in rows if not dup(r)]
        skipped = len(rows) - len(new_rows)
    else:
        new_rows, skipped = rows, 0

    if not new_rows:
        print(f"无新记录可写（去重跳过 {skipped}）。")
        return

    outdir = os.path.join(ROOT, "out")
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, f"_push_{args.table}.json")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"fields": fields, "rows": new_rows}, f, ensure_ascii=False, indent=2)
    n = feishu.batch_create(fs["base_token"], tbl["table_id"], os.path.relpath(tmp))
    print(f"[{args.table}] 写入 {n} 条（去重跳过 {skipped}）。")


def cmd_archive(args):
    cfg = load_config()
    inbox = resolve_inbox(cfg)
    moved = scanner.archive(inbox, args.files)
    print(f"已归档 {len(moved)} 个：{', '.join(moved) if moved else '（无）'}")


def main():
    ap = argparse.ArgumentParser(prog="ideainbox", description="灵感投递箱 → 飞书内容中台")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("setup-base", help="一键建 Base + 三表")
    p.add_argument("--name", default="内容研究中台")
    p.set_defaults(func=cmd_setup_base)

    p = sub.add_parser("scan", help="扫描灵感文件箱")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("push", help="把 records JSON 写入某张表")
    p.add_argument("--table", required=True, choices=["research", "content", "review"])
    p.add_argument("--input", required=True)
    p.add_argument("--no-dedup", action="store_true")
    p.set_defaults(func=cmd_push)

    p = sub.add_parser("archive", help="归档已入库文件")
    p.add_argument("--files", nargs="+", required=True)
    p.set_defaults(func=cmd_archive)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
