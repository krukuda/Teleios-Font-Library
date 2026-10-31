"""ساخت index.json کتابخانه‌ی فونت Teleios از روی fonts/<id>/meta.json.

اجرا (از ریشه‌ی Repository):   python tools/build_index.py
پیش‌نیاز: pip install fonttools

برای هر فونت:
  - هر فایل از نظر sha256 و «نام libass» (nameID 1 جدول name) خوانده می‌شه؛ نام خانواده‌ی نوشته‌شده در meta باید با nameID 1 یا 16 بخونه.
  - مسیرها نسبی به ریشه‌ی Repository هستن؛ ربات آن‌ها را نسبت به آدرس index.json حساب می‌کنه.
  - فایل License هم هش می‌شه. اگه meta «license_file» نداشته باشه (فونت کاربر با تأیید انتشار)، License فایل ندارد و فیلدهایش خالی می‌مونه.
خروجی: index.json (بدون زمان‌بندی تصادفی؛ اگه فایلی تغییر نکنه، خروجی بایت‌به‌بایت یکی می‌مونه)."""
import hashlib
import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = 1


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def names(p: Path) -> tuple:
    f = TTFont(str(p))
    n = f["name"]
    return (n.getDebugName(1) or "", n.getDebugName(16) or n.getDebugName(1) or "",
            bool(f["OS/2"].fsSelection & 0x20))


def build() -> dict:
    fonts = []
    for meta_p in sorted((ROOT / "fonts").glob("*/meta.json")):
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        d = meta_p.parent
        if meta.get("license_file"):
            lic = ROOT / meta["license_file"]
            if not lic.is_file():
                sys.exit(f"{meta['family']}: فایل License پیدا نشد: {meta['license_file']}")
            lic_path, lic_sha = meta["license_file"], sha256(lic)
        else:  # فونت کاربر: مالکیت/حق انتشار را کاربر در Mini App تأیید کرده؛ متن License همراه نیست
            lic_path, lic_sha = "", ""
        weights = {}
        for w, wm in sorted(meta["weights"].items(), key=lambda kv: int(kv[0])):
            rel = f"{d.relative_to(ROOT).as_posix()}/{wm['file']}"
            p = ROOT / rel
            if not p.is_file():
                sys.exit(f"فایل نیست: {rel}")
            n1, n16, bold_bit = names(p)
            if meta["family"] not in (n1, n16) and not n1.startswith(meta["family"]):
                sys.exit(f"{rel}: نام خانواده‌ی «{meta['family']}» با جدول name نمی‌خونه ({n1!r})")
            weights[str(int(w))] = {
                "path": rel, "sha256": sha256(p), "libass": n1,
                "bold": bool(wm.get("bold", bold_bit)),
            }
        fonts.append({
            "family": meta["family"], "label": meta["label"], "langs": meta["langs"],
            "license": meta["license"], "license_path": lic_path,
            "license_sha256": lic_sha, "version": meta["version"], "source": meta["source"],
            "weights": weights,
        })
    return {"v": SCHEMA, "fonts": fonts}


if __name__ == "__main__":
    out = ROOT / "index.json"
    out.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("written", out)
