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
for _p in (ROOT.parent / "template", ROOT):
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
NGUON_ASSET = {
    "favicon-16.png":  "logo/final",
    "favicon-32.png":  "logo/final",
    "avatar-800.png":  "logo/final",
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
            "thuộc tính số", "xem trước", "đo lại", "hạn", "ghi trước", "liên kết",
            "fact"]

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


def render(md: str, o: str) -> str:
    lines, out, i = md.split("\n"), [], 0
    while i < len(lines):
        ln = lines[i]

        if not ln.strip():
            i += 1
            continue

        if ln.startswith("```"):                                    # khối code
            lang_ = ln[3:].strip()
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j]); j += 1
            if j >= len(lines):
                raise LoiCong(f"khối ``` không đóng — {o}")
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
                r"^(```|#{1,3}\s|\||-\s|\d+\.\s|---$)", lines[i].lstrip()):
            para.append(lines[i]); i += 1
        out.append(f'<p>{inline(" ".join(x.strip() for x in para), o)}</p>')

    return "\n".join(out)


def bang(blk: list[str], o: str) -> str:
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in blk]
    if len(rows) < 2 or not all(set(c) <= set("-: ") for c in rows[1]):
        raise LoiCong(f"bảng thiếu dòng ngăn cách '|---|' — {o}")
    head = "".join(f"<th>{inline(c, o)}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{inline(c, o)}</td>" for c in r) + "</tr>"
                   for r in rows[2:])
    return f'<div class="cuon"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


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
@media(max-width:640px){nav.dieu a:not(.tai){display:none}}

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
  ol.tt-ds .chip{grid-row:auto;justify-self:start;margin-bottom:3px}}

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

/* ── HAI CỬA: track record + facts. Cỡ thẻ = lời khai về mức quan trọng ── */
.cua{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:32px 0 0}
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
)


def css(t: dict) -> str:
    """Tầng nhìn của site. Khối TOKEN sinh từ hệ màu; phần còn lại là hằng CSS_THAN.

    Vì sao tách hai: thân CSS không có chỗ nào cần nội suy, mà để nó trong f-string
    thì mọi dấu ngoặc nhọn phải nhân đôi — một dấu quên là một luật CSS chết trong
    im lặng. Tách ra thì thân viết như CSS thật.

    🔴 Nền mặc định THEO MÁY người đọc (prefers-color-scheme). Nút đổi nền chỉ ghi
    đè bằng data-theme; tắt JS thì trang vẫn có đủ hai nền. Đó là ràng buộc cũ của
    site (BRIEF-web.md §110) và nó vẫn đứng — nút là phần THÊM, không phải phần chịu tải.
    """
    v = {**MAC_DINH_HE, **t}
    sang = (f"--bg:{v['paper']};--bg2:{v['bg2']};--card:{v['card']};--inset:{v['inset']};"
            f"--ink:{v['ink']};--muted:{v['muted']};--faint:{v['faint']};"
            f"--line:{v['line']};--line-soft:{v['line_soft']};--accent:{v['accent']};"
            f"--c-xn:{v['xn']};--c-song:{v['song']};--c-sua:{v['sua']};"
            f"--c-bac:{v['bac']};--c-cho:{v['cho']};"
            f"--nut-nen:{v['ink']};--nut-chu:{v['card']};color-scheme:light;")
    toi = (f"--bg:{v['ink']};--bg2:{v['bg2_toi']};--card:{v['card_toi']};--inset:{v['inset_toi']};"
           f"--ink:{v['paper']};--muted:{v['muted_toi']};--faint:{v['faint_toi']};"
           f"--line:{v['line_toi']};--line-soft:{v['line_soft_toi']};--accent:{v['accent_toi']};"
           f"--c-xn:{v['xn_toi']};--c-song:{v['song_toi']};--c-sua:{v['sua_toi']};"
           f"--c-bac:{v['bac_toi']};--c-cho:{v['cho_toi']};"
           f"--nut-nen:{v['paper']};--nut-chu:{v['ink']};color-scheme:dark;")
    return (f":root{{{sang}--display:'{v['display']}',{BODY_FONT},sans-serif;"
            f"--body:'{v['display']}',{BODY_FONT},sans-serif;"
            f"--mono:'JetBrains Mono',ui-monospace,monospace;"
            f"--dw:{v['dw']};--gian-ten:{v['gian_ten']}}}\n"
            f"@media (prefers-color-scheme:dark){{:root:not([data-theme=\"sang\"]){{{toi}}}}}\n"
            f":root[data-theme=\"toi\"]{{{toi}}}\n"
            + CSS_THAN)


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
TOKEN_TEN = {"UNI": "Uniswap", "LDO": "Lido", "HYPE": "Hyperliquid", "PENDLE": "Pendle"}

# Tủ kính hiện mở cho ĐÚNG MỘT token, khai ở đây; toàn bộ nội dung trang sinh từ dữ
# liệu, nên đổi dòng này là trang tự dựng lại cho token khác. Kèm SÀN: dưới 3 bài thì
# chặn — một tủ kính hai bài trưng ra ít hơn cái tên của nó hứa.
TU_KINH = "UNI"
TU_KINH_SAN = 3
TU_KINH_DUONG = f"token/{TU_KINH.lower()}/"

# Mục trên thanh điều hướng — dựng từ ĐÂY, không gõ tay ở từng trang. Trang nào chưa
# tồn tại thì main() tắt mục đó: cổng ⑪ (liên kết) sẽ chặn build nếu một mục trỏ vào
# thư mục không có index.html, và đó là hành vi đúng.
MUC_DIEU_HUONG = [("", "Sổ gốc"), ("facts/", "Facts"),
                  ("track-record/", "Track record"), (TU_KINH_DUONG, "Token"),
                  ("du-lieu/", "Dữ liệu")]
CO_TRANG = {"facts/": False, "track-record/": False, TU_KINH_DUONG: False, "du-lieu/": False}

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
        lo=document.getElementById('loc-lo'), dangLoc=null;
    var ap=function(loc){
      var n=0;
      dong.forEach(function(d){
        var hien = loc==='het' ? true
                 : loc==='doi' ? d.getAttribute('data-doi')==='1'
                 : d.getAttribute('data-st')===loc;
        d.hidden=!hien; if(hien)n++;
      });
      nut.forEach(function(b){
        b.setAttribute('aria-pressed',b.getAttribute('data-loc')===loc?'true':'false');
      });
      if(lo)lo.textContent=n+(n===1?' dòng':' dòng')+' đang hiện';
      dangLoc=loc;
    };
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
    return ('<nav class="dieu">' + "".join(ra)
            + '<button class="nut-nen" id="nut-nen" type="button" '
              'title="Đổi nền sáng/tối" aria-label="Đổi nền sáng/tối">☀ / ☾</button></nav>')


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


def trang(tieu_de: str, than: str, t: dict, goc: str = "", meta: dict = None,
          muc: str = "") -> str:
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
    xt = f"""<meta name="description" content="{ihtml.escape(m.get('mo_ta', ''), quote=True)}">
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
    nap = "".join(f'<link rel="preload" as="font" type="font/woff2" crossorigin '
                  f'href="{g}/font/{f}">' for f in FONT_NAP_TRUOC)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ihtml.escape(tieu_de)}</title>
{xt}
{nap}
<link rel="icon" type="image/png" sizes="32x32" href="{g}/anh/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{g}/anh/favicon-16.png">
<style>{font_face(goc)}{css(t)}</style>
<script>{JS_NEN}</script></head><body>
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
    for m in re.finditer(r'href="([^"]+)"', txt):
        h = ihtml.unescape(m.group(1)).strip()
        if not h or h.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        dich = (goc / h.lstrip("/")) if h.startswith("/") else (tep.parent / h)
        dich = dich.split("#")[0] if isinstance(dich, str) else pathlib.Path(str(dich).split("#")[0])
        if dich.is_file() or (dich / "index.html").is_file():
            continue
        raise LoiCong(f'href nội bộ không tới đâu: "{h}" — {o}')


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
      <span class="chip {cls}">{c['status']}</span></h3>
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
        f'<span class="chip {TRANG_THAI[c["status"]][0]}">{c["status"]}</span>'
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
            f'<ol class="tt-ds" id="tt-ds" data-loc-vung="doi">{hang}</ol></div>')


def cua_vao(gt: list, facts: list) -> str:
    """Hai CỬA lớn thay hai dòng link chữ.

    User 06/08, chỉ vào đúng hai dòng đó: *"cái này nên làm bự lên, thành 2 ô đẹp để
    giới thiệu mỗi ô"*. Và đó là một lỗi bố cục thật, không phải gu: `/track-record/`
    với `/facts/` là hai trang mạnh nhất site có — một trang chở những lần dán số ra
    TRƯỚC khi biết đáp án, một trang chở những phát biểu kiểm lại được bằng đúng một
    lệnh. Trước bản này cả hai nằm dưới dạng hai dòng gạch chân, cùng cỡ chữ với chú
    thích, trôi giữa hai khối lớn. Cỡ chữ trên trang là một lời khai về mức quan trọng,
    và lời khai đó đang nói ngược nội dung.

    Số trên mỗi cửa đọc thẳng từ nguồn của trang nó dẫn tới, không gõ tay — hai chỗ
    cùng giữ một con số là hai chỗ sẽ trôi lệch (`RULES.md §13`).
    """
    if not gt and not facts:
        return ""
    o = []
    if gt:
        xong = sum(1 for c in gt if c["status"] != "ĐANG ĐỨNG")
        o.append(
            f'<a class="cua-o" href="track-record/">'
            f'<span class="k">Track record</span>'
            f'<span class="t">Tôi ghi trước một con số — rồi dán kết quả ngay cạnh nó</span>'
            f'<span class="g">Chở cả những lần tôi sai và những lần chưa tới ngày. Một bảng '
            f'chỉ chở lần đúng thì nó nói về tôi, không nói về đối tượng.</span>'
            f'<span class="n"><b>{len(gt)}</b> lần ghi trước<i></i>'
            f'<b>{xong}</b> đã có kết quả</span>'
            f'<span class="mui" aria-hidden="true">→</span></a>')
    if facts:
        o.append(
            f'<a class="cua-o" href="facts/">'
            f'<span class="k">Facts</span>'
            f'<span class="t">Mỗi mục một con số, một block, một lệnh để bạn tự đọc lại</span>'
            f'<span class="g">Không cần tin tôi: chép lệnh, dán vào máy bạn, đọc ra đúng con '
            f'số đó. Ra số khác cũng là một kết quả — và tôi muốn biết.</span>'
            f'<span class="n"><b>{len(facts)}</b> fact<i></i>mỗi cái một lệnh chạy lại được</span>'
            f'<span class="mui" aria-hidden="true">→</span></a>')
    return f'<div class="cua" data-hien>{"".join(o)}</div>'


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
    co = sorted(((c["han"], s, t, c) for s, t, c in moi if c.get("han")), key=lambda x: x[0])
    if not co:
        return ""
    hang = "".join(
        f'<li><span class="ngay" data-han="{h}">{h[8:10]}/{h[5:7]}/{h[0:4]}</span>'
        f'<a href="bai/{s}/#{c["id"]}">{c["id"]}</a> — {ihtml.escape(c["han_ghi"])}</li>'
        for h, s, t, c in co)
    return (f'<h2 id="sap-phan-dinh">Sắp phân định</h2>'
            f'<p class="dan">Claim tự đặt ngày. Tới ngày đó là có kết quả, và nếu tôi trễ '
            f'thì dòng dưới đây tự đổi thành ĐÃ TỚI HẠN.</p>'
            f'<ul class="han">{hang}</ul>')


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
            for k in ("cau", "chan"):
                for re_, ten in lang.FACT_KY_THUAT:
                    m = re_.search(str(f[k]))
                    if m:
                        raise LoiCong(f"{o} ({fid}) khuôn v2: '{k}' dính {ten}: "
                                      f"{m.group(0)!r} — tầng kỹ thuật nằm ở 'lenh' và "
                                      f"reply, thân bài phải đọc được bởi người đầu tư "
                                      f"chứng khoán chưa chạm crypto")


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
    hang = []
    for f in co:
        card = f.get("card") or {}
        ng = str(f.get("ngay", "")).strip()
        kicker = str(card.get("kicker") or f.get("doi_tuong") or "FACT").strip()
        figure = str(card.get("figure") or "").strip()
        label = str(card.get("label") or "").strip()
        chan = str(f["chan"]).strip()
        kc = f["khoang_cach"]
        dau = f'{ihtml.escape(kicker)}{" · " + vn_ngay(ng) if ng else ""}'
        # Fact chưa có card thì KHÔNG dựng panel rỗng — panel rỗng là một ô trống to
        # giữa trang, tệ hơn hẳn một khối chữ đủ bề ngang.
        fig = (f'<div class="f-fig"><span class="f-kicker">{dau}</span>'
               f'<span class="f-num">{ihtml.escape(figure)}</span>'
               + (f'<span class="f-lab">{ihtml.escape(label)}</span>' if label else "")
               + '</div>') if figure else ""
        o_chan = ("" if chan.upper() == "KHÔNG CÓ" else
                  f'<div class="f-box chan"><span class="k">Fact này KHÔNG nói</span>'
                  f'<span class="v">{ihtml.escape(chan)}</span></div>')
        p_ng = (f'<p class="tro">{ihtml.escape(str(f["nguon"]))}</p>'
                if str(f.get("nguon", "")).strip() else "")
        hang.append(f"""<article class="fact" id="{ihtml.escape(str(f['id']))}">
  <div class="f-top{' co-fig' if fig else ' mot-cot'}">
    {fig}
    <div class="f-body">
      {'' if fig else f'<p class="f-kicker">{dau}</p>'}
      <p class="f-cau">{ihtml.escape(str(f['cau']))}</p>
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
    return (f'<h1>Một con số, một block, một lệnh để bạn tự kiểm</h1>'
            f'<div class="dem"><span class="to">{len(co)}</span> fact · mới nhất trước</div>'
            f'<p class="dan">Fact ngắn hơn bài: không lập luận dài, chỉ một phép đo đứng '
            f'một mình. Mỗi mục ghi rõ <b>đo tại block nào</b>, <b>lệnh nào đọc lại được</b>, '
            f'và — quan trọng không kém — <b>nó KHÔNG nói điều gì</b>. Cái nào cần giải thích '
            f'dài hơn một dòng thì nó là một bài.</p>'
            f'<section class="so">{"".join(hang)}</section>')


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
        hang.append(f"""<article class="tr {cls}">
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
    return (f'<h1>Tôi ghi trước, rồi kết quả ra sao</h1>'
            f'<div class="dem"><span class="to">{len(co)}</span> lần ghi trước &nbsp;·&nbsp; '
            f'<b>{len(xong)}</b> đã có kết quả &nbsp;·&nbsp; <b>{len(cho)}</b> đang chờ</div>'
            f'<p class="dan">Mỗi dòng dưới đây là một con số hoặc một ngưỡng tôi dán ra '
            f'<b>trước khi biết đáp án</b>, kèm chỗ đã dán để người khác kiểm được ngày. '
            f'Bảng này chở cả những lần tôi <b>sai</b> và cả những lần <b>chưa có kết quả</b> — '
            f'nếu nó chỉ chở lần đúng thì nó nói về tôi, không nói về đối tượng. Bộ sinh trang '
            f'chặn build nếu một dòng đã được phân định mà thiếu kết quả.</p>'
            f'<section class="so">{"".join(hang)}</section>')


def dai_bai(bai_list: list, tien_to: str) -> str:
    """Dải bài cuộn NGANG — dùng chung cho trang chủ và tủ kính token.

    Một khuôn, hai chỗ gọi: hai bản chép của cùng một thẻ là hai bản sẽ trôi lệch, và
    lần trôi đó sẽ lộ ra ở chỗ tệ nhất — thẻ bài, thứ người ta nhìn trước khi bấm.
    `tien_to` là đường về thư mục bài, khác nhau theo độ sâu trang gọi.
    """
    the = "".join(
        f'<a class="bai" href="{tien_to}bai/{s}/">'
        f'<span class="d">{f["mau"]} {vn_ngay(str(f["date"])[:10])}</span>'
        f'<span class="t">{ihtml.escape(f["title"])}</span>'
        f'{thanh_mini(dm, n)}'
        f'<span class="s">{n} claim — {sg}</span></a>'
        for f, s, n, sg, dm in bai_list)
    return (f'<section class="khu-bai" data-hien>'
            f'<div class="khu-dau"><h2 id="bai">Bài</h2>'
            f'<div class="dieu-rail">'
            f'<button class="rn" type="button" data-rail="-1" aria-label="Lùi một thẻ">←</button>'
            f'<button class="rn" type="button" data-rail="1" aria-label="Tới một thẻ">→</button>'
            f'</div></div>'
            f'<div class="rail-boc"><div class="rail" id="rail" tabindex="0" role="region" '
            f'aria-label="Danh sách bài — cuộn ngang">{the}</div></div>'
            f'<p class="rail-goi">{len(bai_list)} bài · vuốt ngang, hoặc bấm mũi tên</p></section>')


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

    hang = "".join(
        f'<li class="tt {TRANG_THAI[c["status"]][0]}" data-st="{TRANG_THAI[c["status"]][0]}" '
        f'data-doi="{0 if c["status"] == "ĐANG ĐỨNG" else 1}">'
        # 🔴 Hộp lưới nằm trong một <span> BÊN TRONG <summary>, không phải trên chính
        # <summary>. Đo 06/08 trên Chrome: đặt `display:grid` thẳng lên summary thì
        # phần đang ĐÓNG của <details> vẫn được dựng và nằm luôn trong hộp summary —
        # mỗi dòng cao 720px thay vì 161px, cả trang 15.652px. Trình duyệt không báo
        # gì; lộ ra ở ảnh chụp khổ điện thoại của cổng preview.
        f'<details class="tu-so"><summary><span class="tt-hop">'
        f'<span class="chip {TRANG_THAI[c["status"]][0]}">{c["status"]}</span>'
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
        for s, tieu, c in claims_t)

    tu_kiem = (f'<b>{n_do}</b> dòng gọi lại được bằng đúng một lệnh — mở dòng đó ra là có '
               f'nút bấm, và nó đọc chain thật ngay lúc bạn bấm. ')
    if n_kd:
        tu_kiem += (f'<b>{n_kd}</b> dòng khai sẵn vì sao trình duyệt không gọi lại được. ')
    tu_kiem += (f'{con} dòng còn lại là phép quét trên một khoảng block: cách dựng lại nằm '
                f'ngay trong ô ĐIỀU GÌ BÁC BỎ của chính dòng đó — mở ra là thấy.')

    return (f'<p class="crumb">Tủ kính token · {ma}</p>'
            f'<h1>{ten} — mọi con số kênh này đã ghim, và câu nào còn đứng</h1>'
            f'<p class="dan">Bài sống theo ngày; hồ sơ sống theo đối tượng. Trang này gom mọi '
            f'khẳng định đã đăng về {ten} về một chỗ, giữ nguyên trạng thái hiện tại của từng '
            f'câu — kể cả những câu đã đổ. Bấm một dòng để mở block nó được đọc ra và điều gì '
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
        f'data-loc="{TRANG_THAI[k][0]}" data-tip="{k} · {n}/{tong}"></span>'
        for i, (k, n) in enumerate(co))
    # 🔴 Chip là NÚT, không phải nhãn: nó vừa là chú giải của thanh (bắt buộc — năm
    # trạng thái không phân biệt nổi bằng hue, `NOTES §1`), vừa là bộ lọc của danh sách
    # claim đứng ngay dưới. Tắt JS thì nút không làm gì và chú giải vẫn đọc đủ.
    chip = "".join(
        f'<button class="lg {TRANG_THAI[k][0]}" type="button" data-loc="{TRANG_THAI[k][0]}" '
        f'aria-pressed="false"><span class="sw"></span>{k} <span class="n">{n}</span></button>'
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

    bai, moi_claim, token_cua = [], [], {}

    for md_path in sorted(CONTENT.glob("posts/*.md"), reverse=True):
        o = f"content/posts/{md_path.name}"
        fm, body_md = front(md_path.read_text(encoding="utf-8"), o)
        cj = md_path.with_suffix(".claims.json")
        if not cj.exists():
            raise LoiCong(f"thiếu {cj.name} — mọi bài phải có sổ claim, đó là lý do site này tồn tại")
        claims = json.loads(cj.read_text(encoding="utf-8"))["claims"]

        # cổng chạy TRƯỚC khi in ra bất cứ thứ gì (LAUNCH.md:126)
        kho = body_md + "\n" + json.dumps(claims, ensure_ascii=False) + "\n" + json.dumps(fm, ensure_ascii=False)
        cong_ngon_ngu(kho, o)
        cong_ngoi_xung(kho, o)
        cong_claim(claims, o)
        cong_cau_truc(fm, body_md, claims, o)
        cong_do_lai(claims, o)
        cong_han(claims, o)
        cong_ghi_truoc(claims, o)

        slug_ = md_path.stem
        # Khai token là BẮT BUỘC — nó là khoá của hồ sơ theo đối tượng, và một bài
        # không khai thì nó lặng lẽ rơi khỏi tủ kính của chính token nó nói về.
        tk = fm.get("token", "").strip()
        if tk not in TOKEN_TEN:
            raise LoiCong(f"front matter 'token' thiếu hoặc lạ ({tk!r}) — {o}. "
                          f"Đang biết: {', '.join(sorted(TOKEN_TEN))}. Token mới thì "
                          f"thêm vào TOKEN_TEN kèm tên đầy đủ, đừng viết tắt tuỳ ý")
        token_cua[slug_] = tk
        ho_so = (f'<a class="toi phu" href="../../{TU_KINH_DUONG}">Hồ sơ {TOKEN_TEN[tk]} →</a>'
                 if tk == TU_KINH and CO_TRANG[TU_KINH_DUONG] else "")
        # 🔴 THỨ TỰ TRANG LÀ CÓ CHỦ Ý, đừng đảo lại: sổ claim ĐỨNG TRƯỚC bài viết.
        # Bản đầu đặt bài lên trước và màn hình đầu tiên giống hệt Telegram — người
        # bấm vào từ X/TG đã đọc bài rồi, đưa lại bài là không cho họ lý do ở lại.
        # Bài vẫn đăng đủ dạng native trên X/TG (LAUNCH.md:152), ở đây nó là THAM CHIẾU.
        than = (f"<h1>{ihtml.escape(fm['title'])}</h1>"
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
                + render(body_md, o) + "</section>")
        d = OUT / "bai" / slug_
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            trang(f"{fm['title']} — BlockPinned", than, t, "../..",
                  meta={"mo_ta": fm["mo_ta"].strip(), "duong": f"/bai/{slug_}/",
                        "anh": fm.get("anh"), "loai": "article",
                        "tieu_de_og": fm["title"]}),
            encoding="utf-8")
        # 🔴 Tóm tắt CHỈ đếm "đang đứng" là NÓI DỐI THEO CHIỀU TỰ HẠ MÌNH: bài #1 có
        # 4 claim (1 xác nhận · 1 đứng · 2 đã sửa) mà dòng cũ in "4 claim, 1 đang đứng"
        # ⇒ đọc ra như 3/4 đã đổ. Lỗi này chỉ xuất hiện khi có claim ở trạng thái thứ ba;
        # với N=1 bài toàn "đang đứng" thì công thức cũ trông đúng. Nay in ĐỦ PHỔ.
        dem = {k: sum(1 for c in claims if c["status"] == k) for k in TRANG_THAI}
        tom = " · ".join(f"{n} {k.lower()}" for k, n in dem.items() if n)
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
    than_i = (f'<h1>{ihtml.escape(fm_i["tagline"])}</h1>' + render(body_i, "content/index.md")
              + bang_diem(moi_claim)
              + cua_vao(gt, facts)
              + sap_phan_dinh(moi_claim)
              + dai_bai(bai, ""))
    if not 60 <= len(fm_i.get("mo_ta", "").strip()) <= 200:
        raise LoiCong("content/index.md thiếu 'mo_ta' 60–200 ký tự — trang chủ là chỗ "
                      "hay bị dán link nhất, để trắng là mất ở đúng cửa")
    (OUT / "index.html").write_text(
        trang("BlockPinned — số nào cũng truy ngược được", than_i, t,
              meta={"mo_ta": fm_i["mo_ta"].strip(), "duong": "/", "anh": "avatar-800.png",
                    "loai": "website", "tieu_de_og": "BlockPinned — số nào cũng truy ngược được"}),
        encoding="utf-8")

    # ── TỦ KÍNH token ────────────────────────────────────────────────────────────
    # Dựng SAU vòng lặp vì nó cần cả bài lẫn claim của token; bật/tắt thì đã quyết
    # trước vòng lặp (thanh điều hướng cần biết sớm). Hai con số phải khớp nhau, và
    # lệch thì CHẶN: nếu lượt quét front matter nói "đủ bài" mà lượt dựng thật lại
    # đếm ra ít hơn sàn, nghĩa là hai lượt đọc cùng một thư mục ra hai kết quả.
    bai_tk = [x for x in bai if token_cua[x[1]] == TU_KINH]
    if CO_TRANG[TU_KINH_DUONG]:
        if len(bai_tk) < TU_KINH_SAN:
            raise LoiCong(f"tủ kính {TU_KINH} bật nhưng chỉ dựng được {len(bai_tk)} bài "
                          f"(sàn {TU_KINH_SAN}) — hai lượt đọc cùng thư mục ra hai kết quả")
        claims_tk = [(s, t, c) for s, t, c in moi_claim if token_cua[s] == TU_KINH]
        d_tk = OUT / "token" / TU_KINH.lower()
        d_tk.mkdir(parents=True, exist_ok=True)
        (d_tk / "index.html").write_text(trang(
            f"{TOKEN_TEN[TU_KINH]} — hồ sơ {TU_KINH} — BlockPinned",
            trang_token(TU_KINH, bai_tk, claims_tk), t, "../..", muc=TU_KINH_DUONG,
            meta={"mo_ta": f"Mọi khẳng định BlockPinned đã đăng về {TOKEN_TEN[TU_KINH]}: "
                           f"{len(claims_tk)} câu trên {len(bai_tk)} bài, mỗi câu ghim tại "
                           f"block đã đo, kèm điều gì sẽ bác bỏ nó và trạng thái hiện tại.",
                  "duong": f"/{TU_KINH_DUONG}", "anh": "card-uni-100usd.png", "loai": "website",
                  "tieu_de_og": f"{TOKEN_TEN[TU_KINH]} — mọi con số đã ghim, và câu nào còn đứng"}),
            encoding="utf-8")
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
            trang_ghi_truoc(moi_claim), t, "..", muc="track-record/",
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
        (d_f / "index.html").write_text(trang(
            "Facts — BlockPinned", trang_facts(facts), t, "..", muc="facts/",
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
    if CO_TRANG[TU_KINH_DUONG]:
        # lastmod của tủ kính = ngày bài MỚI NHẤT của chính token đó, không phải ngày
        # bài mới nhất của site: trang này chỉ đổi khi hồ sơ token đổi.
        loc.append((f"{BASE}/{TU_KINH_DUONG}", max(str(f["date"]) for f, *_ in bai_tk)))
    loc.append((f"{BASE}/du-lieu/", ngay_moi))
    loc += [(f"{BASE}/bai/{s}/", f["date"]) for f, s, *_ in bai]
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
    (dich / "index.html").write_text(trang(
        "Dữ liệu thô — BlockPinned", trang_du_lieu(kho), t, "..", muc="du-lieu/",
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
    print(f"  ✓ index.html\n✅ {len(bai)} bài · hệ màu '{ten}' · "
          f"{len(TEN_CONG)}/{len(TEN_CONG)} cổng PASS ({' · '.join(TEN_CONG)})")


if __name__ == "__main__":
    try:
        main()
    except LoiCong as e:
        sys.exit(f"\n🔴 CỔNG CHẶN — không sinh site:\n     {e}\n")
