#!/usr/bin/env python3
"""BlockPinned — sinh site tĩnh từ markdown. Thư viện chuẩn, không phụ thuộc gì.

VÌ SAO CÓ SITE NÀY (LAUNCH.md:148-155): bài đăng trên X/TG mang theo những claim
có điều-bác-bỏ, mà X hết sửa được sau 1 giờ và TG thì trôi. Hai kênh đó biết
"thêm vào", không biết "claim này giờ đang đứng hay đã đổ". Web giữ bản chuẩn
sửa tại chỗ + sổ claim; X/TG vẫn đăng đầy đủ dạng native.

BẢY CỔNG, tất cả đều CHẶN build — không cái nào chỉ cảnh báo:
  1 NGÔN NGỮ   từ đã khai tử + từ nghề repo (dùng CHUNG danh sách với
                template/check_language.py — một chủ, không chép)
  2 CẤU TRÚC   đủ 5 phần chữ ký LAUNCH §1: claim · số kèm block · tự kiểm ·
                điều bác bỏ · disclaimer
  3 CLAIM      mỗi claim phải có falsifier thật + block ghim + trạng thái hợp lệ
  4 NGÔI XƯNG  "chúng tôi" khai số người, mà desk một người (LAUNCH §1)
  5 MARKDOWN   cú pháp không nhận ra thì NỔ, không im lặng bỏ qua
  6 THUỘC TÍNH SỐ  toạ độ/số trong đánh dấu sinh ra phải là số hợp lệ — trình duyệt
                bỏ qua thuộc tính sai trong im lặng, đúng loại lỗi tệ nhất
  7 XEM TRƯỚC  bài phải có dòng mô tả (60–200 ký tự) + ảnh xem trước tồn tại thật:
                thiếu thì link dán ra Telegram/Discord/forum chỉ còn một dòng chữ trơn
  (+ ảnh phục vụ phải TRÙNG BYTE với bản builder sinh ra, và phải khai builder nào)
 11 FACT       đơn vị đăng thứ hai (`brief-chien-luoc-dang-x.md §0b`): mỗi Fact phải
                có ĐỦ ba thứ — một con số · một block · một lệnh tự kiểm — cộng câu
                chặn suy luận sai khai tường minh. Danh sách đầy đủ: TEN_CONG.

Cổng 3 và 5 là bản MÁY của một lỗi thật: bài #1 suýt đăng với một claim bị cắt
mất falsifier, trong khi ô "[x] có falsifier?" vẫn tick vì thừa kế từ bản trước
(LAUNCH §6c). Người phản biện bắt, checklist không bắt. Một renderer nuốt im
một dòng cũng gây đúng lỗi đó, lần này do máy.

Chạy:  python3 site/build.py [--theme benchmark|do|verdigris] [--out <thư mục>]
       mặc định là `benchmark` — hệ nhận diện đã chốt 29/07; hai hệ kia giữ làm hồ sơ
"""
import datetime
import hashlib
import html as ihtml
import json
import pathlib
import re
import shutil
import sys

# keccak thuần stdlib, nằm cạnh file này (cả kho gốc và mirror công khai).
# Nó TỰ KIỂM 5 vector lúc import và chết ngay nếu sai — selector sai thì gọi
# sang hàm khác và trả về số trông như số liệu.
import keccak

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
# Tên miền dùng cho canonical · og:url · sitemap. Ba chỗ này BẮT BUỘC là URL tuyệt đối
# (đường dẫn tương đối trong thẻ og bị mọi nơi bỏ qua trong im lặng).
BASE = "https://blockpinned.com"
# --out để bản mirror công khai dựng thẳng vào docs/ (GitHub Pages chỉ phục vụ
# root hoặc /docs). Một file build duy nhất chạy được ở cả hai chỗ — chép ra bản
# thứ hai là mở đúng cửa trôi lệch mà chú thích ngay dưới đây nói tới.
OUT = ROOT / (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "out")

# ── cổng 1 dùng CHUNG danh sách từ với template/check_language.py ────────────
# Chép danh sách sang đây = hai bản sẽ lệch (luật bằng chứng của desk §13).
# Hai chỗ tìm: kho gốc (~/blockpinned/template) và cạnh chính nó (repo công khai).
# 🔴 VÁ 10/08/2026 (`OPS-T-CONG-CHI-BAO`): đường đầu SAI SUỐT TỪ ĐẦU — `ROOT` là chính
# repo công khai (`~/blockpinned-public`), nên `ROOT.parent / "template"` trỏ vào
# `~/template`, **không tồn tại**. Vòng tìm luôn rơi xuống nhánh hai, tức **bản chép
# cạnh chính nó** — và hai bản đã lệch md5 (bản chép là snapshot commit `5dcbc73`, 05/08).
# Comment ngay trên nói *"dùng CHUNG danh sách"* trong khi máy đọc bản chép ⇒ đúng ca
# `RULES.md §2c`: cổng chạy, in dòng xanh, mà đọc nhầm vật.
# 🔵 Nhánh cuối GIỮ LẠI có chủ ý: repo công khai phải build được một mình (CI, máy khác).
for _p in (ROOT.parent / "blockpinned" / "template", ROOT.parent / "template", ROOT):
    if (_p / "check_language.py").exists():
        sys.path.insert(0, str(_p))
        break
try:
    import check_language as lang
except ImportError:
    sys.exit("🔴 không import được check_language.py — cổng ngôn ngữ là bắt buộc, không có đường vòng")

# 🟡 "ĐÃ XÁC NHẬN" thêm 28/07 — desk đề xuất, user CHƯA chốt bằng chữ (LAUNCH.md:43).
# Vì sao thêm: 28/07 lần đầu một điều-bác-bỏ ghi trước ĐÃ CHẠY và claim sống sót —
# DefiLlama tự tính lại 16/07, số rơi trong khoảng desk ghi trước. Bốn trạng thái cũ
# không chở nổi việc đó: "ĐANG ĐỨNG — chưa có gì bác được" xếp một claim ĐÃ BỊ THỬ VÀ
# SỐNG SÓT chung ô với một claim CHƯA AI THỬ. Đó là hai mức bằng chứng khác hẳn nhau,
# và mức mạnh hơn đúng là thứ kênh này sinh ra để tạo.
# (PROMPT-web.md ④ gọi đây là "khoảnh khắc trung tâm của sản phẩm" — mà mô hình dữ
# liệu lại không có nó. Lỗ chỉ lộ khi khoảnh khắc đó xảy ra thật.)
TRANG_THAI = {
    "ĐÃ XÁC NHẬN": ("xac", "điều bác bỏ đã chạy — đối tượng tự tính lại, số rơi trong khoảng ghi trước"),
    "ĐANG ĐỨNG": ("song", "claim còn hiệu lực, chưa có gì bác được"),
    "ĐÃ SỬA":    ("sua",  "đã tự đính chính; giữ lại để thấy lỗi, không xoá"),
    "BỊ BÁC":    ("bac",  "bằng chứng mới đã bác claim này"),
    "CHỜ SỐ":    ("cho",  "chưa đủ dữ liệu để nói đứng hay đổ"),
}

# Khóa ở trên là schema evidence đã phát hành, không đổi theo câu chữ UI. Nhãn dưới
# đây là lớp đọc cho người ngoài: "vẫn đứng vững" chủ động nhưng vẫn thấp hơn mức
# "đã xác nhận", còn "đã bị bác bỏ" nói trọn nghĩa hơn nhãn cụt "bị bác".
TRANG_THAI_HIEN_THI = {
    "ĐÃ XÁC NHẬN": "ĐÃ XÁC NHẬN",
    "ĐANG ĐỨNG": "VẪN ĐỨNG VỮNG",
    "ĐÃ SỬA": "ĐÃ SỬA",
    "BỊ BÁC": "ĐÃ BỊ BÁC BỎ",
    "CHỜ SỐ": "CHỜ SỐ",
}

THEMES = {
    # 🟢 HỆ ĐÃ CHỐT 06/08/2026 — bản D2, user duyệt tại /thu-d2/ trên chính tên miền.
    # Nguồn: ~/blockpinned/design-v2/implement-D2/ (bp.css + NOTES.md, có số đo).
    # 🔴 BA điều cấm của hệ này, mỗi điều đều ĐO ĐƯỢC, không phải gu:
    #  ① HUE = TRẠNG THÁI CLAIM. Không tồn tại hue thứ sáu đứng cạnh được cả năm trạng
    #    thái (cam ↔ ĐÃ SỬA ΔE 11,1 dark / 8,8 light; mọi sắc đỏ ↔ BỊ BÁC 2,8–8,7) ⇒
    #    nút và link mặc MỰC, không mặc hue.
    #  ② Năm trạng thái không phân biệt được bằng màu đơn thuần (đỏ ↔ lá ΔE 2,7 deutan)
    #    ⇒ mỗi chip mang thêm GLYPH riêng + hình khối riêng. Bỏ glyph là vi phạm.
    #  ③ Cam thương hiệu cấm đứng cạnh chip trạng thái (coral ↔ BỊ BÁC ΔE 11,4 / 6,8):
    #    trong thẻ claim, khối GHIM TẠI mặc mực.
    # Nền ẤM để tone cam cầm nhịp mà không tốn hue nào — neutral có chroma ≈ 0.
    "d2": dict(paper="#faf7f2", ink="#1a1512", accent="#b8412a", accent_toi="#ff7a5c",
               muted="#5f564b", muted_toi="#a89d8f", line="#e6ded1", line_toi="#302a24",
               display="Inter", dw="800", gian_ten="-.01em",
               bg2="#f3efe7", bg2_toi="#15130f", card="#fffdfa", card_toi="#1b1815",
               inset="#f5f1ea", inset_toi="#141210",
               line_soft="#efe9df", line_soft_toi="#241f1a",
               faint="#8a8073", faint_toi="#7d7365",
               xn="#0f8a3c", xn_toi="#35c46a", song="#1d5fae", song_toi="#4d9fff",
               sua="#a16207", sua_toi="#f0b429", bac="#be123c", bac_toi="#ef4056",
               cho="#64748b", cho_toi="#94a3b8"),
    # hệ 29/07 — hướng THE BENCHMARK, GIỮ LÀM HỒ SƠ sau khi D2 được duyệt 06/08.
    # Nguồn duy nhất:
    # template/out/logo/final/he.json (do template/logo_final.py sinh ra).
    # 🔴 HAI mã rubric là BẮT BUỘC, không phải tuỳ chọn thẩm mỹ: #94382A đo được
    # 2,15:1 trên nền ink ⇒ điều cấm ② của bản khai hệ. Nền tối dùng #D26F60 (4,66).
    # muted đo lại đúng lúc lắp, ngưỡng chữ nhỏ 4,5:
    #   #66604F trên limestone = 5,00  ·  #A79E8E trên ink = 5,97
    "benchmark": dict(paper="#ECE5D8", ink="#26221C", accent="#94382A",
                      accent_toi="#D26F60", muted="#66604F", muted_toi="#A79E8E",
                      line="#D9D1C2", line_toi="#3D372E",
                      display="Marcellus", dw="400", gian_ten=".13em"),
    # hệ cũ, GIỮ LÀM HỒ SƠ chứ không phải để chọn lại: Oswald và bộ đỏ #C8231C đã
    # khai tử cùng banner 27/07 (LAUNCH §7e). Chúng còn đây để diff được với bản chốt.
    "do": dict(paper="#F4F5F2", ink="#16191B", accent="#C8231C", accent_toi="#C8231C",
               muted="#5C6670", muted_toi="#9AA0A4", line="#DCDDD8", line_toi="#3A3D40",
               display="Oswald", dw="600", gian_ten=".16em"),
    # hệ ĐỀ XUẤT từ vòng logo 1 — đã bị vòng 2 thay, giữ làm hồ sơ
    "verdigris": dict(paper="#EFEDE5", ink="#15181A", accent="#1F8A72", accent_toi="#1F8A72",
                      muted="#55584F", muted_toi="#9AA0A4", line="#DBD9D0", line_toi="#3A3D40",
                      display="Archivo", dw="700", gian_ten=".16em"),
}

# Mark chính thức, hướng THE BENCHMARK — bốn nhát đục + thanh mốc, khe 12 đơn vị.
# Chép NGUYÊN VĂN từ template/out/logo/final/mark-sang.svg; `fill` trong đó bị CSS
# `.mark path{fill:var(--accent)}` ghi đè nên MỘT bản phục vụ được cả hai nền.
MARK_SVG = (
    '<svg viewBox="0 0 240 240" aria-hidden="true">'
    '<path d="M36,60 Q120,36 204,60 Q120,84 36,60 Z"/>'
    '<path d="M120,84.0 Q142,144 120,206 Q98,144 120,84.0 Z"/>'
    '<path d="M120,84.0 Q102.1,139.9 52,174 Q69.9,116.1 120,84.0 Z"/>'
    '<path d="M120,84.0 Q137.9,139.9 188,174 Q170.1,116.1 120,84.0 Z"/>'
    "</svg>"
)

# Ảnh phục vụ: BUILDER NÀO sinh ra nó. Khai rõ vì cùng một tên file có thể tồn tại ở hai
# chỗ với hai nội dung khác nhau — 🔴 xác 30/07: `avatar-800.png` có cả ở `out/png/` (bản
# 27/07, trước khi chốt mark) và `out/logo/final/` (bản 29/07). Cổng trùng-byte quét "mọi
# chỗ sinh" nên nó nổ, và nó nổ ĐÚNG: không có cách nào biết bản nào là bản thật ngoài
# việc khai ra. Ảnh không có chủ thì không được đi ra ngoài.
# ── LOGO TOKEN, tài sản BÊN THỨ BA ───────────────────────────────────────────────
# Vì sao KHÔNG nằm chung `assets/*.png`: luật ở đó là "mọi PNG phải khai builder nào
# sinh ra nó". Năm ảnh này KHÔNG có builder — chúng là nhận diện của người khác, tải
# về. Nhét chúng vào `NGUON_ASSET` là phải bịa một builder, tức nói dối đúng chỗ cái
# bảng đó sinh ra để nói thật. Nên chúng ở `assets/token/`, và khai XUẤT XỨ ở đây.
#
# 🔵 Đơn vị kiểm là CẶP (token, nguồn) chứ không phải riêng file: một file PNG hợp lệ
# nhưng gắn nhầm token thì mọi cổng đều xanh và trang vẫn treo sai logo lên tên sai.
# Ngày tải ghi ra để lần sau còn biết bản đang phục vụ cũ tới đâu — logo đổi thì bản
# tự host đứng im, và đó là cái giá đã biết khi user chốt tự host (10/08).
LOGO_TOKEN = {
    "UNI":    ("token-uni.png",    "coingecko 12504/uniswap-logo.png",         "2026-08-10"),
    "CAKE":   ("token-cake.png",   "coingecko 12632/pancakeswap-cake-logo",    "2026-08-10"),
    "LDO":    ("token-ldo.png",    "coingecko 13573/Lido_DAO.png",             "2026-08-10"),
    "PENDLE": ("token-pendle.png", "coingecko 15069/Pendle_Logo_Normal-03",    "2026-08-10"),
    # 🔴 Bản gốc là JPEG, đã đổi sang PNG lúc tải: `kich_thuoc_png()` đọc IHDR và NỔ
    # với mọi thứ không phải PNG, nên để nguyên .jpg là chặn build ở lượt sau.
    "HYPE":   ("token-hype.png",   "coingecko 50882/hyperliquid.jpg → png",    "2026-08-10"),
    "MORPHO": ("token-morpho.png", "coingecko 29837/Morpho-token-icon.png",    "2026-08-13"),
    # 🔴 Bản gốc là JPEG (coin id `pump-fun`), đổi sang PNG bằng `sips` lúc tải — cùng
    # lý do đã ghi ở HYPE: `kich_thuoc_png()` đọc IHDR và NỔ với mọi thứ không phải PNG.
    "PUMP":   ("token-pump.png",   "coingecko 67164/pump.jpg → png",           "2026-08-14"),
    "SKY":    ("token-sky.png",    "coingecko 39925/sky.jpg → png",            "2026-08-15"),
}

NGUON_ASSET = {
    # bài SKY 15/08 — nguồn `template/card-sky-sbe-beam.html`, dựng bằng
    # `template/render_card_v2.py` và phục vụ đúng bản PNG trong `template/out/png/`.
    # Hai số trên ảnh là hai vai khác nhau của cùng cơ chế nếu executive spell được
    # thực thi: 27,77M là cấu hình mặc định sau cast; 350M là giới hạn của ví vận hành.
    # Card giữ điều kiện "nếu spell được thực thi" ngay trên tầng đọc để 350M không bị
    # hiểu thành mức chi hiện hành hay một dự báo.
    "card-sky-sbe-beam.png": "png",
    # bài MORPHO 13/08 — dựng bằng KHUÔN v2, đường đi nay đã có chủ và có cổng:
    # nguồn `template/card-morpho-oracle-thang.html` (chép từ `template/card-v2.html`,
    # chỉ thay các ô `data-o`), render bằng `template/render_card_v2.py` — tức nó QUA
    # `card_gate` VÀ qua cổng tràn khung, khác ngoại lệ dựng tay của card HYPE bên dưới.
    # Số trên ảnh ($269 ↔ $269 nghìn tỷ) là hai vế của cùng một đại lượng, lấy từ
    # `Crypto Research/MORPHO/data/frozen_market_origin_2026-08-04.json` khối `B_PAXG`.
    "card-morpho-oracle-thang.png": "png",
    # bài PUMP 14/08 — cùng đường đi có chủ như card MORPHO: nguồn
    # `template/card-pump-unlock-057.html` (chép từ `template/card-v2.html`, chỉ thay
    # các ô `data-o`), render bằng `template/render_card_v2.py` ⇒ QUA `card_gate` và
    # qua cổng tràn khung. `card_gate` đã NỔ một lần khi dựng (dải tham chiếu 227 ký
    # tự > trần 200) và được sửa bằng cách rút chữ, không gỡ cổng.
    # 🔴 Hai vế trên ảnh (0,49% ↔ 9,54%) là CÙNG một đại lượng — lượng đã bán của lượt
    # phát 14/07 ở hai cách đếm. Tỉ số 187 lần cố ý KHÔNG lên hai ô số, vì nó là đại
    # lượng khác và mẫu số của nó là một giả định chia đều; nó nằm ở dải tham chiếu,
    # nơi đủ chữ để nói "năng lực mua BÌNH QUÂN".
    # Số lấy từ `Crypto Research/PUMP/data/pump_cohort_ban_that_2026-08-13.json` và
    # `pump_cuc_time_profile_2026-08-13.json`.
    "card-pump-unlock-057.png": "png",
    "favicon-16.png":  "logo/final",
    "favicon-32.png":  "logo/final",
    "avatar-800.png":  "logo/final",
    "card-hype-doi-dau-muc.png": "png",
    # bài CAKE 10/08 — cùng quy ước tên theo NỘI DUNG, không theo ordinal.
    # Builder: template/build_card_cake_thi_phan_phi.py, số đọc thẳng từ ba artifact
    # của CAKE và có assert từ chối dựng khi cycle 10/08 đã đóng.
    "card-cake-thi-phan-phi-muc.png": "png",
    # bài HYPE 12/08 — 🔴 card này KHÔNG do một `build_card_*.py` sinh ra, và đó là
    # ngoại lệ có chủ ý được user duyệt: bản dựng bằng builder (`template/
    # build_card_hype_thi_phan_ba_cach.py`) qua được `card_gate` nhưng user bác vì
    # bố cục; bản dùng thật là HTML dựng tay, nguồn giữ ở
    # `template/experiments/card-hype-market-share-editorial-v8-FINAL.html`, render
    # bằng Chrome headless. ⇒ nó KHÔNG qua `card_gate`, và ba thứ cổng vốn kiểm đã
    # được kiểm bằng tay, ghi ở `Crypto Research/PUBLISH.md` hàng #62.
    # Số trên ảnh (37,6/22,5/18,1) trùng số trong bài và cùng nguồn artifact
    # `HYPERLIQUID/data/hype_defillama_ssr_perps_20260811.json`.
    # 🔵 Giá trị là `png` chứ KHÔNG phải `experiments`: cột này là ĐƯỜNG DẪN dưới
    # `template/out/`, không phải nhãn xuất xứ. Bản render nằm ở `template/out/png/`
    # và trùng byte với bản phục vụ (đo 12/08) ⇒ khai `png` thì phép so byte ngay
    # dưới THẬT SỰ chạy; khai `experiments` trỏ vào `template/out/experiments/` vốn
    # không tồn tại, và cổng sẽ bỏ qua trong im lặng — đúng cái bẫy mà ghi chú của
    # `card-rh-burn-cham-mot-tuan-muc.png` ngay dưới đã tự mô tả.
    "card-hype-13-hay-70.png": "png",
    "post01-card.png": "png",
    "post02-card.png": "png",
    "post04-card.png": "png",
    "post05-card.png": "png",
    # bài #6 — card không mang số thứ tự bài trong tên vì ordinal chỉ chốt lúc
    # ĐĂNG, mà builder chạy trước đó; `post06-card.png` trong template/out/png
    # đã bị bản #24 (user bác 30/07) chiếm chỗ.
    "card-uni-v4-incidence.png": "png",
    # bài #8 — cùng quy ước tên theo NỘI DUNG. Card này là bản THỨ BA của bài: hai bản
    # trước bị chính user bác vì cùng một lỗi loại — trình bày một TỶ LỆ như một PHÁN
    # QUYẾT (16,7% đối 7,81% đọc ra "v4 tệ hơn", trong khi tăng trưởng nền phí chưa đo).
    # Bản dùng là phép TÁCH: $85,36 đối $14,64 trên mỗi $100 phí swap.
    "card-uni-100usd.png": "png",
    # bài #9 — cùng quy ước tên theo NỘI DUNG, không theo ordinal.
    "card-cmv2-220.png": "png",
    # bài #7 — cùng quy ước đặt tên theo NỘI DUNG, không theo ordinal (lý do ở ghi
    # chú bài #6 ngay trên). Ca này còn là bằng chứng thứ hai cho quy ước đó: ordinal
    # bài #7 suýt phải đổi vì chân X bị dán nhầm bản nháp rồi xoá + đăng lại 31/07.
    "card-pendle-buyback.png": "png",
    # bài #10 — dựng dưới tên "bai11" (ordinal chỉ chốt lúc ĐĂNG, builder chạy trước),
    # nên đổi tên đầu ra của chính builder theo NỘI DUNG chứ không đổi tay khi chép sang
    # đây: tên lệch thì `template/out/png/<tên>` không tồn tại và phép so byte ngay dưới
    # BỎ QUA TRONG IM LẶNG. Hậu tố `-muc` là biến thể nền mực, user chốt 06/08.
    "card-rh-burn-cham-mot-tuan-muc.png": "png",
}

# Ràng buộc NGÔN NGỮ của thân bài: mặt chữ phải dựng đủ dấu tiếng Việt — đó là điều
# kiện, không phải lựa chọn thương hiệu. Trước 06/08 điều kiện này được thoả bằng cách
# nạp thêm Be Vietnam Pro làm lưới đỡ; nay nó được thoả bằng chính subset `vietnamese`
# của Inter, và điều đó ĐO ĐƯỢC (xem khối FONT_MAT). Chuỗi dự phòng cuối cùng là
# `system-ui` — mọi hệ điều hành đang chạy đều dựng đủ dấu tiếng Việt ở font hệ thống.
BODY_FONT = "system-ui"


# Tên các họ cổng — dùng cho dòng in ra, và là chỗ DUY NHẤT đếm chúng.
# Hiện vật đưa lên site — KHAI TỪNG FILE, không quét cả thư mục. Quét thư mục là
# publish thứ chưa ai đọc; mỗi dòng dưới đây là một file đã được mở ra xem.
HIEN_VAT = {
    "verify_post07_2026-07-31.json": "bài #7 — 9/9 kiểm sau đăng",
    "pendle_buy_source_2026-07-31.json": "bài #7 — 65 tx hash + chi tiết từng tx",
    "pendle_buy_tie_2026-07-31.json": "bài #7 — lượt nối swap→hợp đồng, 82,44%",
}

TEN_CONG = ["ngôn ngữ", "cấu trúc", "claim", "ngôi xưng", "đánh dấu",
            "thuộc tính số", "xem trước", "đo lại", "hạn", "quá hạn", "ghi trước", "liên kết",
            "fact", "bố cục", "visual", "tiêu đề"]

# chữ ký hàm hợp lệ: tên + danh sách kiểu, vd `balanceOf(address)` · `x()` · `f(uint256,address)`
RE_KY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\((|[a-z0-9\[\],]+)\)$")


class LoiCong(Exception):
    """Một cổng chặn build. Không có mức 'cảnh báo' — cảnh báo là thứ người ta quen mắt bỏ qua."""


# ════════════════════════════════════════════════════════════ MARKDOWN (tập con)
# Nguyên tắc: cú pháp không nằm trong tập con này thì NỔ. Một renderer im lặng bỏ
# qua một dòng có thể nuốt mất đúng dòng falsifier — và không gate nào bắt được.

RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
RE_BOLD = re.compile(r"\*\*([^*]+)\*\*")
RE_ITAL = re.compile(r"\*([^*]+)\*")
RE_CODE = re.compile(r"`([^`]+)`")
# ký tự mở đầu dòng có nghĩa trong markdown mà tập con này KHÔNG xử lý
RE_LA = re.compile(r"^\s*(?:>|!\[|={3,}|\*\s|\+\s|#{4,}\s|\[\^)")


def inline(s: str, o: str) -> str:
    """Bold/italic/code/link. Code xử lý TRƯỚC để ** trong code không bị đọc là đậm."""
    giu: list[str] = []

    def cat(m):
        giu.append(f'<code>{ihtml.escape(m.group(1))}</code>')
        return f"\x00{len(giu)-1}\x00"

    s = RE_CODE.sub(cat, s)
    if "`" in s:
        raise LoiCong(f"backtick lẻ (code span không đóng) — {o}: {s.strip()[:70]}")
    s = ihtml.escape(s)
    s = RE_LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = RE_BOLD.sub(r"<strong>\1</strong>", s)
    s = RE_ITAL.sub(r"<em>\1</em>", s)
    if "**" in s:
        raise LoiCong(f"còn sót ** sau khi render — {o}: {s.strip()[:70]}")
    for i, c in enumerate(giu):
        s = s.replace(f"\x00{i}\x00", c)
    return s


RE_VISUAL = re.compile(r"^\{\{visual:([a-z0-9-]+)\}\}$")
VISUAL_TYPES = {"flow", "proof", "timeline", "distribution", "dai", "comparison",
                "opposite-direction", "system-map", "waterfall"}
# `dai` thêm 12/08. Bốn khuôn kia đều giả định các mục là những thứ KHÁC NHAU — chặng
# nối tiếp, vòng kiểm, mốc thời gian, nhóm cộng thành tổng. Không khuôn nào chở được
# hình dạng "CÙNG MỘT đại lượng, nhiều con số cùng hợp lệ, rải trên một trục" — mà đó
# đúng là luận điểm lõi của bài HYPE 12/08 (5 nguồn công bố 5 con số cho một câu hỏi;
# 3 cách xếp loại hợp lệ cho 3 tỷ lệ từ cùng một lượng giao dịch). Ép nó thành
# `distribution` là nói dối: các con số đó KHÔNG cộng lại thành gì cả.
# 🔵 Có sẵn `dai-ba-diem` trong `khoi_viz`, nhưng khuôn đó khoá cứng ĐÚNG ba điểm và
# chỉ phục vụ thẻ trang chủ — không có bảng dữ liệu mở ra, không neo claim.
VISUAL_TONES = {"accent", "good", "warn", "bad", "info", "muted"}


def _bang_visual(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{ihtml.escape(str(c))}</th>" for c in headers)
    body = "".join(
        "<tr>" + "".join(
            f'<td data-label="{ihtml.escape(str(headers[n]), quote=True)}">'
            f'{ihtml.escape(str(c))}</td>'
            for n, c in enumerate(row)
        ) + "</tr>" for row in rows
    )
    return f'<div class="bang"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _bo_cham_trang_thai_primer(html: str) -> str:
    """Ẩn emoji trạng thái/cảnh báo khỏi mặt đọc; câu chặn vẫn còn nguyên."""
    for symbol in ("🔴", "🟢", "🔵", "⚪", "⚠️", "⚠"):
        html = html.replace(symbol, "")
    return html


def _hien_dai(x: dict) -> str:
    """Chuỗi hiện ra cho một điểm của `dai`.

    🔵 Vì sao có `hien` riêng thay vì luôn format từ `value`: bài viết "13%" và "44%",
    còn `so_vn(13.0, 1)` ra "13,0". Hình mà ghi khác thân bài một chữ số thì người đọc
    phải dừng lại hỏi cái nào đúng — mà cả hai đều đúng. `value` vẫn BẮT BUỘC là số, vì
    vị trí trên trục tính từ nó; `hien` chỉ đổi cách viết, không đổi chỗ đứng.
    """
    return str(x.get("hien") or so_vn(float(x["value"]), 1))


def _du_lieu_visual(v: dict) -> tuple[list[str], list[list[str]]]:
    """Một cấu hình sinh CẢ visual lẫn bảng kiểm — không có bản số thứ hai để trôi."""
    if v["type"] == "system-map":
        edges = v["edges"]
        return (["tầng", "nút", "vai trò", "đường ra"],
                [[lane["label"], node["value"], node["note"],
                  " · ".join(e["label"] for e in edges if e["from"] == node["id"]) or "—"]
                 for lane in v["lanes"] for node in lane["nodes"]])
    if v["type"] == "waterfall":
        ten = {"start": "đầu kỳ", "change": "thay đổi", "total": "kết quả"}
        return (["vai trò", "dòng", "giá trị", "đọc là"],
                [[ten[x["kind"]], x["label"], x["hien"], x["note"]] for x in v["items"]])
    if v["type"] == "comparison":
        return (["thang", "tham số", "hệ số", "kết quả"],
                [[x["label"], " · ".join(f'{f["label"]}: {f["value"]}' for f in x["facts"]),
                  x["scale"], x["result"]] for x in v["sides"]])
    if v["type"] == "opposite-direction":
        return (["giai đoạn"] + [x["label"] for x in v["series"]],
                [[f'{stage["label"]} — {stage["note"]}']
                 + [str(series["values"][n]["hien"]) for series in v["series"]]
                 for n, stage in enumerate(v["stages"])])
    if v["type"] == "flow":
        return (["chặng", "số đọc", "ý nghĩa tại mốc"],
                [[x["label"], x["value"], x["note"]] for x in v["steps"]])
    if v["type"] == "proof":
        return (["phép thử", "hỏi gì", "kết quả"],
                [[x["label"], x["question"], f'{x["value"]} — {x["note"]}']
                 for x in v["steps"]])
    if v["type"] == "timeline":
        return (["ngày", v.get("unit", "giá trị"), "cách lần trước"],
                [[x["label"], x["value"], x.get("gap", "—")] for x in v["events"]])
    if v["type"] == "dai":
        dv = v.get("don_vi", "")
        return ([v.get("cot", "nguồn"), f"giá trị{f' ({dv})' if dv else ''}", "khai gì"],
                [[x["label"], _hien_dai(x), x["note"]] for x in v["diem"]])
    return (["nhóm", "số mục", "đọc là"],
            [[x["label"], str(x["count"]), x["note"]] for x in v["segments"]])


def render_visual(v: dict, show_claim_refs: bool = True, chapter: str = "",
                  art_direction: str = "") -> str:
    headers, rows = _du_lieu_visual(v)
    bang_html = _bang_visual(headers, rows)
    # D2 là đường rollback: không mượn CSS v3, nhưng dữ liệu không được biến mất.
    # Cùng cấu hình vì thế rơi về bảng đầy đủ thay vì để lộ directive hoặc chữ trần.
    if BO_CUC != "v3":
        return bang_html

    vid, loai = v["id"], v["type"]
    may_bon_van = art_direction == "machine-valves" and bool(chapter)
    if loai == "system-map":
        if may_bon_van:
            stations = []
            for n, lane in enumerate(v["lanes"], 1):
                nodes = "".join(
                    f'<article class="pm-node tone-{node.get("tone", "accent")}">'
                    f'<span>{ihtml.escape(node["label"])}</span>'
                    f'<strong>{ihtml.escape(node["value"])}</strong>'
                    f'<small>{ihtml.escape(node["note"])}</small></article>'
                    for node in lane["nodes"])
                stations.append(
                    f'<section class="pm-station"><header><b>{n:02d}</b><div>'
                    f'<span>{ihtml.escape(lane["label"])}</span>'
                    f'<small>{ihtml.escape(lane["note"])}</small></div></header>{nodes}</section>')
                if n < len(v["lanes"]):
                    ids_here = {node["id"] for node in lane["nodes"]}
                    ids_next = {node["id"] for node in v["lanes"][n]["nodes"]}
                    labels = [e["label"] for e in v["edges"]
                              if e["from"] in ids_here and e["to"] in ids_next]
                    stations.append(
                        '<div class="pm-valve" aria-hidden="true"><i></i>'
                        + "".join(f'<span>{ihtml.escape(label)}</span>' for label in labels)
                        + '</div>')
            than = (f'<span class="pm-map-ghost" aria-hidden="true">MÁY</span>'
                    f'<div class="pm-machine" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">'
                    f'{"".join(stations)}</div>')
        else:
            lane_html = []
            for n, lane in enumerate(v["lanes"], 1):
                nodes = "".join(
                    f'<article class="av-system-node tone-{node.get("tone", "accent")}">'
                    f'<span>{ihtml.escape(node["label"])}</span>'
                    f'<strong>{ihtml.escape(node["value"])}</strong>'
                    f'<small>{ihtml.escape(node["note"])}</small></article>'
                    for node in lane["nodes"])
                lane_html.append(
                    f'<section class="av-system-lane"><header><b>{n:02d}</b><div>'
                    f'<span>{ihtml.escape(lane["label"])}</span>'
                    f'<small>{ihtml.escape(lane["note"])}</small></div></header>{nodes}</section>')
            edge_html = "".join(
                f'<li><code>{ihtml.escape(e["from"])}</code><i aria-hidden="true">→</i>'
                f'<code>{ihtml.escape(e["to"])}</code><span>{ihtml.escape(e["label"])}</span></li>'
                for e in v["edges"])
            than = (f'<div class="av-system" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">'
                    f'<div class="av-system-lanes">{"".join(lane_html)}</div>'
                    f'<ol class="av-system-edges" aria-label="Quan hệ giữa các tầng">{edge_html}</ol></div>')
    elif loai == "waterfall":
        lon = max(abs(float(x["value"])) for x in v["items"])
        item_html = []
        for x in v["items"]:
            rong = max(8.0, abs(float(x["value"])) / lon * 100)
            if may_bon_van:
                phep = "−" if x["kind"] == "change" else "=" if x["kind"] == "total" else ""
                hien = str(x["hien"]).lstrip("−-") if x["kind"] == "change" else str(x["hien"])
                item_html.append(
                    f'<div class="pm-sub-row is-{x["kind"]} tone-{x.get("tone", "accent")}">'
                    f'<span class="pm-sub-op" aria-hidden="true">{phep}</span>'
                    f'<div class="pm-sub-label"><span>{ihtml.escape(x["label"])}</span>'
                    f'<small>{ihtml.escape(x["note"])}</small></div>'
                    f'<b class="pm-sub-figure">{ihtml.escape(hien)}</b>'
                    f'<i class="pm-sub-bar" style="--w:{rong:.2f}%"></i></div>')
            else:
                item_html.append(
                    f'<li class="is-{x["kind"]} tone-{x.get("tone", "accent")}">'
                    f'<span>{ihtml.escape(x["label"])}</span>'
                    f'<div><i style="--w:{rong:.2f}%"></i></div>'
                    f'<strong>{ihtml.escape(x["hien"])}</strong>'
                    f'<small>{ihtml.escape(x["note"])}</small></li>')
        if may_bon_van:
            than = (f'<div class="pm-subtraction" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">{"".join(item_html)}</div>')
        else:
            than = (f'<ol class="av-waterfall" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">{"".join(item_html)}</ol>')
    elif loai == "comparison":
        ben = []
        for x in v["sides"]:
            # Số dài chỉ được ngắt ở dấu phân nhóm, không bẻ giữa một cụm chữ số.
            ket_qua = ihtml.escape(x["result"]).replace(".", ".<wbr>")
            ben.append(
                f'<article class="av-compare-side tone-{x.get("tone", "accent")}">'
                f'<p>{ihtml.escape(x["label"])}</p><div class="av-compare-facts">'
                + "".join(f'<span><small>{ihtml.escape(f["label"])}</small>'
                          f'<strong>{ihtml.escape(f["value"])}</strong></span>' for f in x["facts"])
                + f'</div><div class="av-compare-scale"><small>{ihtml.escape(x["scale_label"])}</small>'
                  f'<strong>{ihtml.escape(x["scale"])}</strong></div>'
                  f'<div class="av-compare-result"><small>{ihtml.escape(x["result_label"])}</small>'
                  f'<strong>{ket_qua}</strong><p>{ihtml.escape(x["note"])}</p></div></article>')
        than = (
            '<div class="av-compare" role="img" aria-label="{}">'
            '<div class="av-compare-input"><small>{}</small><strong>{}</strong></div>'
            '<div class="av-compare-grid">{}<div class="av-compare-gap"><strong>{}</strong><small>{}</small></div>{}</div>'
            '</div>').format(
                ihtml.escape(v["aria"], quote=True), ihtml.escape(v["input_label"]),
                ihtml.escape(v["input_value"]), ben[0], ihtml.escape(v["gap_value"]),
                ihtml.escape(v["gap_label"]), ben[1])
    elif loai == "opposite-direction":
        chuoi = []
        for series in v["series"]:
            diem = []
            truoc = None
            for stage, value in zip(v["stages"], series["values"]):
                so = float(value["value"])
                huong = ("is-start" if truoc is None else
                         "is-up" if so > truoc else "is-down" if so < truoc else "is-flat")
                diem.append(
                    f'<li class="{huong}"><small>{ihtml.escape(stage["label"])}</small>'
                    f'<strong>{ihtml.escape(str(value["hien"]))}</strong>'
                    f'<span>{ihtml.escape(stage["note"])}</span></li>')
                truoc = so
            chuoi.append(
                f'<article class="av-opp-series tone-{series.get("tone", "accent")}">'
                f'<header><div><small>{ihtml.escape(series["label"])}</small>'
                f'<p>{ihtml.escape(series["note"])}</p></div>'
                f'<strong>{ihtml.escape(series["summary"])}</strong></header>'
                f'<ol>{"".join(diem)}</ol></article>')
        than = (f'<div class="av-opposite" role="img" '
                f'aria-label="{ihtml.escape(v["aria"], quote=True)}">{"".join(chuoi)}</div>')
    elif loai == "flow":
        than = '<div class="av-flow" role="img" aria-label="{}">{}</div>'.format(
            ihtml.escape(v["aria"], quote=True), "".join(
                f'<article class="av-node tone-{x.get("tone", "accent")}">'
                f'<span>{ihtml.escape(x["label"])}</span><strong>{ihtml.escape(x["value"])}</strong>'
                f'<small>{ihtml.escape(x["note"])}</small></article>' for x in v["steps"]))
    elif loai == "proof":
        than = '<ol class="av-proof" aria-label="{}">{}</ol>'.format(
            ihtml.escape(v["aria"], quote=True), "".join(
                f'<li class="tone-{x.get("tone", "accent")}"><span>{n:02d}</span><div>'
                f'<small>{ihtml.escape(x["label"])}</small><strong>{ihtml.escape(x["value"])}</strong>'
                f'<p>{ihtml.escape(x["note"])}</p></div></li>'
                for n, x in enumerate(v["steps"], 1)))
    elif loai == "timeline":
        lon = max(float(x["magnitude"]) for x in v["events"])
        diem = []
        for x in v["events"]:
            cao = max(12.0, float(x["magnitude"]) / lon * 100)
            if may_bon_van:
                ky, co, chot = str(x.get("gap", "—")).partition(" · ")
                diem.append(
                    f'<div class="pm-ledger-row tone-{x.get("tone", "info")}" style="--m:{cao:.2f}">'
                    f'<b>{ihtml.escape(x["label"])}</b><div class="pm-ledger-period">'
                    f'<span>{ihtml.escape(ky)}</span>'
                    f'{f"<small>{ihtml.escape(chot)}</small>" if co else ""}</div>'
                    f'<div class="pm-ledger-amount"><i></i><b>{ihtml.escape(x["value"])}</b></div></div>')
            else:
                diem.append(
                    f'<span class="av-time tone-{x.get("tone", "info")}">'
                    f'<i style="--m:{cao:.2f}%"></i><b>{ihtml.escape(x["label"])}</b>'
                    f'<strong>{ihtml.escape(x["value"])}</strong><small>{ihtml.escape(x.get("gap", "—"))}</small></span>')
        if may_bon_van:
            than = (f'<div class="pm-ledger" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">'
                    f'<div class="pm-ledger-row pm-ledger-head" aria-hidden="true">'
                    f'<span>Tháng ghi nhận</span><span>Kỳ economics · ngày chốt</span>'
                    f'<span>{ihtml.escape(v.get("unit", "giá trị"))}</span></div>{"".join(diem)}</div>')
        else:
            than = (f'<div class="av-timeline" tabindex="0" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">{"".join(diem)}</div>')
    elif loai == "dai":
        # 🔴 KHAI GIÁ TRỊ, KHÔNG KHAI VỊ TRÍ — cùng luật `khoi_viz` đã ghi: vị trí là
        # KẾT QUẢ của một phép tính; khai kết quả thì lượt sửa số sau không kéo hình đi
        # theo, và cổng ⑥ vẫn thấy một toạ độ hợp lệ nên không ai bắt được.
        # 🔵 Chữ KHÔNG bám vào trục. Nhãn đặt tuyệt đối trên trục là ứng viên tràn số
        # một ở khổ 360px, và khi các giá trị xúm lại một chỗ thì chúng đè lên nhau mà
        # phép đo tràn vẫn xanh. Trục chỉ chở CHẤM; chữ xuống danh sách bên dưới.
        gt = [float(x["value"]) for x in v["diem"]]
        nho, lon = min(gt), max(gt)
        dv = v.get("don_vi", "")
        dat = lambda x: DAI_TRAI + (x - nho) / (lon - nho) * (DAI_PHAI - DAI_TRAI)
        than = (
            '<div class="av-dai-boc">'
            f'<div class="av-dai" role="img" aria-label="{ihtml.escape(v["aria"], quote=True)}">'
            '<div class="av-dai-truc">'
            + "".join(f'<span class="av-dai-cham tone-{x.get("tone", "accent")}" '
                      f'style="--p:{dat(float(x["value"])):.2f}%"></span>' for x in v["diem"])
            + '</div><div class="av-dai-moc">'
            # Mốc hai đầu lấy `hien` của CHÍNH điểm nhỏ nhất/lớn nhất, không format lại
            # từ số — nếu không thì trục ghi "13,0%" trong khi danh sách ngay dưới và
            # thân bài đều ghi "13%", và người đọc phải dừng lại hỏi cái nào đúng.
            f'<span>{ihtml.escape(_hien_dai(min(v["diem"], key=lambda x: float(x["value"]))) + dv)}</span>'
            f'<span>{ihtml.escape(_hien_dai(max(v["diem"], key=lambda x: float(x["value"]))) + dv)}</span></div></div>'
            '<ol class="av-dai-chu">'
            + "".join(f'<li class="tone-{x.get("tone", "accent")}"><i></i>'
                      f'<b>{ihtml.escape(_hien_dai(x) + dv)}</b>'
                      f'<span>{ihtml.escape(x["label"])}</span>'
                      f'<small>{ihtml.escape(x["note"])}</small></li>' for x in v["diem"])
            + "</ol></div>")
    else:
        if may_bon_van:
            rows = []
            for x in v["segments"]:
                tone = x.get("tone", "accent")
                pipe = "pm-pipe-flow" if tone == "good" else "pm-pipe-shut" if tone == "bad" else "pm-pipe-dot"
                rows.append(
                    f'<div class="pm-capture-row tone-{tone}"><b>{x["count"]}</b>'
                    f'<div class="pm-capture-label"><span>{ihtml.escape(x["label"])}</span>'
                    f'<small>{ihtml.escape(x["note"])}</small></div>'
                    f'<div class="pm-capture-pipes">'
                    + "".join(f'<i class="{pipe}"></i>' for _ in range(x["count"]))
                    + '</div></div>')
            than = (f'<div class="pm-capture" role="img" '
                    f'aria-label="{ihtml.escape(v["aria"], quote=True)}">{"".join(rows)}</div>')
        else:
            than = '<div class="av-distribution" role="img" aria-label="{}"><div class="av-dist-bar">{}</div><div class="av-dist-legend">{}</div></div>'.format(
                ihtml.escape(v["aria"], quote=True),
                "".join(f'<i class="tone-{x.get("tone", "accent")}" style="--n:{x["count"]}"></i>'
                        for x in v["segments"]),
                "".join(f'<span class="tone-{x.get("tone", "accent")}"><i></i><b>{x["count"]}</b>'
                        f'<small>{ihtml.escape(x["label"])}</small></span>' for x in v["segments"]))

    if show_claim_refs:
        claims = " · ".join(
            f'<a href="#{ihtml.escape(cid, quote=True)}">{ihtml.escape(cid)}</a>'
            for cid in v["claims"])
        scope = f'<span>neo vào claim {claims}</span>'
    else:
        # Primer là mặt public dành cho người đọc, không phải giao diện
        # của desk. Provenance nội bộ vẫn nằm trong cấu hình và đi qua
        # `cong_visuals`; chỉ con trỏ file/claim không được lọ ra caption.
        scope = (f'<span class="article-viz-scope">'
                 f'{ihtml.escape(v["public_scope"])}</span>')
    if may_bon_van:
        them = " primer-chapter-map" if loai == "system-map" else ""
        return f'''<figure class="article-viz article-viz-{loai} primer-chapter{them}" id="visual-{vid}" data-chapter="{chapter}" data-spotlight>
  <div class="primer-chapter-inner">
  <header class="article-viz-head primer-chapter-head"><span class="primer-chapter-no" aria-hidden="true">{chapter}</span><div><p>{ihtml.escape(v.get("eyebrow", loai).upper())}</p><h3>{ihtml.escape(v["title"])}</h3></div></header>
  {than}
  <figcaption><span>{ihtml.escape(v["caption"])}</span>{scope}</figcaption>
  <details class="article-viz-data"><summary>Dữ liệu đứng sau hình <span>mở bảng ↓</span></summary>{bang_html}</details>
  </div>
</figure>'''
    return f'''<figure class="article-viz article-viz-{loai}" id="visual-{vid}" data-spotlight>
  <div class="article-viz-head"><p>{ihtml.escape(v.get("eyebrow", loai).upper())}</p><h3>{ihtml.escape(v["title"])}</h3></div>
  {than}
  <figcaption><span>{ihtml.escape(v["caption"])}</span>{scope}</figcaption>
  <details class="article-viz-data"><summary>Dữ liệu đứng sau hình <span>mở bảng ↓</span></summary>{bang_html}</details>
</figure>'''


def render(md: str, o: str, visuals: list | None = None,
           show_claim_refs: bool = True, visual_chapters: dict | None = None,
           art_direction: str = "") -> str:
    visual_map = {v["id"]: v for v in (visuals or [])}
    lines, out, i = md.split("\n"), [], 0
    while i < len(lines):
        ln = lines[i]

        if not ln.strip():
            i += 1
            continue

        vm = RE_VISUAL.fullmatch(ln.strip())
        if vm:
            if vm.group(1) not in visual_map:
                raise LoiCong(f"visual '{vm.group(1)}' có marker nhưng thiếu cấu hình — {o}")
            vid = vm.group(1)
            out.append(render_visual(visual_map[vid], show_claim_refs,
                                     (visual_chapters or {}).get(vid, ""), art_direction))
            i += 1; continue

        if ln.startswith("```"):                                    # khối code
            lang_ = ln[3:].strip()
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            if j >= len(lines):
                raise LoiCong(f"khối ``` không đóng — {o}")
            allocation = _so_do_phan_bo_primer(buf) if art_direction == "machine-valves" else ""
            if allocation:
                out.append(allocation)
            else:
                cls = f' class="l-{lang_}"' if lang_ else ""
                out.append(f'<pre{cls}><code>{ihtml.escape(chr(10).join(buf))}</code></pre>')
            i = j + 1
            continue

        if ln.startswith("## "):
            t = inline(ln[3:].strip(), o)
            out.append(f'<h2 id="{slug(ln[3:])}">{t}</h2>'); i += 1; continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:].strip(), o)}</h3>"); i += 1; continue
        if ln.startswith("# "):
            raise LoiCong(f"'# ' không dùng trong thân bài (tiêu đề lấy từ front matter) — {o}")

        if ln.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].lstrip())
                i += 1
            doan, hien_tai = [], []
            for q in quote + [""]:
                if q:
                    hien_tai.append(q)
                elif hien_tai:
                    doan.append(" ".join(hien_tai)); hien_tai = []
            out.append('<blockquote class="trich">' +
                       "".join(f"<p>{inline(p, o)}</p>" for p in doan) + "</blockquote>")
            continue

        if ln.strip() == "---":
            out.append("<hr>"); i += 1; continue

        if ln.lstrip().startswith("|"):                             # bảng
            blk = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                blk.append(lines[i].strip()); i += 1
            out.append(bang(blk, o)); continue

        if re.match(r"^\d+\.\s", ln) or ln.startswith("- "):        # danh sách
            tag = "ol" if re.match(r"^\d+\.\s", ln) else "ul"
            items = []
            while i < len(lines):
                m = re.match(r"^(?:\d+\.|-)\s+(.*)$", lines[i])
                if not m:
                    if lines[i].startswith("   ") and items:       # dòng nối tiếp
                        items[-1] += " " + lines[i].strip(); i += 1; continue
                    break
                items.append(m.group(1)); i += 1
            body = "".join(f"<li>{inline(x, o)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>"); continue

        if RE_LA.match(ln):                                         # ← cổng 5
            raise LoiCong(f"cú pháp markdown không nằm trong tập con — {o}: {ln.strip()[:70]}")

        para = [ln]                                                 # đoạn văn
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(```|#{1,3}\s|\||-\s|\d+\.\s|---$|\{\{visual:)", lines[i].lstrip()):
            para.append(lines[i]); i += 1
        van = inline(" ".join(x.strip() for x in para), o)
        if para[0].startswith(("🔴", "⚠️")):
            out.append(f'<div class="chan"><p>{van}</p></div>')
        else:
            out.append(f'<p>{van}</p>')

    return "\n".join(out)


def _so_do_phan_bo_primer(lines: list[str]) -> str:
    """Đổi đúng cây phân bổ trong Primer thành flow; mọi nhãn vẫn đọc từ markdown."""
    if len(lines) != 4 or lines[0].strip() != "Net Revenue":
        return ""
    nhanh_mot = re.fullmatch(r"\s*├─\s*(.+?)\s*→\s*(.+?)\s*", lines[1])
    ghi_chu = re.fullmatch(r"\s*│\s*(.+?)\s*", lines[2])
    nhanh_hai = re.fullmatch(r"\s*└─\s*(.+?)\s*→\s*(.+?)\s*", lines[3])
    if not (nhanh_mot and ghi_chu and nhanh_hai):
        return ""
    nhanh = ((nhanh_mot.group(1), nhanh_mot.group(2), ghi_chu.group(1)),
             (nhanh_hai.group(1), nhanh_hai.group(2), ""))
    cards = "".join(
        f'<article><b>{ihtml.escape(ty_le)}</b><span>{ihtml.escape(ten.strip(chr(34)))}</span>'
        f'{f"<small>{ihtml.escape(note)}</small>" if note else ""}</article>'
        for ty_le, ten, note in nhanh)
    return (f'<section class="primer-allocation" aria-label="Sơ đồ phân bổ từ Net Revenue">'
            f'<header>{ihtml.escape(lines[0].strip())}</header><div>{cards}</div></section>')


def _loai_bang(headers: list[str], data_rows: list[list[str]]) -> str:
    """Gắn vai trình bày từ chính header/nhãn; không duy trì registry dữ liệu thứ hai."""
    sach = tuple(re.sub(r"[*_`]", "", c).strip().casefold() for c in headers)
    if sach == ("cách so", "kết quả"):
        return "table-compare"
    if sach == ("bước", "ai làm", "lấy từ đâu"):
        return "table-process"
    if sach == ("đường về tay ai đó", "trạng thái tại lần đo"):
        return "table-status"
    if all(not c for c in sach):
        cot_dau = " ".join(re.sub(r"[*_`]", "", r[0]).casefold()
                           for r in data_rows if r)
        if "stablecoin lưu hành" in cot_dau:
            return "table-finance"
        if "chi phí trực tiếp" in cot_dau:
            return "table-costs"
        if "tổng cung sky" in cot_dau:
            return "table-chain"
        if "sky protocol" in cot_dau:
            return "table-actors"
    return ""


def bang(blk: list[str], o: str) -> str:
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in blk]
    if len(rows) < 2 or not all(set(c) <= set("-: ") for c in rows[1]):
        raise LoiCong(f"bảng thiếu dòng ngăn cách '|---|' — {o}")
    headers, data_rows = rows[0], rows[2:]
    kind = _loai_bang(headers, data_rows)
    head = "".join(f"<th>{inline(c, o)}</th>" for c in headers)
    bar_values = []
    if kind == "table-costs":
        for row in data_rows:
            m = re.search(r"\d[\d.,]*", re.sub(r"[*_`]", "", row[1])) if len(row) > 1 else None
            bar_values.append(float(m.group(0).replace(".", "").replace(",", ".")) if m else 0.0)
    bar_max = max(bar_values, default=0.0)
    body_rows = []
    for row_no, row in enumerate(data_rows):
        row_class = ""
        if kind == "table-status" and len(row) > 1:
            row_class = (' status-live' if row[1].startswith("🟢") else
                         ' status-closed' if row[1].startswith("🔴") else
                         ' status-indirect' if row[1].startswith("⚪") else "")
        cells = "".join(
            f'<td data-col="{ihtml.escape(re.sub(r"[*_`]", "", headers[n]), quote=True)}">'
            f'{inline(c, o)}</td>' for n, c in enumerate(row))
        attrs = f' class="{row_class.strip()}"' if row_class else ""
        if kind == "table-costs" and bar_max:
            attrs += f' style="--bar:{bar_values[row_no] / bar_max * 100:.2f}%"'
        body_rows.append(f'<tr{attrs}>{cells}</tr>')
    table_classes = []
    if all(not c for c in headers):
        table_classes.append("table-key-value")
    if kind:
        table_classes.append(kind)
    table_attr = f' class="{" ".join(table_classes)}"' if table_classes else ""
    wrap_class = "cuon table-module" if kind else "cuon"
    return (f'<div class="{wrap_class}"><table{table_attr}><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table></div>')


def _gom_snapshot_primer(story: str, recap_id: str, o: str) -> str:
    """Giữ recap thành một mạch đọc; gom đúng ba bảng vào financial data sheet."""
    lines, out = story.splitlines(), []
    panels = {"table-finance": "finance", "table-costs": "costs", "table-chain": "chain"}
    found = set()
    for line in lines:
        kind = next((name for name in panels if f" {name}" in line), "")
        if kind and line.startswith('<div class="bang table-module">'):
            if not out or not out[-1].startswith("<p>"):
                raise LoiCong(f"snapshot Primer thiếu heading ngay trước {kind} — {o}")
            title = out.pop()
            panel = panels[kind]
            # Snapshot là bảng báo cáo, không phải data-card. Đổi vai ngay trong
            # markup để nó không còn phụ thuộc vào việc CSS override thắng grid cũ.
            line, changed = re.subn(
                rf'(?<=\s){re.escape(kind)}(?=(?:\s|"))',
                f"report-{panel}", line, count=1)
            if changed != 1:
                raise LoiCong(f"snapshot Primer không đổi được vai bảng {kind} — {o}")
            out.append(f'<section class="snapshot-panel snapshot-panel-{panel}">{title}{line}</section>')
            found.add(kind)
        else:
            out.append(line)
    if found != set(panels):
        raise LoiCong(f"snapshot Primer thiếu bảng để gom: {sorted(set(panels) - found)} — {o}")
    story = "\n".join(out)
    marker = f'<h2 id="{recap_id}">'
    recap_heading = story.find(marker)
    if recap_heading < 0:
        raise LoiCong(f"snapshot Primer thiếu heading recap để gom — {o}")
    recap_start = story.find("</h2>", recap_heading) + len("</h2>")
    snapshot_heading = story.find("\n<h2 ", recap_start)
    first_panel = story.find('<section class="snapshot-panel snapshot-panel-finance">',
                             snapshot_heading)
    if snapshot_heading < 0 or first_panel < 0:
        raise LoiCong(f"snapshot Primer thiếu heading hoặc panel ảnh chụp — {o}")
    snapshot_start = story.find("</h2>", snapshot_heading) + len("</h2>")
    snapshot_end = story.find("\n<h2 ", first_panel)
    if snapshot_start <= snapshot_heading or snapshot_end < 0:
        raise LoiCong(f"snapshot Primer thiếu ranh giới để đóng report form — {o}")
    return (story[:recap_start] + '\n<section class="primer-recap">'
            + story[recap_start:snapshot_heading] + "\n</section>"
            + story[snapshot_heading:snapshot_start]
            + '\n<section class="primer-snapshot-suite">'
            + story[snapshot_start:snapshot_end] + "\n</section>" + story[snapshot_end:])


def slug(s: str) -> str:
    s = s.strip().lower()
    for a, b in zip("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ",
                    "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd"):
        s = s.replace(a, b)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")[:60]


def front(raw: str, o: str) -> tuple[dict, str]:
    if not raw.startswith("---\n"):
        raise LoiCong(f"thiếu front matter — {o}")
    end = raw.index("\n---\n", 3)
    fm = {}
    for ln in raw[4:end].split("\n"):
        if not ln.strip():
            continue
        if ":" not in ln:
            raise LoiCong(f"dòng front matter không có ':' — {o}: {ln[:60]}")
        if ln.startswith(" "):
            raise LoiCong(f"front matter chỉ nhận key:value phẳng, không lồng — {o}: {ln[:60]}")
        k, v = ln.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, raw[end + 5:]


# ═══════════════════════════════════════════════════════════════════════ CỔNG

def cong_visuals(body: str, visuals, claims: list, o: str) -> None:
    """Cổng visual — marker, cấu hình, claim nguồn và hình dạng phải khớp một-một.

    Một visual đẹp nhưng mất claim nguồn là infographic; một marker không cấu hình
    là chữ lạ lọt ra trang; hai cấu hình cùng id làm lần dựng phụ thuộc thứ tự. Cả ba
    đều phải nổ trước khi HTML được viết.
    """
    visuals = visuals or []
    if not isinstance(visuals, list):
        raise LoiCong(f"'visuals' phải là danh sách — {o}")
    marker = re.findall(r"^\{\{visual:([a-z0-9-]+)\}\}$", body, re.M)
    if len(marker) != len(set(marker)):
        raise LoiCong(f"marker visual bị lặp — mỗi visual chỉ được đặt một chỗ — {o}")
    ids_claim = {c["id"] for c in claims}
    ids = []
    for v in visuals:
        if not isinstance(v, dict):
            raise LoiCong(f"mỗi visual phải là object — {o}")
        for k in ("id", "type", "title", "aria", "caption", "claims"):
            if not v.get(k):
                raise LoiCong(f"visual thiếu '{k}' — {o}")
        vid = str(v["id"])
        if not re.fullmatch(r"[a-z0-9-]+", vid):
            raise LoiCong(f"id visual phải dạng a-z/0-9/gạch ngang — {o}: {vid!r}")
        ids.append(vid)
        if v["type"] not in VISUAL_TYPES:
            raise LoiCong(f"visual {vid} có type lạ {v['type']!r}; chỉ nhận {sorted(VISUAL_TYPES)} — {o}")
        if len(str(v["aria"]).strip()) < 20 or len(str(v["caption"]).strip()) < 12:
            raise LoiCong(f"visual {vid} thiếu mô tả đọc màn hình/caption có nghĩa — {o}")
        if not isinstance(v["claims"], list) or not v["claims"]:
            raise LoiCong(f"visual {vid} phải neo vào ít nhất một claim — {o}")
        la = sorted(set(v["claims"]) - ids_claim)
        if la:
            raise LoiCong(f"visual {vid} neo vào claim không tồn tại: {la} — {o}")

        if v["type"] == "comparison":
            thieu_dau = sorted(k for k in ("input_label", "input_value", "gap_value", "gap_label")
                              if not v.get(k))
            if thieu_dau:
                raise LoiCong(f"visual {vid} thiếu {thieu_dau} — {o}")
        if v["type"] == "opposite-direction":
            stages = v.get("stages")
            if not isinstance(stages, list) or not 3 <= len(stages) <= 6:
                raise LoiCong(f"visual {vid}.stages phải có 3–6 mốc — {o}")
            for stage in stages:
                if (not isinstance(stage, dict) or not stage.get("label")
                        or not stage.get("note")):
                    raise LoiCong(f"visual {vid}.stages mỗi mốc cần label/note — {o}")
            series = v.get("series")
            if not isinstance(series, list) or len(series) != 2:
                raise LoiCong(f"visual {vid}.series phải có đúng 2 chuỗi — {o}")
            bien = []
            for s in series:
                if not isinstance(s, dict):
                    raise LoiCong(f"visual {vid}.series phải chứa object — {o}")
                thieu = sorted(k for k in ("label", "note", "summary", "values")
                              if s.get(k) in (None, ""))
                if thieu:
                    raise LoiCong(f"visual {vid}.series thiếu {thieu} — {o}")
                if s.get("tone", "accent") not in VISUAL_TONES:
                    raise LoiCong(f"visual {vid} có tone lạ {s.get('tone')!r} — {o}")
                values = s["values"]
                if not isinstance(values, list) or len(values) != len(stages):
                    raise LoiCong(f"visual {vid}.series.values phải khớp {len(stages)} mốc — {o}")
                for value in values:
                    if (not isinstance(value, dict) or not value.get("hien")
                            or isinstance(value.get("value"), bool)
                            or not isinstance(value.get("value"), (int, float))):
                        raise LoiCong(f"visual {vid}.series.values cần value là SỐ và hien là chữ — {o}")
                bien.append(float(values[-1]["value"]) - float(values[0]["value"]))
            if not bien[0] or not bien[1] or bien[0] * bien[1] >= 0:
                raise LoiCong(f"visual {vid} cần hai chuỗi có hướng ròng NGƯỢC nhau — {o}")
            continue
        if v["type"] == "system-map":
            lanes = v.get("lanes")
            if not isinstance(lanes, list) or not 3 <= len(lanes) <= 5:
                raise LoiCong(f"visual {vid}.lanes phải có 3–5 tầng — {o}")
            node_ids, node_lane = [], {}
            for lane_n, lane in enumerate(lanes):
                if (not isinstance(lane, dict) or not lane.get("label")
                        or not lane.get("note")):
                    raise LoiCong(f"visual {vid}.lanes mỗi tầng cần label/note — {o}")
                nodes = lane.get("nodes")
                if not isinstance(nodes, list) or not 1 <= len(nodes) <= 3:
                    raise LoiCong(f"visual {vid}.lanes.nodes phải có 1–3 nút — {o}")
                for node in nodes:
                    if not isinstance(node, dict):
                        raise LoiCong(f"visual {vid}.lanes.nodes phải chứa object — {o}")
                    thieu = sorted(k for k in ("id", "label", "value", "note")
                                  if node.get(k) in (None, ""))
                    if thieu:
                        raise LoiCong(f"visual {vid}.lanes.nodes thiếu {thieu} — {o}")
                    nid = str(node["id"])
                    if not re.fullmatch(r"[a-z0-9-]+", nid):
                        raise LoiCong(f"visual {vid} có id nút sai dạng: {nid!r} — {o}")
                    if node.get("tone", "accent") not in VISUAL_TONES:
                        raise LoiCong(f"visual {vid} có tone lạ {node.get('tone')!r} — {o}")
                    node_ids.append(nid); node_lane[nid] = lane_n
            if len(node_ids) != len(set(node_ids)):
                raise LoiCong(f"visual {vid} có id nút trùng — {o}")
            edges = v.get("edges")
            if not isinstance(edges, list) or not len(lanes) - 1 <= len(edges) <= 10:
                raise LoiCong(f"visual {vid}.edges phải có {len(lanes) - 1}–10 quan hệ — {o}")
            pairs, touched = [], set()
            for edge in edges:
                if (not isinstance(edge, dict)
                        or any(not edge.get(k) for k in ("from", "to", "label"))):
                    raise LoiCong(f"visual {vid}.edges mỗi quan hệ cần from/to/label — {o}")
                a, b = str(edge["from"]), str(edge["to"])
                if a not in node_lane or b not in node_lane:
                    raise LoiCong(f"visual {vid}.edges trỏ tới nút không tồn tại: {a} → {b} — {o}")
                if node_lane[a] >= node_lane[b]:
                    raise LoiCong(f"visual {vid}.edges phải đi tới tầng sau: {a} → {b} — {o}")
                pairs.append((a, b)); touched.update((a, b))
            if len(pairs) != len(set(pairs)):
                raise LoiCong(f"visual {vid} có quan hệ trùng — {o}")
            bo_quen = sorted(set(node_ids) - touched)
            if bo_quen:
                raise LoiCong(f"visual {vid} có nút không tham gia quan hệ: {bo_quen} — {o}")
            continue
        if v["type"] == "waterfall":
            items = v.get("items")
            if not isinstance(items, list) or not 3 <= len(items) <= 8:
                raise LoiCong(f"visual {vid}.items phải có 3–8 dòng — {o}")
            if any(not isinstance(x, dict) for x in items):
                raise LoiCong(f"visual {vid}.items phải chứa object — {o}")
            if items[0].get("kind") != "start" or items[-1].get("kind") != "total" \
                    or any(x.get("kind") != "change" for x in items[1:-1]):
                raise LoiCong(f"visual {vid} phải theo thứ tự start → change → total — {o}")
            for x in items:
                thieu = sorted(k for k in ("label", "hien", "note", "value", "kind")
                              if x.get(k) in (None, ""))
                if thieu:
                    raise LoiCong(f"visual {vid}.items thiếu {thieu} — {o}")
                if isinstance(x["value"], bool) or not isinstance(x["value"], (int, float)):
                    raise LoiCong(f"visual {vid}.items value phải là SỐ — {o}")
                if x.get("tone", "accent") not in VISUAL_TONES:
                    raise LoiCong(f"visual {vid} có tone lạ {x.get('tone')!r} — {o}")
            tinh = float(items[0]["value"]) + sum(float(x["value"]) for x in items[1:-1])
            if abs(tinh - float(items[-1]["value"])) > 1e-8:
                raise LoiCong(f"visual {vid} không khép số: {tinh:g} ≠ {items[-1]['value']} — {o}")
            continue
        khoa = {"timeline": "events", "distribution": "segments", "dai": "diem",
                "comparison": "sides"}.get(v["type"], "steps")
        ds = v.get(khoa)
        gioi_han = ((3, 16) if khoa == "events" else (2, 8) if khoa == "diem"
                     else (2, 2) if khoa == "sides" else (2, 6))
        if not isinstance(ds, list) or not gioi_han[0] <= len(ds) <= gioi_han[1]:
            raise LoiCong(f"visual {vid}.{khoa} phải có {gioi_han[0]}–{gioi_han[1]} mục — {o}")
        for x in ds:
            if not isinstance(x, dict):
                raise LoiCong(f"visual {vid}.{khoa} phải chứa object — {o}")
            bat_buoc = ({"label", "scale_label", "scale", "result_label", "result", "note", "facts"}
                        if v["type"] == "comparison" else
                        {"label", "value", "note"} if v["type"] in ("flow", "dai") else
                        {"label", "value", "question", "note"} if v["type"] == "proof" else
                        {"label", "value", "magnitude"} if v["type"] == "timeline" else
                        {"label", "count", "note"})
            thieu = sorted(k for k in bat_buoc if x.get(k) in (None, ""))
            if thieu:
                raise LoiCong(f"visual {vid}.{khoa} thiếu {thieu} — {o}")
            if x.get("tone", "accent") not in VISUAL_TONES:
                raise LoiCong(f"visual {vid} có tone lạ {x.get('tone')!r} — {o}")
            if v["type"] == "comparison":
                facts = x.get("facts")
                if (not isinstance(facts, list) or len(facts) != 2
                        or any(not isinstance(f, dict) or not f.get("label") or not f.get("value")
                               for f in facts)):
                    raise LoiCong(f"visual {vid}.{khoa} mỗi bên phải có đúng 2 facts label/value — {o}")
            if v["type"] == "timeline" and (not isinstance(x["magnitude"], (int, float))
                                               or x["magnitude"] <= 0):
                raise LoiCong(f"visual {vid} magnitude phải là số dương — {o}")
            if v["type"] == "distribution" and (not isinstance(x["count"], int)
                                                   or x["count"] <= 0):
                raise LoiCong(f"visual {vid} count phải là số nguyên dương — {o}")
            if v["type"] == "dai" and (isinstance(x["value"], bool)
                                       or not isinstance(x["value"], (int, float))):
                raise LoiCong(f"visual {vid} value của `dai` phải là SỐ, không phải chuỗi "
                              f"(vị trí trên trục tính từ nó) — {o}: {x['value']!r}")
        if v["type"] == "dai":
            gt = [float(x["value"]) for x in ds]
            # 🔴 Trục cần hai đầu KHÁC NHAU. Mọi điểm bằng nhau thì phép quy tỷ lệ chia
            # cho 0; và kể cả có chặn ZeroDivisionError thì một dải mà mọi chấm chồng
            # lên nhau cũng không nói được gì — hình sẽ TRÔNG như một chấm duy nhất
            # trong khi bảng dữ liệu vẫn liệt kê đủ mục.
            if min(gt) == max(gt):
                raise LoiCong(f"visual {vid} có mọi điểm cùng một giá trị ({gt[0]}) — dải "
                              f"cần hai đầu khác nhau, nếu không thì đây là một con số "
                              f"chứ không phải một dải — {o}")
    if len(ids) != len(set(ids)):
        raise LoiCong(f"id visual bị trùng trong cấu hình — {o}")
    if set(marker) != set(ids):
        raise LoiCong(f"marker visual và cấu hình không khớp — marker={sorted(marker)}, "
                      f"cấu hình={sorted(ids)} — {o}")


def cong_visual_html(txt: str, visuals: list, o: str) -> None:
    """Cổng sau render — cấu hình đúng mà renderer làm rơi hình vẫn phải nổ."""
    if not visuals:
        return
    if "{{visual:" in txt:
        raise LoiCong(f"directive visual còn sót sau render — {o}")
    if BO_CUC != "v3":
        return
    if txt.count('<figure class="article-viz ') != len(visuals):
        raise LoiCong(f"visual v3 dựng thiếu figure — cần {len(visuals)} — {o}")
    if txt.count('<details class="article-viz-data">') != len(visuals):
        raise LoiCong(f"visual v3 dựng thiếu bảng dữ liệu gốc — cần {len(visuals)} — {o}")
    expected_labels = sum(len(headers) * len(rows)
                          for headers, rows in (_du_lieu_visual(v) for v in visuals))
    if txt.count('data-label="') != expected_labels:
        raise LoiCong(f"visual v3 dựng thiếu nhãn data card — cần {expected_labels} — {o}")
    for v in visuals:
        if f'id="visual-{v["id"]}"' not in txt:
            raise LoiCong(f"visual v3 dựng thiếu id {v['id']!r} — {o}")

def cong_ngon_ngu(txt: str, o: str) -> None:
    """Cổng 1 — dùng chung RETIRED/JARGON của template/check_language.py."""
    for pat, fix, why in lang.RETIRED:
        if re.search(pat, txt, re.I):
            raise LoiCong(f"TỪ ĐÃ KHAI TỬ '{pat}' trong {o}\n     thay bằng: {fix}\n     vì: {why}")
    for pat, fix in lang.JARGON:
        if re.search(pat, txt, re.I):
            raise LoiCong(f"TỪ NGHỀ REPO '{pat}' trong {o} — người ngoài không đọc được\n     thay bằng: {fix}")


def cong_cau_truc(fm: dict, body: str, claims: list, o: str) -> None:
    """Cổng 2 — 5 phần chữ ký của LAUNCH §1."""
    if not fm.get("title"):
        raise LoiCong(f"thiếu CLAIM (front matter 'title') — {o}")
    ghim = fm.get("ghim", "")
    if not re.search(r"#?\d[\d.]{5,}", ghim):
        raise LoiCong(f"thiếu SỐ KÈM BLOCK — front matter 'ghim' phải mang block number — {o}")
    if not re.search(r"^##\s.*[Tt]ự kiểm", body, re.M):
        raise LoiCong(f"thiếu CÁCH TỰ KIỂM — cần một mục '## …Tự kiểm…' — {o}")
    if not any(c.get("falsifier", "").strip() for c in claims):
        raise LoiCong(f"thiếu ĐIỀU BÁC BỎ — không claim nào có falsifier — {o}")
    if "Không phải lời khuyên đầu tư" not in body:
        raise LoiCong(f"thiếu DISCLAIMER — {o}")
    # 'mo_ta' là dòng hiện ra khi link được dán vào Telegram/Discord/forum, và là dòng
    # máy tìm in dưới tiêu đề. Không có nó thì link ra ngoài chỉ còn một dòng chữ trơn —
    # hỏng ở đúng chỗ người lạ quyết định bấm hay không, mà không lệnh nào báo lỗi.
    md_ = fm.get("mo_ta", "").strip()
    if not 60 <= len(md_) <= 200:
        raise LoiCong(f"'mo_ta' phải dài 60–200 ký tự, đang {len(md_)} — {o}")


def cong_tieu_de(fm: dict, o: str) -> None:
    """Cổng 15 — chuỗi đi vào <h1> và vào thẻ bài không được vượt `H1_TOI_DA`.

    Đo cái ĐI RA MẶT CHỮ, không đo `title`. Bài có `tieu_de_ngan` thì `title` dài bao
    nhiêu cũng được — nó chỉ còn phục vụ `<title>` và og:title, hai chỗ dài là có lợi.

    🔴 `tieu_de_ngan` cũng bị đo. Không có phép này thì trường sinh ra để cứu độ dài lại
    trở thành cửa vòng qua chính cổng đó.
    """
    h1 = _tieu_de_h1(fm)
    if len(h1) > H1_TOI_DA:
        nguon = "tieu_de_ngan" if (fm.get("tieu_de_ngan") or "").strip() else "title"
        raise LoiCong(
            f"tiêu đề hiện trên mặt chữ dài {len(h1)} ký tự, trần {H1_TOI_DA} "
            f"(đang lấy từ '{nguon}') — thêm/rút front matter 'tieu_de_ngan' xuống "
            f"≤{H1_TOI_DA}; 'title' giữ nguyên câu đầy đủ cho <title> và og:title — {o}")


def cong_claim(claims: list, o: str) -> None:
    """Cổng 3 — bản MÁY của LAUNCH §6c. Không có falsifier thì không được đăng."""
    if not claims:
        raise LoiCong(f"không có claim nào — {o}")
    ids = set()
    for c in claims:
        cid = c.get("id", "")
        if not re.fullmatch(r"C\d+", cid):
            raise LoiCong(f"id claim phải dạng C<số> — {o}: {cid!r}")
        if cid in ids:
            raise LoiCong(f"id claim trùng '{cid}' — {o}")
        ids.add(cid)
        if len(c.get("text", "").strip()) < 20:
            raise LoiCong(f"{cid} thiếu nội dung claim — {o}")
        if c.get("status") not in TRANG_THAI:
            raise LoiCong(f"{cid} trạng thái không hợp lệ {c.get('status')!r}; "
                          f"chỉ nhận {list(TRANG_THAI)} — {o}")
        # ≥40 ký tự để không lách bằng "n/a" — falsifier phải là một câu thật
        if len(c.get("falsifier", "").strip()) < 40:
            raise LoiCong(f"{cid} thiếu ĐIỀU BÁC BỎ (hoặc quá ngắn để là một câu thật) — {o}")
        if not c.get("ghim", "").strip():
            raise LoiCong(f"{cid} thiếu block/mốc ghim — {o}")
        if not isinstance(c.get("log"), list) or not c["log"]:
            raise LoiCong(f"{cid} phải có ít nhất một dòng nhật ký — {o}")
        for e in c["log"]:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e.get("ngay", "")):
                raise LoiCong(f"{cid} nhật ký thiếu ngày dạng YYYY-MM-DD — {o}")
            if not e.get("ghi", "").strip():
                raise LoiCong(f"{cid} nhật ký có dòng rỗng — {o}")


def cong_ghi_truoc(claims: list, o: str) -> None:
    """Cổng 10 — đã ghi trước thì PHẢI ghi kết quả, kể cả khi kết quả là mình sai.

    Vì sao là cổng: một bảng "tôi ghi trước rồi kết quả ra sao" mà chỉ chở những lần đúng
    thì tự nó là chọn mẫu, và nó nói nhiều hơn về tác giả bảng so với về đối tượng. Claim
    đã được phân định mà `ghi_truoc` không có `ket_qua` ⇒ chặn build: đó đúng là cửa để
    một lần đổ lặng lẽ rơi khỏi bảng.
    """
    for c in claims:
        g = c.get("ghi_truoc")
        if not g:
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(g.get("ngay", ""))):
            raise LoiCong(f"{c['id']} ghi_truoc.ngay phải dạng YYYY-MM-DD — {o}")
        if len(str(g.get("noi", "")).strip()) < 10:
            raise LoiCong(f"{c['id']} ghi_truoc thiếu 'noi' — ghi trước ở đâu mà người khác "
                          f"kiểm được? không nói ra thì nó không phải ghi trước — {o}")
        if len(str(g.get("so", "")).strip()) < 20:
            raise LoiCong(f"{c['id']} ghi_truoc thiếu 'so' (con số hoặc ngưỡng đã ghi) — {o}")
        if c["status"] == "ĐANG ĐỨNG":
            continue
        for k, n in (("ket_qua", 20), ("ai_phan_dinh", 5)):
            if len(str(g.get(k, "")).strip()) < n:
                raise LoiCong(f"{c['id']} đã được phân định ({c['status']}) mà ghi_truoc thiếu "
                              f"'{k}' — bảng ghi-trước chỉ chở lần đúng là chọn mẫu — {o}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(g.get("ngay_ket", ""))):
            raise LoiCong(f"{c['id']} ghi_truoc.ngay_ket phải dạng YYYY-MM-DD — {o}")


RE_NGAY_VAN = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")


def cong_han(claims: list, o: str) -> None:
    """Cổng 9 — điều-bác-bỏ có NGÀY thì phải khai `han`, để lời hứa không chết trong văn xuôi.

    Vì sao là cổng: một ngày viết trong đoạn văn thì tới ngày đó không gì nhắc ai cả. Khai
    ra thì trang chủ tự in "sắp phân định", và tự in "ĐÃ TỚI HẠN" khi desk trễ — tức chính
    trang công khai là thứ đòi nợ. Claim đã được phân định thì miễn: hạn của nó là lịch sử.
    """
    for c in claims:
        if "han" in c:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c["han"])):
                raise LoiCong(f"{c['id']} 'han' phải dạng YYYY-MM-DD — {o}: {c['han']!r}")
            if len(str(c.get("han_ghi", "")).strip()) < 20:
                raise LoiCong(f"{c['id']} có 'han' mà thiếu 'han_ghi' — phải nói ngày đó "
                              f"PHÂN ĐỊNH cái gì, không chỉ ném ra một cái ngày — {o}")
        elif c["status"] == "ĐANG ĐỨNG" and RE_NGAY_VAN.search(c.get("falsifier", "")):
            raise LoiCong(f"{c['id']} điều-bác-bỏ có ngày "
                          f"{RE_NGAY_VAN.search(c['falsifier']).group()} mà không khai 'han' ⇒ "
                          f"tới ngày đó sẽ không gì nhắc — {o}")


def cong_qua_han(claims: list, o: str) -> None:
    """Cổng — hạn đã TRÔI QUA mà claim vẫn `ĐANG ĐỨNG` ⇒ CHẶN BUILD.

    🔴 VÌ SAO CÓ CỔNG NÀY (16/08/2026, và nó có xác).
    `cong_han` bắt claim phải KHAI `han`; `cong_ghi_truoc` bắt claim đã phân định phải
    có `ket_qua`. Giữa hai cổng đó có một khoảng trống đúng bằng thứ quan trọng nhất:
    **hạn trôi qua mà không ai đọc lại**. Không cổng nào so `han` với hôm nay, nên thứ
    duy nhất phản ứng là JS đếm ngược chạy TRONG TRÌNH DUYỆT NGƯỜI ĐỌC — tức người
    ngoài thấy chữ ĐÃ TỚI HẠN còn desk thì không thấy gì. Cổng canh nợ mà chỉ báo cho
    chủ nợ, không báo cho con nợ.

    Xác: claim `C6` của bài CAKE 10/08 có hạn **12/08**. Sự kiện nó canh xảy ra
    **08:20:12Z ngày 10/08**, tức 2 giờ 6 phút sau khi bài lên. Claim nằm im tới
    **16/08** — trễ 4 ngày sau hạn, 6 ngày sau khi đã phân định được — và trong suốt
    thời gian đó trang chủ vẫn đang in ĐÃ TỚI HẠN cho khách đọc.

    🔵 HAI CỬA RA, cả hai đều hợp lệ, và đó là điểm của cổng — nó không đòi bạn phải
    ĐÚNG, nó đòi bạn phải NÓI:
      ⑴ đọc lại rồi ghi kết quả ⇒ `status` sang `ĐÃ XÁC NHẬN` / `BỊ BÁC` / `ĐÃ SỬA`
         (khi đó `cong_ghi_truoc` tiếp quản và đòi `ket_qua`/`ai_phan_dinh`/`ngay_ket`);
      ⑵ chưa đủ số ⇒ `status` sang `CHỜ SỐ` **và** thêm một dòng `log` nói rõ tới hạn
         mà chưa đo được gì. Đó đúng là câu mà `PUBLISH.md` đã đòi từ 28/07:
         *"tới hạn mà chưa đo thì phải công khai ghi 'chưa đủ số', không được để im"*.
    Không có cửa thứ ba, và **không có cửa dời hạn** — sửa `han` sau khi thấy kết quả
    là dời goalpost, hỏng đúng thứ làm nên một bài ghi trước.

    🔴 Cổng đọc ĐỒNG HỒ, phần dựng thì KHÔNG. Trang tĩnh phải dựng hai lần ra cùng
    byte (vì thế đếm ngược mới nằm ở client), nên ngày hôm nay chỉ được phép quyết
    định **build có chạy hay không**, tuyệt đối không được chảy vào HTML.
    """
    hom_nay = datetime.date.today().isoformat()
    for c in claims:
        if c.get("han") and c["status"] == "ĐANG ĐỨNG" and str(c["han"]) < hom_nay:
            raise LoiCong(
                f"{c['id']} có hạn {c['han']} đã trôi qua mà vẫn 'ĐANG ĐỨNG' — {o}. "
                f"Trang công khai đang in ĐÃ TỚI HẠN cho dòng này. Hai cửa ra: "
                f"⑴ đọc lại rồi đổi status sang ĐÃ XÁC NHẬN/BỊ BÁC/ĐÃ SỬA kèm "
                f"ghi_truoc.ket_qua + ai_phan_dinh + ngay_ket; ⑵ chưa đủ số thì đổi "
                f"sang CHỜ SỐ kèm một dòng log nói rõ tới hạn chưa đo được gì. "
                f"KHÔNG được sửa 'han' — dời hạn sau khi thấy kết quả là dời goalpost")


def cong_do_lai(claims: list, o: str) -> None:
    """Cổng 8 — nút "đo lại ngay" phải khai đủ để CHẠY, hoặc khai rõ vì sao KHÔNG chạy được.

    Vì sao là cổng chứ không phải tuỳ chọn: một nút hỏng là thứ tệ hơn không có nút. Nó
    hứa với người đọc rằng họ tự kiểm được, rồi trả về số 0 hoặc không gì cả — và người
    đọc sẽ đọc số 0 đó thành dữ kiện về chain. Claim nào KHÔNG đo lại được từ trình duyệt
    thì phải nói ra, không được để trống cho người ta tự suy.
    """
    for c in claims:
        if "khong_do_lai" in c and len(str(c["khong_do_lai"]).strip()) < 20:
            raise LoiCong(f"{c['id']} 'khong_do_lai' phải nói RÕ vì sao (≥20 ký tự) — {o}")
        d = c.get("do_lai")
        if not d:
            continue
        if c.get("khong_do_lai"):
            raise LoiCong(f"{c['id']} khai CẢ do_lai lẫn khong_do_lai — chọn một — {o}")
        for k in ("to", "ky", "cong_thuc", "don_vi", "so_ghim", "chu_so"):
            if k not in d:
                raise LoiCong(f"{c['id']} do_lai thiếu '{k}' — {o}")
        if not re.fullmatch(r"0x[0-9a-fA-F]{40}", d["to"]):
            raise LoiCong(f"{c['id']} do_lai.to không phải địa chỉ 20 byte — {o}")
        if not RE_KY.match(d["ky"]):
            raise LoiCong(f"{c['id']} do_lai.ky không phải chữ ký hàm "
                          f"(vd 'balanceOf(address)') — {o}: {d['ky']!r}")
        ct = d["cong_thuc"]
        if "tu" not in ct:
            raise LoiCong(f"{c['id']} cong_thuc thiếu 'tu' (lấy word thứ mấy) — {o}")
        if "chia" not in ct and "thap_phan" not in ct:
            raise LoiCong(f"{c['id']} cong_thuc phải có 'chia' (tỉ lệ) HOẶC 'thap_phan' "
                          f"(quy về đơn vị) — không có thì không biết in số gì — {o}")
        ma_hoa_goi(d)      # nổ ngay tại build nếu tham số không mã hoá được


def cong_danh_dau(txt: str, o: str) -> None:
    """Cổng 6 — thuộc tính SỐ của SVG/HTML phải là số hợp lệ.

    Vì sao có: một phép đổi dấu thập phân `.replace('.', ',')` viết trên chuỗi đánh
    dấu đã ăn mất dấu chấm của TOẠ ĐỘ (`cx="88.1"` → `cx="88,1"`), làm hỏng hai
    chấm tròn của biểu đồ. Năm cổng kia canh NỘI DUNG (từ ngữ · cấu trúc · claim ·
    ngôi xưng · cú pháp markdown) nên không cái nào nhìn tới tầng đánh dấu — trang
    vẫn build sạch, vẫn PASS 5/5, và vẫn hỏng. Trình duyệt im lặng bỏ qua thuộc
    tính sai, đúng loại lỗi tệ nhất: sai mà không báo.
    """
    for m in re.finditer(r'\b(cx|cy|x|y|x1|y1|x2|y2|r|width|height|opacity|stroke-width)='
                         r'"([^"]*)"', txt):
        v = m.group(2)
        if v.startswith("var(") or v.endswith("%") or v.endswith("px"):
            continue
        # chấp nhận cả dạng dấu-chấm-dẫn-đầu (.16) — hợp lệ trong SVG/CSS
        if not re.fullmatch(r"-?(\d+(\.\d+)?|\.\d+)", v):
            raise LoiCong(f"thuộc tính số hỏng {m.group(1)}=\"{v}\" — {o}")


def cong_ngoi_xung(txt: str, o: str) -> None:
    """Cổng 4 — LAUNCH §1: 'chúng tôi' khai SỐ NGƯỜI, mà desk một người."""
    if re.search(r"chúng\s+tôi", txt, re.I):
        raise LoiCong(f"'chúng tôi' — khai số người, desk một người (LAUNCH §1) — {o}")


# ════════════════════════════════════════════════════════════════════ KHUÔN

CSS_THAN = """
*{box-sizing:border-box}
html{background:var(--bg);scroll-behavior:smooth}
body{margin:0;color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.7;
  -webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased;
  background:radial-gradient(1100px 420px at 78% -190px,
    color-mix(in srgb,var(--accent) 13%,transparent),transparent 70%) no-repeat,var(--bg)}
.khung{max-width:900px;margin:0 auto;padding:0 clamp(16px,4vw,26px)}
a{color:var(--ink);text-decoration:none}
main a,footer a{text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--accent) 55%,transparent);
  text-underline-offset:3px;text-decoration-thickness:1.5px}
main a:hover,footer a:hover{color:var(--accent);text-decoration-color:var(--accent)}
p,li,td,th,h1,h2,h3,figcaption{overflow-wrap:break-word}
a,code{word-break:break-word}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:4px}

/* ── đầu trang: dính, có mục lục ngang. MARK tô bằng var(--accent) nên tự đổi mã
   theo nền — cách duy nhất giữ được điều cấm ② của bản khai hệ ── */
header.dau{position:sticky;top:0;z-index:20;margin-bottom:34px;
  background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
.dau .khung{display:flex;align-items:center;gap:12px;padding-top:11px;padding-bottom:11px;flex-wrap:wrap}
.mark{width:31px;height:31px;flex:none}
.mark svg{display:block;width:100%;height:100%}
.mark path{fill:var(--accent)}
.ten{font:var(--dw) 18px/1 var(--display);letter-spacing:var(--gian-ten);text-decoration:none}
.ten span{color:var(--accent)}
nav.dieu{margin-left:auto;display:flex;gap:2px;align-items:center}
nav.dieu a{font:600 13px/1 var(--body);color:var(--muted);padding:7px 11px;border-radius:7px;text-decoration:none}
nav.dieu a:hover{color:var(--ink);background:var(--card)}
nav.dieu a.tai{color:var(--ink);background:var(--card);border:1px solid var(--line)}
button.nut-nen{font:500 12px/1 var(--mono);background:var(--card);border:1px solid var(--line);
  color:var(--muted);padding:7px 9px;border-radius:7px;cursor:pointer;margin-left:6px}
button.nut-nen:hover{color:var(--ink);border-color:var(--muted)}
.tag{font:500 11px/1 var(--mono);letter-spacing:.1em;color:var(--faint);text-transform:uppercase}
@media(max-width:760px){.tag{display:none}}
/* 🔴 KHỔ ĐIỆN THOẠI PHẢI THẤY ĐỦ MỤC. Luật cũ ở đây là `nav.dieu a:not(.tai){display:none}`
   — tức trên điện thoại thanh điều hướng chỉ hiện đúng mục ĐANG MỞ, và người vào bằng
   điện thoại không có cách nào biết Facts · Track record · Token tồn tại. Bản đồ của cả
   site vô hình ở đúng thiết bị phần lớn người đọc dùng (user bắt 06/08). Nay thanh rơi
   xuống hàng thứ hai và CUỘN NGANG — không mục nào bị giấu. */
@media(max-width:640px){
  .dau .khung{gap:8px 10px}
  nav.dieu{order:3;width:100%;margin-left:0;overflow-x:auto;padding:1px 0 3px;
    scrollbar-width:none;-webkit-overflow-scrolling:touch;
    -webkit-mask-image:linear-gradient(90deg,#000 88%,transparent)}
  nav.dieu::-webkit-scrollbar{display:none}
  nav.dieu a{flex:none;white-space:nowrap}
  button.nut-nen{order:2;margin-left:auto}
}

h1{font:var(--dw) clamp(28px,5.2vw,40px)/1.14 var(--display);letter-spacing:-.025em;margin:0 0 16px;text-wrap:balance}
/* Câu mở đầu to hơn phần thân một bậc và nhạt hơn — nó là lời chào, không phải nội
   dung. Chỉ khớp khi ngay sau <h1> có một đoạn văn: trang bài đi <h1>+<section> nên
   không dính, và đó là điều đúng (ở đó thứ đứng đầu phải là sổ claim). */
h1+p{font:400 18.5px/1.66 var(--body);color:var(--muted);max-width:64ch}
h1+p strong{color:var(--ink);font-weight:650}
/* dòng chữ dài quá 75 ký tự thì mắt trượt hàng — bề rộng khung là 900px, không phải
   bề rộng đọc được */
main>p,main>ul,main>ol{max-width:72ch}
h2{font:750 23px/1.28 var(--display);letter-spacing:-.018em;margin:46px 0 14px;text-wrap:balance}
h2::before{content:"";display:block;width:34px;height:3px;border-radius:2px;background:var(--accent);margin-bottom:12px;opacity:.9}
h3{font:650 16.5px/1.45 var(--body);margin:26px 0 8px}
p{margin:0 0 18px}
strong{font-weight:680}
hr{border:0;border-top:1px solid var(--line);margin:34px 0}
ul,ol{margin:0 0 18px;padding-left:21px}
li{margin-bottom:7px}
code{font:500 .875em var(--mono);background:var(--inset);border:1px solid var(--line-soft);
  border-radius:5px;padding:.1em .35em;word-break:break-word}
pre{background:var(--inset);border:1px solid var(--line-soft);border-radius:10px;padding:14px 16px;
  overflow-x:auto;margin:0 0 18px}
pre code{background:none;border:0;padding:0;font-size:12.5px;line-height:1.62}

.cuon{overflow-x:auto;margin:0 0 19px;-webkit-overflow-scrolling:touch;
  border:1px solid var(--line);border-radius:12px;background:var(--card)}
table{border-collapse:collapse;font-size:14.5px;min-width:100%}
th,td{padding:9px 14px;text-align:left;border-bottom:1px solid var(--line-soft);white-space:nowrap}
tr:last-child td{border-bottom:0}
th{font:600 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid var(--line)}

.meta{font:500 12.5px/1.7 var(--mono);color:var(--muted);margin:0 0 26px;
  background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:10px;padding:11px 16px}
.meta b{color:var(--ink);font-weight:600}

/* ── BẢNG ĐIỂM: thanh xếp chồng + chip có SỐ. Màn hình đầu tiên, thứ X/TG không có ── */
.dai,.board{background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:16px 18px 14px;margin:0 0 28px;
  box-shadow:0 1px 2px rgba(0,0,0,.05),0 10px 26px -18px rgba(0,0,0,.5)}
.bh{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.bh b{font:700 13px/1.4 var(--body);letter-spacing:.01em}
.bh span{font:500 11.5px/1.5 var(--mono);color:var(--faint)}
.stack{display:flex;gap:2px;height:22px;border-radius:6px;overflow:hidden;background:var(--inset)}
.seg{background:var(--st);min-width:3px;transition:opacity .16s}
.seg.xac{--st:var(--c-xn)}.seg.song{--st:var(--c-song)}.seg.sua{--st:var(--c-sua)}
.seg.bac{--st:var(--c-bac)}.seg.cho{--st:var(--c-cho)}
/* Thanh CHẠY TỪ 0 khi lọt tầm mắt. Chỉ phép biến hình chạy — bề rộng thật nằm sẵn
   trong HTML, nên tắt JS hoặc tắt chuyển động là thanh đứng ở đúng tỉ lệ, không phải
   ở 0. (Cùng lý do đã BỎ hiệu ứng đếm-lên cho chữ số: NOTES §3.) */
html.chuyen .stack .seg{transform:scaleX(0);transform-origin:left;
  transition:transform .7s cubic-bezier(.22,.75,.3,1) calc(var(--i,0)*90ms),opacity .16s}
html.chuyen .stack.chay .seg{transform:none}
html.js .stack .seg{cursor:pointer}
.stack:hover .seg{opacity:.38}
.stack .seg:hover{opacity:1}
/* Đưa chuột lên một dòng claim thì đoạn thanh của trạng thái ĐÓ sáng lên, và ngược
   lại. Hai khối vốn nói về cùng một tập số — nối chúng bằng mắt thì người đọc không
   phải tự bắc cầu. CSS không so được thuộc tính cha với con, nên năm luật, không một. */
.stack[data-noi="xac"] .seg:not(.xac),
.stack[data-noi="song"] .seg:not(.song),
.stack[data-noi="sua"] .seg:not(.sua),
.stack[data-noi="bac"] .seg:not(.bac),
.stack[data-noi="cho"] .seg:not(.cho){opacity:.3}
.roi{opacity:.4;transition:opacity .16s}
/* vạch tiến trình đọc — dày 2px, nằm trên thanh điều hướng dính */
#bp-tien{position:fixed;left:0;top:0;height:2px;width:100%;z-index:30;background:var(--accent);
  transform:scaleX(0);transform-origin:left;pointer-events:none}
#bp-tip{position:fixed;z-index:60;left:0;top:0;pointer-events:none;opacity:0;
  font:600 11.5px/1 var(--mono);color:var(--ink);background:var(--card);
  border:1px solid var(--line);border-radius:8px;padding:7px 10px;white-space:nowrap;
  box-shadow:0 10px 26px -14px rgba(0,0,0,.65);transition:opacity .13s}
#bp-tip.hien{opacity:1}
.chu-thich{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.lg{display:inline-flex;align-items:center;gap:7px;font:600 12px/1 var(--body);
  padding:7px 11px 7px 9px;border-radius:999px;border:1px solid var(--line);
  background:var(--inset);color:var(--muted);text-decoration:none;cursor:default;
  transition:border-color .16s,background .16s,color .16s,box-shadow .16s}
html.js .lg{cursor:pointer}
.lg .sw{width:9px;height:9px;border-radius:2px;background:var(--st);flex:none}
.lg .n{font:700 12px var(--mono);color:var(--ink)}
.lg.xac{--st:var(--c-xn)}.lg.song{--st:var(--c-song)}.lg.sua{--st:var(--c-sua)}
.lg.bac{--st:var(--c-bac)}.lg.cho{--st:var(--c-cho)}
.lg:hover{border-color:var(--st);color:var(--ink)}
.lg[aria-pressed="true"]{border-color:var(--st);color:var(--ink);
  background:color-mix(in srgb,var(--st) 16%,var(--inset));
  box-shadow:0 0 0 3px color-mix(in srgb,var(--st) 15%,transparent)}
.khi{font:500 12px/1.65 var(--mono);color:var(--faint);margin-top:11px}
.toi{display:inline-block;margin-top:12px;font:700 12.5px/1 var(--mono);letter-spacing:.05em;
  text-decoration:none;color:var(--ink);background:var(--nut-nen);color:var(--nut-chu);
  padding:9px 13px;border-radius:8px}
.toi:hover{filter:brightness(1.1)}

.dem{font:500 15px/1.55 var(--body);color:var(--muted)}
.dem .to{font:700 30px/1 var(--mono);color:var(--ink);vertical-align:-4px;margin-right:4px;letter-spacing:-.02em}
.dem b{font-weight:700}
.dem b.xac{color:var(--c-xn)}.dem b.song{color:var(--c-song)}.dem b.sua{color:var(--c-sua)}
.dem b.bac{color:var(--c-bac)}.dem b.cho{color:var(--c-cho)}
.dem .phu{font:500 12.5px/1.65 var(--body);color:var(--faint);margin-top:8px;
  text-transform:none;letter-spacing:0}

/* ── DÒNG TRẠNG THÁI: mỗi claim một dòng ĐỌC ĐƯỢC BẰNG CHỮ, lọc theo chip ở trên.
   Thay hai thứ user bác 06/08: hàng thẻ số in lại số của chú giải, và dãy mã
   "27/07 · C1" không nói được claim đó nói gì ── */
.tt-khu{margin:0 0 30px}
.tt-dau{display:flex;align-items:center;justify-content:space-between;gap:12px;
  flex-wrap:wrap;margin:0 0 13px}
.nhom-loc{display:flex;gap:6px;flex-wrap:wrap}
.lg-loc{font:600 12px/1 var(--body);padding:8px 13px;border-radius:999px;
  border:1px solid var(--line);background:var(--card);color:var(--muted);cursor:default;
  transition:border-color .16s,color .16s,background .16s}
html.js .lg-loc{cursor:pointer}
.lg-loc .n{font:700 12px var(--mono);color:var(--ink);margin-left:4px}
.lg-loc:hover{color:var(--ink);border-color:var(--muted)}
.lg-loc[aria-pressed="true"]{color:var(--nut-chu);background:var(--nut-nen);border-color:transparent}
.lg-loc[aria-pressed="true"] .n{color:var(--nut-chu)}
.tt-dau .lo{font:500 12px/1.6 var(--mono);color:var(--faint)}
.mo-them{margin-top:10px;width:100%;justify-content:center}
.mo-them[hidden]{display:none}
ol.tt-ds{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
ol.tt-ds li{--st:var(--accent)}
ol.tt-ds li.xac{--st:var(--c-xn)}ol.tt-ds li.song{--st:var(--c-song)}
ol.tt-ds li.sua{--st:var(--c-sua)}ol.tt-ds li.bac{--st:var(--c-bac)}ol.tt-ds li.cho{--st:var(--c-cho)}
/* .tt-hop là HỘP của một dòng — dùng cho cả thẻ <a> (trang chủ) lẫn <summary>
   (tủ kính token). Một khuôn, hai vai: hai bản chép là hai bản sẽ trôi lệch. */
.tt-hop{display:grid;grid-template-columns:auto minmax(0,1fr);gap:5px 14px;align-items:start;
  background:var(--card);border:1px solid var(--line);border-left:3px solid var(--st);
  border-radius:12px;padding:13px 16px;text-decoration:none;list-style:none;
  transition:transform .16s,border-color .16s,box-shadow .16s}
.tt-hop::-webkit-details-marker{display:none}
.tt-hop:hover{transform:translateY(-1px);text-decoration:none;
  border-color:color-mix(in srgb,var(--st) 45%,var(--line));
  box-shadow:0 1px 2px rgba(0,0,0,.05),0 12px 28px -20px rgba(0,0,0,.6)}
ol.tt-ds .chip{grid-row:1/3;align-self:start;margin-top:1px}
ol.tt-ds .tx{font:500 15px/1.6 var(--body);color:var(--ink);
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ol.tt-ds .mt{font:500 11.5px/1.55 var(--mono);color:var(--faint)}
@media(max-width:620px){.tt-hop{grid-template-columns:minmax(0,1fr)}
  ol.tt-ds .chip{grid-row:auto;justify-self:start;margin-bottom:3px}
  /* dòng chú thích gói về MỘT hàng: hai hàng × 8 dòng là gần một màn hình điện
     thoại, mà nó chỉ là nhãn — tiêu đề bài đầy đủ nằm ở đầu bài, không mất đi đâu */
  ol.tt-ds .mt{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}

/* ── TỦ KÍNH: dòng mở ra được. Đóng thì gọn như trang chủ; mở thì có đủ ghim, điều
   bác bỏ, và nút đo lại nếu dòng đó gọi lại được ── */
.crumb{font:700 10.5px/1.5 var(--mono);letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin:0 0 10px}
/* 🔴 KHÔNG đặt display:grid lên chính <summary> — đo được: Chrome dựng cả phần
   đang ĐÓNG của <details> vào trong hộp summary (dòng 720px thay vì 161px, trang
   15.652px, không một lời cảnh báo). Lưới nằm ở .tt-hop bên trong summary. */
details.tu-so>summary{cursor:pointer;list-style:none;display:block}
details.tu-so>summary::-webkit-details-marker{display:none}
details.tu-so .tt-hop{grid-template-columns:auto minmax(0,1fr) 15px}
details.tu-so .mui{grid-row:1/3;grid-column:3;align-self:center;color:var(--faint);
  font:400 12px/1 var(--mono);transition:transform .2s}
details.tu-so[open] .mui{transform:rotate(180deg)}
details.tu-so[open] .tt-hop{border-bottom-left-radius:0;border-bottom-right-radius:0;
  transform:none;box-shadow:none}
details.tu-so[open] .tx{-webkit-line-clamp:9}
.tu-mo{background:var(--card);border:1px solid var(--line);border-top:0;
  border-left:3px solid var(--st);border-radius:0 0 12px 12px;padding:12px 16px 14px}
.tu-mo .dong:last-of-type{margin-bottom:11px}
.tu-mo .tro{margin:0;font:600 12.5px/1.6 var(--mono)}
/* 🔴 Khổ hẹp phải ĐẶT TAY từng ô. Bản đầu chỉ đổi số cột (1fr + 15px) rồi để lưới
   tự xếp — và nó xếp dòng chú thích vào đúng cột 15px, thành một cột chữ dọc mỗi
   dòng một ký tự, cao gần một màn hình. Lưới tự xếp lấp ô trống theo thứ tự, nó
   không biết cột nào là cột dành cho mũi tên. */
@media(max-width:620px){
  details.tu-so .tt-hop{grid-template-columns:minmax(0,1fr) 15px}
  details.tu-so .chip,details.tu-so .tx,details.tu-so .mt{grid-column:1}
  details.tu-so .mui{grid-row:1;grid-column:2;align-self:start}}

/* ── BẢN ĐỒ SITE: hàng ô ngang ở màn hình đầu. Người lạ phải thấy trang có gì
   TRƯỚC khi phải cuộn — đo được: bản trước, mục Bài nằm ở 3.421px trên khổ điện
   thoại, tức 4,2 màn hình mới tới ── */
.ban-do{display:flex;flex-wrap:wrap;gap:12px;margin:26px 0 8px}
.o-map{position:relative;flex:1 1 235px;display:flex;flex-direction:column;gap:3px;
  overflow:hidden;background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:15px 17px 14px;text-decoration:none;
  transition:transform .18s,border-color .18s,box-shadow .18s}
.o-map::before{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:var(--accent)}
.o-map::after{content:"";position:absolute;inset:0;pointer-events:none;background:
  radial-gradient(320px 120px at 85% -26px,color-mix(in srgb,var(--accent) 13%,transparent),transparent 72%)}
.o-map:hover{transform:translateY(-2px);text-decoration:none;color:var(--ink);
  border-color:color-mix(in srgb,var(--accent) 45%,var(--line));
  box-shadow:0 2px 4px rgba(0,0,0,.05),0 16px 34px -24px rgba(0,0,0,.7)}
.o-map>*{position:relative}
.o-map .k{font:700 10.5px/1.5 var(--mono);letter-spacing:.16em;color:var(--accent)}
.o-map .v{font:700 27px/1.15 var(--mono);letter-spacing:-.03em;color:var(--ink)}
.o-map .g{font:400 12.5px/1.5 var(--body);color:var(--muted);padding-right:22px}
.o-map .mui{position:absolute;right:15px;bottom:12px;font-size:17px;color:var(--muted);
  transition:transform .18s,color .18s}
.o-map:hover .mui{transform:translateX(4px);color:var(--accent)}
/* Khổ điện thoại: HAI cột, không phải năm ô xếp dọc — xếp dọc thì chính cái bản đồ
   lại thành một đoạn phải cuộn, tức nó tự phản lại lý do nó tồn tại (đo: 607px).
   Ô lẻ cuối cùng trải hết hàng để không có ô mồ côi. */
@media(max-width:620px){
  .ban-do{gap:9px}
  .o-map{flex:1 1 calc(50% - 5px);padding:13px 14px 12px}
  .o-map .v{font-size:23px}
  .o-map .g{font-size:11.5px;padding-right:16px}
  .o-map .mui{right:12px;bottom:10px;font-size:15px}
  .o-map:last-child:nth-child(odd){flex-basis:100%}
}

/* ── THẺ CỬA lớn — nay là khuôn của MỤC LỤC TOKEN ── */
.cua{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:32px 0 0}
.cua-3{grid-template-columns:repeat(auto-fit,minmax(262px,1fr))}
.cua-o .mini{margin:3px 0 0;display:flex;gap:2px;height:6px;border-radius:3px;
  overflow:hidden;background:var(--inset)}
.cua-o.tok .t{font-size:clamp(17px,2vw,19px)}
.cua-o.tok .n{margin:0;padding:0;border-top:0}
.cua-o.tok .g{margin-top:auto;padding:11px 30px 0 0;border-top:1px solid var(--line-soft)}
@media(max-width:760px){.cua{grid-template-columns:1fr}}
.cua-o{position:relative;display:flex;flex-direction:column;gap:9px;overflow:hidden;
  background:var(--card);border:1px solid var(--line);border-radius:16px;
  padding:20px 22px 18px;text-decoration:none;
  transition:transform .18s,border-color .18s,box-shadow .18s}
.cua-o::before{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:var(--accent)}
.cua-o::after{content:"";position:absolute;inset:0;pointer-events:none;background:
  radial-gradient(420px 160px at 88% -34px,color-mix(in srgb,var(--accent) 15%,transparent),transparent 72%)}
.cua-o:hover{transform:translateY(-2px);text-decoration:none;color:var(--ink);
  border-color:color-mix(in srgb,var(--accent) 45%,var(--line));
  box-shadow:0 2px 4px rgba(0,0,0,.05),0 18px 40px -26px rgba(0,0,0,.7)}
.cua-o>*{position:relative}
.cua-o .k{font:700 10.5px/1.4 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
.cua-o .t{font:700 clamp(18px,2.2vw,21px)/1.32 var(--display);letter-spacing:-.015em;text-wrap:balance}
.cua-o .g{font:400 13.5px/1.62 var(--body);color:var(--muted)}
.cua-o .n{margin-top:auto;padding:11px 36px 0 0;border-top:1px solid var(--line-soft);
  font:500 12px/1.7 var(--mono);color:var(--faint);display:flex;flex-wrap:wrap;
  align-items:baseline;gap:7px}
.cua-o .n b{font:700 17px var(--mono);color:var(--ink);letter-spacing:-.02em}
.cua-o .n i{display:inline-block;width:3px;height:3px;border-radius:50%;
  background:var(--muted);margin:0 3px;vertical-align:middle}
.cua-o .mui{position:absolute;right:20px;bottom:15px;font-size:19px;color:var(--muted);
  transition:transform .18s,color .18s}
.cua-o:hover .mui{transform:translateX(4px);color:var(--accent)}

/* ── SỔ CLAIM — thứ duy nhất trên trang được phép nổi ── */
.so{margin:48px 0 0}
.so>p.dan{font-size:14.5px;color:var(--muted);margin:0 0 20px;max-width:74ch}
.claim{--st:var(--accent);background:var(--card);border:1px solid var(--line);
  border-left:4px solid var(--st);border-radius:14px;padding:18px 20px;margin-bottom:14px;
  scroll-margin-top:82px;transition:box-shadow .18s,border-color .18s}
.claim.xac{--st:var(--c-xn)}.claim.song{--st:var(--c-song)}.claim.sua{--st:var(--c-sua)}
.claim.bac{--st:var(--c-bac)}.claim.cho{--st:var(--c-cho)}
.claim.sua{border-left-style:double;border-left-width:6px}
.claim.cho{border-left-style:dashed}
.claim:hover{box-shadow:0 1px 2px rgba(0,0,0,.05),0 10px 26px -18px rgba(0,0,0,.5)}
.claim:target{border-color:var(--st);box-shadow:0 0 0 3px color-mix(in srgb,var(--st) 20%,transparent)}
.claim h3{margin:0 0 11px;font:700 15px/1.5 var(--body);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.claim .id{font:700 15px var(--mono);color:var(--ink);text-decoration:none}
.claim .id:hover{color:var(--accent)}
.claim>p{margin:0 0 13px;font-size:15.5px;line-height:1.66}

/* năm trạng thái mang BA kênh: màu · glyph · hình khối. Bỏ glyph là vi phạm điều cấm ②:
   đo được đỏ ↔ lá chỉ cách nhau ΔE 2,7 với người mù màu deutan — hue một mình không đủ */
.chip{--st:var(--accent);display:inline-flex;align-items:center;gap:7px;
  font:700 11.5px/1 var(--mono);letter-spacing:.055em;padding:5px 11px;border-radius:999px;
  color:var(--st);border:1.5px solid var(--st);background:color-mix(in srgb,var(--st) 13%,transparent);
  white-space:nowrap}
.chip::before{font-size:11px;line-height:1}
.chip.xac{--st:var(--c-xn)}.chip.xac::before{content:"✓"}
.chip.song{--st:var(--c-song)}.chip.song::before{content:"●"}
.chip.sua{--st:var(--c-sua)}.chip.sua::before{content:"✎"}
.chip.cho{--st:var(--c-cho);border-style:dashed}.chip.cho::before{content:"○"}
/* BỊ BÁC là trạng thái ỒN NHẤT của kênh này ⇒ nền đặc, không phải nền nhạt */
.chip.bac{--st:var(--c-bac);background:var(--c-bac);color:var(--card);border-color:var(--c-bac)}
.chip.bac::before{content:"✕"}

/* 🔴 Trong thẻ claim KHÔNG có cam: khối GHIM TẠI đứng ngay trên keyline đỏ của
   ĐIỀU-GÌ-BÁC-BỎ, mà coral ↔ đỏ đo được ΔE 11,4 (nền tối) / 6,8 (nền sáng) */
.dong{font-size:14px;margin:0 0 11px;background:var(--inset);border:1px solid var(--line-soft);
  border-left:2px solid var(--muted);border-radius:9px;padding:10px 13px;line-height:1.65}
.dong .nhan{font:700 10px var(--mono);letter-spacing:.09em;color:var(--muted);
  display:block;margin-bottom:4px;text-transform:uppercase}
.dong code{font-size:11.5px;background:none;border:0;padding:0;display:block;
  white-space:pre-wrap;color:var(--muted)}
/* điều-bác-bỏ là thứ khác biệt duy nhất của kênh này ⇒ dòng NẶNG NHẤT trong khối claim */
.dong.bac{background:transparent;border:0;border-left:2px solid color-mix(in srgb,var(--c-bac) 45%,transparent);
  border-radius:0;padding:2px 0 2px 12px;font-size:14px;color:var(--muted)}
.dong.bac .nhan{color:var(--c-bac)}
.dong.khongdo{background:transparent;border:1px dashed var(--line);border-radius:9px;
  color:var(--faint);font-size:13px}
.claim .moc{font:500 12.5px/1.7 var(--mono);color:var(--faint);letter-spacing:.02em}
.tro{margin:12px 0 0;font:500 12.5px/1.6 var(--mono)}

.nk{list-style:none;padding:0;margin:14px 0 0;font-size:13.5px}
.nk li{position:relative;padding:7px 0 7px 22px;margin:0;color:var(--muted);line-height:1.6}
.nk li::before{content:"";position:absolute;left:0;top:14px;width:9px;height:9px;border-radius:50%;
  background:var(--st);box-shadow:0 0 0 3px color-mix(in srgb,var(--st) 18%,transparent)}
.nk .d{font:700 11.5px var(--mono);color:var(--ink);margin-right:8px}
.nk .nguon-tro{opacity:.72;font-size:.92em;font-style:italic}

/* ── HÌNH: claim vẽ thành trục số ── */
.hinh{margin:0 0 13px;padding:0}
.thang .hang{margin-bottom:13px}
.thang .nh{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  font:500 12px/1.5 var(--mono);color:var(--muted);margin-bottom:4px}
.thang .nh b{font:700 14px var(--mono);color:var(--ink);white-space:nowrap}
.thang .ray{position:relative;height:14px;background:var(--inset);border-radius:4px;overflow:hidden}
.thang .ray.tr{height:9px;background:none;overflow:visible}
.thang .cot{display:block;height:100%;background:var(--muted);border-radius:0 4px 4px 0}
.thang .cot.toi{background:var(--accent)}
.thang .cot.cu{background:color-mix(in srgb,var(--ink) 22%,transparent)}
.thang .vung{position:absolute;top:0;height:9px;background:var(--accent);
  border-left:2px solid var(--accent);border-right:2px solid var(--accent);opacity:.45}
.thang .nk2{margin:4px 0 0;font-size:11.5px;color:var(--faint)}
.thang .nk2 b{font-size:12px;color:var(--accent)}
.hinh figcaption{font:500 11px/1.5 var(--mono);color:var(--faint);margin-top:8px;
  padding-top:7px;border-top:1px solid var(--line-soft)}

.dan-gt{margin:14px 0 0;font-size:15px}
ul.han{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
ul.han li{background:var(--card);border:1px solid var(--line);border-left:4px dashed var(--c-cho);
  border-radius:12px;padding:13px 16px;font-size:14.5px}
ul.han .ngay{font:700 13px/1.7 var(--mono);letter-spacing:.03em;color:var(--ink);display:block;margin-bottom:3px}
ul.han .con{font-weight:600;color:var(--c-cho);margin-left:9px;font-family:var(--mono);font-size:11.5px}
ul.han .con.qua{color:var(--c-sua)}

/* ── nút ĐO LẠI: mực + hình khối, KHÔNG mặc hue (điều cấm ①) ── */
.dolai-o{margin:0 0 12px;display:flex;flex-direction:column;gap:9px;
  background:var(--inset);border:1px solid var(--line);border-radius:10px;padding:11px 13px}
button.dolai{align-self:flex-start;font:700 12.5px/1 var(--body);letter-spacing:.02em;
  color:var(--nut-chu);background:var(--nut-nen);border:0;border-radius:8px;
  padding:10px 15px;cursor:pointer}
button.dolai:hover{transform:translateY(-1px)}
button.dolai[disabled]{opacity:.6;cursor:progress;transform:none}
.ketqua{font:500 12.5px/1.65 var(--mono);color:var(--muted);
  border-left:2px solid var(--line);padding:2px 0 2px 10px}
.ketqua b{color:var(--ink);font-weight:700}
.ketqua.khop{border-left-color:var(--c-xn)}
.ketqua.khop b{color:var(--c-xn)}
.ketqua.lech{border-left-color:var(--c-sua)}
.ketqua.lech b{color:var(--c-sua)}
.ketqua.loi{border-left-color:var(--c-bac)}
.ketqua.loi b{color:var(--c-bac)}
.ketqua .nguon{display:block;font-size:11px;color:var(--faint);margin-top:3px}

/* bài viết là THAM CHIẾU ở trang này — hạ nhẹ xuống, không tranh chỗ với sổ claim */
.bandaydu{margin-top:56px;padding-top:8px;border-top:1px solid var(--line)}
.bandaydu>p,.bandaydu>ul,.bandaydu>ol{max-width:72ch}
.bandaydu h2{margin-top:34px}

footer{margin-top:64px;padding:22px 0 46px;border-top:1px solid var(--line);background:var(--bg2);
  font:500 12px/1.75 var(--mono);color:var(--faint)}
footer a{color:var(--muted)}

/* ── DẢI BÀI: cuộn NGANG, mỗi thẻ mang thanh trạng thái riêng của bài đó ── */
.khu-bai{margin-top:52px}
.khu-dau{display:flex;align-items:flex-end;gap:14px}
.khu-dau h2{margin:0}
.dieu-rail{margin-left:auto;display:flex;gap:7px;padding-bottom:3px}
button.rn{width:36px;height:36px;border-radius:10px;border:1px solid var(--line);
  background:var(--card);color:var(--muted);font:600 15px/1 var(--body);cursor:pointer;
  transition:color .16s,border-color .16s,transform .16s}
button.rn:hover:not([disabled]){color:var(--ink);border-color:var(--muted);transform:translateY(-1px)}
button.rn[disabled]{opacity:.32;cursor:default}
@media(max-width:560px){.dieu-rail{display:none}}
/* mép phải mờ dần = dấu hiệu "còn nữa bên kia"; tắt khi đã cuộn hết đường */
.rail-boc{position:relative}
.rail-boc::after{content:"";position:absolute;right:0;top:0;bottom:16px;width:52px;
  pointer-events:none;background:linear-gradient(90deg,transparent,var(--bg));
  transition:opacity .22s}
.rail-boc.het::after{opacity:0}
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(250px,1fr);gap:14px;
  margin-top:16px;padding:3px 2px 16px;overflow-x:auto;overscroll-behavior-x:contain;
  scroll-snap-type:x proximity;scroll-padding-left:2px;-webkit-overflow-scrolling:touch;
  scrollbar-width:thin;scrollbar-color:var(--line) transparent}
@media(min-width:760px){.rail{grid-auto-columns:minmax(272px,300px)}}
.rail::-webkit-scrollbar{height:8px}
.rail::-webkit-scrollbar-thumb{background:var(--line);border-radius:99px}
.rail::-webkit-scrollbar-thumb:hover{background:var(--muted)}
.rail:focus-visible{outline:2px solid var(--accent);outline-offset:4px;border-radius:12px}
.bai{scroll-snap-align:start;display:flex;flex-direction:column;gap:10px;
  background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:16px 18px 15px;text-decoration:none;
  transition:border-color .16s,transform .16s,box-shadow .16s}
/* 🔴 Giữ MỰC khi rê chuột. Luật `main a:hover{color:accent}` đúng cho link trong
   thân bài, nhưng ở thẻ lớn nó tô coral cả tiêu đề — mà coral là màu KHUNG TRANG,
   không phải màu trạng thái, và thẻ này đứng ngay dưới một dải chip trạng thái.
   Chuyển động + viền + mũi tên đã đủ báo "bấm được". */
.bai:hover{border-color:var(--muted);transform:translateY(-2px);text-decoration:none;
  color:var(--ink);box-shadow:0 2px 4px rgba(0,0,0,.05),0 16px 34px -24px rgba(0,0,0,.65)}
.bai .d{font:500 11.5px/1.5 var(--mono);color:var(--faint)}
.bai .t{font:650 16.5px/1.42 var(--body);letter-spacing:-.01em;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.bai .mini{display:flex;gap:2px;height:6px;border-radius:3px;overflow:hidden;
  background:var(--inset);margin-top:auto}
.bai .s{font:500 11.5px/1.55 var(--mono);color:var(--faint)}
.rail-goi{margin:2px 0 0;font:500 11.5px/1.6 var(--mono);color:var(--faint)}


/* ── TRANG FACTS: khuôn riêng, không dùng khuôn claim. Panel số bên trái đứng một
   mình được — đó là thứ người ta chụp màn hình và dán đi ── */
.fact{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;
  margin-bottom:16px;scroll-margin-top:82px;
  box-shadow:0 1px 2px rgba(0,0,0,.05),0 10px 26px -18px rgba(0,0,0,.5)}
.fact:target{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 18%,transparent)}
.f-top{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr)}
.f-top.mot-cot{grid-template-columns:1fr}
@media(max-width:820px){.f-top{grid-template-columns:1fr}}
/* Panel số DÍNH theo mép trên: thân fact dài hơn panel rất nhiều, để panel giãn
   theo thân thì con số trôi mất khỏi màn hình đúng lúc người ta đang đọc về nó.
   Đường kẻ dọc đặt ở .f-body chứ không ở panel — panel nay cao theo nội dung. */
/* KHÔNG tô nền cho panel dính: nền chỉ đẹp khi panel cao bằng thẻ, còn khi nó dính
   và trôi xuống thì mảng màu đó đọc thành một hộp lơ lửng giữa thẻ. */
.f-fig{padding:19px 21px;display:flex;flex-direction:column;gap:8px;align-self:start;
  position:sticky;top:74px}
.f-top.co-fig .f-body{border-left:1px solid var(--line)}
@media(max-width:820px){
  .f-fig{position:static;border-bottom:1px solid var(--line);border-radius:14px 14px 0 0}
  .f-top.co-fig .f-body{border-left:0}
}
.f-kicker{font:700 10.5px/1.4 var(--mono);letter-spacing:.14em;color:var(--accent)}
/* con số dài nhất ở đây là 16 ký tự — cỡ chữ phải để nó đứng TRỌN một dòng.
   Một con số bị ngắt dòng giữa chừng là một con số khó đọc lại. */
.f-num{font:700 clamp(21px,2.4vw,28px)/1.12 var(--mono);letter-spacing:-.03em;white-space:nowrap}
@media(max-width:400px){.f-num{font-size:19px;white-space:normal}}
.f-lab{font:700 11.5px/1.5 var(--body);letter-spacing:.05em;color:var(--muted)}
.f-body{padding:19px 21px;display:flex;flex-direction:column;gap:14px;min-width:0}
.f-cau{margin:0;font-size:15.5px;line-height:1.68}
.f-so{margin:0;font:500 12.5px/1.75 var(--mono);color:var(--muted);background:var(--inset);
  border:1px solid var(--line-soft);border-left:2px solid var(--muted);border-radius:9px;
  padding:10px 13px;overflow-wrap:anywhere}
.f-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:700px){.f-grid{grid-template-columns:1fr}}
.f-box .k{font:700 10px/1.5 var(--mono);letter-spacing:.09em;text-transform:uppercase;
  display:block;margin-bottom:5px}
.f-box .v{font-size:13px;line-height:1.6;color:var(--muted)}
.f-box.vi .k{color:var(--accent)}
.f-box.chan{border-left:2px dashed var(--line);padding-left:12px}
.f-box.chan .k{color:var(--muted)}
.f-foot{border-top:1px solid var(--line-soft);padding:12px 21px;display:flex;gap:12px;
  align-items:baseline;flex-wrap:wrap;background:var(--inset)}
.f-foot .lb{font:700 10px var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.f-foot .blk{font:500 12px/1.6 var(--mono);color:var(--ink)}
details.lenh{margin:0 21px 16px}
details.lenh summary{cursor:pointer;font:500 11.5px var(--mono);color:var(--muted);padding:7px 0}
details.lenh summary:hover,details.lenh[open] summary{color:var(--ink)}
.cmd{background:var(--inset);border:1px solid var(--line-soft);border-radius:9px;padding:10px 12px;
  font:400 11.5px/1.6 var(--mono);color:var(--muted);overflow-x:auto;white-space:pre;margin:0}

/* ── TRACK RECORD: ghi trước → kết quả, hai cột đọc thành một chuyển động ── */
.tr{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--st);
  border-radius:14px;overflow:hidden;margin-bottom:15px;--st:var(--accent);
  box-shadow:0 1px 2px rgba(0,0,0,.05),0 10px 26px -18px rgba(0,0,0,.5)}
.tr.xac{--st:var(--c-xn)}.tr.song{--st:var(--c-song)}.tr.sua{--st:var(--c-sua)}
.tr.bac{--st:var(--c-bac)}.tr.cho{--st:var(--c-cho)}
.tr.song{border-left-style:dashed}
.tr.sua{border-left-style:double;border-left-width:6px}
.tr-head{display:flex;align-items:center;gap:11px;flex-wrap:wrap;padding:15px 18px 0}
.tr-head .moc{font:500 12.5px/1.7 var(--mono);color:var(--faint)}
.tr-body{display:grid;grid-template-columns:minmax(0,1fr) 34px minmax(0,1fr);padding:14px 18px 4px}
@media(max-width:820px){.tr-body{grid-template-columns:1fr}}
.tr-body .col{display:flex;flex-direction:column;gap:6px;padding:12px 14px;border-radius:10px}
.tr-body .truoc{background:var(--inset);border:1px solid var(--line-soft)}
.tr-body .sau{background:color-mix(in srgb,var(--st) 9%,transparent);
  border:1px solid color-mix(in srgb,var(--st) 30%,transparent)}
.tr-body .col .k{font:700 10px var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.tr-body .sau .k{color:var(--st)}
.tr-body .col .txt{font-size:13.5px;line-height:1.62;color:var(--muted)}
.tr-body .col .noi{font:500 11.5px/1.55 var(--mono);color:var(--faint);overflow-wrap:anywhere}
.tr-body .mui{display:flex;align-items:center;justify-content:center;color:var(--faint);font-size:18px}
@media(max-width:820px){.tr-body .mui{padding:8px 0;transform:rotate(90deg)}}
.tr-foot{padding:10px 18px 14px;font:500 12.5px/1.6 var(--mono)}

/* ── HIỆN DẦN khi lọt tầm mắt. Chỉ ĐỘ MỜ và VỊ TRÍ chạy — không con số nào chạy:
   hiệu ứng đếm-lên đã bị bỏ vì trong ~0,9s nó in ra những con số CHƯA TỪNG ĐO
   (NOTES §3). Lớp `chuyen` chỉ được gắn khi máy không xin giảm chuyển động, nên
   luật này không bao giờ khớp với người đã tắt — họ thấy trang tĩnh, đủ chữ ── */
html.chuyen [data-hien]{opacity:0;transform:translateY(16px);
  transition:opacity .55s ease,transform .55s cubic-bezier(.2,.7,.3,1)}
html.chuyen [data-hien].hien{opacity:1;transform:none}

@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
"""


# 🔴 TÊN HỆ ĐANG SHIP — hằng, để CHỖ KHÁC ĐỌC ĐƯỢC. Trước 06/08 con số này chỉ tồn
# tại dưới dạng một dòng gán bên trong `main()`, nên `preview.py` (cổng đo tràn khổ
# điện thoại) giữ bản sao riêng của nó và bản sao đó đứng ở `benchmark` — một hệ đã
# khai tử. Tức cổng đo màn hình hẹp đang đo MỘT CÁI HÌNH KHÁC cái đang ship, đúng
# họ lỗi mà chính docstring của `preview.py` cảnh báo. Một tên, một chỗ khai.
HE_MAC_DINH = "d2"

# Giá trị mặc định cho các khoá hệ D2 thêm vào — hai hệ cũ giữ nguyên bản khai của
# chúng và vẫn dựng được: thiếu khoá nào thì lấy ở đây, không nổ.
MAC_DINH_HE = dict(
    bg2="#f3efe7", bg2_toi="#15130f", card="#ffffff", card_toi="#1b1815",
    inset="#f5f1ea", inset_toi="#141210", line_soft="#efe9df", line_soft_toi="#241f1a",
    faint="#8a8073", faint_toi="#7d7365",
    xn="#0f8a3c", xn_toi="#35c46a", song="#1d5fae", song_toi="#4d9fff",
    sua="#a16207", sua_toi="#f0b429", bac="#be123c", bac_toi="#ef4056",
    cho="#64748b", cho_toi="#94a3b8",
    # ── Khoá mở cho BỐ CỤC, mặc định None = GIỮ NGUYÊN nếp D2 ────────────────────
    # `bg_toi`/`ink_toi` None ⇒ nền tối lấy `ink`, chữ tối lấy `paper` — phép lật
    # của D2. Bố cục nào muốn nền tối SÂU HƠN mực (v3: #100f0d) thì khai riêng, chứ
    # không được sửa `ink` — sửa `ink` là đổi luôn màu chữ ở nền sáng.
    bg_toi=None, ink_toi=None,
    # `cu` = "số cũ / đã chết", `bong` = đổ bóng. Hai token này KHÔNG tồn tại ở D2;
    # None ⇒ không sinh dòng nào, nên bản D2 không đổi một byte.
    cu=None, cu_toi=None, bong=None, bong_toi=None,
    # Ngăn xếp font. None ⇒ công thức cũ ('display', BODY_FONT, sans-serif).
    body=None, mono="'JetBrains Mono',ui-monospace,monospace",
)


# 🔴 TRỤC THỨ HAI, RỜI HẲN KHỎI HỆ MÀU. `HE_MAC_DINH`/`--theme` ở trên là BẢNG MÀU;
# trục này là HÌNH — thân CSS nào, vỏ trang nào, hàm mặt có tiêm hook không.
#
# Vì sao phải rời nhau: gộp vào một cờ thì không lượt nào đổi được màu mà giữ hình,
# hay ngược lại — `/thu-v3/` đã tồn tại trong vòng duyệt 10–11/08 để hỏi đúng câu
# "cùng identity màu, hình mới thì thế nào". Gộp cờ vẫn làm mất đường rollback D2.
#
# Vì sao tên là `--bo-cuc` chứ không phải `--he`: trong file này chữ "hệ" ĐÃ CÓ CHỦ —
# thông báo lỗi của `main()` in "hệ màu lạ". Hai vật cùng tên là thứ cắn về sau, và
# nó cắn ở chỗ khó thấy nhất: người đọc log.
#
# 🔵 CÙNG LUẬT "một tên, một chỗ khai" như đoạn ngay trên `HE_MAC_DINH`. `preview.py`
# phải ĐỌC hằng này, KHÔNG giữ bản sao — bản sao là đúng cách nó đứng lại ở `benchmark`
# và đi đo một cái hình khác cái đang ship.
BO_CUC_MAC_DINH = "v3"
BO_CUC_CO = {
    # D2 = bản rollback sau lượt lật production 11/08. Rỗng có chủ ý: cờ
    # `--bo-cuc d2` phải dựng lại đúng byte của giao diện đã phục vụ trước đó.
    "d2": {},
    # v3 = hệ đang phục vụ, từ `design-v3-wow`, phiên codex 10/08. Bản gốc tự khai "token màu vẫn là D2
    # nguyên văn"; ĐO LẠI bằng cách so `css(THEMES['d2'])` với ba khối `:root` của
    # `fold.css` thì lệch 6 ô + thêm 2 token. Chép nguyên văn xuống đây để chênh lệch
    # là một BẢN KHAI đọc được, không phải sai khác âm thầm giữa hai file.
    "v3": dict(
        # `faint` hai chiều đều tăng tương phản — README codex khai rõ, và đây là chỗ
        # DUY NHẤT trong bảng này ảnh hưởng khả năng đọc chứ không phải khẩu vị.
        faint="#746b60", faint_toi="#918678",
        # Nền tối sâu hơn mực, chữ tối dịu hơn giấy — v3 không dùng phép lật của D2.
        bg_toi="#100f0d", ink_toi="#f2ede6", muted_toi="#b0a596",
        cu="rgba(26,21,18,.34)", cu_toi="rgba(242,237,230,.30)",
        bong="0 1px 2px rgba(26,21,18,.05),0 24px 60px -36px rgba(26,21,18,.4)",
        bong_toi="0 2px 4px rgba(0,0,0,.3),0 28px 70px -36px rgba(0,0,0,.85)",
        # Thân chữ mặc font HỆ MÁY; Inter chỉ còn cầm phần display. Đây là quyết định
        # hình của v3, không phải thiếu sót — nên nó khai ở đây chứ không sửa THEMES.
        body="system-ui,sans-serif",
        mono="'JetBrains Mono',ui-monospace,SFMono-Regular,monospace",
    ),
}
BO_CUC = BO_CUC_MAC_DINH   # `main()` đặt lại theo --bo-cuc

# 🔴 BẢN THỬ — `--ban-thu`. Bật thì mỗi trang mang `noindex` và một dải khai rõ đây
# không phải bản phục vụ, còn `sitemap.xml`/`robots.txt` KHÔNG được sinh.
# Vì sao cả ba thứ đó đi CÙNG một cờ chứ không ai nhớ bật tay: `/thu-v3/` nằm trên
# CHÍNH tên miền thật, cùng gốc với trang đang phục vụ. Một bản thử lọt chỉ mục là
# hai URL cùng nội dung tranh nhau, và cái thắng có thể là cái sai — đúng lý lẽ đã
# viết cho `/ghi-truoc/` ở phần sitemap. Sinh sitemap trong bản thử còn tệ hơn: nó
# khai ra URL của trang THẬT (mọi `<loc>` đều dựng từ `BASE`), tức bản thử đi quảng
# cáo cho một tập đường dẫn không phải của nó.
BAN_THU = False

DAI_BAN_THU = ('<div class="wip-note"><b>bản thử</b>'
               '<span>Bố cục đang duyệt — không phải bản phục vụ. '
               'Bản thật ở <a href="/">blockpinned.com</a>.</span></div>')


def css(t: dict) -> str:
    """Tầng nhìn của site. Khối TOKEN sinh từ hệ màu; phần còn lại là hằng CSS_THAN.

    Vì sao tách hai: thân CSS không có chỗ nào cần nội suy, mà để nó trong f-string
    thì mọi dấu ngoặc nhọn phải nhân đôi — một dấu quên là một luật CSS chết trong
    im lặng. Tách ra thì thân viết như CSS thật.

    🔴 Nền mặc định THEO MÁY người đọc (prefers-color-scheme). Nút đổi nền chỉ ghi
    đè bằng data-theme; tắt JS thì trang vẫn có đủ hai nền. Đó là ràng buộc cũ của
    site (BRIEF-web.md §110) và nó vẫn đứng — nút là phần THÊM, không phải phần chịu tải.
    """
    v = {**MAC_DINH_HE, **t, **BO_CUC_CO[BO_CUC]}
    # Token CHỈ có ở bố cục mới. None ⇒ chuỗi rỗng ⇒ bản D2 không đổi một byte.
    them = lambda *k: "".join(f"--{n.replace('_', '-')}:{v[g]};"
                              for n, g in k if v[g] is not None)
    sang = (f"--bg:{v['paper']};--bg2:{v['bg2']};--card:{v['card']};--inset:{v['inset']};"
            f"--ink:{v['ink']};--muted:{v['muted']};--faint:{v['faint']};"
            f"--line:{v['line']};--line-soft:{v['line_soft']};--accent:{v['accent']};"
            f"--c-xn:{v['xn']};--c-song:{v['song']};--c-sua:{v['sua']};"
            f"--c-bac:{v['bac']};--c-cho:{v['cho']};"
            f"--nut-nen:{v['ink']};--nut-chu:{v['card']};color-scheme:light;"
            + them(("cu", "cu"), ("bong", "bong")))
    # 🔴 `bg_toi`/`ink_toi` là NGOẠI LỆ KHAI RÕ của phép lật D2 (nền tối = mực, chữ tối
    # = giấy). Bố cục v3 muốn nền sâu hơn mực; đường tắt "sửa `ink`" sẽ đổi luôn màu
    # CHỮ ở nền sáng — cùng một khoá gánh hai vai, và vai thứ hai hỏng trong im lặng.
    toi = (f"--bg:{v['bg_toi'] or v['ink']};--bg2:{v['bg2_toi']};--card:{v['card_toi']};"
           f"--inset:{v['inset_toi']};"
           f"--ink:{v['ink_toi'] or v['paper']};--muted:{v['muted_toi']};--faint:{v['faint_toi']};"
           f"--line:{v['line_toi']};--line-soft:{v['line_soft_toi']};--accent:{v['accent_toi']};"
           f"--c-xn:{v['xn_toi']};--c-song:{v['song_toi']};--c-sua:{v['sua_toi']};"
           f"--c-bac:{v['bac_toi']};--c-cho:{v['cho_toi']};"
           f"--nut-nen:{v['paper']};--nut-chu:{v['ink']};color-scheme:dark;"
           + them(("cu", "cu_toi"), ("bong", "bong_toi")))
    # Tính ngoài f-string: nhánh dự phòng có dấu nháy đơn, mà nháy đơn lồng trong
    # f-string là lỗi cú pháp ở Python < 3.12 — bản mirror phải chạy được ở mọi máy.
    than_chu = v["body"] or f"'{v['display']}',{BODY_FONT},sans-serif"
    return (f":root{{{sang}--display:'{v['display']}',{BODY_FONT},sans-serif;"
            f"--body:{than_chu};"
            f"--mono:{v['mono']};"
            f"--dw:{v['dw']};--gian-ten:{v['gian_ten']}}}\n"
            f"@media (prefers-color-scheme:dark){{:root:not([data-theme=\"sang\"]){{{toi}}}}}\n"
            f":root[data-theme=\"toi\"]{{{toi}}}\n"
            + than_css())


def than_css() -> str:
    """Thân CSS theo BỐ CỤC. D2 là hằng trong file; v3 là `v3.css` nằm cạnh.

    Vì sao v3 ở FILE chứ không phải hằng chuỗi: 125 KB nhét vào `build.py` thì mọi
    diff về sau đọc không nổi, và CSS mất luôn tô màu cú pháp. Đổi lại phải có một
    lượt kiểm sự tồn tại — thiếu file thì trang vẫn dựng ra nhưng KHÔNG CÓ HÌNH, tức
    hỏng theo kiểu im lặng nhất. Nên ở đây nổ.

    🔵 `ROOT` chạy đúng ở cả hai chỗ: kho gốc `site/v3.css`, mirror `v3.css` cạnh
    `build.py` — cùng hình dạng `keccak.py` đã đi, nên `publish_site.py` chỉ cần khai
    thêm tên file vào danh sách trắng.
    """
    if BO_CUC == "d2":
        return CSS_THAN
    rieng = _doc_ben_canh(f"{BO_CUC}.css", "không có hình")
    # Đường A đã chuyển cả trang bài VN lẫn biên lai EN sang markup WOW. Không còn
    # mặt nào của v3 cần mượn CSS D2; ghép nền cũ ở đây sẽ vừa tăng payload vừa cho
    # hai bộ selector cùng tranh một phần tử. `nen_than_bai()` giữ dưới dạng hồ sơ
    # cho phép đối chiếu vòng tích hợp 11/08, nhưng không còn đi ra production.
    return rieng


# Hai loại trang dựng bằng markup THÂN BÀI của D2 và chưa có bản thiết kế riêng ở bố
# cục mới. Sáu mặt còn lại cố tình KHÔNG nằm đây: chúng đang khớp byte với bản codex,
# và nền thừa kế đổ lên chúng là tự tay phá mất phép so duy nhất đang canh chúng.
# Thêm/bớt tên ở đây là quyết định thiết kế, không phải chi tiết kỹ thuật.
KHOANH_NEN = ":where(body.page-article,body.page-en)"


def nen_than_bai(rieng: str) -> str:
    """Rút từ `CSS_THAN` những luật cho tên mà bố cục mới KHÔNG có, khoanh vào
    `KHOANH_NEN`.

    🔴 VÌ SAO CÓ HÀM NÀY. `than_css()` THAY HẲN thân D2 chứ không gộp. Nhưng
    `build.py` vẫn sinh nguyên markup thân bài của D2 — `pre`, `table`, `td`, `li`,
    `strong`, `.claim`, `.cuon`… — mà bố cục mới không có luật nào cho chúng. Đo
    11/08: **13 thẻ + 43 class** đang dùng trong HTML mất sạch định dạng. Hậu quả
    nhìn thấy được: trang bài hiện ra gần như trần, và hai khung tràn ngang
    (`pre.l-bash` mất `overflow-x:auto` ⇒ 947px; một `<a>` không chỗ ngắt ⇒ 480px).

    🔴 VÌ SAO SINH LÚC BUILD, KHÔNG CHÉP TAY. Chép 24 KB luật sang `v3.css` là dựng
    bản sao thứ hai của một thứ đã có chủ — sửa `CSS_THAN` về sau thì bản chép đứng
    yên và KHÔNG cổng nào biết. Đúng họ "hai bản trôi lệch trong im lặng" mà
    `publish_site.py` sinh ra để chặn. Sinh lại mỗi lượt build thì tiêu chí *"tên nào
    bố cục mới còn thiếu"* được tính lại mỗi lần: hôm nào `v3.css` khai `.claim` thì
    luật `.claim` của D2 TỰ RỜI khỏi đây, không ai phải nhớ đi xoá.

    🔴 VÌ SAO `:where()`. Khoanh vùng bằng `body.page-article X` sẽ NÂNG độ đặc hiệu
    (0,1,2) và đè lên chính luật của bố cục mới — `.than h2` (0,1,1) sẽ THUA nền thừa
    kế, tức bản vá đi ngược ý đồ thiết kế ở đúng chỗ thiết kế có ý kiến. `:where()`
    đóng góp 0 nên selector giữ NGUYÊN độ đặc hiệu gốc: nền chỉ lấp chỗ trống, không
    giành chỗ đã có chủ.

    🔴 TIÊU CHÍ: bỏ một selector CHỈ KHI bố cục mới có selector Y HỆT. Ở đó — và chỉ
    ở đó — nền thừa kế sẽ thắng thuần tuý vì đứng sau, tức cướp một quyết định bố cục
    mới đã ra. Mọi chỗ khác giữ nguyên và để CASCADE phân xử: `.than h2` (0,1,1) vẫn
    thắng `h2` (0,0,1), `.uni-claim .dong .nhan` (0,3,0) vẫn thắng `.dong .nhan` (0,2,0).

    Bản đầu 11/08 dùng tiêu chí khác — *"giữ nếu selector nhắc tới một TÊN mà bố cục
    mới không có"* — và nó SAI theo cách chỉ ảnh chụp mới bắt được. `.dong .nhan` bị
    loại vì cả hai tên đều xuất hiện đâu đó trong `v3.css`; nhưng cả ba chỗ ấy
    (`.cred .nhan`, `.snapshot .sn-dau .nhan`, `.uni-claim .dong .nhan`) đều nằm trong
    ngữ cảnh KHÔNG tồn tại ở trang bài. Mất `display:block` ⇒ nhãn dính liền vào giá
    trị: *"GHIM TẠIRobinhood chain"*, *"ĐIỀU GÌ BÁC BỎ CLAIM NÀYDefiLlama đã nói"*.
    ⇒ **Tên class có mặt trong một file CSS không có nghĩa file ấy vẽ phần tử này ở
    đây.** Chỉ selector trùng khít mới là tranh chấp thật.

    `html`/`body`/`:root` bị loại riêng: khoanh vào trong thì chúng thành selector
    không bao giờ khớp (`body` nằm trong `body`), nên giữ lại chỉ tổ nặng file. Bố cục
    mới đã tự khai cả ba.
    """
    rieng, d2 = _bo_chu_thich(rieng), _bo_chu_thich(CSS_THAN)
    goc = {" ".join(s.split()) for blk in re.findall(r"([^{}]+)\{", rieng)
           for s in blk.split(",") if s.strip()}
    bo_rieng = {"html", "body", ":root"}

    nhom: dict = {}
    for dieu_kien, dau, than in _duyet_luat(d2):
        giu = [f"{KHOANH_NEN} {s}" for s in (" ".join(x.split()) for x in dau.split(","))
               if s and s not in goc and s not in bo_rieng]
        if giu:
            nhom.setdefault(dieu_kien, []).append(",".join(giu) + "{" + than.strip() + "}")
    if not nhom:
        raise LoiCong(f"bố cục {BO_CUC!r}: phép rút nền thân bài ra RỖNG — hoặc bố cục "
                      f"đã tự phủ hết markup D2 (thì xoá hàm này), hoặc phép rút hỏng")
    return "\n".join(t if dk is None else f"{dk}{{\n{t}\n}}"
                     for dk, t in ((k, "\n".join(v)) for k, v in nhom.items()))


def _bo_chu_thich(s: str) -> str:
    return re.sub(r"/\*.*?\*/", "", s, flags=re.S)


def _the_tran(css: str) -> set:
    """Thẻ HTML đứng MỘT MÌNH ở một selector — tức luật nền cho thẻ đó."""
    return {s.strip() for blk in re.findall(r"([^{}]+)\{", css)
            for s in blk.split(",") if re.fullmatch(r"[a-z][a-z0-9]*", s.strip())}


def _duyet_luat(css: str, dieu_kien=None):
    """Sinh (điều-kiện-@media, danh-sách-selector, thân) cho từng luật. `CSS_THAN`
    chỉ lồng một cấp (15 khối `@media`, không `@supports`/`@keyframes`) — đo 11/08."""
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            return
        dau = css[i:j].strip()
        if dau.startswith("@"):
            sau, k = 1, j + 1
            while k < n and sau:
                sau += (css[k] == "{") - (css[k] == "}")
                k += 1
            yield from _duyet_luat(css[j + 1:k - 1], dau)
            i = k
        else:
            k = css.find("}", j)
            if k < 0:
                return
            if dau:
                yield dieu_kien, dau, css[j + 1:k]
            i = k + 1


def than_js() -> str:
    """Tầng tương tác theo BỐ CỤC. D2 dùng `JS_HIEU_UNG`; v3 dùng `v3.js` nằm cạnh."""
    return _doc_ben_canh(f"{BO_CUC}.js", "mất tìm nhanh, menu khổ hẹp và mọi bộ lọc")


def _doc_ben_canh(ten: str, hong_ra_sao: str) -> str:
    """Đọc một file tài sản nằm CẠNH build.py, và NỔ nếu thiếu.

    Vì sao phải nổ chứ không trả chuỗi rỗng: thiếu `v3.css` thì trang vẫn dựng ra đủ
    chữ, đủ số, 12/12 cổng PASS — chỉ là không có hình. Đó là kiểu hỏng tệ nhất của
    lượt này: mọi tín hiệu đều xanh. Cổng duy nhất bắt được nó là lượt kiểm sự tồn tại
    ngay tại đây.

    🔵 `ROOT` chạy đúng ở cả hai chỗ — kho gốc `site/`, mirror thì cạnh `build.py` —
    cùng hình dạng `keccak.py` đã đi, nên `publish_site.py` chỉ cần khai thêm tên file.
    """
    p = ROOT / ten
    if not p.exists():
        raise LoiCong(f"bố cục {BO_CUC!r} cần {ten} nằm cạnh build.py — thiếu nó thì "
                      f"trang vẫn dựng ra và mọi cổng vẫn PASS, chỉ là {hong_ra_sao}")
    return p.read_text(encoding="utf-8")


# ════════════════════════════════════════════════════════════════════════ FONT
# 🔴 TỰ HOST, KHÔNG CDN — 06/08/2026. `BRIEF-web.md` ghi "không CDN" từ đầu, mà bản
# chạy suốt từ 30/07 vẫn nạp `fonts.googleapis.com`. Ba cái giá của CDN, cái thứ ba
# mới là cái đắt:
#  ① hai lượt bắt tay tên miền lạ trước khi có chữ đầu tiên;
#  ② trang phụ thuộc một bên thứ ba để đọc được;
#  ③ mỗi người mở trang đều để lại một lượt gọi tới máy chủ của Google, kèm địa chỉ
#     IP và trang họ đang đọc. Kênh này bán "số nào cũng truy ngược được" — không có
#     lý do gì bắt người đọc trả bằng dấu vết của họ để đọc nó.
#
# 🔵 BE VIETNAM PRO ĐÃ BỎ, và bỏ theo một PHÉP ĐO chứ không theo cảm giác nhẹ máy:
# quét toàn bộ chữ hiện ra của bản dựng 06/08 — 227 ký tự khác nhau — thì **không có
# một ký tự tiếng Việt nào** rơi ra ngoài ba subset của Inter. 18 ký tự nằm ngoài đều
# là mũi tên, ký hiệu toán, mặt trời/mặt trăng và emoji, mà 17/18 nằm ngoài MỌI subset
# của Inter ⇒ Be Vietnam Pro không đỡ được cái nào trong số đó. Nó nằm trong lượt tải
# để phòng một ca không xảy ra. Ca đó xảy ra thì trình duyệt rơi về `system-ui`, và
# đó là hành vi đúng — không phải một trang hỏng.
#
# Bản biến thiên (variable): MỘT file chở cả dải 400–800, thay vì một file mỗi cỡ.
# unicode-range chép NGUYÊN VĂN từ CSS Google phát cho chính bộ file này (06/08/2026)
# — sai một dải thì trình duyệt tải nhầm file, hoặc tải cả ba trong khi chỉ cần một.
#
# 🔴 THỨ TỰ DƯỚI ĐÂY LÀ MỘT LUẬT, KHÔNG PHẢI SẮP CHO ĐẸP: `vietnamese` phải đứng
# CUỐI mỗi họ. Khi hai `@font-face` cùng họ cùng nhận một ký tự, CSS lấy khai báo
# ĐỨNG SAU. Mà dải `latin-ext` (U+0100-02BA) TRÙM lên 13 chữ cái tiếng Việt —
# Ă ă Đ đ ĩ ũ Ơ ơ Ư ư ỳ ỷ ỹ. Xác bằng phép đo trên chính bản dựng: đặt latin-ext
# sau, trình duyệt tải **84 KB** file latin-ext chỉ để dựng 13 chữ đó, trong khi
# **0** ký tự trên toàn site cần riêng dải latin-ext. Đặt vietnamese sau thì 13 chữ
# ấy về file 10 KB, và latin-ext nằm im cho tới khi có bài dùng tới nó thật.
FONT_MAT = [
    ("Inter", "inter-latin.woff2", "400 800",
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
     "U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("Inter", "inter-latin-ext.woff2", "400 800",
     "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
     "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,"
     "U+2113,U+2C60-2C7F,U+A720-A7FF"),
    ("Inter", "inter-vietnamese.woff2", "400 800",
     "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,"
     "U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB"),
    ("JetBrains Mono", "jetbrains-mono-latin.woff2", "400 700",
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
     "U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("JetBrains Mono", "jetbrains-mono-latin-ext.woff2", "400 700",
     "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,"
     "U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,"
     "U+2113,U+2C60-2C7F,U+A720-A7FF"),
    ("JetBrains Mono", "jetbrains-mono-vietnamese.woff2", "400 700",
     "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,"
     "U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB"),
]
# Hai subset này có mặt trên MỌI trang (chữ Việt có dấu + số ở khối mono) nên chúng
# được nạp trước; latin-ext chỉ tải khi có ký tự thuộc dải đó, và bản dựng hiện tại
# không có ký tự nào — nó nằm đây làm lưới đỡ cho bài sau, không tốn lượt tải nào.
FONT_NAP_TRUOC = ["inter-latin.woff2", "inter-vietnamese.woff2",
                  "jetbrains-mono-latin.woff2", "jetbrains-mono-vietnamese.woff2"]


def font_face(goc: str) -> str:
    """Khối @font-face, đường dẫn TƯƠNG ĐỐI theo độ sâu trang.

    🔴 Không dùng đường tuyệt đối `/font/…`: `preview.py` dựng trang bằng `file://`
    để đo tràn khổ điện thoại, và ở đó `/font/` trỏ ra gốc ổ đĩa ⇒ ảnh chụp của cổng
    sẽ là ảnh một trang KHÔNG CÓ font thật. Cổng đo phải nhìn đúng cái sắp ship.
    """
    g = goc or "."
    return "".join(
        f"@font-face{{font-family:'{ho}';font-style:normal;font-weight:{nang};"
        f"font-display:swap;src:url({g}/font/{tep}) format('woff2');"
        f"unicode-range:{dai}}}"
        for ho, tep, nang, dai in FONT_MAT)

# ═══════════════════════════════════════════════════════ TỦ KÍNH THEO TOKEN
# Mọi bài KHAI `token:` ở front matter. Không suy từ tiêu đề: chữ "Uniswap" nằm trong
# cả bài về DefiLlama lẫn bài về Robinhood Chain lẫn bài về Lido (đoạn so sánh), nên
# một trang hồ sơ dựng bằng phép đoán sẽ sai đúng ở chỗ nó được dùng để chứng minh
# chiều sâu. Token lạ ⇒ CHẶN build: thêm tên vào đây là một quyết định, không phải
# một lượt gõ.
TOKEN_TEN = {"UNI": "Uniswap", "LDO": "Lido", "HYPE": "Hyperliquid", "PENDLE": "Pendle",
             "CAKE": "PancakeSwap", "MORPHO": "Morpho", "PUMP": "pump.fun",
             "SKY": "Sky"}

# Tủ kính hiện mở cho ĐÚNG MỘT token, khai ở đây; toàn bộ nội dung trang sinh từ dữ
# liệu, nên đổi dòng này là trang tự dựng lại cho token khác. Kèm SÀN: dưới 3 bài thì
# chặn — một tủ kính hai bài trưng ra ít hơn cái tên của nó hứa.
TU_KINH = "UNI"
TU_KINH_SAN = 3
TU_KINH_DUONG = f"token/{TU_KINH.lower()}/"

# Mục trên thanh điều hướng — dựng từ ĐÂY, không gõ tay ở từng trang. Trang nào chưa
# tồn tại thì main() tắt mục đó: cổng ⑪ (liên kết) sẽ chặn build nếu một mục trỏ vào
# thư mục không có index.html, và đó là hành vi đúng.
#
# 🔴 06/08 vòng 3, hai đổi do user quyết:
#  ① Mục "Token" trỏ `/token/` (MỤC LỤC) chứ không trỏ thẳng tủ kính UNI. Tủ kính chỉ
#    mở cho token đủ sàn, nhưng bản đồ phải chở ĐỦ token — nếu không thì HYPE và
#    PENDLE biến mất khỏi site dù bài của chúng vẫn sống.
#  ② `/du-lieu/` RỜI thanh điều hướng, URL giữ nguyên. Lý do đo được: 3 file ở đó đều
#    thuộc đúng MỘT bài (#7), tức nó phủ 1/8 số bài mà lại đứng ngang hàng Facts và
#    Track record — mục nav hứa nhiều hơn cái nó chở. Nay nó được dẫn từ chỗ nó thuộc
#    về: ô Dữ liệu trong bản đồ trang chủ, và link trong chính bài #7.
MUC_DIEU_HUONG = [("", "Trang chủ"), ("bai/", "Bài viết"), ("token/", "Token"),
                  ("track-record/", "Track record"), ("facts/", "Facts")]
CO_TRANG = {"bai/": False, "facts/": False, "track-record/": False, "token/": False,
            TU_KINH_DUONG: False, "du-lieu/": False}

# Primer không phải bài theo ngày và cũng không phải tủ claim của UNI. Nó có nguồn chữ
# riêng trong `drafts/`, nhưng chỉ phần nằm giữa hai marker được phép đi ra web. Khi
# mirror công khai dựng độc lập, `publish_site.py` vật chất hoá đúng phần đó thành
# `content/primers/<id>.md`; builder kiểm cùng một sha256 ở cả hai đường.
PRIMER_DIR = CONTENT / "primers"


def _than_primer_tu_draft(raw: str, cfg: dict, o: str) -> str:
    start, end = cfg.get("start_marker", ""), cfg.get("end_marker", "")
    if not start or not end:
        raise LoiCong(f"primer thiếu start_marker/end_marker — {o}")
    lines = raw.splitlines()
    dau = [n for n, line in enumerate(lines) if line.startswith(start)]
    cuoi = [n for n, line in enumerate(lines) if line == end]
    if len(dau) != 1 or len(cuoi) != 1 or dau[0] >= cuoi[0]:
        raise LoiCong(f"marker THÂN BÀI primer phải khớp đúng một cặp có thứ tự — {o}")
    body = "\n".join(lines[dau[0] + 1:cuoi[0]]).strip() + "\n"
    if body == "\n":
        raise LoiCong(f"marker primer khớp nhưng thân rỗng — FAIL lượt gọi, không phải bài rỗng — {o}")
    return body


def _chen_sau_mot_lan(body: str, anchor: str, chen: str, o: str) -> str:
    n = body.count(anchor)
    if n != 1:
        raise LoiCong(f"anchor primer phải xuất hiện đúng 1 lần, hiện {n}: {anchor[:70]!r} — {o}")
    return body.replace(anchor, anchor + "\n\n" + chen, 1)


def doc_primers() -> list[dict]:
    """Đọc cấu hình Primer và buộc chữ · visual · nguồn cùng chốt vào một bản."""
    if not PRIMER_DIR.exists():
        return []
    ra, ids, paths, tokens = [], set(), set(), set()
    for p in sorted(PRIMER_DIR.glob("*.json")):
        o = f"content/primers/{p.name}"
        try:
            cfg = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise LoiCong(f"JSON primer hỏng — {o}: {e}") from e
        bat_buoc = ("id", "token", "name", "title", "description", "pin", "edition", "lastmod",
                    "draft", "body_sha256", "start_marker", "end_marker",
                    "source_claims", "placements", "visuals", "recap_heading")
        thieu = [k for k in bat_buoc if cfg.get(k) in (None, "", [])]
        if thieu:
            raise LoiCong(f"primer thiếu {thieu} — {o}")
        pid, token = str(cfg["id"]), str(cfg["token"])
        if not re.fullmatch(r"[a-z0-9-]+", pid) or not re.fullmatch(r"[A-Z0-9]+", token):
            raise LoiCong(f"primer id/token sai dạng — {o}: {pid!r}/{token!r}")
        path = f"token/{pid}/"
        if pid in ids or path in paths or token in tokens:
            raise LoiCong(f"primer trùng id/path/token — {o}")
        ids.add(pid); paths.add(path); tokens.add(token)
        art_direction = str(cfg.get("art_direction", ""))
        if art_direction not in {"", "machine-valves"}:
            raise LoiCong(f"primer art_direction lạ {art_direction!r} — {o}")
        draft_rel = pathlib.PurePosixPath(str(cfg["draft"]))
        if draft_rel.is_absolute() or ".." in draft_rel.parts:
            raise LoiCong(f"primer draft phải là đường tương đối nằm trong kho — {o}")
        draft = ROOT.parent / pathlib.Path(*draft_rel.parts)
        vat_chat = PRIMER_DIR / f"{pid}.md"
        if draft.exists():
            body = _than_primer_tu_draft(draft.read_text(encoding="utf-8"), cfg, o)
            cfg["_body_source"] = str(draft_rel)
        elif vat_chat.exists():
            body = vat_chat.read_text(encoding="utf-8").strip() + "\n"
            cfg["_body_source"] = f"content/primers/{pid}.md"
        else:
            raise LoiCong(f"primer thiếu cả draft riêng lẫn thân đã vật chất hoá — {o}")
        got = hashlib.sha256(body.encode()).hexdigest()
        if got != cfg["body_sha256"]:
            raise LoiCong(f"primer body sha256 lệch: cấu hình {cfg['body_sha256']}, đọc được {got} — {o}")
        if not body.startswith("# "):
            raise LoiCong(f"primer phải bắt đầu bằng đúng một H1 — {o}")
        h1, body = body.split("\n", 1)
        if h1[2:].strip() != cfg["title"]:
            raise LoiCong(f"title primer không trùng H1 trong draft — {o}")
        body = body.lstrip()
        boundary = "# 🔎 Lớp kiểm chứng"
        if body.count(boundary) != 1:
            raise LoiCong(f"primer phải có đúng một ranh giới '# 🔎 Lớp kiểm chứng' — {o}")
        claims = cfg["source_claims"]
        if (not isinstance(claims, list) or not claims
                or any(not isinstance(c, dict) or not c.get("id") or not c.get("label")
                       for c in claims)):
            raise LoiCong(f"primer source_claims cần id/label — {o}")
        # Kho gốc phải giữ đủ con trỏ desk để cổng provenance còn có
        # thứ để kiểm. Mirror public được publisher chủ động lột trường
        # `source`; khi đó thân đã vật chất hoá là nguồn đọc độc lập.
        if draft.exists() and any(not c.get("source") for c in claims):
            raise LoiCong(f"primer kho gốc source_claims cần source nội bộ — {o}")
        claim_ids = [str(c["id"]) for c in claims]
        if len(claim_ids) != len(set(claim_ids)) or any(
                not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]+", x) for x in claim_ids):
            raise LoiCong(f"primer source_claims có id trùng hoặc sai dạng — {o}")
        placements = cfg["placements"]
        visuals = cfg["visuals"]
        if not isinstance(placements, list) or not 3 <= len(visuals) <= 5:
            raise LoiCong(f"primer cần 3–5 visual và placements dạng danh sách — {o}")
        if any(not isinstance(v, dict) or not v.get("public_scope") for v in visuals):
            raise LoiCong(f"primer visual cần public_scope thay cho con trỏ desk — {o}")
        pids = []
        for place in placements:
            if not isinstance(place, dict) or not place.get("visual") or not place.get("after"):
                raise LoiCong(f"primer placement cần visual/after — {o}")
            pids.append(str(place["visual"]))
            body = _chen_sau_mot_lan(body, str(place["after"]),
                                      f'{{{{visual:{place["visual"]}}}}}', o)
        vids = [str(v.get("id")) for v in visuals if isinstance(v, dict)]
        if len(pids) != len(set(pids)) or set(pids) != set(vids):
            raise LoiCong(f"primer placements và visuals không khớp — {o}")
        # Draft là chủ nội dung; lớp web chỉ được phép thay đúng những chuỗi đã khai,
        # kèm số lượt. Mục đích là đi qua từ điển public mà không lặng lẽ biên tập lại
        # một bản 30 nghìn ký tự. Draft đổi một lượt là cổng count nổ và buộc xem lại.
        for rep in cfg.get("web_replacements", []):
            if (not isinstance(rep, dict) or not rep.get("from") or not rep.get("to")
                    or not isinstance(rep.get("count"), int) or rep["count"] <= 0):
                raise LoiCong(f"primer web_replacements cần from/to/count dương — {o}")
            n = body.count(rep["from"])
            if n != rep["count"]:
                raise LoiCong(f"primer replacement {rep['from']!r} chờ {rep['count']} lượt, thấy {n} — {o}")
            body = body.replace(rep["from"], rep["to"])
        public_cfg = {k: cfg[k] for k in ("title", "description", "pin", "edition", "visuals")}
        cong_ngon_ngu(body + "\n" + json.dumps(public_cfg, ensure_ascii=False), o)
        cong_ngoi_xung(body, o)
        cong_visuals(body, visuals, claims, o)
        story, verify = body.split(boundary, 1)
        if not story.strip() or not verify.strip():
            raise LoiCong(f"primer có lớp KỂ hoặc VERIFY rỗng — {o}")
        if story.count(cfg["recap_heading"]) != 1:
            raise LoiCong(f"recap_heading primer phải khớp đúng một lần — {o}")
        cfg.update(_path=path, _story=story.strip(), _verify=verify.strip(),
                   _origin=o, _blockers=len(re.findall(r"^(?:🔴|⚠️)", body, re.M)))
        CO_TRANG[path] = True
        ra.append(cfg)
    return ra


def trang_primer(cfg: dict) -> str:
    """Token Primer: mạch kể mở; lớp kiểm chứng có tên và đóng mặc định."""
    o, visuals = cfg["_origin"], cfg["visuals"]
    chapters = {str(place["visual"]): f"{n:02d}"
                for n, place in enumerate(cfg["placements"], 1)}
    art_direction = str(cfg.get("art_direction", ""))
    story = render(cfg["_story"], o, visuals, show_claim_refs=False,
                   visual_chapters=chapters, art_direction=art_direction).replace(
        '<div class="cuon', '<div class="bang')
    verify = render(cfg["_verify"], o, visuals, show_claim_refs=False,
                    visual_chapters=chapters, art_direction=art_direction).replace(
        '<div class="cuon', '<div class="bang')
    if art_direction == "machine-valves":
        story = _bo_cham_trang_thai_primer(story)
        verify = _bo_cham_trang_thai_primer(verify)
    recap_id = slug(cfg["recap_heading"].removeprefix("## "))
    recap_h2 = f'<h2 id="{recap_id}">'
    if story.count(recap_h2) != 1:
        raise LoiCong(f"renderer làm rơi heading RECAP của primer — {o}")
    story = story.replace(
        recap_h2,
        f'<p class="primer-return"><a href="#visual-{cfg["visuals"][0]["id"]}">'
        '↖ Quay lại bản đồ bốn tầng trước khi đọc phần kết</a></p>' + recap_h2, 1)
    if art_direction == "machine-valves":
        story = _gom_snapshot_primer(story, recap_id, o)
    jump = []
    for heading in re.findall(r"^##\s+(.+)$", cfg["_story"], re.M)[:4]:
        jump.append(f'<a href="#{slug(heading)}">{ihtml.escape(re.sub(r"[*_`]", "", heading))}</a>')
    hero_ghost = (f'<span class="primer-hero-ghost" aria-hidden="true">'
                  f'{ihtml.escape(cfg["token"])}</span>') if art_direction == "machine-valves" else (
                  f'<span class="ghost-num" aria-hidden="true">{ihtml.escape(cfg["token"])}</span>')
    hero_top_open = '<div class="primer-hero-top">' if art_direction == "machine-valves" else ""
    hero_top_close = '</div>' if art_direction == "machine-valves" else ""
    machine_index = ""
    if art_direction == "machine-valves":
        visual_map = {str(v["id"]): v for v in visuals}
        links = []
        for place in cfg["placements"]:
            vid = str(place["visual"]); v = visual_map[vid]
            links.append(
                f'<a href="#visual-{ihtml.escape(vid, quote=True)}"><b>{chapters[vid]}</b>'
                f'<small>{ihtml.escape(v.get("eyebrow", v["type"]).upper())}</small>'
                f'<span>{ihtml.escape(v["title"])}</span></a>')
        machine_index = ('<nav class="primer-machine-index" '
                         'aria-label="Một cỗ máy, bốn lăng kính">'
                         + "".join(links) + '</nav>')
    than = f'''<section class="hero primer-hero">
  {hero_ghost}
  {hero_top_open}<div class="article-path" aria-label="Vị trí Token Primer"><a href="../../">BlockPinned</a><span>/</span><a href="../">Token</a><span>/</span><b>{ihtml.escape(cfg["token"])}</b></div>
  <span class="hero-code" aria-hidden="true">TOKEN PRIMER · SYSTEM / CAPITAL / CAPTURE</span>{hero_top_close}
  <p class="eyebrow"><span>Token Primer · {ihtml.escape(cfg["token"])}</span><span class="im">đọc cỗ máy trước · đọc token sau</span></p>
  <h1 class="display">{_tieu_de_nhan(cfg["title"])}</h1>
  <p class="subline">{ihtml.escape(cfg["description"])}</p>
  <div class="primer-pin"><span><b>GHIM TẠI</b>{ihtml.escape(cfg["pin"])}</span><span><b>BẢN NỘI DUNG</b>{ihtml.escape(cfg["edition"])}</span><span><b>LOẠI</b>Sống theo đối tượng, không theo ngày đăng</span></div>
  {machine_index}
</section>
<nav class="primer-nav" aria-label="Đường đọc Token Primer"><span>Đường đọc</span>{"".join(jump)}<a href="#lop-kiem-chung">Lớp kiểm chứng ↓</a></nav>
<section class="than article-body article-body-centered primer-body" id="primer-story">
  {story}
  <details class="primer-verify" id="lop-kiem-chung">
    <summary><span class="primer-verify-mark" aria-hidden="true">🔎</span><span class="primer-verify-copy"><small>VERIFY · CHỦ ĐỘNG MỞ</small><strong>Lớp kiểm chứng</strong><p>Từ đây trở xuống là phần để tự đo lại, không phải phần bắt buộc để hiểu cỗ máy Sky.</p></span><span class="primer-verify-toggle">Mở ↓</span></summary>
    <div class="primer-verify-body">{verify}</div>
  </details>
</section>'''
    cong_visual_html(than, visuals, o)
    if '<details class="primer-verify" id="lop-kiem-chung" open' in than:
        raise LoiCong(f"VERIFY primer phải đóng mặc định — {o}")
    if than.count('class="chan"') != cfg["_blockers"]:
        raise LoiCong(f"renderer làm rơi câu chặn inline của primer — {o}")
    if art_direction == "machine-valves":
        required = ('class="primer-machine-index"', 'class="pm-subtraction"',
                    'class="pm-map-ghost"', 'class="pm-machine"',
                    'class="pm-ledger"', 'class="pm-capture"')
        missing = [x for x in required if x not in than]
        if missing or than.count('class="primer-chapter-no"') != len(visuals):
            raise LoiCong(f"art direction machine-valves dựng thiếu cấu trúc: {missing} — {o}")
        metric = _metric_tieu_de(cfg["title"])
        if metric and f"${metric}" in cfg["title"] and (
                f'<span class="nhan-manh">${ihtml.escape(metric)}</span>' not in than):
            raise LoiCong(f"primer làm rơi ký hiệu tiền khỏi nhấn số ở hero — {o}")
        headerless = re.findall(
            r'<table([^>]*)><thead><tr>(?:<th></th>)+</tr>', than)
        if any("table-key-value" not in (
                re.search(r'class="([^"]*)"', attrs).group(1).split()
                if re.search(r'class="([^"]*)"', attrs) else []) for attrs in headerless):
            raise LoiCong(f"primer làm rơi kiểu bảng key-value trong thân bài — {o}")
        html_classes = {name for blob in re.findall(r'class="([^"]*)"', than)
                        for name in blob.split()}
        snapshot_html = re.search(
            r'<section class="primer-snapshot-suite">(.*?)</section>\s*<h2 ', than, re.S)
        recap_html = re.search(
            r'<section class="primer-recap">(.*?)</section>\s*<h2 ', than, re.S)
        leaked_card_roles = ([name for name in ("table-finance", "table-costs", "table-chain")
                              if name in html_classes])
        misplaced_panels = ([name for name in ("snapshot-panel-finance", "snapshot-panel-costs",
                                               "snapshot-panel-chain")
                             if recap_html and name in recap_html.group(1)])
        missing_reports = ([name for name in ("report-finance", "report-costs", "report-chain")
                            if not snapshot_html or name not in snapshot_html.group(1)])
        if not snapshot_html or not recap_html or leaked_card_roles or misplaced_panels or missing_reports:
            raise LoiCong(
                f"recap/report Primer sai ranh giới: card={leaked_card_roles}, "
                f"panel-trong-recap={misplaced_panels}, report-thiếu={missing_reports} — {o}")
        editorial = ("table-compare", "table-process", "primer-allocation",
                     "table-status", "report-finance", "report-costs", "report-chain",
                     "primer-recap", "primer-snapshot-suite",
                     "snapshot-panel-finance", "snapshot-panel-costs", "snapshot-panel-chain")
        missing_editorial = [name for name in editorial if name not in html_classes]
        if missing_editorial or '<pre><code>Net Revenue' in than:
            raise LoiCong(f"primer dựng thiếu data module biên tập: {missing_editorial} — {o}")
        status_dots = [dot for dot in ("🔴", "🟢", "🔵", "⚪", "⚠️", "⚠") if dot in than]
        if status_dots:
            raise LoiCong(f"primer machine-valves còn emoji trạng thái trong mặt đọc: {status_dots} — {o}")
    # Cổng này đo HTML đã render, không đo ý định trong CSS. Chỉ
    # `display:none` thì con trỏ desk vẫn nằm trong source public và vẫn là leak.
    private_refs = [str(c["id"]) for c in cfg["source_claims"]]
    private_refs += [str(c.get("source", "")) for c in cfg["source_claims"] if c.get("source")]
    leaked = [ref for ref in private_refs if ref and ref in than]
    if leaked:
        raise LoiCong(f"primer làm lộ con trỏ desk: {leaked} — {o}")
    if "{{visual:" in than or "Không phải lời khuyên đầu tư." not in than or "@BLOCKPINNED" not in than:
        raise LoiCong(f"primer làm rơi directive/disclaimer/chữ ký — {o}")
    return than

# Nút đổi nền. Trang KHÔNG phụ thuộc nó: mặc định đọc prefers-color-scheme của máy,
# nút chỉ ghi đè và nhớ lựa chọn. Tắt JS thì mất nút, không mất nền tối.
JS_NEN = """
(function(){
  var d=document.documentElement,c=localStorage.getItem('bp-nen');
  // Hai lớp này gắn TRONG <head>, trước lượt vẽ đầu tiên — gắn muộn hơn thì trang
  // nháy một nhịp. 'js' = có JavaScript (mở khoá con trỏ chuột cho nút lọc);
  // 'chuyen' = máy KHÔNG xin giảm chuyển động, tức được phép chạy hiệu ứng.
  d.classList.add('js');
  if(!matchMedia('(prefers-reduced-motion:reduce)').matches)d.classList.add('chuyen');
  if(c==='toi'||c==='sang')d.setAttribute('data-theme',c);
  document.addEventListener('click',function(e){
    var b=e.target.closest('#nut-nen'); if(!b)return;
    var toi=matchMedia('(prefers-color-scheme:dark)').matches;
    var nay=d.getAttribute('data-theme')||(toi?'toi':'sang');
    var moi=nay==='toi'?'sang':'toi';
    d.setAttribute('data-theme',moi); localStorage.setItem('bp-nen',moi);
  });
})();
"""


# 🔴 BẢN v3 CỦA KHỐI TRÊN — CỐ Ý CẮT MẤT HANDLER CLICK, và đây là lý do:
# `v3.js` TỰ CẦM nút đổi nền (cùng khoá `bp-nen`, cùng `data-theme`). Ship cả hai thì
# mỗi cú bấm chạy hai lượt lật và nền đứng im — một lỗi không log nào báo, chỉ người
# bấm mới thấy. Phần PHẢI ở lại `<head>` là phần trước-lượt-vẽ: thiếu nó thì trang
# nháy một nhịp sáng trước khi đổi sang nền tối đã lưu.
# ⇒ `<head>` giữ trạng thái, cuối `<body>` giữ tương tác. Chia theo THỜI ĐIỂM CHẠY,
# không theo tính năng — đó là cách duy nhất hai file không giẫm nhau.
JS_NEN_V3 = """
(function(){
  var d=document.documentElement,c=localStorage.getItem('bp-nen');
  d.classList.add('js');
  if(!matchMedia('(prefers-reduced-motion:reduce)').matches)d.classList.add('chuyen');
  if(c==='toi'||c==='sang')d.setAttribute('data-theme',c);
})();
"""


JS_HIEU_UNG = """
// Tầng hiệu ứng. BA luật tự đặt, kiểm được bằng cách tắt JS rồi mở lại trang:
//  ① KHÔNG con số nào do JS sinh ra. Mọi chữ số đã nằm trong HTML từ lúc dựng; tầng
//     này chỉ đổi độ mờ, vị trí, và ẩn/hiện dòng. (Hiệu ứng đếm-lên bị bỏ 05/08 vì
//     trong ~0,9s nó in ra những con số CHƯA TỪNG ĐO — NOTES §3.)
//  ② Tắt JS thì trang vẫn ĐỦ: thanh đứng ở đúng tỉ lệ, mọi dòng hiện, chú giải đọc
//     được, dải bài vẫn vuốt ngang được bằng ngón tay.
//  ③ Người xin giảm chuyển động không mất chức năng nào — chỉ mất phần chạy.
(function(){
  var goc=document.documentElement, chuyen=goc.classList.contains('chuyen');

  // ── hiện dần + thanh xếp chồng chạy từ 0 khi khối lọt tầm mắt
  function mo(e){
    e.classList.add('hien');
    e.querySelectorAll('.stack').forEach(function(s){s.classList.add('chay')});
  }
  var khoi=document.querySelectorAll('[data-hien]');
  // 🔴 threshold PHẢI là 0. Bản đầu để .12 — tức "12% DIỆN TÍCH KHỐI phải lọt tầm
  // mắt" — và nó im lặng nuốt đúng khối quan trọng nhất: danh sách claim cao gấp
  // nhiều lần màn hình, nên 12% của nó không bao giờ lọt và khối nằm ở opacity 0
  // vĩnh viễn. Ngưỡng tính theo diện tích PHẦN TỬ chứ không theo màn hình, nên khối
  // càng dài thì luật càng dễ ăn mất nó. Đo được ở ảnh chụp khổ điện thoại 06/08.
  if(chuyen&&window.IntersectionObserver){
    var xem=new IntersectionObserver(function(ds,o){
      ds.forEach(function(m){if(m.isIntersecting){mo(m.target);o.unobserve(m.target)}});
    },{rootMargin:'0px 0px -6% 0px',threshold:0});
    khoi.forEach(function(e){xem.observe(e)});
    // 🔴 LƯỚI AN TOÀN, không phải phần trang trí: nếu vì bất cứ lý do gì mà lượt gọi
    // của bộ theo dõi không chạy (ảnh chụp máy, trình duyệt lạ, tab nền), khối sẽ nằm
    // ở opacity 0 VĨNH VIỄN — tức hiệu ứng làm mất nội dung. Xác 06/08: ảnh chụp khổ
    // điện thoại của chính cổng preview ra một trang trắng từ khối thứ hai trở xuống.
    // Sau 3 giây thì hiện hết, bất kể có ai cuộn hay không.
    setTimeout(function(){khoi.forEach(mo)},3000);
  }else{ khoi.forEach(mo); }
  // thanh nằm ngoài mọi khối [data-hien] vẫn phải ở đúng tỉ lệ, không đứng ở 0
  document.querySelectorAll('.stack').forEach(function(s){
    if(!s.closest('[data-hien]'))s.classList.add('chay');
  });

  // ── LỌC theo trạng thái. Chú giải của thanh CHÍNH LÀ bộ lọc — không dựng bộ điều
  //    khiển thứ hai, vì hai bộ là hai bản sẽ trôi lệch. Vùng đích tự khai bằng
  //    data-loc-vung, và giá trị của nó là bộ lọc mặc định của trang đó.
  var vung=document.querySelector('[data-loc-vung]');
  if(vung){
    var macDinh=vung.getAttribute('data-loc-vung'),
        nut=document.querySelectorAll('button[data-loc]'),
        dong=vung.querySelectorAll('[data-st]'),
        lo=document.getElementById('loc-lo'), dangLoc=null,
        them=document.getElementById('mo-them'),
        cap=parseInt(vung.getAttribute('data-cap')||'0',10), moRong=false;
    // Màn hẹp cắt sâu hơn: cùng 5 dòng đó trên điện thoại cao gần một màn rưỡi, mà
    // thứ user muốn thấy sớm là BÀI. Ba dòng đủ để hiểu khối này là gì.
    if(cap&&matchMedia('(max-width:620px)').matches)cap=3;
    var ap=function(loc){
      var n=0;                       // số dòng KHỚP bộ lọc
      dong.forEach(function(d){
        var khop = loc==='het' ? true
                 : loc==='doi' ? d.getAttribute('data-doi')==='1'
                 : d.getAttribute('data-st')===loc;
        if(khop)n++;
        // cắt bớt là việc của TẦNG NHÌN: dòng bị cắt vẫn nằm trong trang, vẫn tìm
        // được bằng Ctrl+F sau khi bấm mở, và số trên nút là số thật của bộ lọc.
        d.hidden = !khop || (cap && !moRong && n>cap);
      });
      nut.forEach(function(b){
        b.setAttribute('aria-pressed',b.getAttribute('data-loc')===loc?'true':'false');
      });
      var hien = (cap && !moRong) ? Math.min(n,cap) : n;
      if(lo)lo.textContent = hien<n ? hien+'/'+n+' dòng đang hiện' : n+' dòng đang hiện';
      if(them){
        them.hidden = !cap || n<=cap;
        them.textContent = moRong ? 'Thu gọn' : 'Xem tất cả '+n+' dòng';
      }
      dangLoc=loc;
    };
    if(them)them.addEventListener('click',function(){moRong=!moRong;ap(dangLoc)});
    nut.forEach(function(b){
      b.addEventListener('click',function(){
        var l=b.getAttribute('data-loc');
        ap(l===dangLoc?macDinh:l);           // bấm lại chip đang bật = quay về mặc định
      });
    });
    document.querySelectorAll('.stack .seg[data-loc]').forEach(function(s){
      s.addEventListener('click',function(){
        var l=s.getAttribute('data-loc'); ap(l===dangLoc?macDinh:l);
      });
    });
    ap(macDinh);
  }

  // ── NỐI HAI KHỐI BẰNG MẮT: rê chuột lên một dòng claim thì đoạn thanh của trạng
  //    thái đó sáng lên; rê lên một đoạn thanh thì những dòng KHÁC trạng thái mờ đi.
  //    Hai khối vốn nói về cùng một tập số — người đọc không phải tự bắc cầu.
  function soi(st){
    document.querySelectorAll('.stack').forEach(function(s){
      if(st) s.setAttribute('data-noi',st); else s.removeAttribute('data-noi');
    });
  }
  function mo_dong(st){
    document.querySelectorAll('[data-st]').forEach(function(d){
      d.classList.toggle('roi', !!st && d.getAttribute('data-st') !== st);
    });
  }
  document.querySelectorAll('[data-st]').forEach(function(d){
    d.addEventListener('mouseenter',function(){soi(d.getAttribute('data-st'))});
    d.addEventListener('mouseleave',function(){soi('')});
  });
  document.querySelectorAll('.stack .seg[data-loc]').forEach(function(s){
    s.addEventListener('mouseenter',function(){mo_dong(s.getAttribute('data-loc'))});
    s.addEventListener('mouseleave',function(){mo_dong('')});
  });

  // ── vạch tiến trình đọc. Nó KHÔNG phải một con số — chỉ là chỗ đang đứng trong
  //    trang, thứ trình duyệt vốn đã biết.
  var tien=document.createElement('div'); tien.id='bp-tien'; document.body.appendChild(tien);
  var capTien=function(){
    var h=document.documentElement.scrollHeight-innerHeight;
    tien.style.transform='scaleX('+(h>0?Math.min(scrollY/h,1):0)+')';
  };
  addEventListener('scroll',capTien,{passive:true});
  addEventListener('resize',capTien); capTien();

  // ── chú giải bay trên từng đoạn thanh (thay tooltip mặc định: nó chờ một giây
  //    rồi mới hiện, và ở nền tối nó trắng bệch)
  var tip=null;
  document.querySelectorAll('[data-tip]').forEach(function(e){
    e.addEventListener('mouseenter',function(){
      if(!tip){tip=document.createElement('div');tip.id='bp-tip';document.body.appendChild(tip)}
      tip.textContent=e.getAttribute('data-tip');
      var r=e.getBoundingClientRect();
      tip.style.transform='translate(-50%,-118%)';
      tip.style.left=Math.min(Math.max(r.left+r.width/2,70),innerWidth-70)+'px';
      tip.style.top=r.top+'px';
      tip.classList.add('hien');
    });
    e.addEventListener('mouseleave',function(){if(tip)tip.classList.remove('hien')});
  });

  // ── dải bài: mũi tên cuộn đúng MỘT thẻ (đo bằng khoảng cách thật giữa hai thẻ,
  //    không gõ cứng bề rộng — gõ cứng là một con số thứ hai sẽ trôi lệch với CSS)
  var rail=document.getElementById('rail');
  if(rail){
    var nutR=document.querySelectorAll('button[data-rail]'),
        the=rail.querySelectorAll('.bai');
    var buoc=function(){
      if(the.length>1)return the[1].offsetLeft-the[0].offsetLeft;
      return the.length?the[0].getBoundingClientRect().width:280;
    };
    var capNhat=function(){
      var het=rail.scrollWidth-rail.clientWidth-2;
      nutR.forEach(function(b){
        b.disabled = +b.getAttribute('data-rail')<0 ? rail.scrollLeft<=2 : rail.scrollLeft>=het;
      });
      rail.parentNode.classList.toggle('het', rail.scrollLeft>=het);
    };
    nutR.forEach(function(b){
      b.addEventListener('click',function(){
        rail.scrollBy({left:buoc()*(+b.getAttribute('data-rail')),
                       behavior:chuyen?'smooth':'auto'});
      });
    });
    rail.addEventListener('scroll',capNhat,{passive:true});
    addEventListener('resize',capNhat);
    capNhat();
  }
})();
"""


def dieu_huong(goc: str, dang: str) -> str:
    """Thanh điều hướng. `dang` là mục đang mở — nó KHÔNG được là một link tự trỏ."""
    g = goc or "."
    ra = []
    for duong, nhan in MUC_DIEU_HUONG:
        if duong and not CO_TRANG.get(duong):
            continue
        lop = ' class="tai"' if duong == dang else ""
        ra.append(f'<a href="{g}/{duong}"{lop}>{nhan}</a>')
    if BO_CUC == "d2":
        return ('<nav class="dieu">' + "".join(ra)
                + '<button class="nut-nen" id="nut-nen" type="button" '
                  'title="Đổi nền sáng/tối" aria-label="Đổi nền sáng/tối">☀ / ☾</button></nav>')
    # v3: nút đổi nền RA NGOÀI <nav>, và thêm nút mở menu ở khổ hẹp. Hai thứ này là
    # cấu trúc chứ không phải trang trí — `v3.css` neo `.nut-menu` và `.nut-nen` vào
    # lưới của `.dau`, còn `v3.js` tìm `.nut-menu` bằng `aria-controls` trỏ `#site-nav`.
    # Để nút nền nằm trong nav như D2 thì ở khổ hẹp nó bị gập theo menu và mất luôn.
    return ('<button class="nut-menu" type="button" aria-controls="site-nav" '
            'aria-expanded="false">Menu <span>↘</span></button>'
            '<nav class="dieu" id="site-nav" aria-label="Điều hướng chính">'
            + "".join(ra) + '</nav>'
            '<button id="nut-nen" class="nut-nen" type="button" '
            'aria-label="Đổi nền sáng tối" aria-pressed="false">◐</button>')


def kich_thuoc_png(p: pathlib.Path) -> tuple:
    """Đọc bề rộng/cao từ IHDR của PNG. Không đoán theo tên file, và nổ nếu không phải PNG.

    Vì sao đọc thật: thẻ og:image:width/height mà ghi cứng thì lúc đổi ảnh sẽ thành
    hai con số nói dối trong im lặng — mạng xã hội dựng khung theo số khai, không theo
    ảnh, nên ảnh sẽ bị méo mà không lệnh nào hỏng.
    """
    b = p.read_bytes()[:24]
    if b[:8] != b"\x89PNG\r\n\x1a\n" or b[12:16] != b"IHDR":
        raise LoiCong(f"{p.name} không phải PNG hợp lệ — ảnh xem trước phải đọc được kích thước")
    return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")


# Những cụm dưới đây mang một nghĩa khi đứng cùng nhau. Trình duyệt vốn xem khoảng
# trắng giữa hai tiếng Việt là một điểm ngắt hợp lệ, nên `text-wrap:balance` một mình
# vẫn có thể bẻ "kiểm / chứng" hoặc "bác / bỏ". Danh sách có MỘT chủ ở builder;
# sửa từng heading/card chỉ tạo ra nhiều bản sẽ trôi lệch khi thêm bài mới.
CUM_KHONG_NGAT = (
    "qua từng lần kiểm chứng", "điều bác bỏ", "kiểm chứng", "khẳng định",
    "bác bỏ", "đứng vững", "phân định", "điều tra", "bằng chứng", "hồ sơ",
    "tự kiểm", "ghi trước", "đường về", "trang chủ", "bài viết", "dữ liệu",
)
_RE_CUM_KHONG_NGAT = tuple(
    re.compile(r"(?<!\w)" + re.escape(cum).replace(r"\ ", r"[ \t\r\n]+") + r"(?!\w)", re.I)
    for cum in sorted(CUM_KHONG_NGAT, key=len, reverse=True)
)
_SO = r"(?:\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(?:[KMBT])?"
_RE_SO_KHONG_NGAT = re.compile(
    rf"(?<![\w#])(?:"
    rf"(?:block|blk)\s*#?{_SO}(?:\s*→\s*#?{_SO})?"
    rf"|#\s*{_SO}(?:\s*→\s*#\s*{_SO})?"
    rf"|\d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}Z"
    rf"|\d{{2}}/\d{{2}}/\d{{4}}"
    rf"|\d{{2}}:\d{{2}}(?::\d{{2}})?Z?"
    rf"|0x[0-9a-f]{{4,}}(?:…|\.\.\.)[0-9a-f]{{3,}}"
    rf"|{_SO}\s*(?:giờ|GIỜ)\s+{_SO}\s*(?:phút|PHÚT)"
    rf"|(?:[$€]\s*)?[+\-−±]?{_SO}"
    rf"(?:\s*[–—−-]\s*(?:[$€]\s*)?{_SO})?"
    rf"(?:\s*/\s*(?:[$€]\s*)?{_SO})?"
    rf"(?:\s*×\s*10[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\s*[×x])?"
    rf"(?:\s*(?:%|WETH|ETH|UNI|PENDLE|CAKE|USDC|USD|swap(?:s)?|poolId|pool|"
    rf"bài(?:\s+viết)?|khẳng định|claim|fact|ngày|NGÀY|giờ|GIỜ|phút|PHÚT|lần))?"
    rf")(?!\w)", re.I)
_RE_THANH_PHAN_HTML = re.compile(
    r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|"
    r"<pre\b[^>]*>.*?</pre>|<textarea\b[^>]*>.*?</textarea>|"
    r"<svg\b[^>]*>.*?</svg>|<[^>]+>)", re.I | re.S)


def _map_text_body(html: str, fn, bo_qua_khoa: bool = False) -> str:
    """Áp `fn` chỉ lên text node trong body, không đụng script/style/pre/attribute."""
    m = re.search(r"(<body\b[^>]*>)(.*?)(</body>)", html, re.I | re.S)
    if not m:
        raise LoiCong("HTML không có <body> hoàn chỉnh — không thể khóa xuống dòng")
    phan, khoa = [], 0
    for x in _RE_THANH_PHAN_HTML.split(m.group(2)):
        if not x:
            continue
        if x.startswith("<"):
            nho = x.lower()
            if bo_qua_khoa and re.match(r'<span\b[^>]*class="[^"]*\bkhong-ngat\b', nho):
                khoa += 1
            elif bo_qua_khoa and khoa and re.match(r"</span\s*>", nho):
                khoa -= 1
            phan.append(x)
        else:
            phan.append(x if khoa else fn(x))
    return html[:m.start()] + m.group(1) + "".join(phan) + m.group(3) + html[m.end():]


def khoa_xuong_dong(html: str) -> str:
    """Giữ cụm tiếng Việt và số–đơn vị trên một dòng ở mọi mặt production v3.

    🔴 KHÓA BẰNG KÝ TỰ, KHÔNG BẰNG ELEMENT. Bản đầu (11/08) bọc mỗi cụm số trong
    `<span class="khong-ngat">`. Một element chèn thêm vào khuôn người khác viết
    thì KHÔNG BAO GIỜ trung tính, và nó hỏng theo hai đường khác nhau trong cùng
    một ngày:
      ① mọi selector `... span` của v3.css bắt luôn nó vì nó nằm lọt trong
         <strong>/<b>/<small> — đo được 579 cụm bị đổi kiểu, số tổng /facts/
         tụt 64px→8px, số khẳng định trang chủ 77px→11px và bị VIẾT HOA;
      ② cha nào `display:flex|grid` thì nó thành FLEX/GRID ITEM — khối
         `.provenance` của bài vỡ làm nhiều ô, số rời khỏi câu chứa nó
         (đo: 10 span ở bài CAKE, 6 ở bài HYPE).
    `&nbsp;` không tạo hộp nên không có cửa nào cho hai lỗi trên. Giá phải trả,
    khai ra: nó chỉ chặn ngắt ở KHOẢNG TRẮNG, không chặn ngắt sau gạch/mũi tên
    trong một dải như `block 25.643.032 → 25.729.516` — chấp nhận được, vì thứ
    cần giữ liền là số với ĐƠN VỊ của nó, không phải hai đầu của một dải.
    """
    def sua(txt: str) -> str:
        for mau in _RE_CUM_KHONG_NGAT:
            txt = mau.sub(lambda m: re.sub(r"[ \t\r\n]+", "&nbsp;", m.group(0)), txt)
        return _RE_SO_KHONG_NGAT.sub(
            lambda m: re.sub(r"[ \t\r\n]+", "&nbsp;", m.group(0)), txt)
    return _map_text_body(html, sua)


def cong_xuong_dong(html: str) -> None:
    """Cổng bố cục chữ: helper bị bỏ qua thì build phải nổ, không chờ ảnh chụp."""
    for _, ruot in re.findall(r"<h([12])\b[^>]*>(.*?)</h\1>", html, re.I | re.S):
        if re.search(r"<br\b", ruot, re.I):
            raise LoiCong("heading h1/h2 còn <br> cứng — chỉ được ngắt theo cụm")
    loi = []
    def soi(txt: str) -> str:
        for cum, mau in zip(sorted(CUM_KHONG_NGAT, key=len, reverse=True), _RE_CUM_KHONG_NGAT):
            if mau.search(txt):
                loi.append(f"cụm '{cum}' còn khoảng trắng có thể bị bẻ")
                break
        # 🔴 Chỉ bắt cụm CÒN KHOẢNG TRẮNG THẬT. Số trần (`25.643.032`) không có chỗ
        # ngắt nên không cần khóa; bắt cả nó là bắt oan mọi con số trên site. Từ khi
        # khóa bằng `&nbsp;` thay vì bằng span, đây cũng là phép phân biệt DUY NHẤT
        # còn lại giữa "đã khóa" và "chưa khóa" — không còn element để mà đánh dấu.
        for m in _RE_SO_KHONG_NGAT.finditer(txt):
            if re.search(r"[ \t\r\n]", m.group(0)):
                loi.append(f"số/đơn vị chưa khóa: {m.group(0)!r}")
                break
        return txt
    _map_text_body(html, soi)
    if loi:
        raise LoiCong("; ".join(loi[:3]))


def trang(tieu_de: str, than: str, t: dict, goc: str = "", meta: dict = None,
          muc: str = "", mat: str = "", lang: str = "vi") -> str:
    # Thẻ xem trước: khi link được dán vào Telegram · Discord · forum · tin nhắn riêng,
    # KHÔNG có bộ thẻ này thì nó hiện ra một dòng chữ trơn và không ai bấm. Ảnh dùng lại
    # đúng card đã dựng cho bài trên kênh (2400×1350) — không dựng ảnh riêng cho web.
    m = meta or {}
    anh = m.get("anh") or "avatar-800.png"
    p_anh = ROOT / "assets" / anh
    if not p_anh.exists():
        raise LoiCong(f"front matter 'anh: {anh}' trỏ tới assets/{anh} không tồn tại — "
                      f"thẻ og:image sẽ trỏ vào hư không và link dán ra ngoài mất ảnh")
    w, h = kich_thuoc_png(p_anh)
    url = BASE + m.get("duong", "/")
    # `canonical` vẫn trỏ URL THẬT trong bản thử — đó là điều đúng: nó nói với máy tìm
    # kiếm rằng bản phục vụ mới là bản chính. `noindex` đi kèm để không ai phải tin
    # vào mỗi một tín hiệu.
    # 🔴 Tiền tố `\\n` NẰM TRONG nhánh bật, không phải dòng riêng trong template. Bản đầu
    # viết nó thành một dòng `{...if BAN_THU else ''}`, và nhánh TẮT để lại một dòng
    # trống ⇒ bản D2 lệch một byte mỗi trang, 18/18 trang. Bất biến số một bắt ngay.
    noidx = '\n<meta name="robots" content="noindex">' if BAN_THU else ''
    xt = f"""<meta name="description" content="{ihtml.escape(m.get('mo_ta', ''), quote=True)}">{noidx}
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="BlockPinned">
<meta property="og:locale" content="vi_VN">
<meta property="og:type" content="{m.get('loai', 'website')}">
<meta property="og:title" content="{ihtml.escape(m.get('tieu_de_og', tieu_de), quote=True)}">
<meta property="og:description" content="{ihtml.escape(m.get('mo_ta', ''), quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/anh/{anh}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">"""
    g = goc or "."
    # Cùng luật với `noidx` ngay trên: nhánh TẮT phải ra chuỗi rỗng TUYỆT ĐỐI.
    dai = "\n" + DAI_BAN_THU if BAN_THU else ""
    nap = "".join(f'<link rel="preload" as="font" type="font/woff2" crossorigin '
                  f'href="{g}/font/{f}">' for f in FONT_NAP_TRUOC)
    dau_chung = f"""<!doctype html><html lang="{ihtml.escape(lang, quote=True)}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ihtml.escape(tieu_de)}</title>
{xt}
{nap}
<link rel="icon" type="image/png" sizes="32x32" href="{g}/anh/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{g}/anh/favicon-16.png">
<style>{font_face(goc)}{css(t)}</style>"""
    if BO_CUC == "d2":
        return dau_chung + f"""
<script>{JS_NEN}</script></head><body>{dai}
<header class="dau"><div class="khung">
  <span class="mark">{MARK_SVG}</span>
  <a class="ten" href="{goc or '.'}/">Block<span>Pinned</span></a>
  <span class="tag">số nào cũng truy ngược được</span>
  {dieu_huong(goc, muc)}
</div></header>
<main class="khung">{than}</main>
<footer><div class="khung">
  Bản chuẩn của mọi bài. Sửa tại chỗ, không xoá.<br>
  Không phải lời khuyên đầu tư. ·
  <a href="https://x.com/blockpinned">@blockpinned</a>
</div></footer>
<script>{JS_DO_LAI}</script>
<script>{JS_HIEU_UNG}</script>
</body></html>"""

    # ── VỎ v3 ────────────────────────────────────────────────────────────────────
    # Bốn khác biệt so với D2, mỗi cái có việc chứ không phải khác cho khác:
    #  ① `<body class="…">` — `v3.css` đổi bố cục THEO MẶT (hero, lưới, sticky index).
    #     Thiếu lớp này thì mọi mặt dùng chung một khuôn và sáu thiết kế thành một.
    #  ② `#bp-tien` — thanh tiến độ cuộn, `v3.js` tìm bằng đúng id này.
    #  ③ `#ch-tip` — hộp giải thích của chart, PHẢI đứng ngoài `<main>` để tooltip
    #     không bị `overflow` của khung cắt cụt.
    #  ④ Bỏ `.tag` ("số nào cũng truy ngược được"): v3 đưa câu đó vào hero từng mặt,
    #     để nguyên ở header là nói hai lần — đúng lỗi user đã bác ở lượt 06/08
    #     ("trang chủ bỏ ba con số nói hai lần").
    #
    # 🔵 `JS_DO_LAI` GIỮ NGUYÊN cho v3: nó là TÍNH NĂNG (gọi RPC đo lại tại chỗ) và
    # cổng ⑧ canh nó, còn `v3.js` đo được là không đụng gì tới nút đó. `JS_HIEU_UNG`
    # thì BỎ — `v3.js` tự cầm tầng hiệu ứng, và `v3.css` không có luật nào cho
    # `[data-hien]`/`.stack` nên bỏ đi không làm mất chữ nào (đã kiểm, 0 luật khớp).
    html = dau_chung + f"""
<script>{JS_NEN_V3}</script></head><body class="{mat}">{dai}
<div id="bp-tien" aria-hidden="true"></div>
<header class="dau"><div class="khung">
  <span class="mark">{MARK_SVG}</span>
  <a class="ten" href="{goc or '.'}/">Block<span>Pinned</span></a>
  {dieu_huong(goc, muc)}
</div></header>
<main class="khung">{than}</main>
<div id="ch-tip"></div>
<footer><div class="khung"><p>Bản chuẩn của mọi bài. Sửa tại chỗ, không xoá. \
Không phải lời khuyên đầu tư. · <a href="https://x.com/blockpinned">@blockpinned</a></p></div></footer>
<script>{JS_DO_LAI}</script>
<script>{than_js()}</script>
</body></html>"""
    html = khoa_xuong_dong(html)
    cong_xuong_dong(html)
    return html


def so_vn(v: float, n: int = 3) -> str:
    """Dấu thập phân tiếng Việt là dấu PHẨY. Tách hẳn ra khỏi chuỗi đánh dấu."""
    return f"{v:.{n}f}".replace(".", ",")


def ve_thang(td: dict) -> str:
    """Claim vẽ thành HÌNH — thanh ngang chồng nhau, HTML+CSS thuần, không SVG.

    🔴 Bản đầu vẽ SVG trục số ở khổ 640px rồi để nó co về ~330px trong cột điện
    thoại: chữ co theo còn một nửa, nhãn đè nhau và tràn ra ngoài khung. Chữ trong
    SVG co theo viewBox — muốn chữ đọc được ở mọi khổ thì chữ phải là HTML.
    Và một trục số có hai điểm cách nhau 4× vốn đã không vừa một cột hẹp; hai
    THANH chồng nhau nói đúng cái claim đang nói: bên kia dài gấp mấy lần bên này.

    Hình này SỐNG — đó là chỗ web làm được mà X/TG không: ngày DefiLlama tính lại,
    thanh của họ ngắn lại và tụt vào đúng khoảng đã ghi trước. Ảnh trên X thì đóng
    băng ở lúc đăng.
    """
    hi = td["den"]
    pct = lambda v: max(1.2, v / hi * 100)
    k = td["khoang"]
    g = ['<div class="thang">']
    for d in td["diem"]:
        g.append(
            f'<div class="hang">'
            f'<div class="nh"><span>{ihtml.escape(d["nhan"])}</span>'
            f'<b>${so_vn(d["so"])}M</b></div>'
            f'<div class="ray"><i class="cot {d["ben"]}" style="width:{pct(d["so"]):.1f}%"></i></div>'
            f'</div>')
    g.append(
        f'<div class="hang kh">'
        f'<div class="ray tr"><i class="vung" style="left:{pct(k["tu"]):.1f}%;'
        f'width:{pct(k["den"]) - pct(k["tu"]):.1f}%"></i></div>'
        f'<div class="nh nk2"><span>↑ {ihtml.escape(k["nhan"])}</span>'
        f'<b>${so_vn(k["tu"])}–{so_vn(k["den"])}M</b></div></div>')
    return "\n".join(g) + "</div>"


def ma_hoa_goi(d: dict) -> str:
    """Chữ ký hàm + tham số static → calldata. Selector sinh bằng keccak, KHÔNG gõ tay:
    cái người đọc thấy in trên trang và cái thật sự được gọi phải là một thứ."""
    data = keccak.selector(d["ky"])
    for t in d.get("tham_so", []):
        if isinstance(t, bool) or not isinstance(t, (int, str)):
            raise LoiCong(f"tham số lạ trong do_lai: {t!r} — chỉ nhận số nguyên hoặc 0x…")
        data += f"{t:064x}" if isinstance(t, int) else t[2:].lower().rjust(64, "0")
    return data


def khoi_do_lai(c: dict) -> str:
    """Nút để NGƯỜI ĐỌC tự đo lại claim ngay lúc đọc.

    Vì sao nó là thứ site làm được mà X/TG không: bài trên feed chỉ KỂ rằng số đã được
    đo; ở đây người đọc bấm một lần và tự thấy số bây giờ, kèm block vừa đọc, đặt cạnh
    số đã ghim. Họ rời trang với trạng thái khác lúc vào.

    🔴 Trình tự BẮT BUỘC là ghim TRƯỚC rồi đọc: `eth_blockNumber` → `eth_call` TẠI đúng
    block đó. Gọi `latest` rồi in kèm block đọc sau là hai thời điểm khác nhau dán vào
    một dòng — đúng loại lỗi kênh này đi bác.
    """
    if c.get("khong_do_lai"):
        return ('<p class="dong khongdo"><span class="nhan">KHÔNG ĐO LẠI ĐƯỢC TỪ TRÌNH DUYỆT</span>'
                + ihtml.escape(c["khong_do_lai"]) + "</p>")
    d = c.get("do_lai")
    if not d:
        return ""
    ct = d["cong_thuc"]
    return (
        '<div class="dolai-o">'
        f'<button class="dolai" type="button" data-to="{d["to"]}" data-data="{ma_hoa_goi(d)}"'
        f' data-tu="{ct["tu"]}" data-chia="{ct.get("chia", "")}" data-nhan="{ct.get("nhan", 1)}"'
        f' data-thap-phan="{ct.get("thap_phan", 0)}" data-chu-so="{d["chu_so"]}"'
        f' data-don-vi="{ihtml.escape(d["don_vi"], quote=True)}" data-ghim="{d["so_ghim"]}">'
        'Đo lại ngay ↻</button>'
        '<div class="ketqua" role="status" aria-live="polite">'
        f'gọi <code>{ihtml.escape(d["ky"])}</code> trên <code>{d["to"][:10]}…{d["to"][-4:]}</code>'
        '</div></div>')


JS_DO_LAI = """
// Hai endpoint keyless, đo được 30/07 là cho phép trình duyệt gọi (CORS *). Gọi endpoint
// thứ hai CHỈ khi cái đầu lỗi — 🔴 giới hạn nhịp là thật: một endpoint đã trả 429 ngay
// lượt thứ ba khi thử. Vì vậy trang KHÔNG tự đo lúc mở; chỉ đo khi có người bấm.
const RPC = ["https://ethereum-rpc.publicnode.com", "https://eth.drpc.org"];
async function rpcGoi(ep, method, params) {
  const r = await fetch(ep, {method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({jsonrpc: "2.0", id: 1, method, params})});
  if (!r.ok) throw new Error("HTTP " + r.status);
  const j = await r.json();
  if (j.error) throw new Error(j.error.message || "lỗi RPC");
  return j.result;
}
function chuoiSo(x, n) {
  return x.toLocaleString("vi-VN", {minimumFractionDigits: n, maximumFractionDigits: n});
}
async function doLai(b) {
  const o = b.dataset, ra = b.parentElement.querySelector(".ketqua");
  b.disabled = true; ra.className = "ketqua dang"; ra.textContent = "đang đo…";
  const loi = [];
  for (const ep of RPC) {
    try {
      const blk = await rpcGoi(ep, "eth_blockNumber", []);              // ghim TRƯỚC
      const kq = await rpcGoi(ep, "eth_call", [{to: o.to, data: o.data}, blk]);  // đọc TẠI block đó
      const h = kq.slice(2), w = [];
      for (let i = 0; i < h.length; i += 64) w.push(BigInt("0x" + h.slice(i, i + 64)));
      const tu = Number(o.tu), sc = Number(o.chuSo), ghim = Number(o.ghim);
      const v = o.chia === "" ? Number(w[tu]) / Math.pow(10, Number(o.thapPhan))
                              : Number(w[tu]) / Number(w[Number(o.chia)]) * Number(o.nhan);
      const doi = Math.abs(v - ghim) >= Math.pow(10, -sc) / 2;
      ra.className = "ketqua " + (doi ? "lech" : "khop");
      ra.innerHTML = "<b>" + chuoiSo(v, sc) + " " + o.donVi + "</b> tại block "
        + BigInt(blk).toLocaleString("vi-VN") + " · đã ghim " + chuoiSo(ghim, sc) + " "
        + o.donVi + " ⇒ <b>" + (doi ? "ĐÃ ĐỔI" : "KHÔNG ĐỔI") + "</b>"
        + '<span class="nguon">đọc từ ' + ep.replace("https://", "") + "</span>";
      b.disabled = false; return;
    } catch (e) { loi.push(ep.replace("https://", "") + ": " + e.message); }
  }
  // 🔴 Không in số nào khi đo hỏng. Một số 0 ở đây là bằng chứng về CÔNG CỤ, không phải
  // về chain — in nó ra là làm đúng cái lỗi mà mấy bài trên trang này đi bác.
  ra.className = "ketqua loi";
  ra.innerHTML = "<b>không đo được</b> — cả hai endpoint đều lỗi, nên trang không in số nào."
    + '<span class="nguon">' + loi.join(" · ") + "</span>";
  b.disabled = false;
}
// Đếm ngược tính ở TRÌNH DUYỆT, không lúc build: trang tĩnh không tự dựng lại mỗi ngày,
// nên một con số "còn N ngày" nướng vào HTML sẽ nói dối từ hôm sau.
document.querySelectorAll(".han .ngay[data-han]").forEach(function (e) {
  const con = Math.ceil((new Date(e.dataset.han + "T23:59:59Z") - new Date()) / 86400000);
  const p = document.createElement("span");
  p.className = "con" + (con < 0 ? " qua" : "");
  p.textContent = con < 0 ? "ĐÃ TỚI HẠN" : (con === 0 ? "hôm nay" : "còn " + con + " ngày");
  e.appendChild(p);
});
document.querySelectorAll("button.dolai").forEach(function (b) {
  b.addEventListener("click", function () { doLai(b); });
});
"""


def nguon_html(n) -> str:
    """Trường `nguon` của một dòng nhật ký → HTML.

    🔴 Xác 31/07/2026, người phản biện NGOÀI bắt trên bản đã publish: bản cũ nhét
    thẳng `nguon` vào `href`. Với bài #1–#6 nó vô hại vì `nguon` luôn là URL thật.
    Bài #7 là bài đầu tiên trỏ vào ĐƯỜNG DẪN FILE trong repo ⇒ sinh ra
    `<a href="PENDLE/data/….json">` — URL tương đối, live trả **404**, cả 5 dòng.
    Nhánh xử lý này chưa từng bị chạm suốt 6 bài, nên 6 lần build sạch KHÔNG chứng
    minh gì cả (`RULES.md §2`: control chỉ là control khi nó CÓ THỂ fail).

    Sửa: chỉ thứ nào là URL tuyệt đối mới thành liên kết; còn lại in ra dạng CHỮ, để
    người đọc thấy đó là con trỏ hồ sơ chứ không phải một cái link hứa suông. Không
    cấm trỏ vào file nội bộ — cấm PHÁT RA một href không tới đâu.
    """
    if not n:
        return ""
    s = str(n).strip()
    if re.fullmatch(r"https?://\S+", s):
        return f' <a href="{ihtml.escape(s, quote=True)}">nguồn</a>'
    # đường dẫn NỘI BỘ của chính site: dựng liên kết, và `cong_lien_ket` sẽ kiểm nó
    # tới nơi — khác hẳn bản cũ, vốn dựng liên kết cho MỌI chuỗi rồi không kiểm gì.
    if re.fullmatch(r"/[\w./-]+", s):
        return f' <a href="{ihtml.escape(s, quote=True)}">nguồn</a>'
    return f' <span class="nguon-tro">nguồn: {ihtml.escape(s)}</span>'


def cong_lien_ket(txt: str, o: str, goc: pathlib.Path, tep: pathlib.Path) -> None:
    """Cổng 11 — mọi `href` NỘI BỘ sinh ra phải trỏ tới thứ có thật trong `out/`.

    Cổng 6 đã gọi đúng tên lớp lỗi này — *"trình duyệt bỏ qua thuộc tính sai trong im
    lặng, đúng loại lỗi tệ nhất"* — nhưng phạm vi nó đặt ở thuộc tính SỐ. `href` là
    cùng lớp, lệch đúng một loại trường, và lỗ đó tốn 5 liên kết 404 trên bài #7.
    Cổng này đóng phần còn lại: liên kết ngoài thì không đụng (không gọi mạng lúc
    build), liên kết trong thì phải giải được ra một file hoặc một thư mục có index.
    """
    # 🔴 BÓC RUỘT <script> TRƯỚC KHI QUÉT. Cổng này canh LIÊN KẾT TRONG TÀI LIỆU; một
    # chuỗi `href="` nằm trong mã JS là CHỮ, không phải link — không trình duyệt nào đi
    # tới đâu vì nó. Xác: `v3.js:96` dựng link Quick Find bằng
    # `'href="' + route.href + '"'`, và cổng đọc ra một đường dẫn tên là ' + route.href + '.
    #
    # 🔵 VÌ SAO ĐÂY KHÔNG PHẢI NỚI CỔNG — đo, không lý luận: bốn khối JS của D2
    # (`JS_NEN` · `JS_NEN_V3` · `JS_DO_LAI` · `JS_HIEU_UNG`) có ĐÚNG 0 lượt `href="`.
    # Phần phạm vi mất đi bằng đúng phần trước nay chưa từng kiểm được cái gì. Nhánh
    # D2 không mất một phép kiểm nào, và điều đó kiểm lại được bằng bất biến byte.
    #
    # THẺ MỞ GIỮ LẠI (`\\1`), chỉ ruột bị bỏ — `<script src="…">` vẫn nằm trong chuỗi
    # quét. Bóc cả thẻ là tự mở một lỗ đúng bằng thứ cổng này sinh ra để bịt.
    than = re.sub(r'(<script\b[^>]*>).*?</script>', r'\1', txt, flags=re.S | re.I)
    for m in re.finditer(r'href="([^"]+)"', than):
        h = ihtml.unescape(m.group(1)).strip()
        if not h or h.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        # 🔴 BỎ `?query` TRƯỚC, RỒI MỚI TỚI `#fragment` — đúng thứ tự URL. Từ 11/08 thẻ
        # token trỏ về `../bai/?token=uni` (lọc kho bài theo token), và query string là
        # phần KHÔNG có trên đĩa: giữ nó lại thì cổng đi tìm một file tên là
        # "index.html?token=uni" và chặn một link hoàn toàn đúng. Cắt `#` trước rồi mới
        # cắt `?` sẽ hụt ca `a.html?x=1#y` — nên thứ tự ở đây là bắt buộc, không tuỳ ý.
        h_dia = h.split("#")[0].split("?")[0]
        if not h_dia:                      # href chỉ có query/fragment ⇒ chính trang này
            continue
        dich = (goc / h_dia.lstrip("/")) if h_dia.startswith("/") else (tep.parent / h_dia)
        if dich.is_file() or (dich / "index.html").is_file():
            continue
        raise LoiCong(f'href nội bộ không tới đâu: "{h}" — {o}')


TRANG_THAI_NGAN = {
    "ĐÃ XÁC NHẬN": "xác nhận",
    "ĐANG ĐỨNG": "vẫn đứng vững",
    "ĐÃ SỬA": "đã sửa",
    "BỊ BÁC": "đã bị bác bỏ",
    "CHỜ SỐ": "chờ số",
}


def _metric_tieu_de(tieu_de: str) -> str:
    """Lấy một đại lượng ĐÃ CÓ trong tiêu đề làm ghost number của hero.

    Đây chỉ là lựa chọn trình bày: không tính số mới và không diễn giải lại claim.
    Không có đại lượng thì dùng mã token, thay vì bịa một con số trang trí.
    """
    # Không bắt số nằm trong tên phiên/viết tắt (`v4`, `Q2`): đó là mã, không phải
    # nhân vật số của tiêu đề. Ca thật đầu tiên cho ghost `4` thay vì `3,9×` và EN
    # cho `2` thay vì `−412.960`.
    m = re.search(
        r"(?<![A-Za-z])[−+-]?\d+(?:[.,]\d+)*(?:\s*(?:%|×|lần|USD|ETH|HYPE|UNI|PENDLE|CAKE|validator))?(?![A-Za-z])",
        tieu_de, re.I)
    return m.group(0) if m else ""


def _tieu_de_nhan(tieu_de: str) -> str:
    """Nhấn đúng đại lượng ghost trong tiêu đề; escape từng mảnh trước khi ghép."""
    metric = _metric_tieu_de(tieu_de)
    if not metric:
        return ihtml.escape(tieu_de)
    truoc, sau = tieu_de.split(metric, 1)
    if truoc.endswith("$"):
        truoc, metric = truoc[:-1], "$" + metric
    return (ihtml.escape(truoc) + '<span class="nhan-manh">'
            + ihtml.escape(metric) + "</span>" + ihtml.escape(sau))


H1_TOI_DA = 80
# Vì sao 80 chứ không phải một con số tròn cho đẹp: ở khổ 500px, H1 chạy ~18 ký tự một
# dòng, nên 80 là mốc H1 còn ~4–5 dòng và câu lede vẫn lọt màn hình đầu. Đo 12/08 trên
# bài HYPE (title 152 ký tự): H1 **8 dòng** ở 500px, **6 dòng** ở 1280px — người đọc hết
# màn đầu mà chưa gặp câu văn nào. Trung vị `title` của 12 bài là 78, tức ngưỡng này
# nằm đúng chỗ desk vốn viết, không phải một luật áp từ ngoài vào.


def _tieu_de_h1(fm: dict) -> str:
    """Chuỗi đi vào <h1> và vào MỌI thẻ bài — một nguồn duy nhất.

    🔴 Đừng để hai mặt tự lấy `fm['title']`. Trước lượt này có ba chỗ làm thế (hero,
    thẻ trang chủ/token, thẻ kho bài); thêm một trường mà quên một chỗ thì hai mặt của
    cùng một bài mang hai tiêu đề khác nhau, và không cổng nào bắt được vì cả hai đều
    là chuỗi hợp lệ.

    `title` KHÔNG bị thay: nó vẫn là `<title>` của tab và vẫn là dòng hiện ra khi link
    được dán ra ngoài. Chỗ này chỉ chọn cái gì hiện trên MẶT CHỮ TO.
    """
    return (fm.get("tieu_de_ngan") or "").strip() or fm["title"]


def _khoi_gioi_han(fm: dict) -> str:
    """Giới hạn của phép đọc — khối riêng dưới lede, hiện đầy đủ.

    🔴 Trước 12/08 trường `doc_lai` không có nhà trên bố cục v3. Nó bị `.split('—', 1)[0]`
    nhét vào eyebrow như một mẩu ngắn — hợp đồng định dạng `<mẩu> — <phần còn lại>` mà
    KHÔNG cổng nào cưỡng chế. Đo 12 bài: 1 bài có dấu gạch (29 ký tự, đúng ý đồ), **3 bài
    không có** nên toàn văn 297/272/204 ký tự đổ lên đầu trang bằng chữ hoa mono, 8 bài
    rỗng. `dai_trang_thai()` — chỗ `doc_lai` vốn có nhà tử tế — chỉ chạy ở nhánh D2.

    Giữ TUỲ CHỌN: 8 bài đang trống thì không dựng gì. Bắt buộc nó là bắt viết thêm 8 đoạn
    văn cho một việc thuộc về trình bày.
    """
    d = (fm.get("doc_lai") or "").strip()
    if not d:
        return ""
    return ('  <div class="article-meta article-limits">'
            f'<span><b>GIỚI HẠN</b>{ihtml.escape(d)}</span></div>\n')


def _dem_trang_thai(claims: list) -> dict:
    return {k: sum(1 for c in claims if c["status"] == k) for k in TRANG_THAI}


def _so_claim_v3(claims: list) -> str:
    """Sổ claim theo đúng cấu trúc evidence của mockup WOW.

    Không đọc lại văn xuôi để suy claim: câu, trạng thái, ghim, falsifier và log đều
    đi thẳng từ `claims.json`. Tỷ trọng trong thanh là `flex: số claim`, nên đổi một
    trạng thái thì cả chữ lẫn hình đi theo trong cùng lượt build.
    """
    dem = _dem_trang_thai(claims)
    co = [(k, dem[k]) for k in TRANG_THAI if dem[k]]
    thanh = "".join(
        f'<i class="{TRANG_THAI[k][0]}" style="--n:{n}"></i>' for k, n in co)
    chu_giai = "".join(
        f'<i><span class="dot {TRANG_THAI[k][0]}"></span><b>{n}</b> '
        f'{TRANG_THAI_NGAN[k]}</i>' for k, n in co)
    aria = ", ".join(f"{n} {TRANG_THAI_NGAN[k]}" for k, n in co)

    ds = []
    for c in claims:
        cls, _ = TRANG_THAI[c["status"]]
        nk = "".join(
            f'<li><span class="case-log-date">{ihtml.escape(e["ngay"])}</span>'
            f'<span>{ihtml.escape(e["ghi"])}{nguon_html(e.get("nguon"))}</span></li>'
            for e in c["log"])
        hinh = (f'<figure class="hinh case-claim-scale">{ve_thang(c["thang_do"])}'
                f'<figcaption>{ihtml.escape(c["thang_do"]["nhan"])}</figcaption></figure>'
                if c.get("thang_do") else "")
        ds.append(f'''<article class="case-claim {cls}" id="{c['id']}" data-article-claim data-st="{cls}">
  <header class="case-claim-head">
    <a class="case-claim-id" href="#{c['id']}">{c['id']}</a>
    <span class="case-claim-status {cls}"><i aria-hidden="true"></i>{ihtml.escape(TRANG_THAI_HIEN_THI[c['status']])}</span>
    <span class="case-claim-actions"></span>
  </header>
  <p class="case-claim-text">{ihtml.escape(c['text'])}</p>
{hinh}
  <div class="case-claim-evidence">
    <p class="case-pin"><span>GHIM TẠI</span>{ihtml.escape(c['ghim'])}</p>
    <p class="case-falsifier"><span>ĐIỀU GÌ BÁC BỎ CLAIM NÀY</span>{ihtml.escape(c['falsifier'])}</p>
  </div>
{khoi_do_lai(c)}
  <details class="case-log"><summary>Lịch sử · {len(c['log'])} mốc</summary><ol>{nk}</ol></details>
</article>''')

    return f'''<section class="article-ledger" aria-labelledby="so-claim-title">
<details class="evidence case-evidence" id="so-claim">
  <summary>
    <span class="case-ledger-title"><span>Sổ claim của bài</span><b id="so-claim-title">{len(claims)} khẳng định</b><small>đổi trạng thái tại chỗ · không xoá</small></span>
    <span class="case-ledger-viz">
      <span class="case-ledger-bar" role="img" aria-label="{ihtml.escape(aria, quote=True)}">{thanh}</span>
      <span class="case-ledger-legend">{chu_giai}</span>
    </span>
    <span class="mo">mở {len(claims)} claim</span>
  </summary>
  <div class="trong case-ledger-body">
    <p class="case-ledger-intro">Mỗi claim kèm điều có thể bác bỏ nó, mốc ghim và toàn bộ lịch sử đổi trạng thái.</p>
    <div class="case-claim-list">{"".join(ds)}</div>
  </div>
</details>
</section>'''


def _chart_bai_v3(nb: dict) -> str:
    """Chart của bài phân định DefiLlama, đọc lại từ hiện vật pin như homepage."""
    hv = json.loads((kho_hien_vat() / nb["chart"]["hien_vat"]).read_text(encoding="utf-8"))
    chuoi = [(d["ngay"], int(d["usd"])) for d in hv["chuoi"]]
    svg, du_lieu = ve_chart_hero(chuoi, nb)
    cu, chain, sua = nb["so_cu"], nb["so_chain"], nb["so_sua"]
    lo, hi = nb["khoang"]
    pc = lambda v: v / cu * 100
    trieu = lambda v: f"{v / 1e6:.3f}".replace(".", ",")
    ch = nb["chart"]
    return f'''<figure class="chart chart-card" data-spotlight>
    <div class="chart-dau">
      <b>Phí swap Uniswap v4 — Robinhood chain</b>
      <span class="don-vi">USD/ngày · {chuoi[0][0]} → {chuoi[-1][0]}</span>
      <span class="cach-doc"><i><span class="sw"></span>chuỗi đã tính lại</i><i><span class="sw cu"></span>số cũ đã chết</i></span>
    </div>
    <div class="recalibration" role="img" aria-label="Ngày {ihtml.escape(nb['moc_ngay'])}: số cũ {so_vn_nguyen(cu)} đô; đếm on-chain {so_vn_nguyen(chain)} đô; số tính lại {so_vn_nguyen(sua)} đô">
      <div class="rc-head"><span>Bản đồ tái hiệu chỉnh · {ihtml.escape(nb['moc_ngay'])}</span><em>tỷ lệ so với số cũ = 100%</em></div>
      <div class="rc-track">
        <span class="rc-axis"></span>
        <span class="rc-band" style="--left:{pc(lo):.2f}%;--width:{pc(hi) - pc(lo):.2f}%"></span>
        <i class="rc-pin chain" style="--x:{pc(chain):.2f}%;--delay:.48s"><span class="rc-label"><b>${trieu(chain)}M</b>đếm on-chain</span></i>
        <i class="rc-pin fixed" style="--x:{pc(sua):.2f}%;--delay:.64s"><span class="rc-label"><b>${trieu(sua)}M</b>họ tính lại</span></i>
        <i class="rc-pin old" style="--x:100%;--delay:.8s"><span class="rc-label"><b>${trieu(cu)}M</b>số cũ</span></i>
      </div>
    </div>
    <div class="chart-mobile-nav" aria-label="Đi tới mốc trên biểu đồ"><span>ĐIỂM XEM</span><button type="button" data-chart-jump="pin">{ihtml.escape(nb['moc_ngay'])}</button><button type="button" data-chart-jump="end">Mới nhất →</button></div>
    <div class="chart-cuon">{svg}</div>
    <div class="provenance">
      <svg class="pmark" viewBox="0 0 240 240" aria-hidden="true">{mark_path()}</svg>
      <span class="f"><span class="k">GHIM</span><span>{inline(ch['ghim'], 'trang_chu.chart.ghim')}</span></span>
      <span class="f"><span class="k">NGUỒN</span><span>{inline(ch['nguon'], 'trang_chu.chart.nguon')}</span></span>
      <span class="f"><span class="k">ĐỌC</span><span><b>{vn_ngay(hv['_doc_luc'])}</b></span></span>
      <a class="chay" href="#tu-kiem">tự chạy lại được</a>
    </div>
  </figure><script>window.BP_CHART_DATA={du_lieu};</script>'''


def _hero_bai_v3(fm: dict, claims: list, trang_chu: dict) -> str:
    """Hero article WOW; bài #1 giữ tuyến ba số, các bài khác dùng tuyến claim thật."""
    c0 = claims[0]
    cls0, _ = TRANG_THAI[c0["status"]]
    # 🔵 Số ghost đọc TIÊU ĐỀ ĐẦY ĐỦ, không đọc chuỗi H1. Câu dài là chỗ chắc chắn có
    # con số; dòng H1 ngắn có thể không mang số nào, và khi đó ghost tụt về mã token —
    # mất đúng thứ hero dùng để nhận diện bài. Hai đường độc lập, cố ý.
    metric = _metric_tieu_de(fm["title"]) or fm["token"]
    ngay = vn_ngay(str(fm["date"])[:10])
    nb = trang_chu.get("noi_bat") if trang_chu else None

    if nb:
        cu, chain, sua = nb["so_cu"], nb["so_chain"], nb["so_sua"]
        lan = f"{cu / chain:.1f}".replace(".", ",")
        lech = f"{abs(sua - chain) / chain * 100:.2f}".replace(".", ",")
        ty_so = f'''<div class="heronum article-ratio">
      <p class="l">Chênh lệch ngày {ihtml.escape(nb['moc_ngay'])}</p>
      <p class="v">{lan}<em>×</em></p>
      <p class="d">đã phân định · số tính lại lệch {lech}%</p>
    </div>'''
        duong = f'''<div class="case-path" role="img" aria-label="Tuyến phân định từ số dashboard, qua phép đếm on-chain, tới số đã tính lại">
      <div class="case-step old"><span>01 · DASHBOARD</span><strong>${so_vn_nguyen(cu)}</strong><small>số mở ra điều tra</small></div><i aria-hidden="true">→</i>
      <div class="case-step chain"><span>02 · ON-CHAIN</span><strong>${so_vn_nguyen(chain)}</strong><small>{ihtml.escape(nb['dem_swap'])} swap được đếm</small></div><i aria-hidden="true">→</i>
      <div class="case-step fixed"><span>03 · PHÂN ĐỊNH</span><strong>${so_vn_nguyen(sua)}</strong><small>chuỗi đã được tính lại</small></div>
    </div>'''
        chart = _chart_bai_v3(nb)
    else:
        dem = _dem_trang_thai(claims)
        dang = dem.get("ĐANG ĐỨNG", 0) + dem.get("ĐÃ XÁC NHẬN", 0)
        log = sum(len(c["log"]) for c in claims)
        ty_so = f'''<div class="heronum article-ratio article-ledger-count">
      <p class="l">Sổ bằng chứng của bài</p>
      <p class="v">{len(claims)}<em> claim</em></p>
      <p class="d">{dang} vẫn đứng vững hoặc đã xác nhận</p>
    </div>'''
        duong = f'''<div class="case-path" role="img" aria-label="Tuyến bằng chứng: đối tượng, điều bác bỏ, trạng thái hiện tại">
      <div class="case-step file"><span>01 · ĐỐI TƯỢNG</span><strong>{ihtml.escape(fm['token'])}</strong><small>hồ sơ được ghim theo token</small></div><i aria-hidden="true">→</i>
      <div class="case-step test"><span>02 · TỰ KIỂM</span><strong>{len(claims)}</strong><small>điều bác bỏ viết cùng claim</small></div><i aria-hidden="true">→</i>
      <div class="case-step state {cls0}"><span>03 · SỔ SỐNG</span><strong>{log} mốc</strong><small>lịch sử đổi trạng thái công khai</small></div>
    </div>'''
        chart = ""

    return f'''<section class="hero hero-article">
  <span class="ghost-num" aria-hidden="true">{ihtml.escape(metric)}</span>
  <span class="hero-code" aria-hidden="true">CLAIM {ihtml.escape(c0['id'])} · {ihtml.escape(c0['status'])}</span>
  <div class="article-path" aria-label="Vị trí bài viết">
    <a href="../../">BlockPinned</a><span>/</span><a href="../../#ho-so">Điều tra</a><span>/</span><b>{ihtml.escape(fm['token'])}</b><i><span class="dot {cls0}"></span>{ihtml.escape(TRANG_THAI_NGAN[c0['status']])}</i>
  </div>
  <p class="eyebrow"><span>{ihtml.escape(fm['token'])}</span><span class="im">{ngay}</span></p>
  <h1 class="display">{_tieu_de_nhan(_tieu_de_h1(fm))}</h1>
  <p class="subline">{ihtml.escape(fm['mo_ta'])}</p>
{_khoi_gioi_han(fm)}  <div class="article-verdict">{ty_so}{duong}</div>
{chart}
</section>'''


def trang_bai_v3(fm: dict, claims: list, body_md: str, o: str, ho_so: str,
                  trang_chu: dict, visuals: list) -> str:
    """Dựng trang bài bằng markup WOW, không dùng `.dai/.so/.claim` của D2."""
    reading_layout = fm.get("reading_layout", "standard")
    if reading_layout not in {"standard", "centered"}:
        raise LoiCong(f"reading_layout chỉ nhận standard/centered — {o}")
    lop_doc = " article-body-centered" if reading_layout == "centered" else ""
    muc = []
    for h in re.findall(r"^##\s+(.+)$", body_md, re.M)[:3]:
        nhan = re.sub(r"[*_`]", "", h).strip()
        muc.append(f'<a href="#{slug(h)}">{ihtml.escape(nhan)}</a>')
    ban_dang = (f'<a href="{fm["kenh_x"]}">bản đăng trên X ↗</a>' if fm.get("kenh_x")
                else '<i>chưa đăng trên kênh</i>')
    than = render(body_md, o, visuals).replace('<div class="cuon"><table>', '<div class="bang"><table>')
    return (_hero_bai_v3(fm, claims, trang_chu)
            + '<nav class="article-map" aria-label="Điều hướng trong bài"><span>Đọc theo bằng chứng</span>'
            + '<a href="#so-claim">Sổ claim</a>' + "".join(muc) + '</nav>'
            + _so_claim_v3(claims)
            + f'''<section class="than article-body{lop_doc}" id="ban-day-du">
  <div class="article-meta">
    <span><b>GHIM</b>{ihtml.escape(fm['ghim'])}</span>
    <span><b>NGÀY</b>{vn_ngay(str(fm['date'])[:10])}</span>
    <span class="article-meta-link">{ban_dang}</span>{ho_so}
  </div>
  {than}
</section>''')


def so_claim(claims: list) -> str:
    out = ['<section class="so" data-loc-vung="het"><h2 id="so-claim">Sổ claim</h2>',
           '<p class="dan">Mỗi khẳng định của bài này một dòng, kèm điều gì sẽ bác bỏ nó. '
           'Trạng thái đổi thì sửa tại đây, và ghi lại ngày. Không dòng nào bị xoá.</p>']
    for c in claims:
        cls, _ = TRANG_THAI[c["status"]]
        nk = "".join(
            f'<li><span class="d">{e["ngay"]}</span>{ihtml.escape(e["ghi"])}'
            + nguon_html(e.get("nguon"))
            + "</li>" for e in c["log"])
        hinh = (f'<figure class="hinh">{ve_thang(c["thang_do"])}'
                f'<figcaption>{ihtml.escape(c["thang_do"]["nhan"])}</figcaption></figure>'
                if c.get("thang_do") else "")
        out.append(f"""<article class="claim {cls}" id="{c['id']}" data-st="{cls}">
  <h3><a class="id" href="#{c['id']}">{c['id']}</a>
      <span class="chip {cls}">{TRANG_THAI_HIEN_THI[c['status']]}</span></h3>
  <p style="margin:0">{ihtml.escape(c['text'])}</p>
  {hinh}
  <p class="dong"><span class="nhan">GHIM TẠI</span>{ihtml.escape(c['ghim'])}</p>
  <p class="dong bac"><span class="nhan">ĐIỀU GÌ BÁC BỎ CLAIM NÀY</span>{ihtml.escape(c['falsifier'])}</p>
  {khoi_do_lai(c)}
  <ul class="nk">{nk}</ul>
</article>""")
    return "\n".join(out) + "</section>"


def bang_diem(moi: list) -> str:
    """Bảng điểm của CẢ KÊNH trên trang chủ — sinh từ sổ claim, không gõ tay.

    Vì sao có: bản đầu của trang chủ là một câu tagline, ba đoạn kể về cơ chế, rồi một
    danh sách 4 dòng. Danh sách 4 dòng thì tô vẽ kiểu gì cũng mỏng — thứ thiếu không phải
    màu sắc mà là NÓI ĐƯỢC ĐIỀU GÌ. Phần mạnh nhất của desk (một điều-bác-bỏ đã chạy và
    claim sống sót, một claim bị chính điều-bác-bỏ của nó bác) trước đó không xuất hiện ở
    đâu trên trang chủ cả.

    🔴 VÒNG 2 — 06/08, user bác bản vừa lên, hai câu, hai lỗi khác nhau:

    ① *"3 cái gần như bị trùng"* — hàng bốn THẺ SỐ đứng ngay trên thanh xếp chồng, và
      ba trong bốn thẻ in lại đúng ba con số của chú giải bên dưới (2 · 4 · 2), chỉ khác
      cái nhãn. Một con số nói hai lần ở hai chỗ cách nhau 40px thì lần thứ hai không
      thêm thông tin nào, mà lại chiếm mất chỗ của thứ chưa ai nói. Nay CHÚ GIẢI là chỗ
      DUY NHẤT mang số của từng trạng thái; thẻ số bỏ hẳn.
    ② *"nhìn vô không hiểu"* — khối `ul.diem` cũ in mỗi claim thành một hạt `27/07 · C1`.
      Người đọc không có cách nào biết C1 nói gì mà không bấm đi. Nay mỗi dòng in NGUYÊN
      VĂN câu claim, kèm bài và ngày; dãy mã biến mất.

    Và vì cả hai lỗi trên đều là *"đúng số, sai chỗ đọc"*, phần thay thế không phải một
    khối tĩnh nữa: chú giải trở thành BỘ LỌC của chính danh sách bên dưới nó — bấm chip
    nào thì danh sách còn đúng những claim đang ở trạng thái đó. Số trên chip và số dòng
    hiện ra là CÙNG MỘT phép đếm, nên không có chỗ cho hai mẫu số ghép nhầm vào một câu.
    """
    dem = {k: [c for _, _, c in moi if c["status"] == k] for k in TRANG_THAI}
    d_num = {k: len(v) for k, v in dem.items()}
    doi = sum(n for k, n in d_num.items() if k != "ĐANG ĐỨNG")
    so_bai = len({s for s, _, _ in moi})
    cho_moc = sum(1 for _, _, c in moi if c.get("han") and c["status"] == "ĐANG ĐỨNG")

    # Mỗi dòng mang ĐỦ ba thứ để đọc được mà không phải bấm đi: trạng thái (chip có
    # glyph) · nguyên văn câu claim · bài và ngày. `data-doi` cho bộ lọc biết dòng nào
    # thuộc nhóm "đã đổi trạng thái" — nhóm mặc định, vì đó là thứ X/Telegram không chở.
    hang = "".join(
        f'<li class="tt {TRANG_THAI[c["status"]][0]}" data-st="{TRANG_THAI[c["status"]][0]}" '
        f'data-doi="{0 if c["status"] == "ĐANG ĐỨNG" else 1}">'
        f'<a class="tt-hop" href="bai/{s}/#{c["id"]}">'
        f'<span class="chip {TRANG_THAI[c["status"]][0]}">{TRANG_THAI_HIEN_THI[c["status"]]}</span>'
        f'<span class="tx">{ihtml.escape(c["text"])}</span>'
        f'<span class="mt">{vn_ngay(s[:10])} · {c["id"]} · {ihtml.escape(tieu)}</span>'
        f'</a></li>'
        for s, tieu, c in moi)

    phu = (f'<b>{doi}</b> trong số đó đã ĐỔI TRẠNG THÁI kể từ lúc đăng — đó là phần X và '
           f'Telegram không chở được.')
    if cho_moc:
        phu += f' Còn {cho_moc} mốc tự đặt ngày, chưa tới hạn.'
    return (f'<h2 id="bang-diem">Bảng điểm</h2>'
            f'<section class="board" data-hien>'
            f'<div class="bh"><b>Sổ gốc BlockPinned</b>'
            f'<span>{len(moi)} khẳng định · {so_bai} bài</span></div>'
            f'{thanh_xep(d_num, len(moi))}'
            f'<div class="dem phu">{phu}</div></section>'
            f'<div class="tt-khu" data-hien>'
            f'<div class="tt-dau">'
            f'<div class="nhom-loc">'
            f'<button class="lg-loc" type="button" data-loc="doi">Đã đổi trạng thái '
            f'<span class="n">{doi}</span></button>'
            f'<button class="lg-loc" type="button" data-loc="het">Cả sổ '
            f'<span class="n">{len(moi)}</span></button></div>'
            f'<span class="lo" id="loc-lo"></span></div>'
            # 🔴 CẮT CÒN 5 DÒNG. Trang chủ trước đó in cả 8 dòng "đã đổi" (và 35 dòng
            # nếu bấm "Cả sổ") ngay giữa trang, đẩy mục Bài xuống 4,2 màn hình trên
            # điện thoại — user đo bằng chính ngón tay mình. Danh sách đầy đủ vẫn ở
            # đây, sau đúng một lượt bấm; số trên nút là số THẬT, không phải "xem thêm".
            f'<ol class="tt-ds" id="tt-ds" data-loc-vung="doi" data-cap="5">{hang}</ol>'
            f'<button class="lg-loc mo-them" type="button" id="mo-them" hidden></button></div>')


def ban_do(so_bai: int, so_token: int, gt: list, facts: list, so_hien_vat: int) -> str:
    """BẢN ĐỒ SITE — hàng ô ngang ở màn hình đầu trang chủ.

    User 06/08, vòng 3: *"làm sao để mà người ngoài nhìn vô biết được trang này có
    cái gì… ví dụ như vô sổ gốc rồi kéo mãi xuống mới thấy bài viết?"*. Đo trước khi
    sửa: trên khổ điện thoại, mục **Bài** nằm ở **3.421px** — phải cuộn **4,2 màn
    hình**. Và thanh điều hướng thì giấu mọi mục không phải mục đang mở khi màn hẹp,
    nên người vào bằng điện thoại **không thấy** site có những trang nào.

    Ô ở đây **thay** hai thẻ lớn Track record/Facts của vòng 2, không đứng cạnh chúng:
    cùng một link in hai lần ở hai chỗ chính là lỗi *"3 cái gần như bị trùng"* mà user
    đã bác một vòng trước. Thứ giữ lại từ hai thẻ đó là CHỮ — mỗi ô vẫn mang một câu
    nói nó là gì, chỉ gọn hơn và đứng sớm hơn ba màn hình.

    Số trên ô đọc từ nguồn của chính mục nó dẫn tới. Ô Dữ liệu nằm đây vì user gỡ nó
    khỏi thanh điều hướng — gỡ khỏi nav không có nghĩa là giấu.
    """
    o = [("BÀI VIẾT", so_bai, "sổ claim của từng bài", "#bai"),
         ("TOKEN", so_token, "hồ sơ theo đối tượng", "token/"),
         ("GHI TRƯỚC", len(gt), "dán số trước khi biết đáp án", "track-record/"),
         ("FACTS", len(facts), "một số, một block, một lệnh", "facts/"),
         ("DỮ LIỆU", so_hien_vat, "file thô, tải về đếm lại", "du-lieu/")]
    return '<nav class="ban-do" aria-label="Trang này có gì">' + "".join(
        f'<a class="o-map" href="{d}"><span class="k">{k}</span>'
        f'<span class="v">{n}</span><span class="g">{g}</span>'
        f'<span class="mui" aria-hidden="true">→</span></a>'
        for k, n, g, d in o if n) + "</nav>"


def trang_muc_token(tk: dict, primers: list[dict] | None = None) -> str:
    """Mục lục `/token/` — CẢ BỐN token, kể cả token chưa đủ sàn mở tủ kính.

    User 06/08 chốt giữ sàn 3 bài (chỉ UNI có tủ kính), nhưng thêm trang này, và lý do
    là một luật chứ không phải một trang: **tủ kính có sàn, bản đồ thì không**. Không
    có trang này thì HYPE và PENDLE biến mất khỏi site dù bài của chúng vẫn sống —
    site sẽ nói dối về phạm vi của chính nó, bằng cách im lặng.

    Token chưa đủ sàn KHÔNG được dựng một trang trống cho có: nó trỏ thẳng sang bài,
    và nói rõ còn thiếu mấy bài. Một trang một-bài chỉ là bản chép của bài đó.
    """
    primers = primers or []
    if BO_CUC == "v3":
        return trang_muc_token_v3(tk, primers)

    hang = [
        f'<a class="cua-o tok primer" href="{ihtml.escape(p["id"], quote=True)}/">'
        f'<span class="k">{ihtml.escape(p["token"])}</span><span class="t">{ihtml.escape(p["name"])}</span>'
        f'<span class="n"><b>Primer</b><i></i><b>{len(p["visuals"])}</b> visual</span>'
        f'<span class="g">{ihtml.escape(p["description"])}</span><span class="mui" aria-hidden="true">→</span></a>'
        for p in primers]
    for ma, v in sorted(tk.items(), key=lambda x: (-x[1]["bai"], -x[1]["claim"])):
        co_tu = ma == TU_KINH and CO_TRANG[TU_KINH_DUONG]
        dich = f"{TU_KINH.lower()}/" if co_tu else f"../bai/{v['slug_moi']}/"
        d_num = {k: v["dem"].get(k, 0) for k in TRANG_THAI}
        thieu = TU_KINH_SAN - v["bai"]
        hang.append(
            f'<a class="cua-o tok" href="{dich}">'
            f'<span class="k">{ma}</span>'
            f'<span class="t">{TOKEN_TEN[ma]}</span>'
            f'<span class="n"><b>{v["bai"]}</b> bài<i></i><b>{v["claim"]}</b> khẳng định</span>'
            f'{thanh_mini(d_num, v["claim"])}'
            f'<span class="g">'
            + (f'Hồ sơ đã mở — mọi khẳng định về {TOKEN_TEN[ma]} nằm trên một trang, '
               f'mỗi khẳng định giữ mốc block đã đo.' if co_tu else
               f'Hồ sơ đang tích lũy: cần {TU_KINH_SAN} bài, đang có {v["bai"]}'
               f'{" — còn " + str(thieu) + " bài nữa" if thieu > 0 else ""}. '
               f'Vào thẳng bài mới nhất.')
            + f'</span><span class="mui" aria-hidden="true">→</span></a>')
    tong_b = sum(v["bai"] for v in tk.values())
    tong_c = sum(v["claim"] for v in tk.values())
    return (f'<p class="crumb">Hồ sơ theo đối tượng</p>'
            f'<h1>BlockPinned đã đo được gì, xếp theo token</h1>'
            f'<p class="dan">{len(tk)} token có bài · {len(primers)} Token Primer · {tong_b} bài · {tong_c} khẳng định. Token nào đủ '
            f'<b>{TU_KINH_SAN} bài</b> thì có một trang gom mọi câu về nó — mỗi câu giữ nguyên '
            f'trạng thái hiện tại, kể cả những câu đã bị bác bỏ. Token chưa đủ thì vào thẳng bài, '
            f'vì một trang dựng từ một bài chỉ là bản chép của bài đó.</p>'
            f'<div class="cua cua-3" data-hien>{"".join(hang)}</div>')


def trang_muc_token_v3(tk: dict, primers: list[dict] | None = None) -> str:
    """Mục lục token bằng đúng component v3 mà CSS/JS production đang canh.

    Bản lật production 11/08 vẫn gọi khuôn D2 (`.cua/.cua-o`) trong khi v3 chỉ còn
    luật cho `.token-directory/.token-card`. Kết quả là dữ liệu vẫn đủ nhưng năm thẻ
    rơi thành một dòng chữ nối liền — hỏng hình mà mọi cổng nội dung đều xanh. Khuôn
    này sinh hoàn toàn từ `tk`; mockup chỉ là hợp đồng trình bày, không phải nguồn số.
    """
    primers = primers or []
    ds = sorted(tk.items(), key=lambda x: (-x[1]["bai"], -x[1]["claim"], x[0]))
    tong_b = sum(v["bai"] for _, v in ds)
    tong_c = sum(v["claim"] for _, v in ds)
    so_mo = sum(ma == TU_KINH and CO_TRANG[TU_KINH_DUONG] for ma, _ in ds)

    nut_nhanh = [
        '<button type="button" data-token-tag="all" aria-pressed="true">'
        '<span class="token-logo token-logo-all" aria-hidden="true">'
        '<i></i><i></i><i></i><i></i></span>'
        f'<span class="token-switch-copy"><b>Tất cả</b><small>{tong_c} claim</small></span></button>'
    ]
    ty_le = []
    the = []
    ten_tt = {k: TRANG_THAI_NGAN[k] for k in TRANG_THAI}
    thu_tu_tt = ["ĐÃ XÁC NHẬN", "ĐANG ĐỨNG", "ĐÃ SỬA", "BỊ BÁC", "CHỜ SỐ"]

    for stt, (ma, v) in enumerate(ds, 1):
        ma_nho = ma.lower()
        co_tu = ma == TU_KINH and CO_TRANG[TU_KINH_DUONG]
        # 🔴 MỌI token đi về CÙNG một chỗ: danh sách bài của chính nó. Bản trước chia
        # đôi — token đủ 3 bài vào hồ sơ, token chưa đủ nhảy thẳng vào bài mới nhất —
        # nên hai thẻ trông giống nhau lại làm hai việc khác nhau, và token 1 bài không
        # có chỗ nào xem được nó có gì. User chốt 11/08: bấm token là ra hết bài về nó,
        # kể cả khi mới có một bài. Sổ claim của UNI vẫn còn, nhưng là cửa PHỤ ghi rõ.
        dich = f"../bai/?token={ma_nho}"
        profile = "open" if co_tu else "building"
        nut_nhanh.append(
            f'<button type="button" data-token-tag="{ma_nho}" aria-pressed="false">'
            f'<span class="token-logo"><img src="../anh/token-{ma_nho}.png" width="32" '
            f'height="32" alt="" decoding="async"></span>'
            f'<span class="token-switch-copy"><b>{ma}</b><small>{v["claim"]} claim</small>'
            f'</span></button>')
        ty_le.append(
            f'<span class="{ma_nho}" style="--claims:{v["claim"]}"><b>{ma}</b>'
            f'<i>{v["claim"]}</i></span>')

        thanh, doc_thanh = [], []
        for trang_thai in thu_tu_tt:
            n = v["dem"].get(trang_thai, 0)
            if n:
                thanh.append(f'<i class="{TRANG_THAI[trang_thai][0]}" style="--n:{n}"></i>')
                doc_thanh.append(f'{n} {ten_tt[trang_thai]}')
        trang_thai_the = f'{v["bai"]} bài' if v["bai"] != 1 else "1 bài"
        copy = (f'Mọi bài về {TOKEN_TEN[ma]}, mới nhất trước — kèm trạng thái hôm nay của '
                f'từng khẳng định.')
        the.append(
            f'<a class="token-card{" token-card-featured" if co_tu else ""}" '
            f'data-token-card data-token="{ma_nho}" data-profile="{profile}" '
            f'data-claim-ghost="{v["claim"]:02d}" data-spotlight href="{dich}">'
            f'<span class="token-card-no">{stt:02d}</span>'
            f'<span class="token-card-state{" open" if co_tu else ""}"><i></i>'
            f'{trang_thai_the}</span>'
            f'<span class="token-symbol">{ma}</span><strong>{TOKEN_TEN[ma]}</strong>'
            f'<span class="token-count"><b>{v["bai"]}</b> bài<i></i>'
            f'<b>{v["claim"]}</b> khẳng định</span>'
            f'<span class="token-status-bar" aria-label="{ihtml.escape(", ".join(doc_thanh))}">'
            f'{"".join(thanh)}</span>'
            f'<span class="token-card-copy">{copy}</span>'
            f'<span class="token-card-go">Mở {v["bai"]} bài<i>→</i></span></a>')

    doc_phan_bo = ", ".join(f"{ma} {v['claim']}" for ma, v in ds)
    primer_html = ""
    if primers:
        cards = "".join(
            f'<a class="primer-index-card" href="{ihtml.escape(p["id"], quote=True)}/" '
            f'data-token="{ihtml.escape(p["token"], quote=True)}"><small>TOKEN PRIMER · {ihtml.escape(p["token"])}</small>'
            f'<i>{len(p["visuals"])} visual · VERIFY tách lớp</i><strong>{ihtml.escape(p["name"])} — đọc cỗ máy trước, đọc token sau</strong>'
            f'<span>Mở Primer <i aria-hidden="true">→</i></span></a>' for p in primers)
        primer_html = f'''<section class="primer-directory" aria-labelledby="primer-directory-title">
  <div class="primer-directory-head"><div><p class="section-code">TOKEN PRIMERS</p><h2 id="primer-directory-title">Hồ sơ bắt đầu từ cỗ máy</h2></div><p>Primer không tính vào sổ claim của bài viết; nó gom mô hình kinh doanh, chính sách vốn và đường token capture trên một đường đọc.</p></div>
  <div class="primer-index-grid">{cards}</div>
</section>'''
    return f'''<section class="hero token-index-hero">
  <span class="ghost-num" aria-hidden="true">{len(ds) + len(primers):02d}</span>
  <span class="hero-code" aria-hidden="true">OBJECT INDEX · COVERAGE MAP</span>
  <p class="eyebrow"><span>Hồ sơ theo đối tượng</span><span class="im">độ phủ nhìn được · trạng thái không bị giấu</span></p>
  <h1 class="display">BlockPinned đã đo được gì, <span class="nhan-manh">xếp theo token.</span></h1>
  <p class="subline">{len(ds)} token có bài · {len(primers)} Token Primer · {tong_b} bài · {tong_c} khẳng định. Primer đọc cỗ máy theo đối tượng; phần còn lại mở toàn bộ bài và trạng thái claim.</p>
</section>
{primer_html}
<nav class="token-switcher" aria-label="Lọc nhanh theo token">
  <span class="token-switcher-label">Chọn đối tượng</span>{"".join(nut_nhanh)}
</nav>
<div class="token-overview">
  <div class="token-overview-head"><span><b>{tong_c}</b><small>khẳng định, chia theo {len(ds)} token</small></span><i>độ rộng = số claim</i></div>
  <div class="token-scale" role="img" aria-label="Phân bổ {tong_c} khẳng định: {doc_phan_bo}">{"".join(ty_le)}</div>
</div>
<section class="token-directory" aria-labelledby="token-directory-title">
  <div class="token-directory-head">
    <div><p class="section-code">OBJECT COVERAGE</p><h2 id="token-directory-title">Mỗi token, mọi bài đã viết về nó</h2></div>
    <p class="token-directory-note">Bấm một token để mở toàn bộ bài về nó{
      f' · <a href="{TU_KINH.lower()}/">{TU_KINH} còn có sổ claim riêng →</a>'
      if CO_TRANG[TU_KINH_DUONG] else ''}</p>
  </div>
  <div class="token-grid" id="token-grid">{"".join(the)}</div>
</section>'''


def thanh_mini(dem: dict, tong: int) -> str:
    """Thanh xếp chồng cỡ nhỏ, dùng trong thẻ bài ở dải ngang. Chỉ có hình — chú giải
    của nó là dòng chữ ngay dưới thẻ (*"5 claim — 5 đang đứng"*), nên nó không phải là
    màu-đứng-một-mình."""
    if not tong:
        return ""
    return ('<span class="mini" aria-hidden="true">' + "".join(
        f'<span class="seg {TRANG_THAI[k][0]}" style="width:{n / tong * 100:.2f}%"></span>'
        for k, n in dem.items() if n) + "</span>")


def sap_phan_dinh(moi: list) -> str:
    """Lịch những claim tự đặt NGÀY. Đếm ngược tính bằng JS, không tính lúc build —
    để trang tự đúng qua từng ngày mà không phải dựng lại, và để hai lần dựng cùng
    nội dung vẫn ra cùng byte."""
    # 🔴 VÁ 16/08/2026 — chỉ claim CÒN ĐANG ĐỨNG mới lên đồng hồ.
    # `cong_han` (:1250) đã viết luật này thành lời từ đầu — *"Claim đã được phân định
    # thì miễn: hạn của nó là lịch sử"* — nhưng dòng dựng danh sách thì không lọc, nên
    # bảng chở cả claim đã xong. Hậu quả đo được ngày 16/08: 7 dòng, 3 dòng hiện
    # ĐÃ TỚI HẠN, mà **2 trong 3 đã phân định xong từ 03/08 và 28/07**. Một báo động
    # thật nằm giữa hai báo động giả thì cả ba đều mất tiếng — và đây là khối mà cả
    # trang dựa vào để tự đòi nợ. Cùng loài với `LDO/FACTS.md §24`: cổng không FAIL,
    # nó chỉ in ra thứ trông như câu trả lời.
    co = sorted(((c["han"], s, t, c) for s, t, c in moi
                 if c.get("han") and c["status"] == "ĐANG ĐỨNG"), key=lambda x: x[0])
    if not co:
        return ""
    if BO_CUC != "v3":
        hang = "".join(
            f'<li><span class="ngay" data-han="{h}">{h[8:10]}/{h[5:7]}/{h[0:4]}</span>'
            f'<a href="bai/{s}/#{c["id"]}">{c["id"]}</a> — {ihtml.escape(c["han_ghi"])}</li>'
            for h, s, t, c in co)
        return (f'<h2 id="sap-phan-dinh">Sắp phân định</h2>'
                f'<p class="dan">Claim tự đặt ngày. Tới ngày đó là có kết quả, và nếu tôi trễ '
                f'thì dòng dưới đây tự đổi thành ĐÃ TỚI HẠN.</p>'
                f'<ul class="han">{hang}</ul>')

    # ── v3: ĐỒNG HỒ TỰ TỐ CÁO ────────────────────────────────────────────────────
    # Khối này KHÔNG có trong bản duyệt codex — không phải codex bỏ, mà nó dựng từ một
    # bản site cũ hơn. User chốt 10/08: giữ, và vẽ khuôn v3 cho nó.
    #
    # Bám đúng ba luật hình của v3 chứ không vẽ tự do:
    #  ① eyebrow `section-code` mono giãn chữ, y như `.facts-ledger-head` và
    #     `.track-ledger-head` — khối này là anh em của chúng, không phải khách lạ.
    #  ② hàng ngăn bằng HAIRLINE, không hộp. Luật vòng 2 của `HANDOFF-v3`: "metric
    #     trần + hairline, không hộp".
    #  ③ ACCENT CHỈ Ở ĐIỂM PHÁN ĐỊNH. Ngày và mã claim mặc mực; màu chỉ bật khi dòng
    #     ĐÃ TỚI HẠN. Đó là cùng luật `.tr` của track record dùng — màu là phán quyết,
    #     không phải trang trí.
    #
    # 🔴 GIỮ NGUYÊN hai móc `.han` và `.ngay[data-han]`: `JS_DO_LAI` neo đếm ngược vào
    # đúng chúng. Đổi tên class ở đây là làm chết đồng hồ, mà đồng hồ chết thì trang
    # vẫn dựng, vẫn 12/12 cổng, chỉ là mọi dòng đứng im ở ngày ghi cứng — hỏng theo
    # đúng kiểu im lặng nhất, và là kiểu duy nhất khối này KHÔNG được phép hỏng.
    hang = "".join(
        f'<li class="clock-hang">'
        f'<span class="ngay" data-han="{h}">{h[8:10]}/{h[5:7]}/{h[0:4]}</span>'
        f'<a class="clock-ma" href="bai/{s}/#{c["id"]}">{c["id"]}</a>'
        f'<span class="clock-hua">{ihtml.escape(c["han_ghi"])}</span></li>'
        for h, s, t, c in co)
    return (f'<section class="clock-khu" id="sap-phan-dinh" aria-labelledby="clock-title">'
            f'<div class="clock-dau"><div>'
            f'<p class="section-code">PRE-REGISTERED DEADLINES · {len(co):02d}</p>'
            f'<h2 id="clock-title">Sắp phân định</h2></div>'
            f'<p>Claim tự đặt ngày cho chính nó. Tới ngày đó là có kết quả — và nếu tôi trễ, '
            f'dòng dưới đây <b>tự đổi thành ĐÃ TỚI HẠN</b> mà không cần ai sửa.</p></div>'
            f'<ul class="han clock-ds">{hang}</ul></section>')


def vn_ngay(iso: str) -> str:
    return f"{iso[8:10]}/{iso[5:7]}/{iso[0:4]}"


def doc_facts() -> list:
    """Đọc `content/facts.json` — đơn vị đăng thứ hai (`brief-chien-luoc-dang-x.md §0b`).

    Fact = một phát biểu ĐÚNG TẠI MỘT BLOCK, kiểm được bằng MỘT lệnh. Không phải bài:
    không ordinal, không dòng claim, không trang riêng — cả bộ gom vào `/facts/`.

    🔴 File vắng hoặc danh sách rỗng ⇒ trả `[]` và KHÔNG dựng trang. Một trang rỗng
    đi ra ngoài còn tệ hơn không có trang: nó hứa một mục rồi để trắng.
    """
    p = CONTENT / "facts.json"
    if not p.is_file():
        return []
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise LoiCong(f"content/facts.json không phải JSON hợp lệ — {e}")
    fs = d.get("facts", d) if isinstance(d, dict) else d
    if not isinstance(fs, list):
        raise LoiCong("content/facts.json phải là list, hoặc object có khoá 'facts'")
    return fs


def cong_facts(fs: list) -> None:
    """Cổng ⑪ — luật lọt cửa của `§0b`, phần máy kiểm được.

    Ba thứ bắt buộc vì Fact chỉ có đúng ba thứ: một con số · một block · một lệnh.
    Thiếu bất kỳ cái nào thì nó không còn là Fact, nó là một câu khẳng định trần —
    đúng thứ kênh này sinh ra để không phải là.

    🔴 `chan` (câu chặn suy luận sai) BẮT BUỘC KHAI, kể cả khi không có. Máy không
    biết một fact có suy luận sai phổ thông đi kèm hay không, nên nó không tự quyết
    được — nhưng nó ÉP người viết phải quyết. Để trống không phải một lựa chọn;
    viết "KHÔNG CÓ" là một lựa chọn, và nó để lại dấu vết.
    """
    thay = set()
    for i, f in enumerate(fs, 1):
        o = f"content/facts.json[{i}]"
        if not isinstance(f, dict):
            raise LoiCong(f"{o} phải là object")
        fid = str(f.get("id", "")).strip()
        if not fid:
            raise LoiCong(f"{o} thiếu 'id'")
        if fid in thay:
            raise LoiCong(f"{o} id '{fid}' TRÙNG — id là neo của URL, trùng là mất một mục")
        thay.add(fid)
        for k, ten in (("cau", "câu fact"), ("so", "CON SỐ"),
                       ("block", "BLOCK + giờ đọc"), ("lenh", "LỆNH tự kiểm")):
            if not str(f.get(k, "")).strip():
                raise LoiCong(f"{o} ({fid}) thiếu {ten} — Fact chỉ có ba thứ, "
                              f"thiếu một là không còn là Fact")
        if not re.search(r"\d", str(f["block"])):
            raise LoiCong(f"{o} ({fid}) 'block' không mang số block — "
                          f"'{f['block']}' đọc như một câu, không như một mốc")
        if len(str(f["lenh"]).strip()) < 10:
            raise LoiCong(f"{o} ({fid}) 'lenh' quá ngắn để chạy được: '{f['lenh']}' — "
                          f"đường tự kiểm phải dán vào terminal là chạy")
        if not str(f.get("chan", "")).strip():
            raise LoiCong(f"{o} ({fid}) thiếu 'chan' — câu chặn suy luận sai. "
                          f"Không có suy luận nào cần chặn thì ghi thẳng \"KHÔNG CÓ\"; "
                          f"để trống nghĩa là chưa ai quyết")
        # ── KHOẢNG CÁCH — thêm 01/08 sau khi user bác một ứng viên của desk ──────
        # Ca xác: desk xếp "ENA chưa từng bị đốt một wei nào" lên hàng đầu. Đúng, ghim
        # được block, kiểm bằng một lệnh — và VÔ NGHĨA, vì phần lớn token không đốt.
        # Nó không phân biệt ENA khỏi bất cứ thứ gì. Cổng cũ cho nó qua sạch, vì cả ba
        # thứ nó kiểm đều là câu hỏi "có đúng không", không câu nào hỏi "biết rồi thì
        # đổi được gì".
        #
        # 🔴 MÁY KHÔNG PHÁN ĐƯỢC khoảng cách này có đủ lớn hay không — đó là cổng NGƯỜI,
        # cùng loại với cổng độc giả LAUNCH §6b. Cái máy làm được: ép khai NIỀM TIN bị
        # bác và CHỖ kiểm được niềm tin đó. Và chính chỗ đó loại ca ENA một cách cơ học —
        # không tồn tại màn hình nào hiển thị ENA là "đã đốt", nên `o_dau` không điền nổi.
        kc = f.get("khoang_cach")
        if not isinstance(kc, dict):
            raise LoiCong(
                f"{o} ({fid}) thiếu 'khoang_cach' — Fact phải PHÂN BIỆT đối tượng khỏi "
                f"mặc định của lớp nó. Khai dạng object: "
                f"{{\"tin\": <niềm tin/nguồn nói ngược lại>, \"o_dau\": <chỗ kiểm được>}}. "
                f"Điền không nổi ⇒ fact này không có khoảng cách ⇒ đừng đăng")
        for k, ten in (("tin", "niềm tin bị bác"), ("o_dau", "chỗ kiểm được niềm tin đó")):
            if not str(kc.get(k, "")).strip():
                raise LoiCong(f"{o} ({fid}) 'khoang_cach.{k}' trống — thiếu {ten}")
        for k in ("cau", "so", "chan"):
            cong_ngon_ngu(str(f[k]), f"{o}.{k}")
            cong_ngoi_xung(str(f[k]), f"{o}.{k}")
        for k in ("tin", "o_dau"):
            cong_ngon_ngu(str(kc[k]), f"{o}.khoang_cach.{k}")
            cong_ngoi_xung(str(kc[k]), f"{o}.khoang_cach.{k}")
        # ── KHUÔN v2 — brief §0b chốt 02/08/2026, áp từ Fact 03/08 trở đi ────────
        # Vì sao có: ba Fact đầu phình 2.364 → 4.175 ký tự (Fact 3 DÀI HƠN bài dài
        # #8) mà 12/12 cổng đều PASS — không cổng nào đếm độ dài hay số câu chặn
        # của một Fact. Ranh giới "câu chặn không nhét vừa ⇒ bài dài" sống trong
        # văn xuôi từ 31/07 và không nổ. Chuẩn v2: người đầu tư chứng khoán đọc
        # được thân bài; tầng kỹ thuật nằm ở reply + trường `lenh` của trang này.
        # 🔴 Fact `ngay` ≤ 02/08 giữ luật cũ — ĐÃ ĐĂNG, sửa là đính chính công khai.
        if str(f.get("ngay", "")) >= "2026-08-03":
            if len(str(f["cau"])) > 600:
                raise LoiCong(f"{o} ({fid}) khuôn v2: 'cau' {len(str(f['cau'])):,} ký tự "
                              f"> trần 600 — không nén nổi thì nó là BÀI DÀI, không phải Fact")
            if len(str(f["so"])) > 200:
                raise LoiCong(f"{o} ({fid}) khuôn v2: 'so' {len(str(f['so'])):,} ký tự > 200 "
                              f"— Fact chở MỘT con số chính, không chở chuỗi mốc + tỉ lệ")
            chan = str(f["chan"]).strip()
            if chan.upper() != "KHÔNG CÓ":
                n_cau = len(re.findall(r"[.!?…](?=\s|$)", chan))
                if n_cau > 1:
                    raise LoiCong(f"{o} ({fid}) khuôn v2: 'chan' có {n_cau} câu > 1 — cần "
                                  f"từ 2 câu chặn trở lên thì đây không phải Fact, xếp bài dài")
            # 🔵 `getattr` chứ không import thẳng: nhánh dự phòng ở trên có thể nạp một
            # bản `check_language.py` cũ chưa có tập này, và khi đó hành xử phải như CŨ
            # (chặn cứng mọi nhãn) — thiếu tập không được biến thành "bỏ qua hết".
            khau_vi = getattr(lang, "FACT_KY_THUAT_KHAU_VI", frozenset())
            for k in ("cau", "chan"):
                for re_, ten in lang.FACT_KY_THUAT:
                    # 🔴 Số block hạ xuống KHẨU-VỊ 10/08 (user chốt, `LAUNCH.md §6f`):
                    # bản X đã đăng 07/08 mang `block 29.946.913` trong thân post, đủ bốn
                    # mặt, không ai phản ứng — và nó là tem nhận diện của kênh (`§1`).
                    # Không hạ ở đây thì một Fact qua được `export_post` sẽ RỚT lúc build
                    # web, tức hai cổng cùng khuôn v2 mà phán ngược nhau.
                    if ten in khau_vi:
                        continue
                    m = re_.search(str(f[k]))
                    if m:
                        raise LoiCong(f"{o} ({fid}) khuôn v2: '{k}' dính {ten}: "
                                      f"{m.group(0)!r} — tầng kỹ thuật nằm ở 'lenh' và "
                                      f"reply, thân bài phải đọc được bởi người đầu tư "
                                      f"chứng khoán chưa chạm crypto")


_FACT_REPLY_WEB = re.compile(
    r"^(?:Bằng chứng và cách tự kiểm|Cách tự kiểm riêng con số này):\s*"
    r"ở reply ngay dưới\.?$", re.I)


def cau_fact_web(f: dict) -> str:
    """Thích nghi thân Fact từ bài đăng X sang trang web, không đổi dữ kiện.

    `cau` là bản đã đăng và có thể còn mang câu dẫn sang reply. Trên web, lệnh tự
    kiểm nằm ngay cuối thẻ nên câu dẫn đó sai ngữ cảnh. Nếu một đoạn thân bài trùng
    nguyên văn `chan`, ô giới hạn bên dưới đã đảm nhiệm đúng vai trò của nó.
    """
    chan = str(f["chan"]).strip()
    doan = [x.strip() for x in str(f["cau"]).split("\n\n") if x.strip()]
    return "\n\n".join(x for x in doan if x != chan and not _FACT_REPLY_WEB.fullmatch(x))


def cong_facts_web(html: str, fs: list) -> None:
    """Cổng ⑪b — bản web không được mang chỉ dẫn của thread hoặc lặp ô giới hạn."""
    if "reply ngay dưới" in html.lower():
        raise LoiCong("Fact web còn trỏ người đọc tới 'reply ngay dưới' — web không có reply")
    for f in fs:
        chan = str(f["chan"]).strip()
        if chan.upper() == "KHÔNG CÓ":
            continue
        fid = ihtml.escape(str(f["id"]))
        moc = f'id="{fid}">'
        bat = html.find(moc)
        if bat < 0:
            raise LoiCong(f"Fact web thiếu article cho id '{f['id']}'")
        het = html.find("</article>", bat)
        if het < 0:
            raise LoiCong(f"Fact web không đóng article cho id '{f['id']}'")
        if html[bat:het].count(ihtml.escape(chan)) != 1:
            raise LoiCong(
                f"Fact web '{f['id']}' lặp nguyên văn phần 'Fact này KHÔNG nói' trong thân bài")


def trang_facts(fs: list) -> str:
    """Trang `/facts/` — KHUÔN RIÊNG, không mượn khuôn claim.

    🔴 Vòng port 06/08 để trang này chạy khuôn claim chung và user bác ngay: một Fact
    không có trạng thái, không có nhật ký, không có điều-bác-bỏ — nó có MỘT CON SỐ.
    Khuôn claim xếp con số đó thành dòng thứ hai trong một chồng dòng nhãn giống nhau,
    tức là giấu đúng thứ duy nhất đáng nhìn. Ở đây con số đứng riêng một panel, đủ lớn
    để chụp màn hình dán đi mà vẫn đọc được nguồn.

    Panel số lấy từ `card` trong facts.json — cùng nguồn với card đăng trên kênh, nên
    số trên web và số trên ảnh không thể trôi lệch nhau.
    """
    co = sorted(fs, key=lambda f: str(f.get("ngay", "")), reverse=True)
    # 🔵 v3 giữ nguyên dữ kiện của Fact và chỉ thích nghi hai dấu vết thuộc KÊNH X khi
    # đưa lên web: bỏ câu trỏ tới "reply ngay dưới", và không lặp lại trong thân bài
    # một đoạn đã được đặt riêng ở ô "Fact này KHÔNG nói". `cong_facts_web` khóa đúng
    # hai ranh giới này; số, block, lệnh và câu chặn vẫn có một chủ duy nhất là JSON.
    v3 = BO_CUC == "v3"
    hang, nhay = [], []
    for i, f in enumerate(co, 1):
        stt = f"{i:02d}"
        card = f.get("card") or {}
        ng = str(f.get("ngay", "")).strip()
        kicker = str(card.get("kicker") or f.get("doi_tuong") or "FACT").strip()
        figure = str(card.get("figure") or "").strip()
        label = str(card.get("label") or "").strip()
        chan = str(f["chan"]).strip()
        cau_web = cau_fact_web(f)
        kc = f["khoang_cach"]
        dau = f'{ihtml.escape(kicker)}{" · " + vn_ngay(ng) if ng else ""}'
        # Fact chưa có card thì KHÔNG dựng panel rỗng — panel rỗng là một ô trống to
        # giữa trang, tệ hơn hẳn một khối chữ đủ bề ngang.
        # 🔵 `data-figure-size` ở ngưỡng 13 ký tự: `v3.css` hạ cỡ chữ cho số dài để nó
        # không tràn panel. Ngưỡng lấy nguyên từ bản codex, không tự đặt lại.
        moc_fig = (f' data-ghost="{stt}" data-figure-size='
                   f'"{"long" if len(figure) >= 13 else "standard"}"') if v3 else ""
        fig = (f'<div class="f-fig"{moc_fig}><span class="f-kicker">{dau}</span>'
               f'<span class="f-num">{ihtml.escape(figure)}</span>'
               + (f'<span class="f-lab">{ihtml.escape(label)}</span>' if label else "")
               + '</div>') if figure else ""
        o_chan = ("" if chan.upper() == "KHÔNG CÓ" else
                  f'<div class="f-box chan"><span class="k">Fact này KHÔNG nói</span>'
                  f'<span class="v">{ihtml.escape(chan)}</span></div>')
        p_ng = (f'<p class="tro">{ihtml.escape(str(f["nguon"]))}</p>'
                if str(f.get("nguon", "")).strip() else "")
        if v3:
            # Tên giao thức trên nút nhảy = phần trước dấu · của kicker (bỏ ngày).
            ten_gt = kicker.split("·", 1)[0].strip()
            nhay.append(f'<a href="#{ihtml.escape(str(f["id"]))}" data-fact-link>'
                        f'<span class="fact-switch-no">{stt}</span>'
                        f'<span class="fact-switch-copy"><b>{ihtml.escape(ten_gt)}</b>'
                        f'<small>{ihtml.escape(figure)}</small></span></a>')
        bang = (f'\n  <span class="fact-index" aria-hidden="true">{stt}</span>'
                f'\n  <div class="fact-ribbon" aria-hidden="true"><b>FACT {stt}</b>'
                f'<span>NUMBER</span><i></i><span>CONTEXT</span><i></i>'
                f'<span>BOUNDARY</span><i></i><span>PROOF</span></div>') if v3 else ""
        # 🔵 THỨ TỰ THUỘC TÍNH giữ đúng bản codex (`data-fact` trước `id`) dù trình
        # duyệt không phân biệt. Lý do không phải thẩm mỹ: phép nghiệm thu của lượt
        # này là DIFF TỪNG BYTE thẻ máy sinh với thẻ codex. Thứ tự lệch làm mọi thẻ
        # báo "khác", và một phép so luôn đỏ thì lần sau không ai đọc nó nữa.
        moc_bai = f' data-fact data-fact-index="{stt}"' if v3 else ""
        hang.append(f"""<article class="fact{' fact-wow' if v3 else ''}"{moc_bai} \
id="{ihtml.escape(str(f['id']))}">{bang}
  <div class="f-top{' co-fig' if fig else ' mot-cot'}">
    {fig}
    <div class="f-body">
      {'' if fig else f'<p class="f-kicker">{dau}</p>'}
      <p class="f-cau">{ihtml.escape(cau_web)}</p>
      <p class="f-so">{ihtml.escape(str(f['so']))}</p>
      <div class="f-grid">
        <div class="f-box vi"><span class="k">Vì sao đáng quan tâm</span>
          <span class="v">Điều thường được tin: <i>“{ihtml.escape(str(kc['tin']))}”</i>.
          Chỗ kiểm được: {ihtml.escape(str(kc['o_dau']))}</span></div>
        {o_chan}
      </div>
      {p_ng}
    </div>
  </div>
  <div class="f-foot"><span class="lb">Đọc tại</span>
    <span class="blk">{ihtml.escape(str(f['block']))}</span></div>
  <details class="lenh"><summary>▸ lệnh tự kiểm — dán vào terminal là chạy</summary>
    <pre class="cmd">{ihtml.escape(str(f['lenh']))}</pre></details>
</article>""")
    if not v3:
        return (f'<h1>Một con số, một block, một lệnh để bạn tự kiểm</h1>'
                f'<div class="dem"><span class="to">{len(co)}</span> fact · mới nhất trước</div>'
                f'<p class="dan">Fact ngắn hơn bài: không lập luận dài, chỉ một phép đo đứng '
                f'một mình. Mỗi mục ghi rõ <b>đo tại block nào</b>, <b>lệnh nào đọc lại được</b>, '
                f'và — quan trọng không kém — <b>nó KHÔNG nói điều gì</b>. Cái nào cần giải thích '
                f'dài hơn một dòng thì nó là một bài.</p>'
                f'<section class="so">{"".join(hang)}</section>')
    # ── v3: evidence runway ──────────────────────────────────────────────────────
    # 🔴 MỌI CON SỐ ĐẾM ĐỀU SINH TỪ `len(co)`. Bản codex ghi cứng "06" ở ba chỗ và
    # "Sáu fact" ở aria-label — đúng lúc có Fact thứ bảy thì trang nói dối ở bốn chỗ
    # cùng lúc, và không cổng nào bắt được vì chúng là chữ chứ không phải claim.
    tong = f"{len(co):02d}"
    return (f'''<section class="hero facts-hero">
    <p class="eyebrow">Facts <span class="im">proof by reproduction</span></p>
    <h1 class="display">Con số chỉ đáng tin khi nó để lại <span class="nhan-manh">đường về.</span></h1>
    <span class="ghost-num" aria-hidden="true">{tong}</span>
    <span class="hero-code">PUBLIC EVIDENCE · BLOCKPINNED</span>
    <p class="subline">Không cần tin một đoạn phân tích dài. Mỗi fact đứng trên ba chân: \
<strong>con số</strong>, trạng thái tại <strong>một block</strong>, và <strong>một lệnh</strong> để đọc lại.</p>

    <div class="fact-protocol" aria-label="Cấu trúc của một fact">
      <div class="fact-protocol-line" aria-hidden="true"><i></i></div>
      <article><span>01</span><b>Con số</b><small>thứ đang được khẳng định</small></article>
      <i class="fact-arrow" aria-hidden="true">→</i>
      <article><span>02</span><b>Block</b><small>trạng thái được ghim lại</small></article>
      <i class="fact-arrow" aria-hidden="true">→</i>
      <article><span>03</span><b>Lệnh</b><small>đường tự đọc lại dữ liệu</small></article>
      <div class="fact-protocol-total"><strong>{tong}</strong><span>FACT<br>MỚI NHẤT TRƯỚC</span></div>
    </div>
  </section>

  <nav class="fact-switcher" aria-label="Đi nhanh tới từng fact">
    <span class="fact-switch-label">Đi tới<br>phép đo</span>
    {"".join(nhay)}
  </nav>

  <section class="facts-ledger" aria-label="{len(co)} fact có thể tự kiểm">
    <div class="facts-ledger-head">
      <div><p class="section-code">EVIDENCE LEDGER · {tong} ENTRIES</p><h2>Sổ phép đo</h2></div>
      <p>Mỗi mục đi từ con số xuống đến giới hạn của chính nó. Lệnh tự kiểm nằm ở cuối.</p>
    </div>
    {"".join(hang)}
  </section>''')


def trang_ghi_truoc(moi: list) -> str:
    """Trang riêng: mọi lần desk ghi trước một con số hoặc một ngưỡng, và kết quả.

    Đây là thứ khó làm giả nhất mà desk có: một con số dán công khai TRƯỚC khi biết đáp án.
    Điều kiện để bảng có nghĩa là nó chở CẢ ba trạng thái — thắng, đổ, và đang chờ. Bảng
    chỉ chở lần đúng thì nói về tác giả bảng, không nói về đối tượng.

    🔴 Bố cục HAI CỘT có việc, không phải trang trí: ghi trước ở trái, kết quả ở phải,
    mũi tên ở giữa. Xếp dọc thành một chồng dòng nhãn giống nhau (bản 06/08 trước khi
    user bác) thì mất đúng thứ trang này bán — người đọc phải NHÌN THẤY hai đầu của
    một lời hứa, mới thấy được khoảng cách giữa chúng.
    """
    co = sorted(((c["ghi_truoc"]["ngay"], s, t, c) for s, t, c in moi if c.get("ghi_truoc")),
                key=lambda x: x[0], reverse=True)
    xong = [x for x in co if x[3]["status"] != "ĐANG ĐỨNG"]
    cho = [x for x in co if x[3]["status"] == "ĐANG ĐỨNG"]
    hang = []
    for ngay, sl, tieu, c in co:
        g, cls = c["ghi_truoc"], TRANG_THAI[c["status"]][0]
        dang = c["status"] != "ĐANG ĐỨNG"
        ngay_sau = (vn_ngay(g["ngay_ket"]) if dang else
                    (f'hạn {vn_ngay(c["han"])}' if c.get("han") else "chưa có hạn"))
        cot_sau = (
            f'<div class="col sau"><span class="k">Kết quả</span>'
            f'<span class="ngay">{ngay_sau}</span>'
            f'<span class="txt">{ihtml.escape(g["ket_qua"])}</span>'
            f'<span class="noi">ai phán định: {ihtml.escape(g["ai_phan_dinh"])}</span></div>'
            if dang else
            f'<div class="col sau"><span class="k">Chưa tới ngày</span>'
            f'<span class="ngay">{ngay_sau}</span>'
            f'<span class="txt">Dòng này nằm đây từ trước khi biết đáp án. Tới hạn thì nó '
            f'có kết quả, dù kết quả là tôi sai.</span></div>')
        # v3: thêm móc treo cho bộ lọc + số thứ tự. Thứ tự class và thứ tự thuộc tính
        # giữ ĐÚNG bản codex (`tr track-entry {cls}`) để phép so byte còn dùng được.
        stt = f"{len(hang) + 1:02d}"
        mo_tr = (f'<article class="tr track-entry {cls}" id="track-{stt}" data-track '
                 f'data-track-state="{cls}" data-track-index="{stt}">'
                 f'<span class="track-index" aria-hidden="true">{stt}</span>'
                 if BO_CUC == "v3" else f'<article class="tr {cls}">')
        hang.append(f"""{mo_tr}
  <div class="tr-head"><span class="chip {cls}">{c['status'] if dang else 'ĐANG CHỜ'}</span>
    <span class="moc">{vn_ngay(ngay)} → {ngay_sau}</span></div>
  <div class="tr-body">
    <div class="col truoc"><span class="k">Tôi ghi trước</span>
      <span class="ngay">{vn_ngay(ngay)}</span>
      <span class="txt">{ihtml.escape(g["so"])}</span>
      <span class="noi">{ihtml.escape(g["noi"])}</span></div>
    <div class="mui">→</div>
    {cot_sau}
  </div>
  <div class="tr-foot"><a href="../bai/{sl}/#{c['id']}">{vn_ngay(sl[:10])} · {c['id']} — {ihtml.escape(tieu)}</a></div>
</article>""")
    if BO_CUC != "v3":
        return (f'<h1>Tôi ghi trước, rồi kết quả ra sao</h1>'
                f'<div class="dem"><span class="to">{len(co)}</span> lần ghi trước &nbsp;·&nbsp; '
                f'<b>{len(xong)}</b> đã có kết quả &nbsp;·&nbsp; <b>{len(cho)}</b> đang chờ</div>'
                f'<p class="dan">Mỗi dòng dưới đây là một con số hoặc một ngưỡng tôi dán ra '
                f'<b>trước khi biết đáp án</b>, kèm chỗ đã dán để người khác kiểm được ngày. '
                f'Bảng này chở cả những lần tôi <b>sai</b> và cả những lần <b>chưa có kết quả</b> — '
                f'nếu nó chỉ chở lần đúng thì nó nói về tôi, không nói về đối tượng. Bộ sinh trang '
                f'chặn build nếu một dòng đã được phân định mà thiếu kết quả.</p>'
                f'<section class="so">{"".join(hang)}</section>')

    # ── v3: resolution timeline ──────────────────────────────────────────────────
    # 🔴 ĐẾM THEO CẢ NĂM TRẠNG THÁI, không phải bốn. Bản codex xếp cứng
    # ("xac","song","bac","sua") và BỎ SÓT "cho" (CHỜ SỐ). Hôm nay chưa dòng nào ở
    # trạng thái đó nên không lộ — nhưng ngày có một dòng CHỜ SỐ, nó vẫn hiện trong
    # sổ mà KHÔNG có mặt trong thanh tỷ trọng, tức thanh không khép được với tổng và
    # bộ lọc thiếu một nút. Cùng lớp lỗi với "06" ghi cứng: đúng hôm nay, sai lặng lẽ
    # ngày mai. Trạng thái nào đếm 0 vẫn bị bỏ qua như cũ, nên hôm nay ra y hệt.
    dem = {k: 0 for _, (k, _) in TRANG_THAI.items()}
    for _, _, _, c in co:
        dem[TRANG_THAI[c["status"]][0]] += 1
    thu_tu = [TRANG_THAI[s][0] for s in ("ĐÃ XÁC NHẬN", "ĐANG ĐỨNG", "BỊ BÁC", "ĐÃ SỬA", "CHỜ SỐ")]
    ten_tt = {"xac": "Đã xác nhận", "song": "Đang chờ", "bac": "Đã bị bác bỏ",
              "sua": "Đã sửa", "cho": "Chưa phân định"}
    doan = "".join(f'<i class="{s}" style="--n:{dem[s]}" title="{ten_tt[s]}: {dem[s]}"></i>'
                   for s in thu_tu if dem[s])
    chu_giai = "".join(f'<span><i class="dot {s}"></i><b>{dem[s]}</b> {ten_tt[s]}</span>'
                       for s in thu_tu if dem[s])
    loc = "".join(f'<button type="button" data-track-filter="{s}" aria-pressed="false">'
                  f'<i class="dot {s}"></i>{ten_tt[s]} <b>{dem[s]}</b></button>'
                  for s in thu_tu if dem[s])
    tong = f"{len(co):02d}"
    return (f'''<section class="hero track-hero">
    <p class="eyebrow">Track record <span class="im">prediction → resolution</span></p>
    <h1 class="display">Ghi trước. Để <span class="nhan-manh">kết quả</span> phán quyết.</h1>
    <span class="ghost-num" aria-hidden="true">{tong}</span>
    <span class="hero-code">PUBLIC MEMORY · NO CHERRY-PICKING</span>
    <p class="subline">Mỗi dòng là một con số hoặc một ngưỡng được dán ra \
<strong>trước khi biết đáp án</strong>. Khi kết quả đến, dòng đó vẫn ở lại — dù được xác nhận, \
đã bị bác bỏ hay phải sửa.</p>

    <section class="track-score" aria-label="Tổng quan {len(co)} lần ghi trước">
      <div class="track-total"><span>Tổng sổ</span><strong>{tong}</strong><small>lần ghi trước</small></div>
      <div class="track-distribution">
        <div class="track-distribution-head"><b>Trạng thái phân định</b><span>mới nhất trước</span></div>
        <div class="track-bar">{doan}</div>
        <div class="track-legend">{chu_giai}</div>
      </div>
      <div class="track-rule"><span>01</span><b>Ghi trước</b><i>→</i><span>02</span><b>Chờ dữ liệu</b><i>→</i><span>03</span><b>Giữ nguyên kết quả</b></div>
    </section>
    <p class="track-integrity"><b>Integrity rule</b><span>Sổ giữ cả những lần sai và chưa có kết quả. \
Bộ sinh trang chặn build nếu một dòng đã được phân định mà thiếu kết quả.</span></p>
  </section>

  <nav class="track-filters" aria-label="Lọc Track record theo trạng thái">
    <span>Lọc sổ</span>
    <button type="button" data-track-filter="all" aria-pressed="true">Tất cả <b>{len(co)}</b></button>
    {loc}
  </nav>

  <section class="track-ledger" aria-label="{len(co)} lần ghi trước và kết quả">
    <div class="track-ledger-head"><div><p class="section-code">PUBLIC LEDGER · {tong} ENTRIES</p><h2>Trước và sau</h2></div>
      <p class="track-filter-status" aria-live="polite">Đang hiện {len(co)} dòng</p></div>
    {"".join(hang)}
  </section>''')


def dai_bai(bai_list: list, tien_to: str, them_lop: str = "", *, uu_tien: bool = False,
            tieu_de: str = "Bài", gioi_thieu: str = "", tong_bai: int | None = None,
            xem_tat_ca: str = "") -> str:
    """Preview bài hữu hạn cho v3; dải ngang cũ chỉ còn ở bố cục D2.

    Một khuôn, hai chỗ gọi: hai bản chép của cùng một thẻ là hai bản sẽ trôi lệch, và
    lần trôi đó sẽ lộ ra ở chỗ tệ nhất — thẻ bài, thứ người ta nhìn trước khi bấm.
    `tien_to` là đường về thư mục bài, khác nhau theo độ sâu trang gọi.

    Trang chủ và hồ sơ token KHÔNG phải kho lưu trữ. Chúng chỉ đưa tối đa sáu bài vào
    tầm mắt; `/bai/` mới chịu trách nhiệm tìm, lọc và mở thêm khi số bài lên ba chữ số.
    """
    v3_uu_tien = BO_CUC == "v3" and uu_tien
    tong = len(bai_list) if tong_bai is None else tong_bai
    the = []
    for i, (f, s, n, sg, dm) in enumerate(bai_list, 1):
        lop = "bai bai-lead" if v3_uu_tien and i == 1 else "bai"
        ngay = f'{f["mau"]} {vn_ngay(str(f["date"])[:10])}'
        dau = (f'<span class="bai-top"><span class="d">{ngay}</span>'
               f'<span class="bai-token">{ihtml.escape(f.get("token", ""))}</span></span>'
               if v3_uu_tien else f'<span class="d">{ngay}</span>')
        chan = (f'<span class="bai-foot"><span class="s">{n} claim — {sg}</span>'
                f'<span class="bai-go">Đọc bài <i aria-hidden="true">↗</i></span></span>'
                if v3_uu_tien else f'<span class="s">{n} claim — {sg}</span>')
        the.append(f'<a class="{lop}" href="{tien_to}bai/{s}/">{dau}'
                   f'<span class="t">{ihtml.escape(_tieu_de_h1(f))}</span>'
                   f'{thanh_mini(dm, n)}{chan}</a>')
    # v3 gắn `aria-labelledby="bai"` — khối này CÓ `<h2 id="bai">` bên trong, nên trình
    # đọc màn hình đọc được tên vùng thay vì "section". Lấy từ bản codex. Không gắn cho
    # D2 vì D2 phải trùng từng byte với bản đang phục vụ; đây là nợ nhỏ của D2, ghi ra
    # đây để lượt lật bố cục sau không phải tìm lại.
    nhan = ' aria-labelledby="bai"' if BO_CUC == "v3" else ""
    lop_uu_tien = " article-priority" if v3_uu_tien else ""
    dau_muc = (f'<div class="bai-heading"><p class="section-code">READING DESK · '
               f'{tong} INVESTIGATIONS</p><h2 id="bai">{ihtml.escape(tieu_de)}</h2>'
               f'<p>{ihtml.escape(gioi_thieu)}</p></div>' if v3_uu_tien else
               '<h2 id="bai">Bài viết</h2>')
    if v3_uu_tien:
        den_kho = (f'<a class="bai-archive-link" href="{ihtml.escape(xem_tat_ca, quote=True)}">'
                   f'<span>Xem tất cả</span><b>{tong} bài viết</b><i aria-hidden="true">↗</i></a>'
                   if xem_tat_ca else "")
        return (f'<section class="khu-bai{them_lop}{lop_uu_tien}" data-hien{nhan}>'
                f'<div class="khu-dau">{dau_muc}{den_kho}</div>'
                f'<div class="article-preview-grid">{"".join(the)}</div>'
                f'<p class="article-preview-note">Đang giới thiệu {len(bai_list)} / {tong} bài viết · '
                f'danh mục đầy đủ có tìm kiếm và lọc theo token</p></section>')
    return (f'<section class="khu-bai{them_lop}{lop_uu_tien}" data-hien{nhan}>'
            f'<div class="khu-dau">{dau_muc}'
            f'<div class="dieu-rail">'
            f'<button class="rn" type="button" data-rail="-1" aria-label="Lùi một thẻ">←</button>'
            f'<button class="rn" type="button" data-rail="1" aria-label="Tới một thẻ">→</button>'
            f'</div></div>'
            f'<div class="rail-boc"><div class="rail" id="rail" tabindex="0" role="region" '
            f'aria-label="Danh sách bài — cuộn ngang">{"".join(the)}</div></div>'
            f'<p class="rail-goi">{len(bai_list)} bài · vuốt ngang, hoặc bấm mũi tên</p></section>')


def trang_muc_bai(bai: list) -> str:
    """Kho bài riêng: chịu được 100+ bài mà không biến trang chủ thành một dải vô tận."""
    if BO_CUC != "v3":
        return (f'<h1>Tất cả bài viết</h1><p class="dan">{len(bai)} bài viết, mới nhất trước.</p>'
                + dai_bai(bai, "../"))

    dem_token: dict[str, int] = {}
    for f, _, _, _, _ in bai:
        ma = f.get("token", "").strip()
        dem_token[ma] = dem_token.get(ma, 0) + 1
    nut_token = "".join(
        f'<button type="button" id="token-{ihtml.escape(ma.lower(), quote=True)}" data-article-filter="{ihtml.escape(ma.lower(), quote=True)}" '
        f'aria-pressed="false">{ihtml.escape(ma)} <b>{n}</b></button>'
        for ma, n in sorted(dem_token.items(), key=lambda x: (-x[1], x[0])))

    the = []
    tong_claim = 0
    for i, (f, s, n, sg, dm) in enumerate(bai, 1):
        tong_claim += n
        ma = f.get("token", "").strip()
        ngay = vn_ngay(str(f["date"])[:10])
        # 🔴 Chỉ mục tìm giữ NGUYÊN `title` đầy đủ, dù thẻ hiện dòng ngắn. Người đọc gõ
        # chữ chỉ có trong câu dài thì vẫn phải ra bài. Bỏ vế này là tái tạo đúng lỗi ô
        # tìm claim vá hôm 11/08: chuỗi tìm và chuỗi bị tìm khác nhau, không cổng nào thấy.
        tim = ihtml.escape(f'{f["title"]} {_tieu_de_h1(f)} {ma} {ngay} {sg}', quote=True)
        if ihtml.escape(f["title"], quote=True) not in tim:
            raise LoiCong(
                f"chỉ mục tìm của kho bài mất TIÊU ĐỀ ĐẦY ĐỦ của {s} — thẻ hiện dòng "
                f"ngắn, nên đây là chỗ duy nhất còn giữ câu dài cho ô tìm. Mất nó thì "
                f"gõ đúng chữ trong tiêu đề vẫn ra 0 kết quả, và không mặt nào báo lỗi")
        the.append(f'''<a class="article-archive-card" href="{s}/" data-article-card
  data-article-token="{ihtml.escape(ma.lower(), quote=True)}" data-article-text="{tim}">
  <span class="article-archive-no">{i:02d}</span>
  <span class="article-archive-meta"><b>{ihtml.escape(ma)}</b>{ihtml.escape(f["mau"])} {ngay}</span>
  <strong>{ihtml.escape(_tieu_de_h1(f))}</strong>
  {thanh_mini(dm, n)}
  <span class="article-archive-foot"><small>{n} claim · {ihtml.escape(sg)}</small><i aria-hidden="true">↗</i></span>
</a>''')

    con_lai = max(0, len(bai) - 12)
    nhan_mo_them = (f"Mở thêm {min(12, con_lai)} bài viết ↓"
                    if con_lai else "Mở thêm bài viết ↓")
    an_mo_them = " hidden" if not con_lai else ""

    return f'''<section class="hero article-archive-hero">
  <span class="ghost-num" aria-hidden="true">{len(bai)}</span>
  <span class="hero-code" aria-hidden="true">PUBLIC INVESTIGATION ARCHIVE</span>
  <p class="eyebrow"><span>Kho bài viết</span><span class="im">mới nhất trước</span></p>
  <h1 class="display">Toàn bộ bài đã công bố, <span class="nhan-manh">kèm trạng thái hôm nay.</span></h1>
  <p class="subline">Tìm theo tiêu đề, token hoặc ngày công bố. Mỗi bài dẫn từ câu hỏi ban đầu đến số đo, nguồn và những gì có thể làm kết luận thay đổi.</p>
  <div class="article-archive-stats"><span><b>{len(bai)}</b> bài viết</span><span><b>{tong_claim}</b> claim</span><span><b>{len(dem_token)}</b> token</span></div>
</section>
<section class="article-archive" aria-labelledby="article-archive-title">
  <header class="article-archive-head"><div><p class="section-code">READING DESK · FULL INDEX</p><h2 id="article-archive-title">Tất cả bài viết</h2></div><p data-article-status aria-live="polite">Đang hiện {len(bai)} bài viết</p></header>
  <div class="article-archive-tools">
    <label class="article-archive-search"><span>Tìm bài viết</span><input type="search" data-article-search placeholder="Tiêu đề, token, ngày…" autocomplete="off"><kbd>/</kbd></label>
    <nav class="article-archive-filters" aria-label="Lọc bài theo token">
      <button type="button" data-article-filter="all" aria-pressed="true">Tất cả <b>{len(bai)}</b></button>{nut_token}
    </nav>
  </div>
  <div class="article-archive-grid">{"".join(the)}</div>
  <p class="article-archive-empty" data-article-empty hidden>Không có bài viết khớp từ khoá và token này.</p>
  <div class="article-archive-more"><button type="button" data-article-more{an_mo_them}>{nhan_mo_them}</button></div>
</section>'''


def trang_token(ma: str, bai_t: list, claims_t: list) -> str:
    """TỦ KÍNH một token: mọi khẳng định đã đăng về nó, gom về một trang.

    Vì sao trang này tồn tại: bài sống theo NGÀY, hồ sơ sống theo ĐỐI TƯỢNG. Người
    đang cân nhắc Uniswap không đọc theo ngày đăng — câu họ hỏi là *"kênh này đã đo
    được gì về nó, và những câu đó giờ còn đứng không"*. Trang chủ trả lời câu đó cho
    cả kênh; trang này trả lời cho một token, và đó là dạng hồ sơ gửi ra ngoài được.

    🔴 KHÔNG khai một luật "Đo lại" cho cả trang. Bản mockup 05/08 chốt *"trang token
    KHÔNG có nút Đo lại"*, lý lẽ là bảy con số của UNI đều cộng dồn trên một khoảng
    block chứ không phải một lời gọi tại một block. Lý lẽ đó đúng, nhưng đếm trên dữ
    liệu thật thì **1 trong 19** khẳng định UNI có khai `do_lai` chạy được — nên phát
    biểu theo cả cụm sẽ sai với đúng một dòng, và dòng đó là dòng mạnh nhất. Trang
    này vì thế không hứa gì theo cụm: mỗi dòng in đúng cái nó có — nút ở dòng gọi lại
    được, lý do ở dòng đã khai vì sao không, đường dựng lại ở mọi dòng còn lại.
    """
    ten = TOKEN_TEN[ma]
    d_num = {k: sum(1 for _, _, c in claims_t if c["status"] == k) for k in TRANG_THAI}
    doi = sum(n for k, n in d_num.items() if k != "ĐANG ĐỨNG")
    n_do = sum(1 for _, _, c in claims_t if c.get("do_lai"))
    n_kd = sum(1 for _, _, c in claims_t if c.get("khong_do_lai"))
    con = len(claims_t) - n_do - n_kd

    # v3 bồi móc treo cho tủ bằng chứng (tìm cục bộ · lọc · mở-thu hàng loạt). Thuộc
    # tính CŨ `data-st`/`data-doi` GIỮ NGUYÊN chứ không thay: bỏ chúng là bẻ luôn bộ
    # lọc của D2, mà hai bố cục phải cùng chạy được từ MỘT bộ sinh.
    _v3 = BO_CUC == "v3"
    _lop = lambda c: TRANG_THAI[c["status"]][0]
    _doi = lambda c: 0 if c["status"] == "ĐANG ĐỨNG" else 1
    hang = "".join(
        (f'<li class="tt uni-claim {_lop(c)}" id="uni-claim-{i:02d}" data-uni-claim '
         f'data-uni-state="{_lop(c)}" data-uni-changed="{_doi(c)}" '
         f'data-uni-index="{i:02d}" data-st="{_lop(c)}" data-doi="{_doi(c)}">'
         f'<span class="uni-claim-index" aria-hidden="true">{i:02d}</span>' if _v3 else
         f'<li class="tt {_lop(c)}" data-st="{_lop(c)}" data-doi="{_doi(c)}">')
        # 🔴 Hộp lưới nằm trong một <span> BÊN TRONG <summary>, không phải trên chính
        # PHẢI có dấu + ở đây: nối chuỗi ngầm không chạy sau một biểu thức trong ngoặc.
        +
        # <summary>. Đo 06/08 trên Chrome: đặt `display:grid` thẳng lên summary thì
        # phần đang ĐÓNG của <details> vẫn được dựng và nằm luôn trong hộp summary —
        # mỗi dòng cao 720px thay vì 161px, cả trang 15.652px. Trình duyệt không báo
        # gì; lộ ra ở ảnh chụp khổ điện thoại của cổng preview.
        f'<details class="tu-so"><summary><span class="tt-hop">'
        f'<span class="chip {TRANG_THAI[c["status"]][0]}">{TRANG_THAI_HIEN_THI[c["status"]]}</span>'
        f'<span class="tx">{ihtml.escape(c["text"])}</span>'
        f'<span class="mt">{vn_ngay(s[:10])} · {c["id"]} · {ihtml.escape(tieu)}</span>'
        f'<span class="mui" aria-hidden="true">▾</span>'
        f'</span></summary><div class="tu-mo">'
        f'<p class="dong"><span class="nhan">GHIM TẠI</span>{ihtml.escape(c["ghim"])}</p>'
        f'<p class="dong bac"><span class="nhan">ĐIỀU GÌ BÁC BỎ CLAIM NÀY</span>'
        f'{ihtml.escape(c["falsifier"])}</p>'
        f'{khoi_do_lai(c)}'
        f'<p class="tro"><a href="../../bai/{s}/#{c["id"]}">Mở dòng này trong bài →</a></p>'
        f'</div></details></li>'
        for i, (s, tieu, c) in enumerate(claims_t, 1))

    tu_kiem = (f'<b>{n_do}</b> dòng gọi lại được bằng đúng một lệnh — mở dòng đó ra là có '
               f'nút bấm, và nó đọc chain thật ngay lúc bạn bấm. ')
    if n_kd:
        tu_kiem += (f'<b>{n_kd}</b> dòng khai sẵn vì sao trình duyệt không gọi lại được. ')
    tu_kiem += (f'{con} dòng còn lại là phép quét trên một khoảng block: cách dựng lại nằm '
                f'ngay trong ô ĐIỀU GÌ BÁC BỎ của chính dòng đó — mở ra là thấy.')

    if _v3:
        # ── v3: evidence vault ───────────────────────────────────────────────────
        # 🔴 KHÔNG một con số nào ở đây được gõ tay. Bản codex ghi cứng 24 · 5 · 7 ·
        # "1/17/4/2" · "01/07/16" — mười một con số, ở tám chỗ. Chúng đều đã có sẵn
        # dưới dạng biến trong chính hàm này (`len(claims_t)` · `len(bai_t)` · `doi`
        # · `d_num` · `n_do`/`n_kd`/`con`), nên dán cứng là tự chọn phiên bản sẽ nói
        # dối. Đo đối chiếu 10/08: cả mười một con số suy ra TRÙNG KHÍT bản codex.
        ten_tt = {"xac": "Đã xác nhận", "song": "Vẫn đứng vững", "sua": "Đã sửa", "bac": "Đã bị bác bỏ"}
        thu_tu = ["ĐÃ XÁC NHẬN", "ĐANG ĐỨNG", "ĐÃ SỬA", "BỊ BÁC"]
        thanh = "".join(f'<i class="{TRANG_THAI[k][0]}" style="--n:{d_num[k]}"></i>'
                        for k in thu_tu)
        chu_giai = "".join(f'<span><i class="uni-dot {TRANG_THAI[k][0]}"></i>'
                           f'<b>{d_num[k]}</b>{ten_tt[TRANG_THAI[k][0]]}</span>' for k in thu_tu)
        loc = "".join(f'<button type="button" data-uni-filter="{TRANG_THAI[k][0]}" '
                      f'aria-pressed="false"><i class="uni-dot {TRANG_THAI[k][0]}"></i>'
                      f'{ten_tt[TRANG_THAI[k][0]]} <b>{d_num[k]}</b></button>' for k in thu_tu)
        n = len(claims_t)
        khoi_bai = dai_bai(
            bai_t[:6], "../../", " uni-articles", uu_tien=True,
            tieu_de=f"Bài điều tra về {ma}",
            gioi_thieu="Bắt đầu từ bài gốc để thấy câu hỏi, đường đo và giới hạn trước khi mở từng claim.",
            tong_bai=len(bai_t), xem_tat_ca=f"../../bai/#token-{ma.lower()}")
        return (f'''<section class="hero uni-hero">
    <p class="eyebrow">Hồ sơ token · {ma} <span class="im">cập nhật theo bằng chứng</span></p>
    <div class="uni-hero-grid">
      <div class="uni-hero-copy">
        <div class="uni-title-lockup">
          <img src="../../anh/token-{ma.lower()}.png" width="84" height="84" alt="Logo {ten}">
          <div><span>{ten}</span><h1 class="display">{ma},<em class="cum-tieu-de">qua từng lần kiểm chứng.</em></h1></div>
        </div>
        <p class="subline">Các khẳng định BlockPinned đã công bố về {ma} được tập hợp tại đây — \
kèm mốc đo, nguồn, điều có thể làm kết luận thay đổi và trạng thái hiện tại.</p>
        <a class="uni-hero-jump" href="#bai"><span>Đọc bài viết về {ma}</span><b>{len(bai_t)} bài viết</b><i aria-hidden="true">↓</i></a>
      </div>

      <section class="uni-vault" data-spotlight aria-label="Tổng quan hồ sơ {ma}">
        <div class="uni-vault-total">
          <div class="uni-ring" aria-hidden="true"><span><b>{n}</b><small>CLAIM</small></span></div>
          <div><span class="section-code">EVIDENCE FILE · {ma}</span><strong>{len(bai_t)} bài điều tra</strong>\
<small>{doi} claim đã đổi trạng thái</small></div>
        </div>
        <div class="uni-vault-state">
          <div class="uni-vault-head"><b>Trạng thái hiện tại</b><span>đủ {n} / {n}</span></div>
          <div class="uni-status-bar" aria-hidden="true">{thanh}</div>
          <div class="uni-legend">{chu_giai}</div>
        </div>
        <p class="uni-vault-rule"><b>Audit rule</b><span>Sửa trạng thái, không xoá lịch sử.</span>\
<i aria-hidden="true">→</i><span>Mở từng claim để thấy chính xác điều gì có thể bác bỏ nó.</span></p>
      </section>
    </div>
  </section>

  {khoi_bai}

  <section class="uni-coverage" aria-labelledby="uni-coverage-title">
    <div class="uni-coverage-copy"><p class="section-code">REPRODUCTION COVERAGE</p>\
<h2 id="uni-coverage-title">Biết ngay phép đo nào mở được ở đâu.</h2></div>
    <article><strong>{n_do:02d}</strong><span>Gọi lại trực tiếp</span><small>từ trình duyệt</small></article>
    <article><strong>{n_kd:02d}</strong><span>Nêu rõ giới hạn</span><small>vì sao trình duyệt không gọi lại</small></article>
    <article><strong>{con:02d}</strong><span>Quét theo dải</span><small>dựng lại bằng chỉ dẫn trong claim</small></article>
  </section>

  <section class="uni-evidence" aria-labelledby="uni-ledger-title">
    <div class="uni-ledger-head">
      <div><p class="section-code">PUBLIC CLAIM LEDGER · {n} ENTRIES</p><h2 id="uni-ledger-title">Tủ claim {ma}</h2></div>
      <p class="uni-filter-status" aria-live="polite">Đang hiện {n} claim</p>
    </div>

    <div class="uni-tools">
      <label class="uni-search"><span>Tìm trong hồ sơ</span>\
<input type="search" data-uni-search placeholder="Claim, bài, block, địa chỉ…" autocomplete="off"><kbd>/</kbd></label>
      <nav class="uni-filters" aria-label="Lọc claim {ma}">
        <button type="button" data-uni-filter="all" aria-pressed="true">Tất cả <b>{n}</b></button>
        {loc}
        <button type="button" data-uni-filter="changed" aria-pressed="false">\
<i class="uni-change-mark"></i>Đã đổi <b>{doi}</b></button>
      </nav>
      <div class="uni-open-tools"><button type="button" data-uni-open="all">Mở tất cả</button>\
<button type="button" data-uni-open="none">Thu gọn</button></div>
    </div>

    <ol class="tt-ds tu-ds uni-claims" id="tt-ds">
      {hang}
    </ol>
    <p class="uni-empty" data-uni-empty hidden>Không có claim khớp bộ lọc này.</p>
  </section>''')

    return (f'<p class="crumb">Tủ kính token · {ma}</p>'
            f'<h1>{ten} — mọi con số kênh này đã ghim, và câu nào còn đứng</h1>'
            f'<p class="dan">Bài sống theo ngày; hồ sơ sống theo đối tượng. Trang này gom mọi '
            f'khẳng định đã đăng về {ten} về một chỗ, giữ nguyên trạng thái hiện tại của từng '
            f'câu — kể cả những câu đã bị bác bỏ. Bấm một dòng để mở block nó được đọc ra và điều gì '
            f'sẽ bác bỏ nó.</p>'
            f'<section class="board" data-hien>'
            f'<div class="bh"><b>Hồ sơ {ten}</b>'
            f'<span>{len(claims_t)} khẳng định · {len(bai_t)} bài</span></div>'
            f'{thanh_xep(d_num, len(claims_t))}'
            f'<div class="dem phu"><b>{doi}</b> trong số đó đã đổi trạng thái kể từ lúc đăng. '
            f'{tu_kiem}</div></section>'
            f'<div class="tt-khu" data-hien>'
            f'<div class="tt-dau"><div class="nhom-loc">'
            f'<button class="lg-loc" type="button" data-loc="het">Cả hồ sơ '
            f'<span class="n">{len(claims_t)}</span></button>'
            f'<button class="lg-loc" type="button" data-loc="doi">Đã đổi trạng thái '
            f'<span class="n">{doi}</span></button></div>'
            f'<span class="lo" id="loc-lo"></span></div>'
            f'<ol class="tt-ds tu-ds" id="tt-ds" data-loc-vung="het">{hang}</ol></div>'
            + dai_bai(bai_t, "../../"))


def trang_du_lieu(kho: pathlib.Path) -> str:
    """Trang `/du-lieu/` — danh sách hiện vật thô, sinh từ HIEN_VAT chứ không quét thư mục.

    Vì sao có trang này: từ 31/07 hiện vật đã được chép lên site, nhưng KHÔNG có mục
    nào dẫn tới chúng — muốn tải phải đoán đúng tên file. Một file nằm trên máy chủ mà
    không có đường vào thì đúng bằng không có.

    Mô tả từng file lấy từ trường `_doc` NGAY TRONG file, không gõ lại ở đây: một dòng
    mô tả chép tay là một dòng sẽ trôi lệch khỏi thứ nó mô tả.
    """
    hang = []
    for ten_f, nhan in HIEN_VAT.items():
        f = kho / ten_f
        try:
            doc = json.loads(f.read_text(encoding="utf-8")).get("_doc", "")
        except (json.JSONDecodeError, OSError, AttributeError):
            doc = ""
        kb = f.stat().st_size / 1024
        hang.append(
            f'<article class="claim">'
            f'<h3><a class="id" href="{ihtml.escape(ten_f)}">{ihtml.escape(ten_f)}</a>'
            f'<span class="moc">{so_vn(kb, 1)} KB · {ihtml.escape(nhan)}</span></h3>'
            + (f'<p class="dong"><span class="nhan">FILE NÀY LÀ GÌ</span>'
               f'{ihtml.escape(str(doc))}</p>' if doc else "")
            + f'<p class="dong"><span class="nhan">TẢI VỀ</span>'
              f'<code>curl -sO {BASE}/du-lieu/{ihtml.escape(ten_f)}</code></p>'
            + '</article>')
    return (f'<h1>Dữ liệu thô đứng sau bài</h1>'
            f'<div class="dem"><span class="to">{len(HIEN_VAT)}</span> file · JSON</div>'
            f'<p class="dan">Tải về, mở ra, đếm lại. Mỗi file mang sẵn một trường '
            f'<code>_doc</code> nói nó là gì và <b>vòng đo nào của nó đã hỏng</b> — một tập '
            f'dữ liệu không kể được chỗ nó từng sai thì không kiểm lại được.</p>'
            f'<section class="so">{"".join(hang)}</section>'
            f'<p class="dan-gt">Không phải bài nào cũng có file ở đây. Một phép đo chỉ sinh '
            f'file thô khi nó là phép <b>quét</b> — nghìn lượt log, nhiều vòng đối chứng. '
            f'Phép đo gọi một hàm tại một block thì đường tự kiểm ngắn hơn file: lệnh gọi in '
            f'ngay trong sổ claim của bài, bấm “Đo lại” là chạy.</p>')


def trang_du_lieu_v3(kho: pathlib.Path) -> str:
    """Kho hiện vật v3: biến mỗi JSON thành một bản ghi kiểm được bằng byte.

    Nội dung mô tả vẫn có một chủ là `_doc` trong file. Tầng trình bày chỉ tính ba
    thuộc tính từ chính byte đang phát hành — kích thước, số trường gốc và SHA-256 —
    nên người tải có thể kiểm mình đang cầm đúng hiện vật mà trang mô tả.
    """
    tep = []
    tong_byte = 0
    for stt, (ten_f, nhan) in enumerate(HIEN_VAT.items(), 1):
        f = kho / ten_f
        raw = f.read_bytes()
        tong_byte += len(raw)
        try:
            obj = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            obj = {}
        doc = str(obj.get("_doc", "")) if isinstance(obj, dict) else ""
        so_truong = len(obj) if isinstance(obj, dict) else 0
        kb = len(raw) / 1024
        bam = hashlib.sha256(raw).hexdigest()
        lenh = f"curl -sO {BASE}/du-lieu/{ten_f}"
        tep.append(f'''<article class="data-file" id="file-{stt:02d}" data-data-file data-file-index="{stt:02d}">
  <header class="data-file-head">
    <span class="data-file-index">FILE {stt:02d}</span>
    <span class="data-file-format">JSON · {so_vn(kb, 1)} KB</span>
    <span class="data-file-actions"></span>
  </header>
  <h2><a href="{ihtml.escape(ten_f, quote=True)}" download>{ihtml.escape(ten_f)}</a></h2>
  <p class="data-file-role">{ihtml.escape(nhan)}</p>
  <div class="data-file-doc"><span>_doc</span><p>{ihtml.escape(doc)}</p></div>
  <dl class="data-file-facts">
    <div><dt>Kích thước</dt><dd>{so_vn(kb, 1)} KB</dd></div>
    <div><dt>Trường gốc</dt><dd>{so_truong}</dd></div>
    <div><dt>Định dạng</dt><dd>JSON</dd></div>
  </dl>
  <div class="data-hash"><span>SHA-256</span><code>{bam}</code>
    <button type="button" data-copy-text="{bam}" data-copy-idle="Sao chép hash">Sao chép hash</button></div>
  <div class="data-download">
    <code>{ihtml.escape(lenh)}</code>
    <button type="button" data-copy-text="{ihtml.escape(lenh, quote=True)}" data-copy-idle="Sao chép lệnh">Sao chép lệnh</button>
    <a href="{ihtml.escape(ten_f, quote=True)}" download>Tải JSON ↓</a>
  </div>
</article>''')

    nav = "".join(
        f'<a href="#file-{i:02d}"><span>{i:02d}</span>{ihtml.escape(ten)}</a>'
        for i, ten in enumerate(HIEN_VAT, 1))
    return f'''<section class="hero data-hero">
  <span class="ghost-num" aria-hidden="true">{len(HIEN_VAT)}</span>
  <span class="hero-code" aria-hidden="true">PUBLIC EVIDENCE ARCHIVE</span>
  <p class="eyebrow"><span>KHO HIỆN VẬT</span><span class="im">JSON · TỰ HOST</span></p>
  <h1 class="display">Dữ liệu thô <span class="nhan-manh">đứng sau bài</span></h1>
  <p class="subline">Tải file gốc, kiểm hash, rồi đếm lại. Trường <code>_doc</code> trong mỗi file nói nó là gì và vòng đo nào của nó đã hỏng.</p>
  <div class="data-protocol">
    <div class="heronum"><p class="l">Hiện vật đang phát hành</p><p class="v">{len(HIEN_VAT)}<em> file</em></p><p class="d">đọc và tải trực tiếp</p></div>
    <div class="data-path" role="img" aria-label="Tuyến kiểm hiện vật: đọc mô tả gốc, đối chiếu SHA-256, tải về đếm lại">
      <div><span>01 · ĐỌC</span><b>_doc</b><small>mô tả nằm trong file</small></div><i>→</i>
      <div><span>02 · ĐỐI CHIẾU</span><b>SHA-256</b><small>hash từ đúng byte phát hành</small></div><i>→</i>
      <div><span>03 · DỰNG LẠI</span><b>curl</b><small>tải về và tự đếm</small></div>
    </div>
  </div>
  <div class="data-stats"><span><b>{so_vn(tong_byte / 1024, 1)} KB</b> tổng dung lượng</span><span><b>{len(HIEN_VAT)}</b> hash công khai</span><span><b>0</b> tài sản ngoài miền</span></div>
</section>
<nav class="data-map" aria-label="Chỉ mục hiện vật"><span>CHỈ MỤC FILE</span>{nav}</nav>
<section class="data-ledger" aria-labelledby="data-ledger-title">
  <header class="data-ledger-head"><div><span>PUBLIC DATA LEDGER</span><h2 id="data-ledger-title">{len(HIEN_VAT)} hiện vật tải được</h2></div><p>Mỗi dòng dưới đây có mô tả gốc, hash và lệnh tải của chính byte đang phục vụ.</p></header>
  {"".join(tep)}
</section>
<aside class="data-note"><span>PHẠM VI</span><p>Không phải bài nào cũng có file ở đây. Phép quét qua nhiều log và nhiều vòng đối chứng mới cần hiện vật thô; phép gọi một hàm tại một block có đường tự kiểm ngắn hơn, nằm ngay trong sổ claim của bài.</p></aside>'''


def thanh_xep(dem: dict, tong: int) -> str:
    """Thanh xếp chồng + chip có SỐ — bảng điểm dùng chung cho trang bài và trang chủ.

    🔴 Bề rộng tính bằng dấu CHẤM: đây là CSS, không phải chữ hiện ra. `so_vn` đổi dấu
    thập phân sang phẩy cho người đọc, và một `width:77,14%` là một luật CSS chết trong
    im lặng — đúng họ lỗi mà cổng ⑥ (thuộc tính số) sinh ra để bắt.

    Mỗi chip mang GLYPH riêng (CSS `.chip::before`) chứ không chỉ mang màu: đo được đỏ
    và xanh lá chỉ cách nhau ΔE 2,7 với người mù màu deutan, nên màu một mình không
    phân biệt nổi năm trạng thái.
    """
    if not tong:
        return ""
    co = [(k, n) for k, n in dem.items() if n]
    # `--i` là số thứ tự để CSS trễ nhịp từng đoạn khi thanh chạy từ 0. Bề rộng vẫn nằm
    # sẵn trong HTML ⇒ tắt JS là thanh đứng yên ở đúng tỉ lệ thật, không phải ở 0.
    seg = "".join(
        f'<span class="seg {TRANG_THAI[k][0]}" style="width:{n / tong * 100:.2f}%;--i:{i}" '
        f'data-loc="{TRANG_THAI[k][0]}" data-tip="{TRANG_THAI_HIEN_THI[k]} · {n}/{tong}"></span>'
        for i, (k, n) in enumerate(co))
    # 🔴 Chip là NÚT, không phải nhãn: nó vừa là chú giải của thanh (bắt buộc — năm
    # trạng thái không phân biệt nổi bằng hue, `NOTES §1`), vừa là bộ lọc của danh sách
    # claim đứng ngay dưới. Tắt JS thì nút không làm gì và chú giải vẫn đọc đủ.
    chip = "".join(
        f'<button class="lg {TRANG_THAI[k][0]}" type="button" data-loc="{TRANG_THAI[k][0]}" '
        f'aria-pressed="false"><span class="sw"></span>{TRANG_THAI_HIEN_THI[k]} <span class="n">{n}</span></button>'
        for k, n in co)
    return (f'<div class="stack" aria-hidden="true">{seg}</div>'
            f'<div class="chu-thich">{chip}</div>')


def dai_trang_thai(claims: list, doc_lai: str, ho_so: str = "") -> str:
    """Màn hình đầu tiên. Người bấm vào từ X/TG đã đọc bài rồi — thứ họ chưa biết là
    claim giờ còn đứng không. Trả lời trước, bài để sau.

    `ho_so` là đường sang tủ kính của token bài này thuộc về — chỉ có khi token đó
    thật sự có trang, và cổng ⑪ (liên kết) sẽ chặn build nếu nó trỏ vào thư mục rỗng.
    """
    d = {k: sum(1 for c in claims if c["status"] == k) for k in TRANG_THAI}
    return f"""<section class="dai" data-hien>
  <div class="bh"><b>Sổ claim của bài này</b><span>{len(claims)} khẳng định · trạng thái đổi thì ghi thêm, không xoá</span></div>
  {thanh_xep(d, len(claims))}
  <div class="khi">{ihtml.escape(doc_lai)}</div>
  <a class="toi" href="#so-claim">Xem sổ claim ↓</a>{ho_so}
</section>"""


# ═════════════════════════════════════════════════════════════════════ BUILD

def lap_asset() -> None:
    """Đưa ảnh phục vụ (favicon + card xem trước) vào bản dựng — kèm cổng chống trôi lệch.

    Bản phục vụ nằm ở `site/assets/` vì bản mirror công khai KHÔNG có `template/`
    (nó chỉ chở đúng phần đi ra). Nhưng nguồn sinh ra chúng là
    `template/logo_final.py` ⇒ khi kho gốc có mặt, ép trùng BYTE. Chép tay đúng một
    lần thì được, từ lần thứ hai là hai bản trôi lệch trong im lặng (luật bằng chứng
    của desk §13),
    và đó cũng đúng lý do `publish_site.py` sinh mirror thay vì chép tay.
    """
    kho = ROOT / "assets"
    if not (kho / "favicon-32.png").exists():
        raise LoiCong("thiếu assets/favicon-32.png — favicon thuộc hệ đã chốt "
                      "(template/out/logo/final/he.json), không phải trang trí")
    dich = OUT / "anh"
    dich.mkdir(parents=True, exist_ok=True)
    for f in sorted(kho.glob("*.png")):
        if f.name not in NGUON_ASSET:
            raise LoiCong(f"assets/{f.name} chưa khai builder nào sinh ra nó — thêm vào "
                          f"NGUON_ASSET, đừng để một ảnh không có chủ đi ra ngoài")
        g = ROOT.parent / "template" / "out" / NGUON_ASSET[f.name] / f.name
        if g.exists() and g.read_bytes() != f.read_bytes():
            raise LoiCong(f"assets/{f.name} LỆCH với bản do {NGUON_ASSET[f.name]}/ sinh ra — "
                          f"chạy lại builder rồi chép lại, đừng sửa tay bản này")
        kich_thuoc_png(f)      # nổ sớm nếu file hỏng, thay vì để mạng xã hội dựng khung sai
        (dich / f.name).write_bytes(f.read_bytes())

    # ── LOGO TOKEN (chỉ bố cục v3 dùng tới) ──────────────────────────────────────
    # Ba phép kiểm, mỗi phép bịt một kiểu hỏng-trong-im-lặng khác nhau:
    #  ① thiếu file ⇒ NỔ. Cổng ⑪ chỉ canh `href`, KHÔNG canh `src` — nên một logo
    #    thiếu sẽ đi qua trọn 12 cổng và chỉ hiện ra ở trình duyệt như một ô vỡ.
    #  ② không phải PNG hợp lệ ⇒ `kich_thuoc_png()` nổ (bản HYPE gốc là JPEG).
    #  ③ token có trong `TOKEN_TEN` mà thiếu khai logo ⇒ NỔ. Không có phép này thì
    #    token thứ sáu lặng lẽ ra mắt với một ô trống ở chỗ nhận diện của nó.
    if BO_CUC == "v3":
        thieu = sorted(set(TOKEN_TEN) - set(LOGO_TOKEN))
        if thieu:
            raise LoiCong(f"token {', '.join(thieu)} có tên trong TOKEN_TEN nhưng chưa khai "
                          f"logo trong LOGO_TOKEN — bố cục v3 treo logo ở tủ kính và mục "
                          f"lục token, thiếu khai là một ô vỡ không cổng nào bắt")
        for ma, (tep, xuat_xu, _ngay) in sorted(LOGO_TOKEN.items()):
            p = kho / "token" / tep
            if not p.exists():
                raise LoiCong(f"thiếu assets/token/{tep} (logo {ma}, nguồn: {xuat_xu}) — "
                              f"cổng ⑪ canh href chứ KHÔNG canh src, nên thiếu nó thì build "
                              f"vẫn xanh 12/12 và ô vỡ chỉ lộ ra trên trình duyệt người đọc")
            kich_thuoc_png(p)
            (dich / tep).write_bytes(p.read_bytes())

    # ── FONT tự host. Hai chiều đều CHẶN, vì cả hai chiều đều hỏng trong im lặng:
    # thiếu file thì `@font-face` trỏ vào hư không (chữ vẫn hiện — bằng font hệ thống —
    # và không lệnh nào báo); thừa file thì một mặt chữ không ai khai đi ra ngoài.
    khai = {tep for _, tep, _, _ in FONT_MAT}
    kho_f, dich_f = kho / "font", OUT / "font"
    dich_f.mkdir(parents=True, exist_ok=True)
    for tep in sorted(khai):
        f = kho_f / tep
        if not f.is_file():
            raise LoiCong(f"thiếu assets/font/{tep} — FONT_MAT khai nó, mà file không có. "
                          f"Tải lại từ Google Fonts (bản variable) rồi để vào assets/font/")
        (dich_f / tep).write_bytes(f.read_bytes())
    for f in sorted(kho_f.glob("*.woff2")):
        if f.name not in khai:
            raise LoiCong(f"assets/font/{f.name} không có trong FONT_MAT — khai nó kèm "
                          f"unicode-range, hoặc bỏ file. Font không khai thì không ai "
                          f"biết trang đang nạp cái gì")


# ── TẦNG BIÊN LAI EN ─────────────────────────────────────────────────────────
# 🔴 ĐÂY KHÔNG PHẢI BẢN DỊCH, và sự phân biệt đó là lý do nó tồn tại.
# `LAUNCH §1` chốt "kênh chính tiếng Việt + tầng biên lai tiếng Anh". Tầng đó chưa
# bao giờ được dựng, nên lượt đối chất đầu (07/08, HRC) suýt gửi một câu EN trỏ vào
# trang VN — tức đặt bằng chứng SAU bức tường ngôn ngữ đúng chỗ bên nhận cần kiểm.
# Nặng hơn phần lập luận: các câu KHAI GIỚI HẠN là thứ chặn người ta đọc claim rộng
# hơn nó nói, và chúng chỉ có tiếng Việt.
#
# Vì sao KHÔNG làm nút chuyển VN↔EN: nút chuyển hàm ý "cùng nội dung, khác tiếng" ⇒
# đẻ ra N cặp văn xuôi phải khớp nhau vĩnh viễn, không cổng nào soi được — đúng hình
# dạng defect bài #10 (hai mặt một bài nói ngược nhau) nhân lên cỡ nguyên bài. Trang
# này là TÀI LIỆU KHÁC LOẠI: số + lời gọi + điều bác bỏ + giới hạn. Không có văn xuôi
# chung nên không có gì để lệch; thứ chung duy nhất là các trường trong claims.json,
# và chúng bị cổng dưới đây canh.
#
# 🔴 KHÔNG khai hreflang: hai trang không phải bản dịch của nhau.

def _so_trong(txt: str, toi_thieu: int = 4) -> set:
    """Bóc số, bỏ dấu phân cách để '1,311,093' (EN) và '1.311.093' (VN) so được.
    TRẦN ĐÃ KHAI: chỉ soi số từ `toi_thieu` chữ số trở lên — dưới ngưỡng là nhiễu
    (số claim, '0/29', '58 transfers') và sẽ làm cổng kêu oan tới mức bị bỏ qua."""
    ra = set()
    for m in re.finditer(r"\d[\d.,]*\d|\d", txt):
        n = m.group().replace(",", "").replace(".", "")
        if len(n) >= toi_thieu:
            ra.add(n)
    return ra


def _bien_lai_en_v3(fm: dict, claims: list, en: dict, slug_: str) -> str:
    """Evidence receipt dùng cùng vocabulary WOW với trang bài, không giả làm bản dịch."""
    esc = ihtml.escape
    dem = _dem_trang_thai(claims)
    co = [(k, dem[k]) for k in TRANG_THAI if dem[k]]
    thanh = "".join(f'<i class="{TRANG_THAI[k][0]}" style="--n:{n}"></i>' for k, n in co)
    chu_giai = "".join(
        f'<i><span class="dot {TRANG_THAI[k][0]}"></span><b>{n}</b> '
        f'{esc(TRANG_THAI_EN.get(k, k).lower())}</i>' for k, n in co)
    aria = ", ".join(f"{n} {TRANG_THAI_EN.get(k, k).lower()}" for k, n in co)
    cards = []
    for c in claims:
        cls, _ = TRANG_THAI[c["status"]]
        cards.append(f'''<article class="case-claim {cls}" id="{c['id']}" data-article-claim data-st="{cls}">
  <header class="case-claim-head"><a class="case-claim-id" href="#{c['id']}">{c['id']}</a>
    <span class="case-claim-status {cls}"><i aria-hidden="true"></i>{esc(TRANG_THAI_EN.get(c['status'], c['status']))}</span>
    <span class="case-claim-actions"></span></header>
  <p class="case-claim-text">{esc(c['en']['text'])}</p>
  <div class="case-claim-evidence">
    <p class="case-pin"><span>PINNED AT</span>{esc(c['en']['ghim'])}</p>
    <p class="case-falsifier"><span>WHAT WOULD FALSIFY THIS CLAIM</span>{esc(c['en']['falsifier'])}</p>
  </div>
</article>''')

    c0 = claims[0]
    cls0, _ = TRANG_THAI[c0["status"]]
    metric = _metric_tieu_de(en["og_title"]) or fm["token"]
    active = dem.get("ĐANG ĐỨNG", 0) + dem.get("ĐÃ XÁC NHẬN", 0)
    claim_ledger = f'''<section class="article-ledger" aria-labelledby="so-claim-title">
<details class="evidence case-evidence" id="so-claim">
  <summary>
    <span class="case-ledger-title"><span>Article claim ledger</span><b id="so-claim-title">{len(claims)} claims</b><small>state changes stay visible</small></span>
    <span class="case-ledger-viz"><span class="case-ledger-bar" role="img" aria-label="{esc(aria, quote=True)}">{thanh}</span><span class="case-ledger-legend">{chu_giai}</span></span>
    <span class="mo">open {len(claims)} claims</span>
  </summary>
  <div class="trong case-ledger-body"><p class="case-ledger-intro">Each claim carries its current state, pinned evidence and an explicit falsifier.</p><div class="case-claim-list">{"".join(cards)}</div></div>
</details></section>'''

    how = "".join(f"<li><b>{esc(a)}</b> — <code>{esc(b)}</code></li>"
                  for a, b in en.get("how_to_check", []))
    limits = "".join(f"<li>{esc(x)}</li>" for x in en.get("limits", []))
    source_x = (f'<li>As posted on X: <a href="{fm["kenh_x"]}">{esc(fm["kenh_x"])}</a></li>'
                if fm.get("kenh_x") else "")
    return f'''<section class="hero hero-article receipt-hero">
  <span class="ghost-num" aria-hidden="true">{esc(metric)}</span>
  <span class="hero-code" aria-hidden="true">EVIDENCE RECEIPT · {esc(c0['id'])}</span>
  <div class="article-path" aria-label="Article location"><a href="../../">BlockPinned</a><span>/</span><b>Evidence receipt</b><span>/</span><b>{esc(fm['token'])}</b><i><span class="dot {cls0}"></span>{esc(TRANG_THAI_EN.get(c0['status'], c0['status']).lower())}</i></div>
  <p class="eyebrow"><span>English evidence layer</span><span class="im">{esc(str(fm['date']))}</span></p>
  <h1 class="display">{_tieu_de_nhan(en['og_title'])}</h1>
  <p class="subline">{esc(en['intro'])}</p>
  <div class="article-verdict">
    <div class="heronum article-ratio article-ledger-count"><p class="l">Public claim ledger</p><p class="v">{len(claims)}<em> claims</em></p><p class="d">{active} standing or confirmed</p></div>
    <div class="case-path" role="img" aria-label="Evidence path from source through checks to current state">
      <div class="case-step file"><span>01 · SOURCE</span><strong>{esc(fm['token'])}</strong><small>subject pinned in the record</small></div><i aria-hidden="true">→</i>
      <div class="case-step test"><span>02 · CHECK</span><strong>{len(claims)}</strong><small>explicit falsifiers</small></div><i aria-hidden="true">→</i>
      <div class="case-step state {cls0}"><span>03 · CURRENT</span><strong>{active}/{len(claims)}</strong><small>standing or confirmed</small></div>
    </div>
  </div>
</section>
<nav class="article-map" aria-label="Article sections"><span>Evidence first</span><a href="#so-claim">Claims</a><a href="#how-to-check">How to check</a><a href="#limits">Limits</a><a href="#sources">Sources</a></nav>
{claim_ledger}
<section class="than article-body receipt-body">
  <div class="article-meta"><span><b>PIN</b>{esc(en['pin'])}</span><span><b>DATE</b>{esc(str(fm['date']))}</span><span class="article-meta-link"><a href="../../bai/{slug_}/">Full write-up in Vietnamese →</a></span></div>
  <h2 id="how-to-check">How to check</h2><ul class="receipt-checks">{how}</ul>
  <h2 id="limits">What this does not cover</h2><ul>{limits}</ul>
  <h2 id="sources">Sources</h2><ul><li>Full write-up: <a href="../../bai/{slug_}/">/bai/{slug_}/</a></li>{source_x}</ul>
  <p class="receipt-policy">Corrections are made in place and never deleted; every claim above carries its current status. <b>Not investment advice.</b></p>
</section>'''


def bien_lai_en(fm: dict, claims: list, body_md: str, slug_: str, t: dict, o: str):
    """Sinh /en/<slug>/ nếu claims.json có khối `en`. Không có ⇒ bỏ qua (opt-in).

    Cổng — mỗi cái NỔ ĐƯỢC:
      (a) khai `en` mà claim nào thiếu `en.text`/`en.falsifier` ⇒ LoiCong. Không cho
          ra một trang biên lai thủng claim.
      (b) 🔴 SỐ TRÊN TRANG EN PHẢI CÓ MẶT Ở BẢN VN. Đây là phép so hai mặt mà
          `OPS-T-CROSS-SURFACE-DIFF` còn thiếu; thêm một bề mặt mà không thêm phép so
          là tự dựng lại defect bài #10.
    """
    en = fm.get("_en")
    if not en:
        return None
    # 🔴 `ghim` BẮT BUỘC phải có bản EN, không được rơi về trường VN. Bản đầu 07/08
    #    dùng lại thẳng `c["ghim"]` và trang EN in ra một ô neo TIẾNG VIỆT chở số định
    #    dạng Việt (`299.024.976,59`) — người đọc Anh parse dấu chấm/phẩy ngược lại, tức
    #    RỦI RO ĐỌC SAI SỐ ngay ở ô neo phép đo. Không cổng nào bắt; mở ảnh ra nhìn mới thấy.
    #    Fallback im lặng sang trường VN chính là cơ chế đã để nó lọt ⇒ bỏ hẳn fallback.
    thieu = [c["id"] for c in claims
             if not (c.get("en", {}).get("text", "").strip()
                     and c.get("en", {}).get("falsifier", "").strip()
                     and c.get("en", {}).get("ghim", "").strip())]
    if thieu:
        raise LoiCong(f"khai khối `en` nhưng claim {thieu} thiếu en.text/en.falsifier/en.ghim — {o}. "
                      f"Biên lai thủng claim còn tệ hơn không có biên lai")

    vn = " ".join([body_md, fm.get("ghim", ""), fm.get("mo_ta", "")]
                  + [str(c.get(k, "")) for c in claims
                     for k in ("text", "ghim", "falsifier", "khong_do_lai", "do_lai")])
    en_txt = " ".join([en.get("intro", ""), en.get("pin", "")]
                      + [x for pair in en.get("how_to_check", []) for x in pair]
                      + list(en.get("limits", []))
                      + [c["en"]["text"] + " " + c["en"]["falsifier"] + " " + c["en"]["ghim"]
                         for c in claims])
    la = _so_trong(en_txt) - _so_trong(vn)
    if la:
        raise LoiCong(f"trang EN mang số KHÔNG có ở bản VN: {sorted(la)} — {o}. "
                      f"Hai mặt của một bài không được nói khác nhau (defect bài #10)")

    esc = ihtml.escape
    muc = "".join(
        f'<article class="claim {TRANG_THAI[c["status"]][0]}">'
        f'<h3>{c["id"]} <span class="tt">{esc(TRANG_THAI_EN.get(c["status"], c["status"]))}</span></h3>'
        f'<p class="ct">{esc(c["en"]["text"])}</p>'
        f'<p class="ghim"><b>Pinned at:</b> {esc(c["en"]["ghim"])}</p>'
        f'<p class="fal"><b>What would falsify it:</b> {esc(c["en"]["falsifier"])}</p>'
        f'</article>' for c in claims)
    cach = "".join(f"<li><b>{esc(a)}</b> — <code>{esc(b)}</code></li>"
                   for a, b in en.get("how_to_check", []))
    gh = "".join(f"<li>{esc(x)}</li>" for x in en.get("limits", []))
    than = (_bien_lai_en_v3(fm, claims, en, slug_) if BO_CUC == "v3" else
            (f"<h1>{esc(en['og_title'])}</h1>"
             f'<p class="dan">{esc(en["intro"])}</p>'
             f'<p class="meta">{fm["mau"]} {fm["date"]} &nbsp;·&nbsp; {esc(en["pin"])}</p>'
             f'<h2>Claims</h2>{muc}'
             f'<h2>How to check</h2><ul class="cach">{cach}</ul>'
             f'<h2>What this does not cover</h2><ul class="gh">{gh}</ul>'
             f'<h2>Sources</h2><ul class="cach">'
             f'<li>Full write-up (<b>in Vietnamese</b>): '
             f'<a href="../../bai/{slug_}/">/bai/{slug_}/</a></li>'
             + (f'<li>As posted on X: <a href="{fm["kenh_x"]}">{esc(fm["kenh_x"])}</a></li>'
                if fm.get("kenh_x") else "")
             + '</ul>'
             # 🔴 Chrome của site (nav + footer) là tiếng Việt và DÙNG CHUNG cho 10 trang —
             #    không sửa nó cho một trang. Nhưng footer chở HAI câu CÓ NGHĨA với người đọc:
             #    chính sách đính chính và disclaimer. Để chúng chỉ-tiếng-Việt trên một trang
             #    biên lai gửi ra ngoài là bỏ sót đúng thứ trang này sinh ra để phục vụ ⇒ đưa
             #    bản EN vào THÂN, chỗ trang này kiểm soát. Chrome còn lại thuần thẩm mỹ.
             + '<p class="dan" style="margin-top:2.5rem">Corrections are made in place and '
               'never deleted; every claim above carries its current status. '
               '<b>Not investment advice.</b></p>'))
    d = OUT / "en" / slug_
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(
        trang(en["title"], than, t, "../..", mat="page-en",
              lang="en" if BO_CUC == "v3" else "vi",
              meta={"mo_ta": en["mo_ta"].strip(), "duong": f"/en/{slug_}/",
                    "anh": fm.get("anh"), "loai": "article",
                    "tieu_de_og": en["og_title"]}),
        encoding="utf-8")
    return f"en/{slug_}/"


TRANG_THAI_EN = {"ĐÃ XÁC NHẬN": "CONFIRMED", "ĐANG ĐỨNG": "STANDING",
                 "ĐÃ SỬA": "CORRECTED", "BỊ BÁC": "REFUTED"}


# ═════════════════════════════════════════════════ TRANG CHỦ, BỐ CỤC v3
# Khu này khác hẳn nhóm mặt ①. Ở đó ba builder codex đọc thẳng bản production nên nội
# dung đã có chủ; ở đây `fold-home.tpl.html` chỉ có HAI marker và mọi thứ còn lại là
# HTML viết tay với số nướng sẵn — tức nội dung KHÔNG có chủ nào ngoài chính file mẫu.
#
# 🟢 User chốt 10/08: mỗi bài muốn lên khu spotlight thì KHAI khối `trang_chu` trong
# `claims.json` của nó. Bài không khai vẫn nằm ở dải bài bên dưới ⇒ khu này tự giới
# hạn theo dữ liệu, không bao giờ đứng chờ một ô trống.

def kho_hien_vat() -> pathlib.Path:
    """Kho hiện vật, tra đúng một công thức cho cả kho gốc lẫn mirror công khai."""
    kho = next((k for k in (ROOT.parent / "blockpinned" / "data", ROOT.parent / "data")
                if k.is_dir()), None)
    if kho is None:
        raise LoiCong(f"không tìm thấy kho hiện vật cạnh {ROOT}")
    return kho


VIZ_CO = ("ray", "doi-ray", "doi-so", "dai-ba-diem")
# Hai mốc bố cục của dải ba điểm. Khai ở đây MỘT LẦN vì `khoi_viz` và cổng đều đọc.
DAI_TRAI, DAI_PHAI = 11.7, 92.5


def cong_trang_chu(kh: dict, o: str) -> None:
    """Cổng ⑬ — khối `trang_chu` khai sai thì NỔ, không lặng lẽ dựng một ô méo.

    Vì sao cần: khối này chở SỐ đi thẳng vào thuộc tính `style` (bề rộng thanh, vị trí
    chấm). Sai kiểu thì cổng ⑥ bắt được vì nó canh thuộc tính số — nhưng sai NGHĨA
    (`nho` lớn hơn `lon`, phần trăm âm, thiếu nhãn) thì cổng ⑥ vẫn thấy một số hợp lệ.
    """
    nb = kh.get("noi_bat")
    if nb is not None:
        for k in ("ma", "moc", "so_cu", "so_chain", "so_sua", "khoang", "moc_ngay",
                  "dem_swap", "chart"):
            if k not in nb:
                raise LoiCong(f"trang_chu.noi_bat thiếu '{k}' — {o}")
        lo, hi = nb["khoang"]
        if not lo < nb["so_sua"] < hi:
            raise LoiCong(f"trang_chu.noi_bat: số tính lại {nb['so_sua']:,} KHÔNG nằm trong "
                          f"khoảng ghi trước {lo:,}–{hi:,} — {o}. Khối này dựng lên để nói "
                          f"'rơi đúng khoảng đã ghim'; số không rơi vào đó thì câu chuyện "
                          f"đổi, và trang phải đổi theo chứ không phải vẽ tiếp cái cũ")
        if nb["so_cu"] <= nb["so_chain"]:
            raise LoiCong(f"trang_chu.noi_bat: số cũ phải LỚN HƠN số đếm on-chain (đây là "
                          f"ca thổi phồng) — {o}")
    the = kh.get("the")
    if the is not None:
        for k in ("viz", "so_chinh", "ghim_nho"):
            if k not in the:
                raise LoiCong(f"trang_chu.the thiếu '{k}' — {o}")
        v = the["viz"]
        if v.get("kieu") not in VIZ_CO:
            raise LoiCong(f"trang_chu.the.viz kiểu lạ {v.get('kieu')!r} — chỉ có "
                          f"{', '.join(VIZ_CO)} — {o}")
        if v["kieu"] == "ray" and not 0 < float(v["phan"]) <= 100:
            raise LoiCong(f"trang_chu.the.viz.phan phải trong (0,100] — {o}")
        if v["kieu"] == "dai-ba-diem":
            a, b, c = float(v["nho"]), float(v["giua"]), float(v["lon"])
            if not a <= b <= c or a == c:
                raise LoiCong(f"trang_chu.the.viz ba điểm phải nho ≤ giữa ≤ lớn và nho ≠ lớn "
                              f"(đang là {a} · {b} · {c}) — {o}. Sai thứ tự thì chấm giữa "
                              f"nhảy ra ngoài dải mà cổng ⑥ vẫn thấy một số hợp lệ")


def khoi_viz(v: dict) -> str:
    """Bốn KHUÔN mini-viz. Codex vẽ tay bốn hình cho bốn bài; đây là bốn khuôn dùng lại.

    🔴 Khai GIÁ TRỊ, không khai VỊ TRÍ. Vị trí là kết quả của một phép tính — khai kết
    quả thì lượt sửa số sau sẽ không kéo hình đi theo, và không cổng nào bắt được vì
    một toạ độ cũ vẫn là một toạ độ hợp lệ.
    """
    k = v["kieu"]
    if k == "ray":
        return (f'<div class="viz"><div class="nh"><span>{ihtml.escape(v["nhan"])}</span>'
                f'<b>{ihtml.escape(v["gia_tri"])}</b></div>'
                f'<div class="ray"><i style="width:{float(v["phan"]):.2f}%;--i:0"></i></div></div>')
    if k == "doi-ray":
        return (f'<div class="viz"><div class="nh"><span>{ihtml.escape(v["nhan_a"])}</span>'
                f'<b>{ihtml.escape(v["gia_tri_a"])}</b></div><div class="ray"></div>'
                f'<div class="nh hang2"><span>{ihtml.escape(v["nhan_b"])}</span>'
                f'<b>{ihtml.escape(v["gia_tri_b"])}</b></div>'
                f'<div class="ray"><i style="width:100%;--i:1"></i></div></div>')
    if k == "doi-so":
        khong = " khong" if v.get("b_la_khong") else ""
        return (f'<div class="viz"><div class="doi">'
                f'<span class="ve"><span class="n">{ihtml.escape(v["so_a"])}</span>'
                f'<span class="t">{ihtml.escape(v["nhan_a"])}</span></span>'
                f'<span class="mui">→</span>'
                f'<span class="ve"><span class="n{khong}">{ihtml.escape(v["so_b"])}</span>'
                f'<span class="t">{ihtml.escape(v["nhan_b"])}</span></span></div></div>')
    # dai-ba-diem — vị trí TÍNH từ ba giá trị, tuyến tính giữa hai mốc bố cục
    a, b, c = float(v["nho"]), float(v["giua"]), float(v["lon"])
    dat = lambda x: DAI_TRAI + (x - a) / (c - a) * (DAI_PHAI - DAI_TRAI)
    return (f'<div class="viz"><div class="rai"><span class="truc"></span>'
            f'<span class="cham vien" style="left:{dat(a):.1f}%"></span>'
            f'<span class="cham" style="left:{dat(b):.1f}%"></span>'
            f'<span class="cham vien" style="left:{dat(c):.1f}%"></span>'
            f'<span class="nhan-cham" style="left:{dat(b):.1f}%">{ihtml.escape(v["nhan_giua"])}</span>'
            f'<span class="nhan-duoi" style="left:{dat(a):.1f}%">{so_vn(a, 2)}</span>'
            f'<span class="nhan-duoi" style="left:{dat(c):.1f}%">{so_vn(c, 2)}</span>'
            f'</div></div>')


def the_ho_so(fm: dict, slug_: str, the: dict, dem: dict, tien_to: str = "") -> str:
    """Một thẻ trong khu Hồ sơ điều tra. Tiêu đề · token · ngày lấy từ front matter."""
    chip = "".join(f'<i><span class="dot {TRANG_THAI[k][0]}"></span>{n} {k.lower()}</i>'
                   for k, n in dem.items() if n)
    return (f'<a class="ho-so" href="{tien_to}bai/{slug_}/">'
            f'<p class="eyebrow-nho"><span>{ihtml.escape(fm.get("token", ""))}</span>'
            f'<span class="im">{vn_ngay(str(fm["date"])[:10])}</span></p>'
            f'<h3>{ihtml.escape(fm["title"])}</h3>'
            + khoi_viz(the["viz"])
            + f'<p class="so-chinh">{inline(the["so_chinh"], "trang_chu.the.so_chinh")}</p>'
            f'<p class="trang-thai">{chip}'
            f'<span class="ghim-nho">{ihtml.escape(the["ghim_nho"])}</span></p></a>')


# ── Chart hero. Port từ `design-v3-wow/build_fold.py`, đổi đúng một thứ: chuỗi số
# đọc từ HIỆN VẬT ĐÃ PIN thay vì mảng dán cứng trong script dùng-một-lần.
CH_W, CH_H = 1000, 320
CH_TREN, CH_DUOI, CH_TRAI, CH_PHAI = 26, 30, 6, 86
CH_YMAX = 1_600_000


def _ch_toa(chuoi: list) -> list:
    pw, ph = CH_W - CH_TRAI - CH_PHAI, CH_H - CH_TREN - CH_DUOI
    n = len(chuoi)
    return [(CH_TRAI + i * pw / (n - 1), CH_TREN + (1 - v / CH_YMAX) * ph)
            for i, (_, v) in enumerate(chuoi)]


def ve_chart_hero(chuoi: list, nb: dict) -> tuple:
    """SVG chart + mảng dữ liệu cho JS. Trả (svg, json).

    🔴 Mọi toạ độ in ra ĐỀU đi qua cổng ⑥ (thuộc tính số) — đó là cổng sinh ra sau
    một lượt `.replace('.', ',')` ăn mất dấu chấm của `cx=`. Nên ở đây số thập phân
    tuyệt đối KHÔNG được đổi sang dấu phẩy; dấu phẩy chỉ dành cho CHỮ người đọc.
    """
    ch = nb["chart"]
    pts = _ch_toa(chuoi)
    day = CH_H - CH_DUOI
    i_sua = next(i for i, (n, _) in enumerate(chuoi) if n == nb["moc_ngay"])
    i_moc = next(i for i, (n, _) in enumerate(chuoi) if n == ch["moc_sua"])
    duong = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    mien = duong + f" L{pts[-1][0]:.1f},{day} L{pts[0][0]:.1f},{day} Z"
    dinh = max(v for _, v in chuoi)
    dinh_vn = f"{dinh/1e6:.2f}".replace(".", ",")
    g = [f'<svg viewBox="0 0 {CH_W} {CH_H}" role="img" aria-label="Phí Uniswap v4 theo '
         f'ngày, {chuoi[0][0]} tới {chuoi[-1][0]}, đỉnh ${dinh_vn}M">']
    g.append('<defs>'
             '<linearGradient id="bp-area" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" style="stop-color:var(--accent);stop-opacity:.28"/>'
             '<stop offset=".72" style="stop-color:var(--accent);stop-opacity:.035"/>'
             '<stop offset="1" style="stop-color:var(--accent);stop-opacity:0"/>'
             '</linearGradient>'
             '<linearGradient id="bp-scan" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" style="stop-color:var(--accent);stop-opacity:0"/>'
             '<stop offset=".5" style="stop-color:var(--accent);stop-opacity:.3"/>'
             '<stop offset="1" style="stop-color:var(--accent);stop-opacity:0"/>'
             '</linearGradient></defs>')
    for v in range(0, CH_YMAX + 1, 400_000):
        y = CH_TREN + (1 - v / CH_YMAX) * (CH_H - CH_TREN - CH_DUOI)
        g.append(f'<line class="truc" x1="{CH_TRAI}" y1="{y:.1f}" x2="{CH_W-CH_PHAI}" y2="{y:.1f}"/>')
        nhan = "$0" if v == 0 else f"${v/1e6:.1f}M".replace(".", ",")
        g.append(f'<text x="{CH_W-CH_PHAI+10}" y="{y+4:.1f}">{nhan}</text>')
    for i in range(0, len(chuoi), 7):
        neo = "start" if i == 0 else "middle"
        g.append(f'<text x="{pts[i][0]:.1f}" y="{CH_H-8}" text-anchor="{neo}">{chuoi[i][0]}</text>')
    xm = pts[i_moc][0]
    g.append(f'<line class="moc" x1="{xm:.1f}" y1="{CH_TREN-6}" x2="{xm:.1f}" y2="{day}"/>')
    g.append(f'<text class="nhan-moc" x="{xm+7:.1f}" y="{CH_TREN+6}">{ihtml.escape(ch["nhan_moc"])}</text>')
    g.append(f'<path class="mien" d="{mien}"/>')
    g.append(f'<path class="duong-glow" d="{duong}"/>')
    g.append(f'<path class="duong" d="{duong}"/>')
    g.append(f'<rect class="chart-scan" x="-260" y="{CH_TREN}" width="160" height="{day-CH_TREN}"/>')
    xs, ys = pts[i_sua]
    g.append(f'<circle class="diem-sua" cx="{xs:.1f}" cy="{ys:.1f}" r="5"/>')
    g.append(f'<line class="leader" x1="{xs-118:.1f}" y1="52" x2="{xs-7:.1f}" y2="{ys-7:.1f}"/>')
    g.append(f'<text class="nhan-ma" x="{CH_TRAI+4}" y="40">{nb["moc_ngay"]} từng bị báo '
             f'<tspan style="font-weight:700;text-decoration:line-through">'
             f'${so_vn_nguyen(nb["so_cu"])}</tspan></text>')
    g.append(f'<text class="nhan-ma" x="{CH_TRAI+4}" y="56">đã tính lại còn '
             f'<tspan style="font-weight:700">${so_vn_nguyen(chuoi[i_sua][1])}</tspan>'
             f' — điểm khoanh</text>')
    xe, ye = pts[-1]
    g.append(f'<circle class="pulse-ring" cx="{xe:.1f}" cy="{ye:.1f}" r="8"/>')
    g.append(f'<circle class="diem-cuoi" cx="{xe:.1f}" cy="{ye:.1f}" r="5"/>')
    g.append(f'<text class="nhan-cuoi" x="{xe-9:.1f}" y="{ye-13:.1f}" text-anchor="end">'
             f'{chuoi[-1][0]} · ${so_vn_nguyen(chuoi[-1][1])}</text>')
    g.append(f'<line class="soi" id="soi" x1="0" y1="{CH_TREN}" x2="0" y2="{day}"/>')
    g.append('<circle class="soi-diem" id="soidiem" r="5"/>')
    g.append("</svg>")
    rows = [[chuoi[i][0], chuoi[i][1], round(pts[i][0], 1), round(pts[i][1], 1)]
            for i in range(len(chuoi))]
    return "\n".join(g), json.dumps(rows, ensure_ascii=False)


def so_vn_nguyen(n) -> str:
    """Số nguyên kiểu Việt: dấu CHẤM ngăn nghìn. Tách khỏi `so_vn` (thập phân, dấu phẩy)."""
    return f"{int(n):,}".replace(",", ".")


def mark_path() -> str:
    """Ruột của mark, không kèm thẻ <svg> — chỗ nào cần class riêng thì tự bọc.

    Bóc từ `MARK_SVG` chứ KHÔNG chép lại bốn đường path: bản codex đã chép tay một
    lần và rụng mất số 0 (`84` thay vì `84.0`). Hình vẫn đúng, nhưng đó là một bản sao
    tài sản thương hiệu bắt đầu trôi — và bản sao thứ hai thì không ai so lại nữa.
    """
    return re.sub(r"^<svg[^>]*>|</svg>$", "", MARK_SVG)


def khoi_noi_bat(nb: dict, slug_: str, chuoi: list, doc_luc: str) -> str:
    """Khối `Phân định mới nhất` — spotlight của trang chủ.

    🔴 BỐN CON SỐ VÀO, MỌI THỨ CÒN LẠI TÍNH RA. Bản codex ghi cứng năm vị trí trong
    bản đồ tái hiệu chỉnh (`--left:23.09%`, `--x:25.65%`, …) cộng hai tỷ lệ trong câu
    chữ ("3,9 lần", "lệch 1,93%"). Đo 10/08: cả bảy đều suy được từ số cũ · số đếm
    on-chain · khoảng ghi trước · số tính lại, và bản tính ĐÚNG HƠN bản codex ở hai ô
    (23,07 và 5,15 — codex làm tròn hai đầu khoảng ±10%).

    Khai toạ độ là khai KẾT QUẢ của một phép tính. Lượt sửa số sau sẽ không kéo hình
    đi theo, và không cổng nào bắt được vì một toạ độ cũ vẫn là một toạ độ hợp lệ.
    """
    cu, chain, sua = nb["so_cu"], nb["so_chain"], nb["so_sua"]
    lo, hi = nb["khoang"]
    lan = f"{cu / chain:.1f}".replace(".", ",")            # "3,9"
    lech = f"{abs(sua - chain) / chain * 100:.2f}".replace(".", ",")   # "1,93"
    pc = lambda v: v / cu * 100
    ch = nb["chart"]
    svg, du_lieu = ve_chart_hero(chuoi, nb)
    trieu = lambda v: f"{v / 1e6:.3f}".replace(".", ",")
    return (f'''<section class="hero finding-home" id="moi-nhat">
  <span class="ghost-num" aria-hidden="true">{lan}×</span>
  <span class="hero-code" aria-hidden="true">{ihtml.escape(nb["ma"])}</span>
  <p class="eyebrow"><span>Phân định mới nhất</span><span class="im">{ihtml.escape(nb["moc"])}</span></p>
  <h2 class="finding-title">Con số bị thổi <span class="nhan-manh">{lan} lần</span> đã phải tính lại.</h2>
  <p class="subline">BlockPinned đếm <b>{ihtml.escape(nb["dem_swap"])} swap</b> tận gốc, dán trước \
kết quả công khai — và chuỗi phí Uniswap v4 của DefiLlama được tính lại <b>đúng khoảng đã ghim, \
lệch {lech}%</b>. <a href="bai/{slug_}/">Đọc bài đầy đủ →</a></p>

  <div class="numrow">
    <div class="heronum">
      <p class="l">Phí {ihtml.escape(nb["moc_ngay"])} · sau tính lại</p>
      <p class="v">${so_vn_nguyen(sua)}</p>
      <p class="d">lệch {lech}% so với số ghi trước</p>
    </div>
    <div class="mstack">
      <div class="m"><p class="l">Từng bị báo</p><p class="v"><b>${so_vn_nguyen(cu)}</b></p></div>
      <div class="m"><p class="l">Tôi đếm trên chain</p><p class="v"><b>${so_vn_nguyen(chain)}</b></p></div>
      <div class="m"><p class="l">Khoảng ghi trước · công khai 26/07</p><p class="v"><b>±10%</b></p></div>
    </div>
  </div>

  <figure class="chart chart-card scan-surface" data-cursor-scan>
    <span class="cursor-scan" aria-hidden="true"></span>
    <div class="chart-dau">
      <b>Phí swap Uniswap v4 — Robinhood chain</b>
      <span class="don-vi">USD/ngày · {chuoi[0][0]} → {chuoi[-1][0]}</span>
      <span class="cach-doc"><i><span class="sw"></span>chuỗi đã tính lại</i>\
<i><span class="sw cu"></span>số cũ đã chết</i></span>
    </div>
    <div class="recalibration" role="img" aria-label="Ngày {ihtml.escape(nb["moc_ngay"])}: \
số cũ {so_vn_nguyen(cu)} đô; đếm on-chain {so_vn_nguyen(chain)} đô; số tính lại \
{so_vn_nguyen(sua)} đô, nằm trong khoảng ghi trước cộng trừ 10 phần trăm">
      <div class="rc-head"><span>Bản đồ tái hiệu chỉnh · {ihtml.escape(nb["moc_ngay"])}</span>\
<em>tỷ lệ so với số cũ = 100%</em></div>
      <div class="rc-track">
        <span class="rc-axis"></span>
        <span class="rc-band" style="--left:{pc(lo):.2f}%;--width:{pc(hi) - pc(lo):.2f}%"></span>
        <i class="rc-pin chain" style="--x:{pc(chain):.2f}%;--delay:.48s">\
<span class="rc-label"><b>${trieu(chain)}M</b>đếm on-chain</span></i>
        <i class="rc-pin fixed" style="--x:{pc(sua):.2f}%;--delay:.64s">\
<span class="rc-label"><b>${trieu(sua)}M</b>họ tính lại</span></i>
        <i class="rc-pin old" style="--x:100%;--delay:.8s">\
<span class="rc-label"><b>${trieu(cu)}M</b>số cũ</span></i>
      </div>
    </div>
    <div class="chart-mobile-nav" aria-label="Đi tới mốc trên biểu đồ"><span>ĐIỂM XEM</span>\
<button type="button" data-chart-jump="pin">{ihtml.escape(nb["moc_ngay"])}</button>\
<button type="button" data-chart-jump="end">Mới nhất →</button></div>
    <div class="chart-cuon">{svg}</div>
    <div class="provenance">
      <svg class="pmark" viewBox="0 0 240 240" aria-hidden="true">{mark_path()}</svg>
      <span class="f"><span class="k">GHIM</span><span>{inline(ch["ghim"], "trang_chu.chart.ghim")}</span></span>
      <span class="f"><span class="k">NGUỒN</span><span>{inline(ch["nguon"], "trang_chu.chart.nguon")}</span></span>
      <span class="f"><span class="k">ĐỌC</span><span><b>{vn_ngay(doc_luc)}</b></span></span>
      <a class="chay" href="bai/{slug_}/#tu-kiem">tự chạy lại được</a>
    </div>
  </figure>
</section>
<script>window.BP_CHART_DATA={du_lieu};</script>''')


def trang_chu_v3(bai: list, moi_claim: list, gt: list, tk: dict, khai: dict) -> str:
    """Thân trang chủ, bố cục v3. Bốn khu: sổ gốc · màn đầu · phân định · hồ sơ."""
    dem = {k: sum(1 for _, _, c in moi_claim if c["status"] == k) for k in TRANG_THAI}
    tong = len(moi_claim)
    thu_tu = ["ĐÃ XÁC NHẬN", "ĐANG ĐỨNG", "ĐÃ SỬA", "BỊ BÁC", "CHỜ SỐ"]
    nhan_ng = {k: TRANG_THAI_NGAN[k] for k in TRANG_THAI}
    thanh = "".join(f'<i class="{TRANG_THAI[k][0]}" style="--n:{dem[k]}"></i>'
                    for k in thu_tu if dem[k])
    chu_giai = "".join(f'<span><i class="dot {TRANG_THAI[k][0]}"></i><b>{dem[k]}</b>'
                       f'<small>{nhan_ng[k]}</small></span>' for k in thu_tu if dem[k])
    doc_bar = ", ".join(f"{dem[k]} {nhan_ng[k]}" for k in thu_tu if dem[k])

    # ── khu Hồ sơ điều tra: CHỈ bài có khai `trang_chu.the` ──────────────────────
    the_ds = [the_ho_so(f, s, khai[s]["the"], dm)
              for f, s, _, _, dm in bai if s in khai and "the" in khai[s]]
    # ── khối Phân định: bài có khai `trang_chu.noi_bat` ──────────────────────────
    nb_slug = next((s for s in khai if "noi_bat" in khai[s]), None)
    khoi_nb = ""
    if nb_slug:
        nb = khai[nb_slug]["noi_bat"]
        hv = json.loads((kho_hien_vat() / nb["chart"]["hien_vat"]).read_text(encoding="utf-8"))
        chuoi = [(d["ngay"], int(d["usd"])) for d in hv["chuoi"]]
        khoi_nb = khoi_noi_bat(nb, nb_slug, chuoi, hv["_doc_luc"])

    khoi_bai = dai_bai(
        bai[:6], "", " home-articles", uu_tien=True,
        tieu_de="Bài điều tra mới nhất",
        gioi_thieu="Mỗi bài đi từ câu hỏi, qua phép đo, đến điều gì có thể chứng minh kết luận sai.",
        tong_bai=len(bai), xem_tat_ca="bai/")

    return (f'''<section class="ledger-asset" id="so-goc" aria-labelledby="ledger-title">
  <div class="ledger-head">
    <div>
      <p class="ledger-kicker">Tài sản công khai · cập nhật tại chỗ</p>
      <h2 id="ledger-title">Sổ gốc không xoá phần sai.</h2>
      <p>Mỗi khẳng định có trạng thái, điều bác bỏ và lịch sử thay đổi — người đọc thấy cả \
những lần BlockPinned phải sửa mình.</p>
    </div>
    <a href="track-record/">Mở toàn bộ sổ gốc →</a>
  </div>
  <div class="ledger-grid">
    <div class="ledger-total"><strong>{tong}</strong>\
<span>khẳng định<small>trong {len(bai)} bài</small></span></div>
    <div class="ledger-states">
      <div class="ledger-bar" role="img" aria-label="{tong} khẳng định: {doc_bar}">{thanh}</div>
      <div class="ledger-legend">{chu_giai}</div>
    </div>
    <div class="ledger-preregister"><span>GHI TRƯỚC</span><strong>{len(gt)}</strong>\
<p>lần công khai con số trước khi biết đáp án</p></div>
  </div>
</section>

<section class="home-intro">
  <div class="home-intro-grid">
    <div class="home-promise">
      <p class="eyebrow"><span>Crypto research · evidence first</span>\
<span class="im">không kèo · không nhận định giá</span></p>
      <h1>Nghiên cứu crypto: <span class="nhan-manh">số nào cũng truy ngược được.</span></h1>
      <p class="home-lede">BlockPinned soi những con số đang được thị trường trích dẫn — từ \
dashboard, báo cáo đến dữ liệu on-chain — rồi đếm lại từ nguồn.</p>
      <div class="home-method" aria-label="Phương pháp BlockPinned">
        <span><b>01</b> đi tận nguồn</span><span><b>02</b> ghim điều bác bỏ</span>\
<span><b>03</b> sửa tại chỗ</span>
      </div>
    </div>
    <nav class="home-map" aria-label="Khám phá BlockPinned">
      <a class="home-door" href="#bai"><span class="door-no">01</span>\
<span class="door-copy"><b>Bài điều tra</b><small>Đọc trọn câu hỏi, đường đo và phần có thể sai.</small></span>\
<span class="door-go" aria-hidden="true">↘</span></a>
      <a class="home-door" href="token/"><span class="door-no">02</span>\
<span class="door-copy"><b>Token</b><small>Hồ sơ theo đối tượng, gom mọi câu đã ghim.</small></span>\
<span class="door-go" aria-hidden="true">↗</span></a>
      <a class="home-door" href="facts/"><span class="door-no">03</span>\
<span class="door-copy"><b>Facts</b><small>Một số · một block · một lệnh tự kiểm.</small></span>\
<span class="door-go" aria-hidden="true">↗</span></a>
      <a class="home-door" href="track-record/"><span class="door-no">04</span>\
<span class="door-copy"><b>Track record</b><small>Claim nào vẫn đứng vững, đã sửa hay đã bị bác bỏ.</small></span>\
<span class="door-go" aria-hidden="true">↗</span></a>
    </nav>
  </div>
</section>

{khoi_bai}

{khoi_nb}

<section class="inv-khu" id="ho-so">
  <div class="inv-dau">
    <p class="kicker">Hồ sơ điều tra</p>
    <span class="dem-bai">{len(bai)} bài · {len(tk)} token</span>
    <a href="#bai">xem tất cả</a>
  </div>
  <div class="inv">{"".join(the_ds)}</div>
</section>''' + sap_phan_dinh(moi_claim))


def cong_bo_cuc(html_chu: str, html_token: str, so_bai: int, so_token: int) -> None:
    """Chặn đúng ca 11/08: HTML còn đủ chữ nhưng selector của mặt đang phát hành mất.

    Kiểm overflow không bắt được ca này vì chữ trần tự xuống dòng và không hề tràn.
    Component bắt buộc + số item mới là hợp đồng giữa builder với CSS/JS.
    """
    if BO_CUC == "v3":
        nhan_nav = ["Trang chủ", "Bài viết", "Token", "Track record", "Facts"]
        if [nhan for _, nhan in MUC_DIEU_HUONG] != nhan_nav:
            raise LoiCong("menu phải dùng chung: " + " · ".join(nhan_nav))
        for ten_mat, html in (("trang chủ", html_chu), ("token", html_token)):
            nav = re.search(r'<nav class="dieu"[^>]*>(.*?)</nav>', html, re.S)
            if not nav:
                raise LoiCong(f"{ten_mat} mất thanh điều hướng dùng chung")
            nhan_thuc = [
                ihtml.unescape(re.sub(r"<[^>]+>", "", x)).replace("\xa0", " ").strip()
                for x in re.findall(r"<a\b[^>]*>(.*?)</a>", nav.group(1), re.S)
            ]
            if nhan_thuc != nhan_nav:
                raise LoiCong(f"menu {ten_mat} không dùng chung: {nhan_thuc!r}")
        moc_bai = 'class="khu-bai home-articles article-priority"'
        if (moc_bai not in html_chu
                or len(re.findall(r'<a class="bai(?: bai-lead)?" href=', html_chu)) != min(6, so_bai)
                or 'class="bai-archive-link" href="bai/"' not in html_chu):
            raise LoiCong("preview bài trang chủ v3 thiếu cấu trúc, sai số thẻ hoặc mất lối vào kho bài")
        if html_chu.index(moc_bai) > html_chu.index('id="ho-so"'):
            raise LoiCong("mục bài trang chủ v3 đã tụt xuống sau hồ sơ — phải là cửa vào ở nửa đầu trang")
        if (not all(x in html_token for x in ('class="token-switcher"',
                                               'class="token-overview"',
                                               'class="token-directory"',
                                               'class="token-grid"'))
                or html_token.count(" data-token-card") != so_token):
            raise LoiCong("mục token v3 thiếu cấu trúc token-directory hoặc mất token-card")
    else:
        if ('class="khu-bai"' not in html_chu
                or html_chu.count('<a class="bai"') != so_bai):
            raise LoiCong("mục bài trang chủ D2 thiếu khu-bai hoặc mất thẻ bài")
        if ('class="cua cua-3"' not in html_token
                or html_token.count('class="cua-o tok"') != so_token):
            raise LoiCong("mục token D2 thiếu lưới cua hoặc mất token")


def cong_bai_token(html_tu: str, so_bai: int) -> None:
    """Bài gốc trên hồ sơ token phải đứng trước tủ claim, không chìm ở chân trang."""
    if BO_CUC != "v3":
        return
    moc_bai = 'class="khu-bai uni-articles article-priority"'
    if (moc_bai not in html_tu
            or len(re.findall(r'<a class="bai(?: bai-lead)?" href=', html_tu)) != min(6, so_bai)
            or 'class="bai-archive-link" href="../../bai/#token-' not in html_tu):
        raise LoiCong("preview bài token v3 thiếu cấu trúc, sai số thẻ hoặc mất lối vào kho bài")
    if html_tu.index(moc_bai) > html_tu.index('class="uni-coverage"'):
        raise LoiCong("mục bài token v3 đã tụt xuống sau tủ claim — phải đứng ngay sau phần mở đầu")


def cong_muc_bai(html_bai: str, so_bai: int, so_token: int) -> None:
    """Kho bài là cửa mở rộng; mọi bài phải có mặt dù preview chỉ giữ sáu thẻ."""
    if BO_CUC != "v3":
        return
    if (not all(x in html_bai for x in ('class="article-archive"',
                                        'data-article-search',
                                        'data-article-filter="all"',
                                        'data-article-more'))
            or html_bai.count(" data-article-card") != so_bai
            or html_bai.count(" data-article-filter=") != so_token + 1):
        raise LoiCong("kho bài v3 thiếu tìm/lọc/mở-thêm hoặc mất bài/token")
    nut = re.search(r'<button\b([^>]*)data-article-more([^>]*)>(.*?)</button>',
                    html_bai, re.S)
    if not nut:
        raise LoiCong("kho bài v3 mất nút mở thêm")
    thuoc_tinh = nut.group(1) + nut.group(2)
    nhan = ihtml.unescape(re.sub(r"<[^>]+>", "", nut.group(3))).replace("\xa0", " ").strip()
    if so_bai <= 12:
        if "hidden" not in thuoc_tinh or re.search(r"Mở thêm\s+\d+", nhan):
            raise LoiCong("kho bài đã hiện đủ mà nút mở thêm vẫn hiện hoặc còn mang số nháp")
    else:
        con_lai = min(12, so_bai - 12)
        if "hidden" in thuoc_tinh or f"Mở thêm {con_lai} bài viết" not in nhan:
            raise LoiCong("nút mở thêm của kho bài không khớp số bài còn lại")


def main() -> None:
    # Mặc định là hệ ĐÃ CHỐT. Bản đầu đọc argv bằng cách "có chữ verdigris ở đâu đó
    # trong argv" — thứ đó lặng lẽ đúng cho tới khi đường dẫn --out chứa chữ đó.
    ten = HE_MAC_DINH
    if "--theme" in sys.argv:
        xin = sys.argv[sys.argv.index("--theme") + 1]
        if xin not in THEMES:
            sys.exit(f"🔴 hệ màu lạ {xin!r} — chỉ có {list(THEMES)}")
        ten = xin
    t = THEMES[ten]
    # 🔴 BỐ CỤC gán vào biến MODULE, không luồn qua tham số. Lý do là hình dạng của
    # chính file này: `trang()` nhận `t`, nhưng `trang_facts()` · `so_claim()` ·
    # `bang_diem()` thì KHÔNG — luồn tham số qua chúng là sửa chữ ký của mười mấy hàm
    # cho một thứ hằng suốt một lượt dựng. `CO_TRANG` và `HIEN_VAT` đã đi đường này.
    global BO_CUC, BAN_THU
    if "--bo-cuc" in sys.argv:
        xin = sys.argv[sys.argv.index("--bo-cuc") + 1]
        if xin not in BO_CUC_CO:
            sys.exit(f"🔴 bố cục lạ {xin!r} — chỉ có {list(BO_CUC_CO)}")
        BO_CUC = xin
    BAN_THU = "--ban-thu" in sys.argv
    # 🔴 DỌN thư mục ra trước khi dựng — cùng lỗi đã vá cho mirror, và nó vẫn còn ở đây:
    # xác 30/07, hai favicon của bản dựng cũ nằm lại ở gốc out/ sau khi ảnh chuyển sang
    # out/anh/. Bài đổi tên thì trang cũ cũng sống mãi ở đường cũ, không lệnh nào báo.
    # Chốt an toàn: chỉ dọn thứ TRÔNG NHƯ một bản dựng cũ (rỗng, hoặc có index.html) —
    # để `--out <thư mục có việc khác>` không bị xoá bừa.
    if OUT.is_dir():
        ds = list(OUT.iterdir())
        if ds and not (OUT / "index.html").exists():
            sys.exit(f"🔴 {OUT} có sẵn file mà KHÔNG phải bản dựng (thiếu index.html) — "
                     f"đổi --out, tôi không xoá thư mục của việc khác")
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    lap_asset()
    primers = doc_primers()

    # 🔴 Thanh điều hướng dựng TRƯỚC trang đầu tiên, nên phải biết trước trang nào sẽ có.
    # Bản đầu định đọc sau vòng lặp — nhưng trang bài được ghi TRONG vòng lặp, tức nó sẽ
    # mang một thanh điều hướng khai theo trạng thái chưa biết. Cổng ⑪ bắt được ca trỏ
    # vào thư mục rỗng, nhưng không bắt được ca ngược: có trang mà mục bị tắt.
    CO_TRANG["facts/"] = bool(doc_facts())
    CO_TRANG["du-lieu/"] = bool(HIEN_VAT)
    try:
        CO_TRANG["track-record/"] = any(
            c.get("ghi_truoc")
            for p in CONTENT.glob("posts/*.claims.json")
            for c in json.loads(p.read_text(encoding="utf-8"))["claims"])
    except (json.JSONDecodeError, KeyError, TypeError):
        CO_TRANG["track-record/"] = False   # vòng lặp dưới sẽ báo lỗi đúng chỗ hỏng

    # Tủ kính bật/tắt phải biết TRƯỚC vòng lặp, vì thanh điều hướng được dựng cùng
    # trang bài đầu tiên. Lượt quét này chỉ đọc front matter — rẻ, và nó là chỗ duy
    # nhất quyết định mục "Token" có mặt hay không.
    dem_token = {}
    for p in CONTENT.glob("posts/*.md"):
        fm0, _ = front(p.read_text(encoding="utf-8"), f"content/posts/{p.name}")
        dem_token[fm0.get("token", "")] = dem_token.get(fm0.get("token", ""), 0) + 1
    CO_TRANG[TU_KINH_DUONG] = dem_token.get(TU_KINH, 0) >= TU_KINH_SAN
    CO_TRANG["bai/"] = bool([k for k in dem_token if k])
    # Mục lục token có mặt khi có BẤT KỲ token nào — nó là bản đồ, không phải tủ kính,
    # nên nó không có sàn. Sàn chỉ chặn việc MỞ MỘT TRANG RIÊNG cho token mỏng.
    CO_TRANG["token/"] = bool([k for k in dem_token if k]) or bool(primers)

    bai, moi_claim, token_cua, khai_tc = [], [], {}, {}

    for md_path in sorted(CONTENT.glob("posts/*.md"), reverse=True):
        o = f"content/posts/{md_path.name}"
        fm, body_md = front(md_path.read_text(encoding="utf-8"), o)
        cj = md_path.with_suffix(".claims.json")
        if not cj.exists():
            raise LoiCong(f"thiếu {cj.name} — mọi bài phải có sổ claim, đó là lý do site này tồn tại")
        _cj = json.loads(cj.read_text(encoding="utf-8"))
        claims = _cj["claims"]
        # khối `en` (nếu có) đi kèm fm để bien_lai_en() đọc — nguồn vẫn là MỘT file
        fm["_en"] = _cj.get("en")
        # Khối trang chủ (bố cục v3) — CỔNG CHẠY DÙ BỐ CỤC NÀO. Khai sai mà chỉ nổ ở
        # lượt v3 nghĩa là một lượt dựng D2 bình thường vẫn im lặng cho nó đi qua, rồi
        # nó nổ ở đúng lượt xuất bản. Cổng phải canh DỮ LIỆU, không canh chế độ dựng.
        if _cj.get("trang_chu"):
            cong_trang_chu(_cj["trang_chu"], o)
            khai_tc[md_path.stem] = _cj["trang_chu"]

        # cổng chạy TRƯỚC khi in ra bất cứ thứ gì (LAUNCH.md:126)
        visuals = _cj.get("visuals", [])
        kho = (body_md + "\n" + json.dumps(claims, ensure_ascii=False) + "\n"
               + json.dumps(fm, ensure_ascii=False) + "\n"
               + json.dumps(visuals, ensure_ascii=False))
        cong_ngon_ngu(kho, o)
        cong_ngoi_xung(kho, o)
        cong_claim(claims, o)
        cong_cau_truc(fm, body_md, claims, o)
        cong_tieu_de(fm, o)
        cong_do_lai(claims, o)
        cong_han(claims, o)
        cong_qua_han(claims, o)
        cong_ghi_truoc(claims, o)
        cong_visuals(body_md, visuals, claims, o)

        slug_ = md_path.stem
        # Khai token là BẮT BUỘC — nó là khoá của hồ sơ theo đối tượng, và một bài
        # không khai thì nó lặng lẽ rơi khỏi tủ kính của chính token nó nói về.
        tk = fm.get("token", "").strip()
        if tk not in TOKEN_TEN:
            raise LoiCong(f"front matter 'token' thiếu hoặc lạ ({tk!r}) — {o}. "
                          f"Đang biết: {', '.join(sorted(TOKEN_TEN))}. Token mới thì "
                          f"thêm vào TOKEN_TEN kèm tên đầy đủ, đừng viết tắt tuỳ ý")
        token_cua[slug_] = tk
        if tk == TU_KINH and CO_TRANG[TU_KINH_DUONG]:
            ho_so = (f'<a class="article-token-link" href="../../{TU_KINH_DUONG}">'
                     f'Hồ sơ {TOKEN_TEN[tk]} →</a>' if BO_CUC == "v3" else
                     f'<a class="toi phu" href="../../{TU_KINH_DUONG}">Hồ sơ {TOKEN_TEN[tk]} →</a>')
        else:
            ho_so = ""
        # 🔴 THỨ TỰ TRANG LÀ CÓ CHỦ Ý, đừng đảo lại: sổ claim ĐỨNG TRƯỚC bài viết.
        # Bản đầu đặt bài lên trước và màn hình đầu tiên giống hệt Telegram — người
        # bấm vào từ X/TG đã đọc bài rồi, đưa lại bài là không cho họ lý do ở lại.
        # Bài vẫn đăng đủ dạng native trên X/TG (LAUNCH.md:152), ở đây nó là THAM CHIẾU.
        than = (trang_bai_v3(fm, claims, body_md, o, ho_so, _cj.get("trang_chu", {}), visuals)
                if BO_CUC == "v3" else
                (f"<h1>{ihtml.escape(fm['title'])}</h1>"
                 + dai_trang_thai(claims, fm.get("doc_lai", ""), ho_so)
                 + so_claim(claims)
                 + f'<section class="bandaydu"><h2 id="ban-day-du">Bài đầy đủ</h2>'
                   f'<p class="meta">{fm["mau"]} {fm["date"]} &nbsp;·&nbsp; '
                   f'GHIM TẠI {ihtml.escape(fm["ghim"])}'
                   # kenh_x KHÔNG bắt buộc: web là sổ gốc, X/TG là phân phối
                   # (LAUNCH.md:155) ⇒ bản chuẩn phải tồn tại được TRƯỚC lúc đăng.
                   # Bản đầu bắt buộc trường này, tức bắt sổ gốc phải đợi kênh phân
                   # phối — ngược đúng chiều kiến trúc, và nó chỉ lộ ở bài thứ hai.
                   + (f' &nbsp;·&nbsp; <a href="{fm["kenh_x"]}">bản đăng trên X</a>'
                      if fm.get("kenh_x") else
                      ' &nbsp;·&nbsp; <i>chưa đăng trên kênh</i>') + '</p>'
                 + render(body_md, o, visuals) + "</section>"))
        cong_visual_html(than, visuals, o)
        d = OUT / "bai" / slug_
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            trang(f"{fm['title']} — BlockPinned", than, t, "../..", mat="page-article",
                  meta={"mo_ta": fm["mo_ta"].strip(), "duong": f"/bai/{slug_}/",
                        "anh": fm.get("anh"), "loai": "article",
                        "tieu_de_og": fm["title"]}),
            encoding="utf-8")
        _en_duong = bien_lai_en(fm, claims, body_md, slug_, t, o)
        if _en_duong:
            print(f"  ✓ {_en_duong}  ·  biên lai EN ({len(claims)} claim)")
        # 🔴 Tóm tắt CHỈ đếm "đang đứng" là NÓI DỐI THEO CHIỀU TỰ HẠ MÌNH: bài #1 có
        # 4 claim (1 xác nhận · 1 đứng · 2 đã sửa) mà dòng cũ in "4 claim, 1 đang đứng"
        # ⇒ đọc ra như 3/4 đã đổ. Lỗi này chỉ xuất hiện khi có claim ở trạng thái thứ ba;
        # với N=1 bài toàn "đang đứng" thì công thức cũ trông đúng. Nay in ĐỦ PHỔ.
        dem = {k: sum(1 for c in claims if c["status"] == k) for k in TRANG_THAI}
        tom = " · ".join(f"{n} {TRANG_THAI_NGAN[k]}" for k, n in dem.items() if n)
        bai.append((fm, slug_, len(claims), tom, dem))
        for c in claims:
            moi_claim.append((slug_, fm["title"], c))
        print(f"  ✓ bai/{slug_}/  ·  {len(claims)} claim ({tom})")

    gt = [c for _, _, c in moi_claim if c.get("ghi_truoc")]
    facts = doc_facts()
    cong_facts(facts)          # cổng ⑪ chạy TRƯỚC khi dựng, kể cả khi danh sách rỗng
    fm_i, body_i = front((CONTENT / "index.md").read_text(encoding="utf-8"), "content/index.md")
    cong_ngon_ngu(body_i, "content/index.md")
    cong_ngoi_xung(body_i, "content/index.md")
    # 🔴 DẢI NGANG thay chồng dọc — user 06/08: *"bài viết để cuối, có cách nào phát
    # triển theo chiều ngang thay vì chiều dọc kéo xuống như cũ"*. Bài NẰM CUỐI là có
    # chủ ý và giữ nguyên (người bấm vào từ X/TG đã đọc bài rồi); thứ đổi là 8 thẻ xếp
    # dọc — chúng đẩy chân trang xuống gần hai màn hình và mỗi thẻ chỉ chở đúng một dòng
    # chữ. Xếp ngang thì cùng chỗ đó chở được thêm một thanh trạng thái cho từng bài.
    # Hồ sơ theo token — gom SAU vòng lặp, dùng cho cả bản đồ trang chủ lẫn `/token/`
    tk = {}
    for f, s, n, sg, dm in bai:
        v = tk.setdefault(token_cua[s],
                          {"bai": 0, "claim": 0, "dem": {}, "slug_moi": s, "ngay": ""})
        v["bai"] += 1
        v["claim"] += n
        for k, x in dm.items():
            v["dem"][k] = v["dem"].get(k, 0) + x
        if str(f["date"]) > v["ngay"]:
            v["ngay"], v["slug_moi"] = str(f["date"]), s

    # `/bai/` là kho riêng, không phải dải thứ ba trên trang chủ. Preview ở trang chủ
    # và hồ sơ token chỉ giữ sáu bài; tại đây mọi bài vẫn có mặt và có thể tìm/lọc.
    d_bai = OUT / "bai"
    d_bai.mkdir(parents=True, exist_ok=True)
    html_bai = trang(
        "Tất cả bài viết — BlockPinned", trang_muc_bai(bai), t, "..",
        muc="bai/", mat="page-article-archive",
        meta={"mo_ta": f"Kho {len(bai)} bài điều tra BlockPinned, tìm theo tiêu đề, "
                       f"mốc ngày hoặc token; mỗi bài giữ nguyên sổ claim và đường tự kiểm.",
              "duong": "/bai/", "anh": "avatar-800.png", "loai": "website",
              "tieu_de_og": "Tất cả bài viết — BlockPinned"})
    cong_muc_bai(html_bai, len(bai), len(tk))
    (d_bai / "index.html").write_text(html_bai, encoding="utf-8")
    print(f"  ✓ bai/  ·  kho {len(bai)} bài · {len(tk)} token")

    # 🔴 THỨ TỰ TRANG CHỦ, vòng 3: bản đồ ĐỨNG ĐẦU (người lạ phải thấy site có gì
    # trước khi phải cuộn), rồi bảng điểm, rồi BÀI, rồi mốc chờ. Bài dời lên trên
    # "Sắp phân định" vì user đo bằng chính tay mình: *"vô sổ gốc rồi kéo mãi xuống
    # mới thấy bài viết"* — 4,2 màn hình trên điện thoại ở bản trước.
    than_i = (trang_chu_v3(bai, moi_claim, gt, tk, khai_tc) if BO_CUC == "v3" else
              f'<h1>{ihtml.escape(fm_i["tagline"])}</h1>'
              + ban_do(len(bai), len(tk), gt, facts, len(HIEN_VAT))
              + render(body_i, "content/index.md")
              + bang_diem(moi_claim)
              + dai_bai(bai, "")
              + sap_phan_dinh(moi_claim))
    if not 60 <= len(fm_i.get("mo_ta", "").strip()) <= 200:
        raise LoiCong("content/index.md thiếu 'mo_ta' 60–200 ký tự — trang chủ là chỗ "
                      "hay bị dán link nhất, để trắng là mất ở đúng cửa")
    html_chu = trang("BlockPinned — số nào cũng truy ngược được", than_i, t, mat="home-page",
                     meta={"mo_ta": fm_i["mo_ta"].strip(), "duong": "/", "anh": "avatar-800.png",
                           "loai": "website", "tieu_de_og": "BlockPinned — số nào cũng truy ngược được"})
    (OUT / "index.html").write_text(html_chu, encoding="utf-8")

    # ── TỦ KÍNH token ────────────────────────────────────────────────────────────
    # Dựng SAU vòng lặp vì nó cần cả bài lẫn claim của token; bật/tắt thì đã quyết
    # trước vòng lặp (thanh điều hướng cần biết sớm). Hai con số phải khớp nhau, và
    # lệch thì CHẶN: nếu lượt quét front matter nói "đủ bài" mà lượt dựng thật lại
    # đếm ra ít hơn sàn, nghĩa là hai lượt đọc cùng một thư mục ra hai kết quả.
    # Mục lục token — không có sàn, chở đủ mọi token có bài
    d_mt = OUT / "token"
    d_mt.mkdir(parents=True, exist_ok=True)
    ds_tk = " · ".join(f"{m} {v['bai']} bài"
                       for m, v in sorted(tk.items(), key=lambda x: -x[1]["bai"]))
    html_token = trang(
        "Token — hồ sơ theo đối tượng — BlockPinned", trang_muc_token(tk, primers), t, "..",
        muc="token/", mat="page-token-index",
        meta={"mo_ta": f"Mọi token BlockPinned đã đo, kèm số bài và số khẳng định của "
                       f"từng cái: {ds_tk}; hiện có {len(primers)} Token Primer theo đối tượng.",
              "duong": "/token/", "anh": "avatar-800.png", "loai": "website",
              "tieu_de_og": "BlockPinned đã đo được gì, xếp theo token"})
    cong_bo_cuc(html_chu, html_token, len(bai), len(tk))
    (d_mt / "index.html").write_text(html_token, encoding="utf-8")
    print(f"  ✓ token/  ·  mục lục {len(tk)} token có bài + {len(primers)} Primer")

    for primer in primers:
        d_primer = OUT / "token" / primer["id"]
        d_primer.mkdir(parents=True, exist_ok=True)
        html_primer = trang(
            f'{primer["title"]} — BlockPinned', trang_primer(primer), t, "../..",
            muc="token/", mat=("page-token-primer" +
                                (f' primer-{primer["art_direction"]}'
                                 if primer.get("art_direction") else "")),
            meta={"mo_ta": primer["description"], "duong": f'/{primer["_path"]}',
                  "anh": primer.get("image", "avatar-800.png"), "loai": "article",
                  "tieu_de_og": primer["title"]})
        (d_primer / "index.html").write_text(html_primer, encoding="utf-8")
        print(f'  ✓ {primer["_path"]}  ·  Token Primer · {len(primer["visuals"])} visual')

    bai_tk = [x for x in bai if token_cua[x[1]] == TU_KINH]
    if CO_TRANG[TU_KINH_DUONG]:
        if len(bai_tk) < TU_KINH_SAN:
            raise LoiCong(f"tủ kính {TU_KINH} bật nhưng chỉ dựng được {len(bai_tk)} bài "
                          f"(sàn {TU_KINH_SAN}) — hai lượt đọc cùng thư mục ra hai kết quả")
        claims_tk = [(s, t, c) for s, t, c in moi_claim if token_cua[s] == TU_KINH]
        d_tk = OUT / "token" / TU_KINH.lower()
        d_tk.mkdir(parents=True, exist_ok=True)
        html_tu = trang(
            f"{TOKEN_TEN[TU_KINH]} — hồ sơ {TU_KINH} — BlockPinned",
            trang_token(TU_KINH, bai_tk, claims_tk), t, "../..", muc=TU_KINH_DUONG, mat="page-token-uni",
            meta={"mo_ta": f"Mọi khẳng định BlockPinned đã đăng về {TOKEN_TEN[TU_KINH]}: "
                           f"{len(claims_tk)} câu trên {len(bai_tk)} bài, mỗi câu ghim tại "
                           f"block đã đo, kèm điều gì sẽ bác bỏ nó và trạng thái hiện tại.",
                  "duong": f"/{TU_KINH_DUONG}", "anh": "card-uni-100usd.png", "loai": "website",
                  "tieu_de_og": f"{TOKEN_TEN[TU_KINH]} — mọi con số đã ghim, và câu nào còn đứng"})
        cong_bai_token(html_tu, len(bai_tk))
        (d_tk / "index.html").write_text(html_tu, encoding="utf-8")
        print(f"  ✓ {TU_KINH_DUONG}  ·  {len(claims_tk)} khẳng định trên {len(bai_tk)} bài")
    elif len(bai_tk) >= TU_KINH_SAN:
        raise LoiCong(f"{TU_KINH} có {len(bai_tk)} bài (đủ sàn) mà mục Token lại tắt — "
                      f"lượt quét front matter và lượt dựng không đồng ý với nhau")

    # trang /track-record/ — thứ khó làm giả nhất desk có, nên nó được một URL riêng để dán
    # 🔴 ĐỔI TÊN 31/07: `/ghi-truoc/` → `/track-record/` (user chốt). Lý do đổi nằm ở
    # `brief-chien-luoc-dang-x.md §0b`: tên cũ mô tả THAO TÁC (ghi vào lúc nào) chứ không
    # mô tả thứ đang nằm ở đó, và nó đứng quá gần tên định đặt cho đơn vị đăng thứ hai.
    # Chữ "ghi trước" trong THÂN BÀI giữ nguyên tiếng Việt — nó là giọng kênh và đã nằm
    # trong bài đã đăng. Chỉ URL + nhãn mục đổi (LAUNCH §1: shell EN, ruột VN).
    if gt:
        d_gt = OUT / "track-record"
        d_gt.mkdir(parents=True, exist_ok=True)
        (d_gt / "index.html").write_text(trang(
            "Track record — tôi ghi trước, rồi kết quả ra sao — BlockPinned",
            trang_ghi_truoc(moi_claim), t, "..", muc="track-record/", mat="page-track-record",
            meta={"mo_ta": "Mọi lần BlockPinned dán một con số hoặc một ngưỡng ra công khai "
                           "trước khi biết đáp án, kèm kết quả — cả những lần sai và những "
                           "lần chưa có kết quả.",
                  "duong": "/track-record/", "anh": "post01-card.png", "loai": "website",
                  "tieu_de_og": "Track record — tôi ghi trước, rồi kết quả ra sao"}),
            encoding="utf-8")
        print(f"  ✓ track-record/  ·  {len(gt)} lần ghi trước")

        # 🔴 Đường cũ PHẢI còn sống. Đã kiểm 31/07: không bài X/TG nào đã đăng chứa URL
        # `/ghi-truoc/` — nhưng site sống từ 30/07, trang bài có link nội bộ tới nó, và
        # một URL đã từng phục vụ thì không được trả 404 chỉ vì desk đổi ý về cái tên.
        d_cu = OUT / "ghi-truoc"
        d_cu.mkdir(parents=True, exist_ok=True)
        (d_cu / "index.html").write_text(
            '<!doctype html><html lang="vi"><head><meta charset="utf-8">'
            f'<link rel="canonical" href="{BASE}/track-record/">'
            '<meta name="robots" content="noindex">'
            '<meta http-equiv="refresh" content="0; url=/track-record/">'
            '<title>Đã chuyển sang /track-record/</title></head>'
            '<body><p>Trang này đã chuyển sang '
            f'<a href="{BASE}/track-record/">{BASE}/track-record/</a>.</p></body></html>\n',
            encoding="utf-8")
        print("  ✓ ghi-truoc/  ·  trang chuyển hướng sang track-record/")

    # trang /facts/ — đơn vị đăng thứ hai (§0b). Rỗng thì KHÔNG dựng: một mục trống
    # đi ra ngoài là một lời hứa để trắng, tệ hơn không có mục.
    if facts:
        d_f = OUT / "facts"
        d_f.mkdir(parents=True, exist_ok=True)
        noi_facts = trang_facts(facts)
        cong_facts_web(noi_facts, facts)
        (d_f / "index.html").write_text(trang(
            "Facts — BlockPinned", noi_facts, t, "..", muc="facts/", mat="page-facts",
            meta={"mo_ta": "Mỗi mục là một sự thật đúng tại một block, kèm một lệnh để bạn "
                           "tự đọc lại con số đó. Không phân tích, không nhận định giá.",
                  "duong": "/facts/", "anh": "avatar-800.png", "loai": "website",
                  "tieu_de_og": "Facts — mỗi mục một con số, một block, một lệnh"}),
            encoding="utf-8")
        print(f"  ✓ facts/  ·  {len(facts)} fact")

    # ── sitemap + robots: điều kiện để máy tìm THẤY trang ────────────────────────
    # Thiếu hai file này thì site vẫn sống, chỉ là không ai tìm ra — đúng loại hỏng
    # KHÔNG báo lỗi. lastmod lấy từ ngày bài, không lấy giờ chạy, để hai lần dựng cùng
    # nội dung ra cùng một byte (dựng không tất định thì mọi phép so bản chép vô nghĩa).
    ngay_moi = max(f["date"] for f, *_ in bai)
    loc = [(BASE + "/", ngay_moi)]
    if gt:
        loc.append((f"{BASE}/track-record/", ngay_moi))
    # 🔴 `/ghi-truoc/` KHÔNG vào sitemap: nó là trang chuyển hướng, đã gắn `noindex`.
    # Khai một URL chuyển hướng trong sitemap là bảo máy tìm kiếm đi lập chỉ mục cái
    # bóng của trang thật — hai URL cùng nội dung, và cái thắng có thể là cái sai.
    if facts:
        loc.append((f"{BASE}/facts/", max(str(f.get("ngay", "")) or ngay_moi for f in facts)))
    loc.append((f"{BASE}/token/", ngay_moi))
    loc += [(f'{BASE}/{p["_path"]}', str(p["lastmod"])) for p in primers]
    if CO_TRANG[TU_KINH_DUONG]:
        # lastmod của tủ kính = ngày bài MỚI NHẤT của chính token đó, không phải ngày
        # bài mới nhất của site: trang này chỉ đổi khi hồ sơ token đổi.
        loc.append((f"{BASE}/{TU_KINH_DUONG}", max(str(f["date"]) for f, *_ in bai_tk)))
    loc.append((f"{BASE}/du-lieu/", ngay_moi))
    loc += [(f"{BASE}/bai/{s}/", f["date"]) for f, s, *_ in bai]
    # Bản thử KHÔNG sinh hai file này — lý do đầy đủ ở chỗ khai `BAN_THU`. Tóm tắt:
    # mọi `<loc>` dựng từ `BASE`, nên sitemap của bản thử khai ra URL của trang THẬT.
    if not BAN_THU:
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in loc)
            + "</urlset>\n", encoding="utf-8")
        (OUT / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    # 🔴 Xác 31/07/2026: hai file này KHÔNG do build sinh ra, nhưng `--out` bị dọn sạch
    # mỗi lần dựng ⇒ mọi lần build đều XOÁ chúng, im lặng. `CNAME` mất là mất tên miền
    # blockpinned.com; `.nojekyll` mất là GitHub Pages bật Jekyll và nuốt mọi thư mục
    # bắt đầu bằng dấu gạch dưới. Lần này bắt được ở bước xem `git status` TRƯỚC khi
    # push, không nhờ cổng nào ⇒ sinh chúng ở đây để không phải bắt bằng mắt lần nữa.
    # Hiện vật của bài — đưa lên site để câu "tự kiểm lại" có thứ để tải về. Không có
    # bước này thì mục nguồn chỉ trỏ vào một đường dẫn trong máy của người viết, tức
    # một lời hứa không ai thực hiện được (xác 31/07: 5 con trỏ như vậy trên bài #7).
    kho = next((k for k in (ROOT.parent / "blockpinned" / "data", ROOT.parent / "data")
                if k.is_dir()), None)
    if kho is None:
        raise LoiCong(f"không tìm thấy kho hiện vật cạnh {ROOT}")
    dich = OUT / "du-lieu"; dich.mkdir(parents=True, exist_ok=True)
    # 🔴 KHÔNG đặt tên biến này là `ten` — `ten` là tên hệ màu, dùng ở dòng tổng kết
    # cuối main(); bản đầu giẫm lên nó và in ra "hệ màu 'pendle_buy_tie_….json'".
    for ten_hv in HIEN_VAT:
        f = kho / ten_hv
        if not f.is_file():
            raise LoiCong(f"hiện vật đã khai nhưng không có: {f}")
        shutil.copy2(f, dich / ten_hv)
    than_du_lieu = trang_du_lieu_v3(kho) if BO_CUC == "v3" else trang_du_lieu(kho)
    (dich / "index.html").write_text(trang(
        "Dữ liệu thô — BlockPinned", than_du_lieu, t, "..", muc="du-lieu/", mat="page-du-lieu",
        meta={"mo_ta": "File JSON thô đứng sau các bài: tải về, mở ra, đếm lại. Mỗi file "
                       "mang sẵn một dòng nói nó là gì và vòng đo nào của nó đã hỏng.",
              "duong": "/du-lieu/", "anh": "avatar-800.png", "loai": "website",
              "tieu_de_og": "Dữ liệu thô đứng sau bài"}),
        encoding="utf-8")
    print(f"  ✓ du-lieu/  ·  {len(HIEN_VAT)} hiện vật + trang danh sách")

    (OUT / "CNAME").write_text(BASE.split("//")[1] + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    # cổng 1 + 4 chạy LẠI trên HTML đã sinh: nếu khuôn tự nhét chữ cấm thì phải bắt
    for f in OUT.rglob("*.html"):
        txt = f.read_text(encoding="utf-8")
        cong_ngon_ngu(txt, str(f.relative_to(OUT)))
        cong_ngoi_xung(txt, str(f.relative_to(OUT)))
        cong_danh_dau(txt, str(f.relative_to(OUT)))
        cong_lien_ket(txt, str(f.relative_to(OUT)), OUT, f)

    # Đếm cổng lấy từ chính danh sách, không gõ tay: bản cũ ghi cứng "6/6" và nó thành
    # sai ngay lần thêm cổng thứ bảy — cùng họ "một con số viết ra rồi không ai đếm lại".
    # 🔴 Dòng tổng phải khai BỐ CỤC, không chỉ hệ màu. Bản đầu chỉ in hệ màu, nên một
    # lượt `--bo-cuc v3` in ra y hệt lượt D2 — người đọc log không phân biệt được hai
    # bản dựng khác hẳn nhau. Đó đúng họ lỗi §2c mà file này vừa vá ở cổng ngôn ngữ:
    # máy chạy đúng, in dòng xanh, mà dòng xanh nói về một vật khác.
    print(f"  ✓ index.html\n✅ {len(bai)} bài · hệ màu '{ten}' · bố cục '{BO_CUC}' · "
          f"{len(TEN_CONG)}/{len(TEN_CONG)} cổng PASS ({' · '.join(TEN_CONG)})")


if __name__ == "__main__":
    try:
        main()
    except LoiCong as e:
        sys.exit(f"\n🔴 CỔNG CHẶN — không sinh site:\n     {e}\n")
