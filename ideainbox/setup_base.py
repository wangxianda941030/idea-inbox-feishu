"""一键创建飞书内容中台 Base + 三张表，回填 config.json。

用法: python -m ideainbox setup-base [--name 浪人Banks内容研究中台]
"""
from . import feishu
from .config import load_config, save_config, load_tables


def run(name="内容研究中台"):
    cfg = load_config()
    tables = load_tables()

    print("检查 lark-cli 授权 ...")
    feishu.check_auth()

    print(f"创建 Base「{name}」 ...")
    base_token, url = feishu.create_base(name)
    print(f"  base_token = {base_token}")
    print(f"  url        = {url}")

    ids = {}
    for key in ("research", "content", "review"):
        spec = tables[key]
        tid = feishu.create_table(base_token, spec["name"], spec["fields"])
        ids[key] = tid
        print(f"  建表 {spec['name']} -> {tid}")

    # 删掉 base 自带的默认空表
    try:
        for t in feishu.list_tables(base_token):
            if t["name"] == "数据表":
                feishu.delete_table(base_token, t["id"])
                print("  已删除默认空表")
    except Exception:
        pass

    cfg["feishu"]["base_token"] = base_token
    cfg["feishu"]["base_url"] = url
    for key in ids:
        cfg["feishu"]["tables"][key]["table_id"] = ids[key]
    save_config(cfg)
    print(f"\n完成！已回填 config.json。Base 链接：{url}")
    return base_token, ids, url
