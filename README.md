# Teleios Font Library

کتابخانه‌ی عمومی فونت‌های ربات Teleios برای Hard Sub. ربات و Mini App فهرست فونت‌ها را از `index.json` این Repository می‌خوانند؛ هیچ فونتی داخل کد Notebook ثبت نمی‌شود.

## ساختار

```
index.json                 فهرست تولیدشده (نباید دستی ویرایش شود؛ با tools/build_index.py ساخته می‌شود)
tools/build_index.py       ساخت index.json از روی meta.json هر فونت
fonts/<id>/meta.json       مشخصات فونت: خانواده، برچسب، زبان‌ها، License، نسخه، منبع، وزن‌ها
fonts/<id>/LICENSE.txt     متن کامل License همان فونت (الزامی)
fonts/<id>/*.ttf           فایل‌های فونت
```

فونت‌های فعلی:

| شناسه | خانواده | نسخه | License | وزن‌ها |
|---|---|---|---|---|
| `vazirmatn` | Vazirmatn | v33.003 (از https://github.com/rastikerdar/vazirmatn/tree/v33.003) | SIL OFL 1.1 | 100 تا 900 (۹ وزن) |
| `dejavu-sans` | DejaVu Sans | 2.37 (بسته‌ی fonts-dejavu-core) | Bitstream Vera License؛ تغییرات DejaVu عمومی | 200، 400، 700 |

## افزودن فونت جدید (بدون تغییر کد ربات یا Notebook)

1. پوشه‌ی `fonts/<id>/` را بساز (شناسه‌ی کوچک انگلیسی، مثلاً `my-font`).
2. فایل‌های `.ttf`/`.otf` و متن کامل License را داخلش بگذار. License بدون متن کامل پذیرفته نمی‌شود.
3. `meta.json` بنویس؛ `weights` کلیدهای عددی ۱۰۰ تا ۹۰۰ (مضرب ۱۰۰) دارد و هر کدام `file` دارد. اگر وزن ضخیم است `"bold": true` بگذار.
4. `python tools/build_index.py` را اجرا کن (نیاز به `fonttools`). اسکریپت هش SHA-256 و نام libass هر فایل را می‌خواند و اگر نام خانواده با جدول name نخواند، خطا می‌دهد.
5. `fonts/<id>/`، `index.json` را commit کن.

ربات در فاصله‌ی بررسی کاتالوگ (پیش‌فرض هر ۶ ساعت) فونت جدید را می‌بیند و Mini App از همان فهرست نمایش می‌دهد.

## قوانین

- فقط فونت‌هایی که License انتشار مجدد دارند. فونت‌های معمولی باید فایل License کامل خودشان را داشته باشند.
- فونت‌های کاربر (`fonts/user-<hash>/`) فقط با تیک تأیید صریح کاربر در Mini App اضافه می‌شوند؛ کاربر مالکیت یا حق انتشار را تأیید کرده و متن License همراه ندارد. این فونت‌ها دائمی‌اند و حذف کامل آن‌ها از تاریخچه‌ی Git ممکن نیست.
- **فونت‌های Embedded زیرنویس کاربران هرگز نباید در این Repository قرار بگیرند.** این فایل‌ها متعلق به کاربرند و انتشارشان فقط با تأیید صریح جداگانه ممکن است؛ این Repository فعلاً هیچ مسیر ورودی برای آن ندارد.
- هیچ توکن یا Secret در این Repository نگذار.
- `index.json` هش SHA-256 هر فایل را دارد؛ ربات فایلی را که هشش نخواند استفاده نمی‌کند.

## نحوه‌ی مصرف توسط ربات

- ربات `FONT_CATALOG_URL` را به آدرس raw این `index.json` می‌گیرد، مثلاً `https://raw.githubusercontent.com/<owner>/Teleios-Font-Library/main/index.json`.
- مسیرهای `path` نسبت به همین آدرس حساب می‌شوند؛ با تغییر نام Repository فقط `FONT_CATALOG_URL` عوض می‌شود.
- نتیجه‌ی دانلود در کش دیسک با کلید SHA-256 ذخیره می‌شود؛ اگر GitHub در دسترس نباشد، آخرین کش معتبر استفاده می‌شود.
- هیچ توکنی برای خواندن لازم نیست (Repository عمومی است).
