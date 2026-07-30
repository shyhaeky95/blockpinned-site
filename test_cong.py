#!/usr/bin/env python3
"""Ép cả 5 cổng của build.py NỔ — vì một cổng chưa từng fail thì chưa phải cổng.

`luật bằng chứng của desk §2`: *"cấu hình nào của thế giới sẽ làm nó NỔ?
Không có ⇒ đừng gọi nó là control. Nó là kiểm tra chính tả."*

Mỗi ca: chép site sang thư mục tạm → bẻ ĐÚNG MỘT thứ → build phải chết, và phải
chết vì ĐÚNG lý do đó (khớp chuỗi), không phải vì một lỗi tình cờ nào khác.
Control âm: bản chưa bẻ phải PASS — nếu nó cũng fail thì mọi ca dương vô nghĩa.

Chạy:  python3 site/test_cong.py
"""
import json, pathlib, re, shutil, subprocess, sys, tempfile

SITE = pathlib.Path(__file__).parent
MD = "content/posts/2026-07-27-defillama-uniswap-v4.md"
CJ = "content/posts/2026-07-27-defillama-uniswap-v4.claims.json"


def sua_md(root, fn):
    p = root / "site" / MD
    p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")


def sua_claims(root, fn):
    p = root / "site" / CJ
    d = json.loads(p.read_text(encoding="utf-8"))
    fn(d["claims"])
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


CA = [
    ("control âm — không bẻ gì", None, None),
    ("① NGÔN NGỮ · từ đã khai tử",
     lambda r: sua_md(r, lambda s: s.replace("Tự kiểm, không cần tin tôi",
                                             "Biên lai, không cần tin tôi")),
     "TỪ ĐÃ KHAI TỬ"),
    ("① NGÔN NGỮ · từ nghề repo",
     lambda r: sua_md(r, lambda s: s.replace("Bốn chỗ nó có thể sai",
                                             "Trần của phép tách đó")),
     "TỪ NGHỀ REPO"),
    ("② CẤU TRÚC · mất mục tự kiểm",
     lambda r: sua_md(r, lambda s: s.replace("## Tự kiểm, không cần tin tôi",
                                             "## Vài đường dẫn")),
     "thiếu CÁCH TỰ KIỂM"),
    ("② CẤU TRÚC · mất disclaimer",
     lambda r: sua_md(r, lambda s: s.replace("Không phải lời khuyên đầu tư.", "")),
     "thiếu DISCLAIMER"),
    ("② CẤU TRÚC · block ghim không có số block",
     lambda r: sua_md(r, lambda s: re.sub(r"^ghim: .*$", "ghim: Robinhood chain, hôm kia",
                                          s, count=1, flags=re.M)),
     "thiếu SỐ KÈM BLOCK"),
    ("③ CLAIM · falsifier bị cắt  ← ĐÚNG LỖI LAUNCH §6c",
     lambda r: sua_claims(r, lambda cs: cs[0].update(falsifier="")),
     "thiếu ĐIỀU BÁC BỎ"),
    ("③ CLAIM · lách bằng falsifier rỗng nghĩa",
     lambda r: sua_claims(r, lambda cs: cs[0].update(falsifier="n/a")),
     "thiếu ĐIỀU BÁC BỎ"),
    ("③ CLAIM · trạng thái tự chế",
     lambda r: sua_claims(r, lambda cs: cs[1].update(status="CHẮC ĐÚNG")),
     "trạng thái không hợp lệ"),
    ("③ CLAIM · mất block ghim",
     lambda r: sua_claims(r, lambda cs: cs[2].update(ghim="")),
     "thiếu block/mốc ghim"),
    ("③ CLAIM · nhật ký rỗng",
     lambda r: sua_claims(r, lambda cs: cs[0].update(log=[])),
     "ít nhất một dòng nhật ký"),
    ("④ NGÔI XƯNG · 'chúng tôi'",
     lambda r: sua_md(r, lambda s: s.replace("Tôi mở issue báo họ", "Chúng tôi mở issue báo họ")),
     "chúng tôi"),
    ("⑤ MARKDOWN · cú pháp ngoài tập con (blockquote)",
     lambda r: sua_md(r, lambda s: s.replace("Không phải lời khuyên đầu tư.",
                                             "> Không phải lời khuyên đầu tư.")),
     "không nằm trong tập con"),
    ("⑤ MARKDOWN · ** không đóng",
     lambda r: sua_md(r, lambda s: s.replace("**$5,01M**", "**$5,01M")),
     "còn sót **"),
    ("⑤ MARKDOWN · khối ``` không đóng",
     lambda r: sua_md(r, lambda s: s.replace('"\n```\n\n4. **Đếm tận gốc:**',
                                             '"\n\n4. **Đếm tận gốc:**')),
     "không đóng"),
]


def main():
    dat = sai = 0
    for ten, be, mong in CA:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            shutil.copytree(SITE, root / "site")
            # check_language.py nằm ở ../template trong kho gốc, và NGAY CẠNH
            # build.py trong repo mirror công khai. Neo cứng một chỗ thì bộ thử
            # chỉ chạy được ở kho gốc — nghĩa là bản công khai đi ra mà không
            # cổng nào từng bị ép. Lỗi lộ đúng lần đầu chạy test từ trong mirror.
            lang = next(p / "check_language.py"
                        for p in (SITE.parent / "template", SITE)
                        if (p / "check_language.py").exists())
            (root / "template").mkdir()
            shutil.copy(lang, root / "template")
            shutil.copy(lang, root / "site")
            if be:
                be(root)
            r = subprocess.run([sys.executable, str(root / "site" / "build.py")],
                               capture_output=True, text=True)
            ra = (r.stdout or "") + (r.stderr or "")
            if mong is None:
                ok = r.returncode == 0
                note = "PASS như kỳ vọng" if ok else f"LẼ RA PHẢI PASS — {ra.strip()[-160:]}"
            else:
                ok = r.returncode != 0 and mong in ra
                note = ("chặn đúng lý do" if ok else
                        ("KHÔNG CHẶN — cổng thủng" if r.returncode == 0
                         else f"chặn SAI lý do: {ra.strip()[-120:]}"))
            print(f"  {'✓' if ok else '✗'}  {ten:<52} {note}")
            dat += ok; sai += not ok
    print(f"\n{'✅' if not sai else '🔴'} {dat}/{len(CA)} ca đúng"
          + ("" if not sai else f" · {sai} ca SAI — có cổng không nổ được"))
    sys.exit(1 if sai else 0)


if __name__ == "__main__":
    main()
