"""灵感文件箱扫描与归档。不要求任何格式，任意文本都能读。"""
import datetime as dt
import os
import shutil

READABLE_EXT = (".txt", ".md", ".markdown", ".text", "")
PROCESSED = "processed"


def _read(path):
    for enc in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except Exception:
            continue
    return ""


def scan(inbox):
    """返回未处理文件 [{name, content}]。"""
    out = []
    if not os.path.isdir(inbox):
        return out
    for name in sorted(os.listdir(inbox)):
        path = os.path.join(inbox, name)
        if not os.path.isfile(path):
            continue
        if os.path.splitext(name)[1].lower() not in READABLE_EXT:
            continue
        content = _read(path).strip()
        if content:
            out.append({"name": name, "content": content})
    return out


def archive(inbox, names):
    """把已入库文件移到 processed/（带时间戳，不覆盖）。返回已移动的文件名。"""
    proc = os.path.join(inbox, PROCESSED)
    os.makedirs(proc, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    moved = []
    for name in names:
        src = os.path.join(inbox, name)
        if not os.path.isfile(src):
            continue
        base, ext = os.path.splitext(name)
        shutil.move(src, os.path.join(proc, f"{base}__{stamp}{ext}"))
        moved.append(name)
    return moved
