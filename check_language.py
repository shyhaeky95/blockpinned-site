#!/usr/bin/env python3
"""Cổng NGÔN NGỮ — chạy trước mỗi lần đăng.

Vì sao có: quyết định về ngôn ngữ công khai được ghi ở tài liệu kế hoạch của desk,
nhưng chữ THI HÀNH nằm ở kho này. Không cổng nào bắc cầu hai kho ⇒ 27/07 quyết định
bỏ một từ chỉ lan được đúng một nửa (banner đổi, khuôn card không), sống 9 tiếng.

Bắt hai loại:
  ① TỪ ĐÃ KHAI TỬ  — bỏ khỏi ngôn ngữ công khai VN, có ngày + lý do
  ② TỪ NGHỀ CỦA REPO — chính xác trong nhà, là tiếng lóng nội bộ khi ra ngoài (LAUNCH §6b.4)

Chạy:  python3 template/check_language.py        → quét mặc định
       python3 template/check_language.py <file> → quét file cụ thể
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent

# ── ① từ đã khai tử: (mẫu, thay bằng, ngày+lý do) ────────────────────────────
RETIRED = [
    (r"biên lai", "truy ngược / ghim block / tự kiểm",
     "27/07 — 'receipt' là slang mạnh ở CT tiếng Anh, 'biên lai' tiếng Việt nghe như hoá đơn"),
    (r"\bnấc\b|bậc gãy", "cú tụt",
     "27/07 — chữ TỰ BỊA, không phải tiếng Việt có sẵn; bỏ ở 3dff3da TRƯỚC khi bài #1 đăng. "
     "Thêm vào danh sách 28/07 sau khi nó QUAY LẠI trong một bản viết lại và suýt thành "
     "TRÍCH SAI nguyên văn bài #1 — đúng lỗ LAUNCH §7:144: bộ lọc chỉ biết từ đã có trong danh sách"),
]

# ── ② từ nghề của repo, không mang ra ngoài (LAUNCH §6b.4) ───────────────────
JARGON = [
    (r"\btrần của\b", "nói thẳng giới hạn là gì"),
    (r"\bcửa sổ đọc\b", "'số đọc đến ngày …'"),
    (r"\bcận dưới\b", "'ít nhất là …'"),
    (r"\bđăng ký trước\b", "'ghi trước'"),
    (r"\bfan-out\b", "—"),
    (r"\bwrite-set\b", "—"),
    (r"\bpositive control\b", "—"),
]

# quét cái ĐI RA NGOÀI, không quét hồ sơ nội bộ
TARGETS = ["drafts/*.md", "template/out/*.txt", "template/out/*.html"]
# file sinh chữ công khai — bỏ qua dòng comment (đó là hồ sơ ghi lý do, phải giữ)
GENERATORS = ["template/build_cards.py", "template/build_post01.py",
              "template/assets_profile.py", "template/variants_tone.py"]


def scan(path: pathlib.Path, skip_comments: bool, jargon: bool = True):
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if skip_comments and line.lstrip().startswith("#"):
            continue
        for pat, fix, why in RETIRED:
            if re.search(pat, line, re.I):
                out.append(("🔴 TỪ ĐÃ KHAI TỬ", i, pat, fix, why, line.strip()[:80]))
        if not jargon:
            continue
        for pat, fix in JARGON:
            if re.search(pat, line, re.I):
                out.append(("🟡 từ nghề repo", i, pat, fix, "LAUNCH §6b.4", line.strip()[:80]))
    return out


def main():
    files = ([pathlib.Path(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else
             [p for g in TARGETS for p in ROOT.glob(g)] +
             [ROOT / g for g in GENERATORS])
    hard = soft = 0
    for p in files:
        if not p.exists():
            continue
        gen = str(p).endswith(".py")
        # draft lẫn ghi chú nội bộ ⇒ chỉ soi TỪ ĐÃ KHAI TỬ; từ nghề chỉ soi bản xuất
        pure = "template/out/" in str(p)
        for kind, ln, pat, fix, why, txt in scan(p, skip_comments=gen, jargon=pure):
            if kind.startswith("🔴"):
                hard += 1
            else:
                soft += 1
            try: shown = p.relative_to(ROOT)
            except ValueError: shown = p
            print(f"{kind}  {shown}:{ln}\n"
                  f"    khớp : {pat}\n    thay : {fix}\n    vì   : {why}\n    dòng : {txt}\n")
    n = len([p for p in files if p.exists()])
    print(f"quét {n} file · 🔴 {hard} từ đã khai tử · 🟡 {soft} từ nghề repo")
    if hard:
        sys.exit("\n🔴 CÓ TỪ ĐÃ KHAI TỬ — không đăng cho tới khi sửa.")
    if soft:
        print("\n🟡 Từ nghề không chặn đăng, nhưng cân nhắc: người ngoài không đọc được.")
    else:
        print("✅ sạch")


if __name__ == "__main__":
    main()
