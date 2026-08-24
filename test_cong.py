#!/usr/bin/env python3
"""Ép mọi cổng của build.py NỔ — vì một cổng chưa từng fail thì chưa phải cổng.

`luật bằng chứng của desk §2`: *"cấu hình nào của thế giới sẽ làm nó NỔ?
Không có ⇒ đừng gọi nó là control. Nó là kiểm tra chính tả."*

Mỗi ca: chép site sang thư mục tạm → bẻ ĐÚNG MỘT thứ → build phải chết, và phải
chết vì ĐÚNG lý do đó (khớp chuỗi), không phải vì một lỗi tình cờ nào khác.
Control âm: bản chưa bẻ phải PASS — nếu nó cũng fail thì mọi ca dương vô nghĩa.

Chạy:  python3 site/test_cong.py
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile

SITE = pathlib.Path(__file__).parent
MD = "content/posts/2026-07-27-defillama-uniswap-v4.md"
CJ = "content/posts/2026-07-27-defillama-uniswap-v4.claims.json"
PENDLE_CJ = "content/posts/2026-07-31-pendle-buyback-cot-bang-0.claims.json"
HYPE_CJ = "content/posts/2026-08-12-hype-thi-phan-13-hay-70.claims.json"
CAKE_CJ = "content/posts/2026-08-10-cake-mat-thi-phan-ma-thu-nhieu-phi-hon.claims.json"
SKY_PRIMER = "content/primers/sky.json"


def sua_md(root, fn):
    p = root / "site" / MD
    p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")


def sua_claims(root, fn):
    p = root / "site" / CJ
    d = json.loads(p.read_text(encoding="utf-8"))
    fn(d["claims"])
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def sua_json_bai(root, path, fn):
    p = root / "site" / path
    d = json.loads(p.read_text(encoding="utf-8"))
    fn(d)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def sua_primer_h1(root, moi):
    """Đổi chuỗi THẬT SỰ ra mặt chữ của Primer: H1 trong thân + `tieu_de_ngan` + sha.

    🔴 Vì sao ca thử cần helper này (20/08): trước đây hero Primer lấy cứng
    `cfg["title"]`, nên ca thử nào cần hero mang một con số chỉ việc dựa vào
    title sẵn có. Từ khi Primer có `tieu_de_ngan`, hero đọc chuỗi khác — ca thử
    cũ vẫn "chạy" nhưng cổng thành VÔ HIỆU, và nó báo *"cổng thủng"* trong khi
    cổng vẫn đúng. Ca thử phải đặt con số vào đúng chuỗi mà hero đọc.
    """
    md = root / "site" / "content" / "primers" / "sky.md"
    dong = md.read_text(encoding="utf-8").split("\n")
    dong[0] = f"# {moi}"
    than = "\n".join(dong).strip() + "\n"
    md.write_text(than, encoding="utf-8")
    p = root / "site" / SKY_PRIMER
    d = json.loads(p.read_text(encoding="utf-8"))
    d["tieu_de_ngan"] = moi
    d["body_sha256"] = hashlib.sha256(than.encode()).hexdigest()
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def vat_chat_primers(root):
    """Bộ thử chỉ chép `site/`; đưa thân Primer vào như publish_site làm cho mirror."""
    for p in sorted((SITE / "content" / "primers").glob("*.json")):
        cfg = json.loads(p.read_text(encoding="utf-8"))
        co_san = SITE / "content" / "primers" / f'{cfg["id"]}.md'
        if co_san.is_file():
            body = co_san.read_text(encoding="utf-8").strip() + "\n"
        else:
            draft = SITE.parent / cfg["draft"]
            lines = draft.read_text(encoding="utf-8").splitlines()
            dau = [n for n, line in enumerate(lines) if line.startswith(cfg["start_marker"])]
            cuoi = [n for n, line in enumerate(lines) if line == cfg["end_marker"]]
            if len(dau) != 1 or len(cuoi) != 1 or dau[0] >= cuoi[0]:
                raise RuntimeError(f"marker Primer hỏng trong fixture: {draft}")
            body = "\n".join(lines[dau[0] + 1:cuoi[0]]).strip() + "\n"
        if hashlib.sha256(body.encode()).hexdigest() != cfg["body_sha256"]:
            raise RuntimeError(f"sha256 Primer hỏng trong fixture: {p}")
        out = root / "site" / "content" / "primers" / f'{cfg["id"]}.md'
        out.write_text(body, encoding="utf-8")


# Fact mẫu HỢP LỆ — bộ thử tự dựng, không lấy từ content/ thật. Lý do: `facts.json`
# thật có thể rỗng (và đang rỗng), nên ca thử phải mang theo nguyên liệu của nó.
# Số dưới đây là số THẬT đã đo (ENA/FACTS.md:12) nhưng dùng ở đây chỉ để cổng có
# thứ để nhai — bộ thử KHÔNG phải đường xuất bản.
FACT_MAU = {
    "id": "T001", "ngay": "2026-07-31", "doi_tuong": "ENA",
    "cau": "ENA chưa từng bị đốt một wei nào.",
    "so": "totalSupply() = 15.000.000.000 ENA = đúng 15e27 wei",
    "block": "blk 25.571.508",
    "lenh": "cast call 0x57e114b691db790c35207b2e685d4a43181e6061 \"totalSupply()(uint256)\"",
    "chan": "\"Không có đốt\" không có nghĩa là sắp in thêm — đã mint hết từ đầu.",
    "khoang_cach": {"tin": "Trang dữ liệu X hiển thị một ô 'đã đốt' khác 0 cho token này",
                    "o_dau": "ô 'Burned' trên trang token của X"},
    "nguon": "ENA/FACTS.md:12",
}

FACT_EN_MAU = {
    "slug": "ena-supply-snapshot",
    "title": "ENA supply at block 25,571,508",
    "og_title": "ENA supply at block 25,571,508",
    "mo_ta": "An English evidence receipt for the ENA supply snapshot, with the pinned block, current-state command, falsifier and explicit measurement limits.",
    "intro": "This receipt separates the pinned snapshot from a later current-state read.",
    "headline_metric": {
        "label": "supply",
        "value": "15,000,000,000",
        "note": "ENA at the snapshot",
    },
    "metrics": [
        {"label": "supply", "value": "15,000,000,000", "note": "ENA at the snapshot"},
        {"label": "block", "value": "25,571,508", "note": "pinned on 2026-07-31"},
        {"label": "raw", "value": "15e27", "note": "base units"},
    ],
    "claim": "ENA supply was 15,000,000,000 at block 25,571,508 on 2026-07-31.",
    "pin": "Block 25,571,508 · 2026-07-31",
    "falsifier": "Withdraw the claim if the pinned call returns a different supply.",
    "limits": ["Snapshot only.", "The command can read a later state.", "No price claim."],
    "sources": [
        {"label": "Source A", "url": "https://example.com/a"},
        {"label": "Source B", "url": "https://example.com/b"},
    ],
    "image": "avatar-800.png",
}


def sua_facts(root, fn, nhan_doi=False):
    f = json.loads(json.dumps(FACT_MAU))
    fn(f)
    ds = [f, json.loads(json.dumps(FACT_MAU))] if nhan_doi else [f]
    (root / "site" / "content" / "facts.json").write_text(
        json.dumps({"facts": ds}, ensure_ascii=False, indent=2), encoding="utf-8")


def sua_fact_en(root, fn):
    def sua(f):
        f["en"] = json.loads(json.dumps(FACT_EN_MAU))
        fn(f["en"])
    sua_facts(root, sua)


def sua_builder(root, cu, moi):
    p = root / "site" / "build.py"
    txt = p.read_text(encoding="utf-8")
    if cu not in txt:
        raise RuntimeError(f"bộ thử không tìm thấy đoạn builder cần bẻ: {cu}")
    p.write_text(txt.replace(cu, moi, 1), encoding="utf-8")


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
    ("⑤ MARKDOWN · cú pháp ngoài tập con (ảnh inline)",
     lambda r: sua_md(r, lambda s: s.replace("## Tự kiểm",
                                             "![ảnh không qua asset gate](x.png)\n\n## Tự kiểm", 1)),
     "không nằm trong tập con"),
    ("⑤ MARKDOWN · ** không đóng",
     lambda r: sua_md(r, lambda s: s.replace("**$5,01M**", "**$5,01M")),
     "còn sót **"),
    ("⑤ MARKDOWN · khối ``` không đóng",
     lambda r: sua_md(r, lambda s: s.replace('"\n```\n\n4. **Đếm tận gốc:**',
                                             '"\n\n4. **Đếm tận gốc:**')),
     "không đóng"),
    # ⑦ THẺ XEM TRƯỚC — thêm 30/07. Đây là cổng canh đúng chỗ người LẠ quyết định bấm
    # hay không: thiếu mô tả thì link dán vào Telegram/Discord/forum ra một dòng chữ
    # trơn, và thiếu ảnh thì og:image trỏ vào hư không. Cả hai đều hỏng KHÔNG báo lỗi.
    ("⑦ XEM TRƯỚC · mất mô tả",
     lambda r: sua_md(r, lambda s: re.sub(r"^mo_ta: .*$", "mo_ta: ngắn quá", s,
                                          count=1, flags=re.M)),
     "'mo_ta' phải dài 60–200"),
    ("⑦ XEM TRƯỚC · ảnh trỏ vào file không có",
     lambda r: sua_md(r, lambda s: re.sub(r"^anh: .*$", "anh: khong-ton-tai.png", s,
                                          count=1, flags=re.M)),
     "không tồn tại"),
    # ⑧ ĐO LẠI — thêm 30/07. Một nút hỏng TỆ HƠN không có nút: nó hứa người đọc tự kiểm
    # được rồi trả về số 0 hoặc không gì, và số 0 đó bị đọc thành dữ kiện về chain.
    ("⑧ ĐO LẠI · thiếu trường bắt buộc",
     lambda r: sua_claims(r, lambda cs: cs[0].update(
         do_lai={"to": "0x" + "1" * 40, "ky": "owner()"})),
     "do_lai thiếu"),
    ("⑧ ĐO LẠI · chữ ký hàm không phải chữ ký",
     lambda r: sua_claims(r, lambda cs: cs[0].update(
         do_lai={"to": "0x" + "1" * 40, "ky": "đọc số dư", "cong_thuc": {"tu": 0, "thap_phan": 18},
                 "don_vi": "ETH", "chu_so": 4, "so_ghim": 0})),
     "không phải chữ ký hàm"),
    ("⑧ ĐO LẠI · địa chỉ không phải 20 byte",
     lambda r: sua_claims(r, lambda cs: cs[0].update(
         do_lai={"to": "0xabc", "ky": "owner()", "cong_thuc": {"tu": 0, "thap_phan": 18},
                 "don_vi": "ETH", "chu_so": 4, "so_ghim": 0})),
     "không phải địa chỉ 20 byte"),
    ("⑧ ĐO LẠI · lý do 'không đo được' viết cho có",
     lambda r: sua_claims(r, lambda cs: cs[0].update(khong_do_lai="chưa làm")),
     "phải nói RÕ vì sao"),
    # ⑨ HẠN — thêm 30/07. Một ngày viết trong đoạn văn thì tới ngày đó không gì nhắc ai.
    ("⑨ HẠN · điều-bác-bỏ có ngày mà không khai hạn",
     lambda r: sua_claims(r, lambda cs: (cs[1].update(status="ĐANG ĐỨNG"), cs[1].pop("han", None))),
     "mà không khai 'han'"),
    ("⑨ HẠN · khai hạn nhưng không nói ngày đó phân định gì",
     lambda r: sua_claims(r, lambda cs: cs[0].update(han="2026-12-31", han_ghi="xem lại")),
     "thiếu 'han_ghi'"),
    # ⑨b QUÁ HẠN — thêm 16/08. Khoảng trống giữa ⑨ (phải KHAI hạn) và ⑩ (đã phân
    # định thì phải ghi kết quả) đúng bằng thứ quan trọng nhất: hạn TRÔI QUA mà không
    # ai đọc lại. Xác: CAKE C6 hạn 12/08 nằm im tới 16/08, trong khi trang công khai
    # vẫn in ĐÃ TỚI HẠN cho khách đọc — cổng canh nợ mà chỉ báo cho chủ nợ.
    ("⑨b QUÁ HẠN · hạn đã trôi mà claim vẫn ĐANG ĐỨNG",
     lambda r: sua_claims(r, lambda cs: cs[0].update(
         status="ĐANG ĐỨNG", han="2020-01-01",
         han_ghi="ngày này phải đọc lại và ghi kết quả vào đây, kể cả khi ngược bài")),
     "đã trôi qua mà vẫn 'ĐANG ĐỨNG'"),
    ("⑨b QUÁ HẠN · CHỜ SỐ là cửa ra hợp lệ — KHÔNG được nổ",
     lambda r: sua_claims(r, lambda cs: cs[0].update(
         status="CHỜ SỐ", han="2020-01-01",
         han_ghi="ngày này phải đọc lại và ghi kết quả vào đây, kể cả khi ngược bài")),
     None),
    # ⑩ GHI TRƯỚC — thêm 30/07. Đây là cửa để một lần ĐỔ lặng lẽ rơi khỏi bảng.
    ("⑩ GHI TRƯỚC · đã phân định mà không ghi kết quả",
     lambda r: sua_claims(r, lambda cs: cs[0]["ghi_truoc"].pop("ket_qua")),
     "thiếu 'ket_qua'"),
    ("⑩ GHI TRƯỚC · không nói ghi trước Ở ĐÂU",
     lambda r: sua_claims(r, lambda cs: cs[0]["ghi_truoc"].update(noi="")),
     "thiếu 'noi'"),
    ("⑦ XEM TRƯỚC · ảnh chưa khai builder nào sinh",
     lambda r: (r / "site" / "assets" / "la-mat.png").write_bytes(
         (r / "site" / "assets" / "favicon-16.png").read_bytes()),
     "chưa khai builder"),

    # ── ⑪ FACT — đơn vị đăng thứ hai (brief-chien-luoc-dang-x.md §0b) ───────────
    # Chặn đúng ba thứ làm nên một Fact (số · block · lệnh) + câu chặn suy luận sai.
    # 🔴 Ca cuối là control DƯƠNG: một facts.json HỢP LỆ phải build được. Thiếu nó thì
    # sáu ca trên không phân biệt được "cổng chặn đúng" với "cổng chặn tất".
    ("⑪ FACT · thiếu con số",
     lambda r: sua_facts(r, lambda f: f.pop("so")),
     "thiếu CON SỐ"),
    ("⑪ FACT · 'block' không mang số block",
     lambda r: sua_facts(r, lambda f: f.update(block="đọc hôm nay")),
     "không mang số block"),
    ("⑪ FACT · lệnh tự kiểm ngắn tới mức không chạy được",
     lambda r: sua_facts(r, lambda f: f.update(lenh="cast")),
     "quá ngắn để chạy được"),
    ("⑪ FACT · để trống câu chặn suy luận sai",
     lambda r: sua_facts(r, lambda f: f.update(chan="")),
     "chưa ai quyết"),
    ("⑪ FACT · hai fact trùng id",
     lambda r: sua_facts(r, lambda f: None, nhan_doi=True),
     "TRÙNG"),
    ("⑪ FACT · kết luận định giá lọt vào câu fact  ← nhóm ①b",
     lambda r: sua_facts(r, lambda f: f.update(cau="Token này đang rẻ so với doanh thu.")),
     "TỪ ĐÃ KHAI TỬ"),
    # ── KHOẢNG CÁCH — ca xác: desk xếp "ENA chưa từng bị đốt" lên hàng đầu, user bác.
    # Đúng, ghim được block, kiểm bằng một lệnh — và không phân biệt ENA khỏi bất cứ
    # thứ gì, vì phần lớn token không đốt. Ba ca dưới ép cổng mới bắt đúng ca đó.
    ("⑪ FACT · KHOẢNG CÁCH · không khai gì  ← ca ENA 01/08",
     lambda r: sua_facts(r, lambda f: f.pop("khoang_cach")),
     "thiếu 'khoang_cach'"),
    ("⑪ FACT · KHOẢNG CÁCH · khai niềm tin nhưng KHÔNG có chỗ kiểm",
     lambda r: sua_facts(r, lambda f: f.update(
         khoang_cach={"tin": "ai cũng tưởng token này có đốt", "o_dau": ""})),
     "chỗ kiểm được niềm tin đó"),
    ("⑪ FACT · KHOẢNG CÁCH · khai dạng chuỗi thay vì object",
     lambda r: sua_facts(r, lambda f: f.update(khoang_cach="có khoảng cách")),
     "thiếu 'khoang_cach'"),
    # ── KHUÔN v2 — brief §0b chốt 02/08, áp cho Fact `ngay` ≥ 2026-08-03. Xác:
    # ba Fact đầu phình 2.364 → 4.175 ký tự (Fact 3 DÀI HƠN bài dài #8) mà 12/12
    # cổng PASS sạch — không cổng nào đếm độ dài hay số câu chặn của một Fact.
    ("⑪ FACT v2 · 'cau' quá trần 600",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03", cau="Con số này đứng yên qua từng lần đọc. " * 20)),
     "trần 600"),
    ("⑪ FACT v2 · 'chan' hai câu — hết tư cách Fact",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03",
         chan="Không có đốt không có nghĩa là sắp in thêm. Và đây là câu thứ hai.")),
     "câu > 1"),
    ("⑪ FACT v2 · 'cau' dính tên hàm — thân bài phải đọc được",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03", cau="ENA chưa từng bị đốt: totalSupply() đứng yên.")),
     "dính tên hàm"),
    ("⑪ FACT v2 · 'so' chở chuỗi mốc dài quá 200",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03", so="ngày 14/07: 138 điểm · " * 12)),
     "MỘT con số chính"),
    # ── SỐ BLOCK hạ xuống KHẨU-VỊ 10/08 (user chốt, `LAUNCH.md §6f`) ────────────
    # Xác: bản X đã đăng 07/08 mang `block 29.946.913` trong thân post, đủ bốn mặt,
    # hậu kiểm Telegram khớp 2.505/2.505 ký tự, không ai phản ứng — và số block là tem
    # nhận diện của kênh (`LAUNCH.md §1`). Hai ca dưới đi thành CẶP có chủ ý: nếu chỉ
    # có ca dương thì "đậu" có thể vì cổng đã chết hẳn, không phải vì nó hẹp đúng chỗ.
    ("⑪ FACT v2 · số block trong 'cau' phải BUILD ĐƯỢC (hạ xuống KHẨU-VỊ 10/08)",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03",
         cau="Lượt gần nhất tính tới block 29.946.913 chỉ còn 0,159746%.")),
     None),
    ("⑪ FACT v2 · hex trong 'cau' VẪN phải chặn — cặp đối chứng của ca trên",
     lambda r: sua_facts(r, lambda f: f.update(
         ngay="2026-08-03",
         cau="Giao dịch 0x166841f7f811e9563a1138e28bc7d94d49e2 chứng trọn cơ chế.")),
     "dính địa chỉ/hex"),
    ("⑪ FACT v2 · control CHỐNG NHIỄU — Fact cũ (≤02/08) chan dài KHÔNG bị bắt",
     lambda r: sua_facts(r, lambda f: f.update(
         chan="Không có đốt không có nghĩa là sắp in thêm. Và đây là câu thứ hai.")),
     None),
    ("⑪ FACT v2 · control DƯƠNG — Fact mới viết đúng khuôn phải BUILD ĐƯỢC",
     lambda r: sua_facts(r, lambda f: f.update(ngay="2026-08-03")),
     None),
    ("⑪ FACT · control DƯƠNG — facts.json hợp lệ phải BUILD ĐƯỢC",
     lambda r: sua_facts(r, lambda f: None),
     None),
    # ── BẢN WEB — `cau` đã đăng có thể mang dấu vết riêng của thread X ──────────
    # Hai ca bẻ lớp thích nghi để chứng minh cổng ⑪b bắt được chính hai lỗi từng
    # xuất hiện live: trỏ tới một reply không tồn tại và lặp nguyên văn ô giới hạn.
    ("⑪b FACT WEB · còn câu 'reply ngay dưới' phải NỔ",
     lambda r: (
         sua_facts(r, lambda f: f.update(
             cau=f["cau"] + "\n\nBằng chứng và cách tự kiểm: ở reply ngay dưới.")),
         sua_builder(r, "cau_web = cau_fact_web(f)", "cau_web = str(f['cau'])")),
     "còn trỏ người đọc tới 'reply ngay dưới'"),
    ("⑪b FACT WEB · lặp nguyên văn ô giới hạn phải NỔ",
     lambda r: (
         sua_facts(r, lambda f: f.update(cau=f["cau"] + "\n\n" + f["chan"])),
         sua_builder(r, "cau_web = cau_fact_web(f)", "cau_web = str(f['cau'])")),
     "lặp nguyên văn phần 'Fact này KHÔNG nói'"),
    # ── BIÊN LAI EN CỦA FACT — opt-in, không đẻ bài dài làm vật đệm ────────────
    ("⑪c FACT EN · thiếu headline metric phải NỔ",
     lambda r: sua_fact_en(r, lambda en: en.pop("headline_metric")),
     "headline_metric phải có label/value/note"),
    ("⑪c FACT EN · thiếu trường bắt buộc phải NỔ",
     lambda r: sua_fact_en(r, lambda en: en.pop("falsifier")),
     "thiếu trường bắt buộc"),
    ("⑪c FACT EN · số lạ không có ở Fact nguồn phải NỔ",
     lambda r: sua_fact_en(r, lambda en: en.update(
         claim=en["claim"] + " A separate total was 99,999.")),
     "mang số KHÔNG có ở Fact nguồn"),
    ("⑪c FACT EN · control DƯƠNG — biên lai đủ mặt phải BUILD ĐƯỢC",
     lambda r: sua_fact_en(r, lambda en: None),
     None),

    # ── BỐ CỤC v3 + lượt bóc <script> của cổng ⑪ (10/08) ─────────────────────────
    # Bốn ca dưới đi thành BỘ. Ca ① một mình không đủ: nó xanh cả khi cổng ⑪ đã chết
    # hẳn. Ca ④ là cặp đối chứng của nó — cùng chuỗi `href="…"` không giải được, chỉ
    # khác chỗ đứng (trong <script> hay trong thân trang), và hai ca phải cho hai kết
    # quả NGƯỢC nhau. Một mình ca ④ cũng không đủ, vì nó xanh cả khi cổng chưa hề
    # được nới. Phải có cả hai mới phân biệt được "cổng hẹp đúng chỗ" với "cổng thủng".
    ("BỐ CỤC v3 · control DƯƠNG — dựng được, và href trong <script> KHÔNG bị chặn",
     None, None, ["--bo-cuc", "v3"]),
    ("BỐ CỤC v3 · thiếu v3.css phải NỔ — trang đủ chữ mà không có hình là hỏng im nhất",
     lambda r: (r / "site" / "v3.css").unlink(),
     "cần v3.css"),
    ("BỐ CỤC v3 · thiếu v3.js phải NỔ",
     lambda r: (r / "site" / "v3.js").unlink(),
     "cần v3.js"),
    ("BỐ CỤC v3 · token rơi về chữ trần phải NỔ",
     lambda r: sua_builder(r, '<div class="token-grid" id="token-grid">',
                           '<div class="token-grid-hong" id="token-grid">'),
     "mục token v3 thiếu cấu trúc"),
    ("BỐ CỤC v3 · preview bài trang chủ mất component phải NỔ",
     lambda r: sua_builder(r, 'bai[:6], "", " home-articles", uu_tien=True,',
                           'bai[:6], "", uu_tien=True,'),
     "preview bài trang chủ v3 thiếu cấu trúc"),
    ("BỐ CỤC v3 · preview bài token mất ưu tiên phải NỔ",
     lambda r: sua_builder(r, 'bai_t[:6], "../../", " uni-articles", uu_tien=True,',
                           'bai_t[:6], "../../", uu_tien=True,'),
     "preview bài token v3 thiếu cấu trúc"),
    ("BỐ CỤC v3 · kho bài mất component phải NỔ",
     lambda r: sua_builder(r, '<section class="article-archive"',
                           '<section class="article-archive-hong"'),
     "kho bài v3 thiếu tìm/lọc/mở-thêm"),
    ("BỐ CỤC v3 · bỏ helper khóa xuống dòng phải NỔ",
     lambda r: sua_builder(r, "html = khoa_xuong_dong(html)", "html = html"),
     "còn khoảng trắng có thể bị bẻ"),
    # 🔴 SỬA 13/08/2026 — ca này TỪNG là "kho 11 bài mà nút mở thêm còn hiện", và nó
    # CHẾT IM LẶNG khi kho vượt 12 bài: phép bẻ cũ (`an_mo_them = ""`) là no-op ở nhánh
    # `so_bai > 12` vì lúc đó nút VỐN phải hiện. Bài thứ 13 (MORPHO, 13/08) đưa kho sang
    # nhánh kia và ca thử báo "cổng thủng" trong khi cổng vẫn đúng — hỏng ở FIXTURE, không
    # ở cổng. Nay bẻ bằng cách ĐẢO điều kiện, nên nó nổ được ở CẢ HAI nhánh:
    #   · kho ≤12 bài  → nút hiện trong khi phải ẩn
    #   · kho >12 bài  → nút ẩn trong khi phải hiện
    # Không còn phụ thuộc số bài, tức không chết lại khi kho lớn lên.
    ("BỐ CỤC v3 · nút mở thêm ngược trạng thái kho phải NỔ",
     lambda r: sua_builder(r, 'an_mo_them = " hidden" if not con_lai else ""',
                           'an_mo_them = "" if not con_lai else " hidden"'),
     "nút mở thêm"),
    ("BỐ CỤC v3 · menu đổi riêng Trang chủ thành Sổ gốc phải NỔ",
     lambda r: sua_builder(r, 'MUC_DIEU_HUONG = [("", "Trang chủ"),',
                           'MUC_DIEU_HUONG = [("", "Sổ gốc"),'),
     "menu phải dùng chung"),
    ("VISUAL · marker còn nhưng cấu hình bị xoá phải NỔ",
     lambda r: sua_json_bai(r, PENDLE_CJ, lambda d: d["visuals"].pop(0)),
     "marker visual và cấu hình không khớp"),
    ("VISUAL · type ngoài bộ template phải NỔ",
     lambda r: sua_json_bai(r, PENDLE_CJ,
                            lambda d: d["visuals"][0].update(type="pie")),
     "type lạ"),
    ("VISUAL · renderer làm rơi figure phải NỔ",
     lambda r: sua_builder(r, '<figure class="article-viz article-viz-{loai}"',
                           '<figure class="article-viz-hong article-viz-{loai}"'),
     "visual v3 dựng thiếu figure"),
    ("⑪ LIÊN KẾT · href hỏng trong THÂN TRANG vẫn phải chặn — cặp đối chứng của ca trên",
     lambda r: sua_md(r, lambda s: s.replace(
         "## Tự kiểm", "Xem [chỗ này](/khong-he-ton-tai/) đã.\n\n## Tự kiểm", 1)),
     "href nội bộ không tới đâu"),
    # ⑮ TIÊU ĐỀ — thêm 12/08. Cổng đo chuỗi ĐI RA MẶT CHỮ, không đo `title`.
    # 🔵 Bài mẫu `2026-07-27-defillama-uniswap-v4` có title dài ĐÚNG 80 ký tự — đúng
    # trần. Nên cặp biên đã có sẵn: "control âm — không bẻ gì" chứng minh 80 QUA, ca
    # ngay dưới thêm một ký tự để chứng minh 81 NỔ. Không ca nào một mình đủ: ca nổ
    # xanh cả khi trần bị đặt sai chỗ, ca qua xanh cả khi cổng chưa hề chạy.
    ("⑮ TIÊU ĐỀ · title 81 ký tự (trần 80) phải NỔ",
     lambda r: sua_md(r, lambda s: re.sub(r"^(title: .*)$", r"\1u", s,
                                          count=1, flags=re.M)),
     "trần 80"),
    # Trường sinh ra để CỨU độ dài không được thành cửa vòng qua chính cổng đó.
    ("⑮ TIÊU ĐỀ · tieu_de_ngan cũng vượt trần phải NỔ",
     lambda r: sua_md(r, lambda s: re.sub(
         r"^(title: .*)$", lambda m: m.group(1) + "\ntieu_de_ngan: " + "x" * 81,
         s, count=1, flags=re.M)),
     "đang lấy từ 'tieu_de_ngan'"),
    # Control DƯƠNG của cùng cổng: title dài gấp đôi trần vẫn PHẢI dựng được khi bài đã
    # khai dòng ngắn — ca này đỏ nghĩa là cổng đang chặn đúng thứ nó sinh ra để cho qua.
    ("⑮ TIÊU ĐỀ · control DƯƠNG — title vượt trần + tieu_de_ngan ngắn phải QUA",
     lambda r: sua_md(r, lambda s: re.sub(
         r"^title: (.*)$",
         lambda m: f"title: {m.group(1)}{' và một vế nữa cho thật dài' * 3}"
                   f"\ntieu_de_ngan: Bản sửa của DefiLlama mới chỉ chạy một chiều",
         s, count=1, flags=re.M)),
     None),
    # Thẻ hiện dòng ngắn ⇒ chỉ mục tìm là chỗ DUY NHẤT còn giữ câu dài. Mất nó thì gõ
    # đúng chữ trong tiêu đề vẫn ra 0 kết quả — cùng hình dạng lỗi ô tìm claim vá 11/08.
    ("⑮ TIÊU ĐỀ · chỉ mục tìm kho bài rơi mất title đầy đủ phải NỔ",
     lambda r: sua_builder(r, '{f["title"]} {_tieu_de_h1(f)} {ma} {ngay} {sg}',
                           '{_tieu_de_h1(f)} {ma} {ngay} {sg}'),
     "mất TIÊU ĐỀ ĐẦY ĐỦ"),
    # ⑭ VISUAL · khuôn `dai` — thêm 12/08. Bài mẫu của bộ thử không có visual, nên ba ca
    # dưới bẻ thẳng cấu hình của bài HYPE, bài đầu tiên dùng khuôn này.
    ("⑭ VISUAL dai · value là CHUỖI phải NỔ",
     lambda r: sua_json_bai(r, HYPE_CJ, lambda d: d["visuals"][0]["diem"][0].__setitem__(
         "value", "13%")),
     "phải là SỐ"),
    # Mọi điểm bằng nhau ⇒ phép quy tỷ lệ chia cho 0. Và kể cả chặn được lỗi chia, một
    # dải mà mọi chấm chồng lên nhau vẫn TRÔNG như một chấm trong khi bảng liệt kê đủ mục.
    ("⑭ VISUAL dai · mọi điểm cùng một giá trị phải NỔ",
     lambda r: sua_json_bai(r, HYPE_CJ, lambda d: [
         x.__setitem__("value", 50) for x in d["visuals"][0]["diem"]]),
     "cần hai đầu khác nhau"),
    ("⑭ VISUAL dai · 9 điểm (trần 8) phải NỔ",
     lambda r: sua_json_bai(r, HYPE_CJ, lambda d: d["visuals"][0].__setitem__(
         "diem", [dict(d["visuals"][0]["diem"][0], value=i + 1, label=f"n{i}")
                  for i in range(9)])),
     "phải có 2–8 mục"),
    # ⑯ VISUAL opposite-direction — pilot CAKE 14/08. Ba ca phân biệt một cấu hình
    # thật sự chở hai hướng với một bảng chỉ tình cờ có hai hàng số.
    ("⑯ VISUAL opposite · hai chuỗi cùng hướng phải NỔ",
     lambda r: sua_json_bai(r, CAKE_CJ, lambda d: d["visuals"][0]["series"][1]["values"][-1].update(
         value=100000, hien="$100.000")),
     "hướng ròng NGƯỢC nhau"),
    ("⑯ VISUAL opposite · số điểm không khớp số mốc phải NỔ",
     lambda r: sua_json_bai(r, CAKE_CJ, lambda d: d["visuals"][0]["series"][1]["values"].pop()),
     "phải khớp 3 mốc"),
    ("⑯ VISUAL opposite · value dạng chuỗi phải NỔ",
     lambda r: sua_json_bai(r, CAKE_CJ, lambda d: d["visuals"][0]["series"][0]["values"][0].update(
         value="74%")),
     "cần value là SỐ"),
    # ⑰ TOKEN PRIMER + hai primitive mới. Cả ba ca bẻ dữ liệu trong config; nếu chỉ
    # nhìn HTML mẫu thì builder có thể trôi mà bộ thử vẫn xanh.
    ("⑰ VISUAL system-map · edge trỏ nút không tồn tại phải NỔ",
     lambda r: sua_json_bai(r, SKY_PRIMER,
                            lambda d: d["visuals"][0]["edges"][0].update(to="ghost-node")),
     "nút không tồn tại"),
    ("⑰ VISUAL waterfall · phép tính không khép phải NỔ",
     lambda r: sua_json_bai(r, SKY_PRIMER,
                            lambda d: d["visuals"][1]["items"][-1].update(value=41.09)),
     "không khép số"),
    ("⑰ PRIMER · body sha256 lệch phải NỔ",
     lambda r: sua_json_bai(r, SKY_PRIMER, lambda d: d.update(body_sha256="0" * 64)),
     "body sha256 lệch"),
    ("⑰ PRIMER · visual thiếu nhãn public phải NỔ",
     lambda r: sua_json_bai(r, SKY_PRIMER,
                            lambda d: d["visuals"][0].update(public_scope="")),
     "primer visual cần public_scope"),
    ("⑰ PRIMER · art direction ngoài registry phải NỔ",
     lambda r: sua_json_bai(r, SKY_PRIMER,
                            lambda d: d.update(art_direction="bon-card-cung-khuon")),
     "primer art_direction lạ"),
    ("⑰ PRIMER · renderer làm rơi ledger của machine-valves phải NỔ",
     lambda r: sua_builder(r, 'class="pm-ledger"', 'class="pm-ledger-hong"'),
     "art direction machine-valves dựng thiếu cấu trúc"),
    ("⑰ PRIMER · data card làm rơi nhãn cột phải NỔ",
     lambda r: sua_builder(r, 'data-label="', 'data-card-label="'),
     "visual v3 dựng thiếu nhãn data card"),
    ("⑰ PRIMER · hero tô số mà làm rơi ký hiệu tiền phải NỔ",
     lambda r: (sua_primer_h1(r, "SKY: cỗ máy stablecoin $10 tỷ"),
                sua_builder(r, 'if truoc.endswith("$"):',
                            'if False and truoc.endswith("$"):')),
     "làm rơi ký hiệu tiền khỏi nhấn số"),
    ("⑰ PRIMER · bảng key-value rơi về bảng trần phải NỔ",
     lambda r: sua_builder(r, 'table_classes.append("table-key-value")',
                           'table_classes.append("table-key-value-hong")'),
     "làm rơi kiểu bảng key-value"),
    ("⑰ PRIMER · bảng so sánh rơi về table chung phải NỔ",
     lambda r: sua_builder(r, 'return "table-compare"', 'return "table-compare-hong"'),
     "dựng thiếu data module biên tập"),
    ("⑰ PRIMER · sơ đồ phân bổ rơi về code block phải NỔ",
     lambda r: sua_builder(r, 'return (f\'<section class="primer-allocation"',
                           'return (f\'<section class="primer-allocation-hong"'),
     "dựng thiếu data module biên tập"),
    ("⑰ PRIMER · snapshot cuối bài rơi thành ba khối rời phải NỔ",
     lambda r: sua_builder(r, 'class="primer-snapshot-suite"',
                           'class="primer-snapshot-suite-hong"'),
     "recap/report Primer sai ranh giới"),
    ("⑰ PRIMER · recap rơi lại vào report grid phải NỔ",
     lambda r: sua_builder(r, 'class="primer-recap"',
                           'class="primer-recap-hong"'),
     "recap/report Primer sai ranh giới"),
    ("⑰ PRIMER · snapshot dính lại vai card-grid phải NỔ",
     lambda r: sua_builder(r, 'f"report-{panel}"', 'kind'),
     "recap/report Primer sai ranh giới"),
    # 🔴 VÁ 22/08 — HAI CA NÀY TỪNG BÁM VÀO NỘI DUNG MỘT BÀI CỤ THỂ, và ngày Primer
    # SKY lên v6.0 (thân bài sạch emoji trạng thái) thì cả hai **rỗng nghĩa**: tắt bộ
    # gỡ mà không có gì để gỡ thì cổng không có gì để cắn ⇒ 90/90 tụt xuống 88/90.
    # May là nó rỗng theo hướng KÊU TO. Nhưng phép sửa KHÔNG phải cắm emoji ngược vào
    # bài — đó là viết nội dung phục vụ fixture, đúng thứ docstring file này tố cáo.
    # ⇒ Ca nay **tự mang mồi**: bẻ bộ gỡ VÀ chèn dấu, nên nó thử CỔNG chứ không thử
    # xem hôm nay bài có tình cờ chứa dấu nào không.
    ("⑰ PRIMER · tam giác cảnh báo lọt lại mặt đọc phải NỔ",
     # hai vết bẻ: ⑴ bỏ ⚠️ khỏi bộ gỡ ⑵ chèn một ⚠️ để bộ gỡ có cơ hội bỏ sót.
     # Cổng ở `build.py` giữ NGUYÊN tuple của nó (không có dấu `:` cuối) nên vẫn soi ⚠️.
     lambda r: (sua_builder(r, '("🔴", "🟢", "🔵", "⚪", "⚠️", "⚠"):',
                            '("🔴", "🟢", "🔵", "⚪"):'),
                sua_builder(r, 'story = _bo_cham_trang_thai_primer(story)',
                            'story = _bo_cham_trang_thai_primer(story + "<p>⚠️ mồi</p>")')),
     "còn emoji trạng thái trong mặt đọc"),
    ("⑰ PRIMER · emoji trạng thái lọt lại mặt đọc phải NỔ",
     # bỏ hẳn lượt gọi bộ gỡ, và chèn mồi ngay tại chỗ nó vừa bị bỏ.
     lambda r: sua_builder(r, 'story = _bo_cham_trang_thai_primer(story)',
                           'story = story + "<p>🔴 mồi</p>"'),
     "còn emoji trạng thái trong mặt đọc"),
    ("⑰ PRIMER · con trỏ desk lọt ra caption public phải NỔ",
     lambda r: sua_builder(
         r,
         'story = render(cfg["_story"], o, visuals, show_claim_refs=False,',
         'story = render(cfg["_story"], o, visuals, show_claim_refs=True,'),
     "primer làm lộ con trỏ desk"),
    ("⑰ PRIMER · VERIFY mở sẵn phải NỔ",
     lambda r: sua_builder(r, '<details class="primer-verify" id="lop-kiem-chung">',
                           '<details class="primer-verify" id="lop-kiem-chung" open>'),
     "VERIFY primer phải đóng mặc định"),
]

# Ca nào cần cờ riêng thì khai ở đây, không nhét thêm cột vào mọi tuple cũ:
# chúng không có lý do gì phải mọc thêm một ô rỗng vì vài ca cần cờ riêng.
THEM_ARGV = {ten: ca[3] for ca in CA if len(ca) > 3 for ten in [ca[0]]}
# Ba ca v3 dưới đây cần cờ nhưng khai ở dạng tuple 3 phần tử cho gọn — nối cờ ở đây.
for _t in ("BỐ CỤC v3 · thiếu v3.css phải NỔ — trang đủ chữ mà không có hình là hỏng im nhất",
           "BỐ CỤC v3 · thiếu v3.js phải NỔ",
           "BỐ CỤC v3 · token rơi về chữ trần phải NỔ",
           "BỐ CỤC v3 · preview bài trang chủ mất component phải NỔ",
           "BỐ CỤC v3 · preview bài token mất ưu tiên phải NỔ",
           "BỐ CỤC v3 · kho bài mất component phải NỔ",
           "BỐ CỤC v3 · bỏ helper khóa xuống dòng phải NỔ",
           "BỐ CỤC v3 · nút mở thêm ngược trạng thái kho phải NỔ",
           "BỐ CỤC v3 · menu đổi riêng Trang chủ thành Sổ gốc phải NỔ"):
    THEM_ARGV[_t] = ["--bo-cuc", "v3"]


def main():
    dat = sai = 0
    for ten, be, mong, *_ in CA:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            shutil.copytree(SITE, root / "site")
            vat_chat_primers(root)
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
            # 🔴 Kho hiện vật phải có mặt trong thư mục tạm, nếu không thì control âm
            # ("không bẻ gì") FAIL vì lý do của bộ thử chứ không phải của bài — và một
            # control âm hỏng làm cả bộ mất nghĩa. Bước đưa hiện vật lên site được thêm
            # 31/07 (build.py ~:1222) nhưng bộ thử không được cập nhật cùng lúc; lộ ra
            # đúng lần dựng bài #8. Chỉ chép ĐÚNG các file đã khai ở HIEN_VAT.
            # 🔴 Dùng ĐÚNG công thức tra của build.py — kho gốc có `site/` còn mirror
            # công khai thì PHẲNG, nên `SITE.parent` trỏ hai chỗ khác nhau. Bản vá đầu
            # chỉ đúng ở kho gốc và vẫn FAIL khi publish_site chạy test từ trong mirror.
            kho_goc = next((k for k in (SITE.parent / "blockpinned" / "data",
                                        SITE.parent / "data")
                            if k.is_dir()), None)
            if kho_goc is not None:
                (root / "data").mkdir(exist_ok=True)
                for f in kho_goc.iterdir():
                    if f.is_file() and f.suffix == ".json":
                        shutil.copy2(f, root / "data" / f.name)
            if be:
                be(root)
            r = subprocess.run([sys.executable, str(root / "site" / "build.py")]
                               + THEM_ARGV.get(ten, []),
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
