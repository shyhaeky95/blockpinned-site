#!/usr/bin/env python3
"""Cổng NGÔN NGỮ — chạy trước mỗi lần đăng.

Vì sao có: quyết định về ngôn ngữ công khai được ghi ở tài liệu kế hoạch của desk,
nhưng chữ THI HÀNH nằm ở kho này. Không cổng nào bắc cầu hai kho ⇒ 27/07 quyết định
bỏ một từ chỉ lan được đúng một nửa (banner đổi, khuôn card không), sống 9 tiếng.

Bắt ba loại:
  ① TỪ ĐÃ KHAI TỬ  — bỏ khỏi ngôn ngữ công khai VN, có ngày + lý do
  ①b KẾT LUẬN ĐỊNH GIÁ — LAUNCH §6 cấm nhận định giá; chặn cùng mức với ①
  ② TỪ NGHỀ CỦA REPO — chính xác trong nhà, là tiếng lóng nội bộ khi ra ngoài (LAUNCH §6b.4)

Chạy:  python3 template/check_language.py        → quét mặc định
       python3 template/check_language.py <file> → quét file cụ thể
       python3 template/check_language.py --selftest → control dương, 0 phụ thuộc file ngoài
"""
import os, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent.parent

# ── ① từ đã khai tử: (mẫu, thay bằng, ngày+lý do) ────────────────────────────
RETIRED_TU = [
    (r"biên lai", "truy ngược / ghim block / tự kiểm",
     "27/07 — 'receipt' là slang mạnh ở CT tiếng Anh, 'biên lai' tiếng Việt nghe như hoá đơn"),
    (r"\bnấc\b|bậc gãy", "cú tụt",
     "27/07 — chữ TỰ BỊA, không phải tiếng Việt có sẵn; bỏ ở 3dff3da TRƯỚC khi bài #1 đăng. "
     "Thêm vào danh sách 28/07 sau khi nó QUAY LẠI trong một bản viết lại và suýt thành "
     "TRÍCH SAI nguyên văn bài #1 — đúng lỗ LAUNCH §7:144: bộ lọc chỉ biết từ đã có trong danh sách"),
]

# ── ①b KẾT LUẬN ĐỊNH GIÁ — user chốt 31/07 (`cau-hoi-nha-dau-tu.md` V1) ──────
#
# Luật: khuôn V1 cho phép đăng MẪU SỐ (doanh thu · cung · tỉ lệ · so ngang đối thủ
# cùng cửa sổ) và CẤM đăng KẾT LUẬN. Nguyên văn user: "ko cần kết luận đắt rẻ mua
# đc hay ko là đc". Nền: LAUNCH §6 "Không nhận định giá, không kèo".
#
# 🔴 RANH GIỚI CỦA CHÍNH DANH SÁCH NÀY — đọc trước khi thêm mẫu:
#   Cấm KẾT LUẬN VỀ TÀI SẢN, không cấm CHỮ. "chi phí rẻ" · "phí đắt" · "pool wash
#   rẻ" đều là mô tả CHI PHÍ và phải đi qua được. Vì vậy không có mẫu `\brẻ\b`
#   trần; mọi mẫu đều buộc chữ vào một vật định giá hoặc một hành vi giao dịch.
#   So sánh bằng SỐ vẫn hợp lệ: "tỉ lệ thấp hơn X" đi qua, "rẻ hơn X" thì không.
#
# 🔴 Đặt vào RETIRED (chặn cứng) chứ KHÔNG mở danh sách thứ ba: site/build.py:306
#   lặp thẳng `lang.RETIRED` và `lang.JARGON`. Một danh sách mới = một chỗ phải
#   nhớ nối tay ⇒ đúng lỗ mà docstring file này đang kể (27/07, luật lan nửa
#   đường, sống 9 tiếng). Hợp ở đây thì web + mirror công khai nhận tự động.
VALUATION = [
    (r"\b(?:đang|khá|quá|hơi|vẫn|còn|rất)\s+(?:rẻ|đắt)\b", "bỏ hẳn câu — hoặc chỉ để lại con số",
     "31/07 V1 — kết luận đắt/rẻ về tài sản"),
    # 🔴 Bản đầu là `\b(?:rẻ|đắt)\s+hơn\b` trần — selftest bắt DƯƠNG TÍNH GIẢ ngay
    # lượt chạy đầu: nó chặn "chi phí đọc log rẻ hơn một lệnh RPC". Cấm chữ, không
    # cấm kết luận. Nay buộc vế sau phải là một TÀI SẢN (ticker viết hoa) hoặc một
    # nhóm đối chiếu — đúng hình dạng của kết luận bị cấm: "X rẻ hơn Y".
    # 🟠 Còn hở, khai thẳng: "chi phí rẻ hơn RPC" vẫn nổ oan vì RPC viết hoa. Chấp
    # nhận — nổ oan tốn một lượt sửa câu, lọt thì ra kết luận định giá công khai.
    (r"\b(?:rẻ|đắt)\s+hơn\s+(?:[A-Z][A-Za-z0-9]{1,9}\b|đối thủ|các dự án|thị trường|peer|trung bình ngành)",
     "so bằng SỐ: 'tỉ lệ … thấp hơn/cao hơn …'",
     "31/07 V1 — so ngang được phép, nhưng bằng mẫu số chứ không bằng phán quyết"),
    (r"\b(?:token|coin|đồng|tài sản|cổ phiếu|mức giá|thị giá)\b[^.\n]{0,24}\b(?:rẻ|đắt)\b",
     "bỏ hẳn câu — hoặc chỉ để lại con số",
     "31/07 V1 — chữ đắt/rẻ buộc vào chính tài sản, dù không có 'đang/quá'"),
    (r"định giá\s+(?:thấp|cao|rẻ|đắt|hấp dẫn|quá|hợp lý)|bị\s+định giá", "chỉ đăng mẫu số",
     "31/07 V1 — 'định giá thấp' là kết luận, không phải phép đo"),
    (r"\bgiá\s+(?:mục tiêu|hời)\b|\bgiá trị (?:thật|nội tại)\b", "—",
     "31/07 V1 — giả định có một giá 'đúng' mà bài không đo được"),
    (r"\bunder\s?-?\s?valued\b|\bover\s?-?\s?valued\b|\bupside\b", "—",
     "31/07 V1 — bản EN của cùng kết luận"),
    (r"\b(?:nên|đáng|khuyến nghị)\s+(?:mua|bán|gom|nắm giữ|vào|thoát)\b", "—",
     "31/07 V1 — khuyến nghị giao dịch; LAUNCH §6 cấm tuyệt đối"),
    # 🔴 `gom hàng` ĐÃ BỎ khỏi mẫu này — lượt quét thật bắt nó ở `_skeleton-bai08.md:13`,
    # câu "UNI bị burn đến từ người đi gom hàng": mô tả người gom tài sản ra khỏi
    # TokenJar, không phải kèo. Đây là chữ tiếng Việt có nghĩa đen, không phải tiếng
    # lóng riêng của thị trường ⇒ cấm nó là cấm CHỮ, đúng thứ ranh giới trên bác.
    (r"\bmúc\b|\ball[-\s]?in\b|\bđu đỉnh\b|\bbắt đáy\b|\bvào lệnh\b", "—",
     "31/07 V1 — tiếng lóng kèo; cùng họ với khuyến nghị"),
    (r"\bcơ hội đầu tư\b|\bkênh đầu tư\b|\btiềm năng tăng giá\b", "—",
     "31/07 V1 — khung 'đây là cơ hội' là kết luận, kể cả khi không nói mua"),
]

# hợp hai nhóm — mọi bên tiêu thụ (site/build.py, test_cong.py, bản mirror công
# khai) lặp `RETIRED`, nên luật mới lan hết mà không phải nối tay chỗ nào
RETIRED = RETIRED_TU + VALUATION

# ── ② từ nghề của repo, không mang ra ngoài (LAUNCH §6b.4) ───────────────────
JARGON = [
    # 🔴 NỚI 30/07 — bản cũ `\btrần của\b` chỉ bắt đúng MỘT cách nói. Draft #27 v2
    # viết "mức trần" ba lần, cổng trả SẠCH, và người phản biện NGOÀI bắt được thứ
    # máy bỏ sót. Cùng lỗ đã ghi cho chữ `nấc` (LAUNCH §6d ô #5): bộ lọc chỉ biết
    # đúng chuỗi đã khai. `LAUNCH §6b.4` khai tử CHỮ "trần", không khai tử riêng
    # cụm "trần của". Quét từ-nghề chỉ chạy trên file ĐÃ EXPORT nên nới rộng không
    # làm ồn ghi chú nội bộ trong draft.
    (r"\btrần\b", "nói thẳng giới hạn: 'pool fee' · 'giới hạn của phép đo'"),
    (r"\bcửa sổ đọc\b", "'số đọc đến ngày …'"),
    (r"\bcận dưới\b", "'ít nhất là …'"),
    (r"\bđăng ký trước\b", "'ghi trước'"),
    (r"\bfan-out\b", "—"),
    (r"\bwrite-set\b", "—"),
    (r"\bpositive control\b", "—"),
]

# ── ③ thuật ngữ MÁY trong THÂN POST FACT — khuôn v2, brief §0b chốt 02/08 ────
# 🔴 KHÔNG nhập vào RETIRED/JARGON: hai danh sách đó cấm chữ trên MỌI mặt công
# khai, còn các mẫu dưới đây chỉ cấm ở đúng MỘT chỗ — thân post X của một Fact
# (chuẩn người đọc: người đầu tư chứng khoán chưa chạm crypto). Cùng chuỗi đó
# ở tầng reply (`## BẢN X REPLY`), ở bài dài, ở web /facts/ là HỢP LỆ — nhét
# vào RETIRED là cấm luôn lệnh tự kiểm ở nơi nó bắt buộc phải sống.
# Dùng chung bởi: template/export_post.py (cổng xuất) · site/build.py (cổng ⑪).
FACT_KY_THUAT = [
    (re.compile(r"\b(curl|cast|wget)\b", re.I), "lệnh terminal"),
    (re.compile(r"\b0x[0-9a-fA-F]{4,}"), "địa chỉ/hex"),
    (re.compile(r"[A-Za-z_][A-Za-z0-9_]+\([A-Za-z0-9_,.]*\)"), "tên hàm"),
    (re.compile(r"\bjson-?rpc\b", re.I), "jsonrpc"),
    (re.compile(r"\b(block|blk)\s*#?\s*[\d.]{4,}", re.I), "số block"),
]

# 🔴 TÁCH MỨC 10/08/2026 — user chốt trong phiên audit cổng (`OPS-T-CONG-CHI-BAO`).
# Bốn nhãn còn lại làm người đọc TẮT thật: `curl …`, `0x166841f7…`, `market(bytes32)`
# là chữ của máy, không ai đọc tiếp. Nhưng **một mốc block viết đời thường thì không** —
# xác: bản X đã đăng 07/08 mang nguyên `block 29.946.913` trong thân post, đủ bốn mặt,
# hậu kiểm Telegram khớp 2.505/2.505 ký tự, **không ai phản ứng**. Số block còn là NHẬN
# DIỆN của kênh (`LAUNCH.md §1`: tem block number). Chặn nó là chặn chữ ký của kênh.
# ⇒ nhãn trong tập này sinh finding mức KHẨU-VỊ. Consumer nào KHÔNG biết tập này thì
# hành xử như cũ (chặn cứng) ⇒ thêm tập là nới CÓ KIỂM SOÁT, không phải đổi ngầm.
# Hình tuple KHÔNG đổi — `site/build.py:1970` unpack đúng hai phần tử.
FACT_KY_THUAT_KHAU_VI = {"số block"}

# quét cái ĐI RA NGOÀI, không quét hồ sơ nội bộ
TARGETS = ["drafts/*.md", "template/out/*.txt", "template/out/*.html"]
# file sinh chữ công khai — bỏ qua dòng comment (đó là hồ sơ ghi lý do, phải giữ)
GENERATORS = ["template/build_cards.py", "template/build_post01.py",
              "template/assets_profile.py", "template/variants_tone.py"]


def scan(path: pathlib.Path, skip_comments: bool, jargon: bool = True,
         valuation: bool = True, cat_ghi_chu: bool = False):
    """`valuation=False` ⇒ bỏ nhóm ①b.

    🔴 Vì sao ①b KHÔNG quét draft, dù nó chặn cứng: lượt chạy thật bắt
    `2026-07-29-bai04-hype-netflow-unlock.md:147` — một GHI CHÚ BIÊN TẬP viết
    *«Không biến thành bài "HYPE đáng mua vì unlock thấp"»*. Cổng bắt đúng chuỗi
    cấm, nhưng câu đó tồn tại để CẤM chính nó. Draft là nơi bàn về câu chữ, nên
    nó chở câu bị cấm một cách hợp lệ; bản EXPORT thì không. Quét ①b ở đúng chỗ
    chữ đi ra ngoài — cùng chỗ đang quét từ-nghề. `site/build.py` lặp `RETIRED`
    trọn gói và điều đó ĐÚNG ở đó: nội dung site là chữ đã xuất bản, không phải draft.
    """
    rules = RETIRED if valuation else RETIRED_TU
    out = []
    dong = path.read_text(encoding="utf-8").split("\n")
    # 🔴 `cat_ghi_chu` thêm 10/08/2026 (`OPS-T-CONG-CHI-BAO`). Mục `## Ghi chú dựng
    # bài` là HỒ SƠ NỘI BỘ — nó bàn VỀ câu chữ nên nó chở từ nghề một cách hợp lệ, y
    # như lý do `valuation` không quét draft (xác 29/07 ghi ở docstring trên).
    # Đo 10/08: lượt `soi.py` đầu tiên trên draft pools.trade trả **6 ĐÁNG-SỬA, cả 6
    # nằm trong ghi chú** (dòng 95 · 96 · 105 …) — không dòng nào đi ra ngoài.
    # 🔵 Cắt bằng CHỈ SỐ DÒNG, không bằng cách bỏ text: số dòng phải giữ đúng, vì
    # "vị trí lỗi" là một trong ba thứ cổng bắt buộc phải trả (`LAUNCH.md §6f`).
    # 🟠 Mặc định `False` — KHÔNG đổi hành xử cũ. Ô `OPS-T-LANG-GATE-DEFAULT-DO` hỏi
    # nên miễn trừ file hay sửa chữ; cờ này mở ĐƯỜNG THỨ BA (cắt theo MỤC, không theo
    # file) nhưng chọn đường nào vẫn là quyết định của user ở ô đó.
    if cat_ghi_chu:
        for k, l in enumerate(dong):
            if re.match(r"^##\s+Ghi chú", l):
                dong = dong[:k]
                break
    for i, line in enumerate(dong, 1):
        if skip_comments and line.lstrip().startswith("#"):
            continue
        for pat, fix, why in rules:
            if re.search(pat, line, re.I):
                kind = "🔴 KẾT LUẬN ĐỊNH GIÁ" if "V1 —" in why else "🔴 TỪ ĐÃ KHAI TỬ"
                out.append((kind, i, pat, fix, why, line.strip()[:80]))
        if not jargon:
            continue
        for pat, fix in JARGON:
            if re.search(pat, line, re.I):
                out.append(("🟡 từ nghề repo", i, pat, fix, "LAUNCH §6b.4", line.strip()[:80]))
    return out


# ── control dương + control âm cho nhóm ①b ───────────────────────────────────
#
# Vì sao có: một cổng chưa từng nổ và một cổng không có gì để bắt trông GIỐNG HỆT
# nhau ở đầu ra ("✅ sạch"). Bài #7 đã trả giá đúng chỗ này — vòng 1 của một phép
# đo trả `H_KHÔNG` mà số 0 đó là DƯƠNG TÍNH GIẢ. Ở đây: PHAI_NO phải bắt được
# từng mẫu, PHAI_QUA phải đi lọt — nếu không thì luật đang cấm CHỮ chứ không cấm
# KẾT LUẬN, và nó sẽ chặn oan những câu mô tả chi phí mà repo dùng liên tục.
PHAI_NO = [
    "token này đang rẻ so với doanh thu",
    "mức giá vẫn đắt nếu nhìn vào cung",
    "rẻ hơn UNI cùng cửa sổ 63 ngày",
    "thị trường đang định giá thấp phần doanh thu này",
    "nó bị định giá dưới giá trị thật",
    "giá mục tiêu quanh vùng này",
    "clearly undervalued at this level",
    "still has upside from here",
    "nên mua khi phí protocol bật",
    "đáng nắm giữ dài hạn",
    "múc thôi",
    "đây là cơ hội đầu tư hiếm",
]
PHAI_QUA = [
    "pool wash rẻ nhất nhận 0,51% ngân sách",          # mô tả CHI PHÍ
    "UNI bị burn đến từ người đi gom hàng",             # hồi quy: bắt oan ở _skeleton-bai08.md:13
    "chi phí đọc log rẻ hơn một lệnh RPC đầy đủ",       # 🔴 ca khó nhất: 'rẻ hơn' về chi phí
    "phí gas đắt vào giờ cao điểm",
    "tỉ lệ đốt trên nền phí thấp hơn kỳ trước",         # so ngang BẰNG SỐ — phải lọt
    "doanh thu 63 ngày là $367k, đối thủ là $219k",
    "144.388,02 PENDLE mua vào qua 65 giao dịch",       # 'mua vào' là phép ĐO, không phải kèo
    "đây không phải lời khuyên đầu tư",                 # disclaimer chuẩn của mọi bài
]


def selftest():
    def hit(s):
        return [p for p, _, _ in VALUATION if re.search(p, s, re.I)]
    sai = []
    for s in PHAI_NO:
        if not hit(s):
            sai.append(f"🔴 ÂM TÍNH GIẢ — không mẫu nào bắt: {s!r}")
    for s in PHAI_QUA:
        h = hit(s)
        if h:
            sai.append(f"🔴 DƯƠNG TÍNH GIẢ — {h[0]!r} chặn oan: {s!r}")
    chua_no = [p for p, _, _ in VALUATION
               if not any(re.search(p, s, re.I) for s in PHAI_NO)]
    for p in chua_no:
        sai.append(f"🟠 MẪU CHẾT — không ca nào trong PHAI_NO làm nó nổ: {p!r}")
    # ── ② CHẾ ĐỘ: cùng một VẬT, bốn cách gõ ⇒ phải cùng một câu trả lời ──────
    #
    # 🔴 Ca ⓑ là control ÂM cho xác 03–04/08: trên mã cũ (`"template/out/" in str(p)`)
    # nó trả False ⇒ nhánh từ-nghề + nhánh định-giá TẮT ⇒ cổng in "✅ sạch" trên một
    # bản xuất bẩn. Selftest cũ PASS suốt trong khi lỗi vẫn sống, vì **không ca nào
    # của nó đi qua nhánh này** — nó chỉ kiểm MẪU, không kiểm CÔNG TẮC.
    ca_che_do = [
        ("ⓐ từ gốc kho, path tương đối",   ROOT,             "template/out/x.txt", True),
        ("ⓑ từ template/, path tương đối", ROOT / "template", "out/x.txt",          True),
        ("ⓒ đường tuyệt đối",              ROOT,             str(OUT_DIR / "x.txt"), True),
        ("ⓓ ÂM: draft từ gốc kho",         ROOT,             "drafts/x.md",        False),
        ("ⓔ ÂM: draft từ template/",       ROOT / "template", "../drafts/x.md",     False),
    ]
    cwd0 = os.getcwd()
    try:
        for ten, cwd, arg, mong in ca_che_do:
            os.chdir(cwd)
            duoc = la_ban_xuat(pathlib.Path(arg))
            if duoc != mong:
                sai.append(f"🔴 CHẾ ĐỘ SAI — {ten}: `{arg}` ⇒ bản xuất={duoc}, phải={mong}")
    finally:
        os.chdir(cwd0)

    for line in sai:
        print(line)
    print(f"\nselftest ①b · {len(PHAI_NO)} ca phải nổ · {len(PHAI_QUA)} ca phải qua · "
          f"{len(VALUATION)} mẫu")
    print(f"selftest CHẾ ĐỘ · {len(ca_che_do)} cách gõ cho cùng một vật")
    if sai:
        sys.exit(f"🔴 SELFTEST HỎNG — {len(sai)} ca")
    print("✅ selftest sạch — cổng nổ đúng chỗ và im đúng chỗ")
    print("🔵 KHÔNG đo được ở đây, ghi ra thay vì giả vờ: ca ⓐ–ⓔ kiểm CÔNG TẮC chọn chế "
          "độ, không kiểm dây nối từ công tắc tới `scan()`. Dây đó phải đo bằng một lượt "
          "chạy thật trên bản xuất có từ nghề, gọi từ hai chỗ đứng khác nhau.")


OUT_DIR = (ROOT / "template" / "out").resolve()


def la_ban_xuat(p: pathlib.Path) -> bool:
    """Vật này có phải BẢN XUẤT không — hỏi về VẬT, không hỏi cách gõ lệnh.

    🔴 XÁC 03–04/08/2026, hai lượt. Dòng cũ là `pure = "template/out/" in str(p)`
    — một phép thử trên CHUỖI đường dẫn. CÙNG MỘT FILE cho hai kết quả khác nhau
    tuỳ chỗ đứng lúc gọi:

        cd <kho>          && python3 template/check_language.py template/out/x.txt → 2 hit
        cd <kho>/template && python3 check_language.py out/x.txt                   → ✅ sạch

    Nhánh TỪ NGHỀ và nhánh ①b KẾT LUẬN ĐỊNH GIÁ (thứ **chặn cứng**) không chạy, mà
    cổng vẫn in dòng xanh. Draft bài #33 nhận "✅ sạch" rồi người phản biện NGOÀI
    bắt 4 lần chữ `trần` — mẫu bắt nó đã nằm sẵn trong chính file này.

    ⇒ `resolve()` trước rồi mới hỏi. Tương đối, tuyệt đối, hay qua symlink đều phải
    cho CÙNG một câu trả lời. Luật: `Crypto Research/RULES.md §2c`.
    """
    try:
        return p.resolve().is_relative_to(OUT_DIR)
    except (OSError, ValueError):
        return False


def main():
    if "--selftest" in sys.argv:
        return selftest()
    # `--ban-xuat`: ép chế độ đầy đủ cho văn bản KHÔNG nằm trong template/out/
    # (bản dán tay, reply, file tạm). Thiếu cửa này thì một văn bản sắp ra ngoài mà
    # nằm chỗ khác vẫn bị soi ở chế độ draft — đúng lỗ vừa vá, đi lối khác.
    ep = "--ban-xuat" in sys.argv
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = ([pathlib.Path(a) for a in argv] if argv else
             [p for g in TARGETS for p in ROOT.glob(g)] +
             [ROOT / g for g in GENERATORS])
    hard = soft = 0
    n_xuat = n_khac = 0
    for p in files:
        if not p.exists():
            continue
        gen = str(p).endswith(".py")
        # draft lẫn ghi chú nội bộ ⇒ chỉ soi TỪ ĐÃ KHAI TỬ; từ nghề chỉ soi bản xuất
        pure = ep or la_ban_xuat(p)
        n_xuat += pure
        n_khac += not pure
        for kind, ln, pat, fix, why, txt in scan(p, skip_comments=gen, jargon=pure,
                                                 valuation=pure):
            if kind.startswith("🔴"):
                hard += 1
            else:
                soft += 1
            try: shown = p.relative_to(ROOT)
            except ValueError: shown = p
            print(f"{kind}  {shown}:{ln}\n"
                  f"    khớp : {pat}\n    thay : {fix}\n    vì   : {why}\n    dòng : {txt}\n")
    n = len([p for p in files if p.exists()])
    # 🔴 Dòng này PHẢI khai NHÁNH, không chỉ đếm file (`RULES.md §2c` điểm 2): một cổng
    # có chế độ tắt mà không nói nó đang ở chế độ nào thì "✅" của hai chế độ trông y
    # hệt nhau — và đó chính là cách lỗ trên sống được hai ngày.
    print(f"quét {n} file · {n_xuat} bản xuất (soi ĐỦ: khai tử + định giá + từ nghề) · "
          f"{n_khac} draft/generator (chỉ soi từ khai tử)" + (" · --ban-xuat ÉP" if ep else ""))
    print(f"🔴 {hard} từ đã khai tử · 🟡 {soft} từ nghề repo")
    if hard:
        sys.exit("\n🔴 CÓ TỪ ĐÃ KHAI TỬ — không đăng cho tới khi sửa.")
    if soft:
        print("\n🟡 Từ nghề không chặn đăng, nhưng cân nhắc: người ngoài không đọc được.")
    else:
        print("✅ sạch")


if __name__ == "__main__":
    main()
