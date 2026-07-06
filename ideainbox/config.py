"""配置与路径。"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
CONFIG_EXAMPLE = os.path.join(CONFIG_DIR, "config.example.json")
TABLES_PATH = os.path.join(CONFIG_DIR, "tables.json")


def _strip(obj):
    if isinstance(obj, dict):
        return {k: _strip(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [_strip(x) for x in obj]
    return obj


def load_config():
    path = CONFIG_PATH if os.path.exists(CONFIG_PATH) else CONFIG_EXAMPLE
    with open(path, "r", encoding="utf-8") as f:
        cfg = _strip(json.load(f))
    cfg["_path"] = path
    cfg["_using_example"] = (path == CONFIG_EXAMPLE)
    return cfg


def save_config(cfg):
    clean = {k: v for k, v in cfg.items() if not k.startswith("_")}
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)


def load_tables():
    with open(TABLES_PATH, "r", encoding="utf-8") as f:
        return _strip(json.load(f))


def resolve_inbox(cfg):
    d = cfg.get("inbox_dir", "./inbox")
    if not os.path.isabs(d):
        d = os.path.join(ROOT, d)
    return os.path.abspath(d)
