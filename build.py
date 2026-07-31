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
    # 🟢 HỆ ĐÃ CHỐT 29/07 — hướng THE BENCHMARK. Nguồn duy nhất:
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
    # bài #7 — cùng quy ước đặt tên theo NỘI DUNG, không theo ordinal (lý do ở ghi
    # chú bài #6 ngay trên). Ca này còn là bằng chứng thứ hai cho quy ước đó: ordinal
    # bài #7 suýt phải đổi vì chân X bị dán nhầm bản nháp rồi xoá + đăng lại 31/07.
    "card-pendle-buyback.png": "png",
}

# Thân bài LUÔN là Be Vietnam Pro ở cả hai hệ — đó là ràng buộc NGÔN NGỮ
# (font dựng cho dấu tiếng Việt), không phải lựa chọn thương hiệu.
BODY_FONT = "Be Vietnam Pro"


# Tên các họ cổng — dùng cho dòng in ra, và là chỗ DUY NHẤT đếm chúng.
TEN_CONG = ["ngôn ngữ", "cấu trúc", "claim", "ngôi xưng", "đánh dấu",
            "thuộc tính số", "xem trước", "đo lại", "hạn", "ghi trước", "liên kết"]

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

def css(t: dict) -> str:
    return f"""
/* ── TOKEN: đổi hệ = sửa ĐÚNG khối này. Nguồn gốc: template/build_cards.py (hệ đỏ
   đang công khai) và template/reference/…Logo-Explorations (hệ verdigris đề xuất).
   Hai bản có thể trôi lệch — đây là mối nối đã biết, không phải đã đồng bộ. ── */
:root{{
  --paper:{t['paper']}; --ink:{t['ink']}; --accent:{t['accent']};
  --muted:{t['muted']}; --line:{t['line']};
  --display:'{t['display']}',system-ui,sans-serif;
  --body:'{BODY_FONT}',system-ui,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
  --dw:{t['dw']}; --gian-ten:{t['gian_ten']};
}}
@media (prefers-color-scheme:dark){{
  /* 🔴 accent PHẢI đổi MÃ, không chỉ đảo paper/ink. Bản khai hệ cấm #94382A trên nền
     tối — đo được 2,15:1, rớt cả ngưỡng 3,0 của đồ hoạ phi-văn-bản. Bản đầu của file
     này đảo hai màu nền mà giữ nguyên accent, tức tự vi phạm đúng điều cấm ② trong
     im lặng: không cổng nào của site nhìn tới cặp (màu, nền) ở chế độ tối. */
  :root{{ --paper:{t['ink']}; --ink:{t['paper']}; --accent:{t['accent_toi']};
          --line:{t['line_toi']}; --muted:{t['muted_toi']}; }}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:17px;line-height:1.72;-webkit-text-size-adjust:100%}}
.khung{{max-width:680px;margin:0 auto;padding:0 22px}}
a{{color:var(--ink);text-decoration:underline;text-decoration-color:var(--accent);
  text-underline-offset:3px;text-decoration-thickness:1.5px}}
a:hover{{color:var(--accent)}}
/* URL dài trong bài (github.com/…/issues/8242) không có chỗ ngắt tự nhiên ⇒ nó
   nong CẢ TRANG rộng ra và mọi thứ khác tràn theo. Đo được bằng preview.py --do-tran. */
p,li,td,th,h1,h2,h3,figcaption{{overflow-wrap:break-word}}
a,code{{word-break:break-word}}

/* đầu trang: MARK chính thức nằm trong .mark (hằng số MARK_SVG), tô bằng var(--accent)
   nên nó tự đổi mã theo nền — đó là cách duy nhất giữ được điều cấm ② của bản khai hệ */
header.dau{{border-bottom:1.5px solid var(--ink);margin-bottom:38px}}
.dau .khung{{display:flex;align-items:center;gap:13px;padding-top:22px;padding-bottom:18px;flex-wrap:wrap}}
.mark{{width:21px;height:21px;flex:none}}
.mark svg{{display:block;width:100%;height:100%}}
.mark path{{fill:var(--accent)}}
.ten{{font:var(--dw) 20px/1 var(--display);letter-spacing:var(--gian-ten);text-decoration:none}}
.tag{{font:500 11.5px/1 var(--mono);letter-spacing:.1em;color:var(--muted);margin-left:auto}}
@media(max-width:540px){{.tag{{margin-left:0;width:100%;order:3}}}}

h1{{font:var(--dw) clamp(27px,5.4vw,37px)/1.22 var(--display);letter-spacing:-.005em;margin:0 0 16px}}
h2{{font:var(--dw) 22px/1.32 var(--display);letter-spacing:.005em;margin:44px 0 12px;
  padding-top:14px;border-top:1.5px solid var(--line)}}
h3{{font:600 16.5px/1.4 var(--body);margin:28px 0 8px}}
p{{margin:0 0 17px}}
strong{{font-weight:650}}
hr{{border:0;border-top:1.5px solid var(--line);margin:34px 0}}
ul,ol{{margin:0 0 17px;padding-left:21px}} li{{margin-bottom:7px}}
code{{font:500 .875em var(--mono);background:color-mix(in srgb,var(--ink) 7%,transparent);
  padding:.1em .35em;word-break:break-word}}
pre{{background:color-mix(in srgb,var(--ink) 7%,transparent);padding:15px;overflow-x:auto;
  border-left:3px solid var(--accent);margin:0 0 17px}}
pre code{{background:none;padding:0;font-size:12.5px;line-height:1.62}}

.cuon{{overflow-x:auto;margin:0 0 19px;-webkit-overflow-scrolling:touch}}
table{{border-collapse:collapse;font-size:14.5px;min-width:100%}}
th,td{{padding:8px 13px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}}
th{{font:600 11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);border-bottom:1.5px solid var(--ink)}}

.meta{{font:500 12.5px/1.65 var(--mono);color:var(--muted);margin:0 0 30px}}
.meta b{{color:var(--ink);font-weight:600}}

/* ── SỔ CLAIM — thứ duy nhất trên trang được phép nổi ── */
.so{{margin:52px 0 0;padding-top:22px;border-top:3px solid var(--ink)}}
.so>p.dan{{font-size:15px;color:var(--muted);margin-bottom:26px}}
.claim{{border:1.5px solid var(--line);border-left:4px solid var(--accent);
  padding:17px 19px;margin-bottom:15px;scroll-margin-top:20px}}
.claim.sua,.claim.bac,.claim.cho{{border-left-color:var(--muted)}}
.claim.xac{{border-left-width:7px}}
.claim h3{{margin:0 0 9px;font:600 16px/1.5 var(--body)}}
.claim .id{{font:600 12px var(--mono);color:var(--muted);text-decoration:none}}
.chip{{display:inline-block;font:600 11px/1 var(--mono);letter-spacing:.09em;
  padding:5px 9px;vertical-align:2px;margin-left:8px;white-space:nowrap}}
/* xac = đã bị thử và sống sót. Cùng nền accent với "đang đứng" (cả hai còn hiệu lực),
   thêm viền ink để đọc ra "có hai bên cùng ký": desk đo, đối tượng tự tính lại.
   🟡 Đây là xử lý TẠM cho tới vòng thiết kế thật — hình thức chưa qua ai duyệt. */
.chip.xac{{background:var(--accent);color:var(--paper);
  border:1.5px solid var(--ink);padding:3.5px 7.5px}}
.chip.song{{background:var(--accent);color:var(--paper)}}
.chip.sua{{background:var(--ink);color:var(--paper)}}
.chip.bac{{border:1.5px solid var(--ink);color:var(--ink);text-decoration:line-through}}
.chip.cho{{border:1.5px dashed var(--muted);color:var(--muted)}}
.dong{{font-size:14px;margin:11px 0 0;padding-left:13px;border-left:2px solid var(--line)}}
.dong .nhan{{font:600 10.5px var(--mono);letter-spacing:.1em;color:var(--muted);
  display:block;margin-bottom:3px}}
.nk{{list-style:none;padding:0;margin:13px 0 0;font-size:14px}}
.nk li{{padding:7px 0 7px 13px;border-left:2px solid var(--line);margin:0}}
.nk .d{{font:600 11.5px var(--mono);color:var(--accent);margin-right:7px}}

/* ── DÃI TRẠNG THÁI — màn hình đầu tiên, thứ X/TG không có ── */
.dai{{border:2px solid var(--ink);padding:16px 18px;margin:0 0 30px}}
.dem{{font:500 15px/1.5 var(--mono)}}
.dem .to{{font:700 27px var(--mono);color:var(--accent);vertical-align:-3px;margin-right:2px}}
.dem b.song,.dem b.xac{{color:var(--accent)}}
.khi{{font:500 12px/1.6 var(--mono);color:var(--muted);margin-top:7px}}
.toi{{display:inline-block;margin-top:12px;font:600 12.5px var(--mono);letter-spacing:.06em;
  text-decoration:none;border-bottom:2px solid var(--accent);padding-bottom:2px}}

/* ── HÌNH: claim vẽ thành trục số. Sống được — refill hạ thì chấm di chuyển ── */
.hinh{{margin:17px 0 6px;padding:0}}
.thang .hang{{margin-bottom:13px}}
.thang .nh{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  font:500 12px/1.5 var(--mono);color:var(--muted);margin-bottom:4px}}
.thang .nh b{{font:700 14px var(--mono);color:var(--ink);white-space:nowrap}}
.thang .ray{{position:relative;height:15px;background:color-mix(in srgb,var(--ink) 8%,transparent)}}
.thang .ray.tr{{height:9px;background:none}}
.thang .cot{{display:block;height:100%;background:var(--ink)}}
.thang .cot.toi{{background:var(--accent)}}
/* cu = con số ĐÃ BỊ THAY nhưng không được xoá khỏi hình — người đọc phải thấy
   cái thanh dài ngày trước đó, nếu không thì hình mất luôn phần đáng kể nhất */
.thang .cot.cu{{background:color-mix(in srgb,var(--ink) 22%,transparent)}}
.thang .vung{{position:absolute;top:0;height:9px;background:var(--accent);
  border-left:2px solid var(--accent);border-right:2px solid var(--accent);opacity:.45}}
.thang .nk2{{margin:4px 0 0;font-size:11.5px}}
.thang .nk2 b{{font-size:12px;color:var(--accent)}}
.hinh figcaption{{font:500 11px/1.5 var(--mono);color:var(--muted);margin-top:8px;
  padding-top:7px;border-top:1px solid var(--line)}}

/* điều-bác-bỏ là thứ khác biệt duy nhất của kênh này ⇒ nó phải là dòng NẶNG NHẤT
   trong khối claim, không phải một đoạn văn thường như bản đầu */
.dong.bac{{border-left:3px solid var(--accent);
  background:color-mix(in srgb,var(--accent) 7%,transparent);
  padding:9px 12px;margin-top:13px;font-size:14.5px}}
.dong.bac .nhan{{color:var(--accent)}}

.dem .phu{{font:500 12px/1.6 var(--mono);color:var(--muted);margin-top:7px;
  text-transform:none;letter-spacing:0}}
ul.diem{{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-direction:column;gap:0}}
ul.diem li{{display:grid;grid-template-columns:auto 1fr;gap:0 12px;padding:11px 0;
  border-top:1px solid var(--line);font-size:15px}}
ul.diem li:last-child{{border-bottom:1px solid var(--line)}}
ul.diem .tick{{font:600 10.5px/1.7 var(--mono);letter-spacing:.08em;text-transform:uppercase;
  border:1px solid currentColor;border-radius:2px;padding:0 5px;height:fit-content;
  white-space:nowrap}}
ul.diem .tick.xac,ul.diem .tick.bac{{color:var(--accent)}}
ul.diem .tick.sua{{color:var(--muted)}}
.dan-gt{{margin:14px 0 0;font-size:15px}}
.claim .moc{{font:500 12.5px/1.7 var(--mono);color:var(--muted);letter-spacing:.03em}}
.tro{{margin:12px 0 0;font:500 12.5px/1.6 var(--mono)}}
ul.han{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0}}
ul.han li{{padding:13px 0;border-top:1px solid var(--line);font-size:15px}}
ul.han li:last-child{{border-bottom:1px solid var(--line)}}
ul.han .ngay{{font:600 12.5px/1.7 var(--mono);letter-spacing:.04em;color:var(--accent);
  display:block;margin-bottom:3px}}
ul.han .con{{font-weight:500;color:var(--muted);margin-left:9px}}
ul.han .con.qua{{color:var(--accent);font-weight:600}}
.dolai-o{{margin-top:13px;display:flex;flex-direction:column;gap:8px}}
button.dolai{{align-self:flex-start;font:600 12.5px/1 var(--mono);letter-spacing:.06em;
  color:var(--paper);background:var(--accent);border:0;border-radius:2px;
  padding:9px 13px;cursor:pointer}}
button.dolai:hover{{filter:brightness(1.08)}}
button.dolai:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
button.dolai[disabled]{{opacity:.55;cursor:progress}}
.ketqua{{font:500 12.5px/1.65 var(--mono);color:var(--muted);
  border-left:2px solid var(--line);padding:2px 0 2px 10px}}
.ketqua b{{color:var(--ink);font-weight:600}}
.ketqua.khop{{border-left-color:var(--accent)}}
.ketqua.lech{{border-left-color:var(--accent)}}
.ketqua.loi{{border-left-color:var(--ink)}}
.nk .nguon-tro{{opacity:.72;font-size:.92em;font-style:italic}}
.ketqua .nguon{{display:block;font-size:11px;opacity:.75;margin-top:3px}}
.dong.khongdo{{border-left:3px solid var(--line);padding:9px 12px;margin-top:13px;
  font-size:14px;color:var(--muted)}}

/* bài viết là THAM CHIẾU ở trang này — hạ nhẹ xuống, không tranh chỗ với sổ claim */
.bandaydu{{margin-top:56px;padding-top:6px;border-top:3px solid var(--ink)}}
.bandaydu h2{{border-top:0;padding-top:0;margin-top:16px}}

footer{{margin-top:64px;padding:22px 0 46px;border-top:1.5px solid var(--ink);
  font:500 12px/1.75 var(--mono);color:var(--muted)}}
footer a{{color:var(--muted)}}
.bai{{display:block;padding:17px 0;border-bottom:1px solid var(--line);text-decoration:none}}
.bai .t{{font:600 18.5px/1.4 var(--body);margin-bottom:5px}}
.bai .s{{font:500 12px var(--mono);color:var(--muted)}}
"""


FONTS = ("https://fonts.googleapis.com/css2?family=Marcellus"
         "&family=Archivo:wght@600;700;800"
         "&family=Oswald:wght@500;600;700&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,650;0,700;1,400"
         "&family=IBM+Plex+Mono:wght@400;500;600&display=swap")


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


def trang(tieu_de: str, than: str, t: dict, goc: str = "", meta: dict = None) -> str:
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
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ihtml.escape(tieu_de)}</title>
{xt}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="icon" type="image/png" sizes="32x32" href="{goc or '.'}/anh/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{goc or '.'}/anh/favicon-16.png">
<style>{css(t)}</style></head><body>
<header class="dau"><div class="khung">
  <span class="mark">{MARK_SVG}</span>
  <a class="ten" href="{goc or '.'}/">BLOCK·PINNED</a>
  <span class="tag">SỐ NÀO CŨNG TRUY NGƯỢC ĐƯỢC</span>
</div></header>
<main class="khung">{than}</main>
<footer><div class="khung">
  Bản chuẩn của mọi bài. Sửa tại chỗ, không xoá.<br>
  Không phải lời khuyên đầu tư. ·
  <a href="https://x.com/blockpinned">@blockpinned</a>
</div></footer>
<script>{JS_DO_LAI}</script>
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
    out = ['<section class="so"><h2 id="so-claim">Sổ claim</h2>',
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
        out.append(f"""<article class="claim {cls}" id="{c['id']}">
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
    """
    dem = {k: [c for _, _, c in moi if c["status"] == k] for k in TRANG_THAI}
    o = " · ".join(f'<b class="{TRANG_THAI[k][0]}">{len(v)}</b> {k.lower()}'
                   for k, v in dem.items() if v)
    doi = sum(len(v) for k, v in dem.items() if k != "ĐANG ĐỨNG")

    def lien(ten: str) -> str:
        # 🔴 Nhãn phải mang NGÀY BÀI, không chỉ id claim: hai bài đều có C1, nên một dãy
        # "C1 · C1" là đọc nhầm ngay. Lỗi này chỉ lộ khi có ≥2 bài cùng trạng thái.
        return " · ".join(
            f'<a href="bai/{s}/#{c["id"]}">{s[8:10]}/{s[5:7]}·{c["id"]}</a>'
            for s, _, c in moi if c["status"] == ten)
    dong = []
    if dem["ĐÃ XÁC NHẬN"]:
        dong.append(f'<li><span class="tick xac">sống sót</span>điều-bác-bỏ đã chạy và claim '
                    f'đứng vững: {lien("ĐÃ XÁC NHẬN")}</li>')
    if dem["BỊ BÁC"]:
        dong.append(f'<li><span class="tick bac">đổ</span>claim bị chính điều-bác-bỏ của nó '
                    f'bác, và nằm nguyên trên trang: {lien("BỊ BÁC")}</li>')
    if dem["ĐÃ SỬA"]:
        dong.append(f'<li><span class="tick sua">đã sửa</span>tự đính chính, giữ lại để thấy '
                    f'lỗi: {lien("ĐÃ SỬA")}</li>')
    return (f'<h2 id="bang-diem">Bảng điểm</h2>'
            f'<div class="dem"><span class="to">{len(moi)}</span> claim &nbsp;·&nbsp; {o}'
            f'<div class="phu">{doi} trong số đó đã ĐỔI TRẠNG THÁI kể từ lúc đăng — '
            f'đó là phần X và Telegram không chở được.</div></div>'
            + (f'<ul class="diem">{"".join(dong)}</ul>' if dong else ""))


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


def trang_ghi_truoc(moi: list) -> str:
    """Trang riêng: mọi lần desk ghi trước một con số hoặc một ngưỡng, và kết quả.

    Đây là thứ khó làm giả nhất mà desk có: một con số dán công khai TRƯỚC khi biết đáp án.
    Điều kiện để bảng có nghĩa là nó chở CẢ ba trạng thái — thắng, đổ, và đang chờ. Bảng
    chỉ chở lần đúng thì nói về tác giả bảng, không nói về đối tượng.
    """
    co = sorted(((c["ghi_truoc"]["ngay"], s, t, c) for s, t, c in moi if c.get("ghi_truoc")),
                key=lambda x: x[0], reverse=True)
    xong = [x for x in co if x[3]["status"] != "ĐANG ĐỨNG"]
    cho = [x for x in co if x[3]["status"] == "ĐANG ĐỨNG"]
    hang = []
    for ngay, sl, tieu, c in co:
        g, cls = c["ghi_truoc"], TRANG_THAI[c["status"]][0]
        dang = c["status"] != "ĐANG ĐỨNG"
        moc = (f'{vn_ngay(ngay)} &nbsp;→&nbsp; {vn_ngay(g["ngay_ket"])}' if dang
               else f'{vn_ngay(ngay)} &nbsp;→&nbsp; '
                    + (f'hạn {vn_ngay(c["han"])}' if c.get("han") else "chưa có hạn"))
        kq = (f'<p class="dong bac"><span class="nhan">KẾT QUẢ · {ihtml.escape(g["ai_phan_dinh"])}</span>'
              f'{ihtml.escape(g["ket_qua"])}</p>' if dang else
              '<p class="dong"><span class="nhan">CHƯA CÓ KẾT QUẢ</span>'
              'Dòng này nằm đây từ trước khi biết đáp án. Tới hạn thì nó có kết quả, '
              'dù kết quả là tôi sai.</p>')
        hang.append(f"""<article class="claim {cls}">
  <h3><span class="chip {cls}">{c['status'] if dang else 'ĐANG CHỜ'}</span>
      <span class="moc">{moc}</span></h3>
  <p class="dong"><span class="nhan">TÔI GHI TRƯỚC</span>{ihtml.escape(g["so"])}</p>
  <p class="dong"><span class="nhan">Ở ĐÂU</span>{ihtml.escape(g["noi"])}</p>
  {kq}
  <p class="tro"><a href="../bai/{sl}/#{c['id']}">{vn_ngay(sl[:10])}·{c['id']} — {ihtml.escape(tieu)}</a></p>
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


def dai_trang_thai(claims: list, doc_lai: str) -> str:
    """Màn hình đầu tiên. Người bấm vào từ X/TG đã đọc bài rồi — thứ họ chưa biết là
    claim giờ còn đứng không. Trả lời trước, bài để sau."""
    d = {k: sum(1 for c in claims if c["status"] == k) for k in TRANG_THAI}
    o = " · ".join(f'<b class="{TRANG_THAI[k][0]}">{n}</b> {k.lower()}'
                   for k, n in d.items() if n)
    return f"""<section class="dai">
  <div class="dem"><span class="to">{len(claims)}</span> claim &nbsp;·&nbsp; {o}</div>
  <div class="khi">{ihtml.escape(doc_lai)}</div>
  <a class="toi" href="#so-claim">Xem sổ claim ↓</a>
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


def main() -> None:
    # Mặc định là hệ ĐÃ CHỐT. Bản đầu đọc argv bằng cách "có chữ verdigris ở đâu đó
    # trong argv" — thứ đó lặng lẽ đúng cho tới khi đường dẫn --out chứa chữ đó.
    ten = "benchmark"
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
    bai, moi_claim = [], []

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
        # 🔴 THỨ TỰ TRANG LÀ CÓ CHỦ Ý, đừng đảo lại: sổ claim ĐỨNG TRƯỚC bài viết.
        # Bản đầu đặt bài lên trước và màn hình đầu tiên giống hệt Telegram — người
        # bấm vào từ X/TG đã đọc bài rồi, đưa lại bài là không cho họ lý do ở lại.
        # Bài vẫn đăng đủ dạng native trên X/TG (LAUNCH.md:152), ở đây nó là THAM CHIẾU.
        than = (f"<h1>{ihtml.escape(fm['title'])}</h1>"
                + dai_trang_thai(claims, fm.get("doc_lai", ""))
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
        bai.append((fm, slug_, len(claims), tom))
        for c in claims:
            moi_claim.append((slug_, fm["title"], c))
        print(f"  ✓ bai/{slug_}/  ·  {len(claims)} claim ({tom})")

    gt = [c for _, _, c in moi_claim if c.get("ghi_truoc")]
    fm_i, body_i = front((CONTENT / "index.md").read_text(encoding="utf-8"), "content/index.md")
    cong_ngon_ngu(body_i, "content/index.md")
    cong_ngoi_xung(body_i, "content/index.md")
    ds = "".join(
        f'<a class="bai" href="bai/{s}/"><div class="t">{ihtml.escape(f["title"])}</div>'
        f'<div class="s">{f["mau"]} {f["date"]} · {n} claim — {sg}</div></a>'
        for f, s, n, sg in bai)
    than_i = (f'<h1>{ihtml.escape(fm_i["tagline"])}</h1>' + render(body_i, "content/index.md")
              + bang_diem(moi_claim)
              + ('<p class="dan-gt"><a href="ghi-truoc/">Xem đủ những lần tôi ghi trước một '
                 'con số rồi đối chiếu kết quả →</a></p>' if gt else "")
              + sap_phan_dinh(moi_claim)
              + f'<h2 id="bai">Bài</h2>{ds}')
    if not 60 <= len(fm_i.get("mo_ta", "").strip()) <= 200:
        raise LoiCong("content/index.md thiếu 'mo_ta' 60–200 ký tự — trang chủ là chỗ "
                      "hay bị dán link nhất, để trắng là mất ở đúng cửa")
    (OUT / "index.html").write_text(
        trang("BlockPinned — số nào cũng truy ngược được", than_i, t,
              meta={"mo_ta": fm_i["mo_ta"].strip(), "duong": "/", "anh": "avatar-800.png",
                    "loai": "website", "tieu_de_og": "BlockPinned — số nào cũng truy ngược được"}),
        encoding="utf-8")

    # trang /ghi-truoc/ — thứ khó làm giả nhất desk có, nên nó được một URL riêng để dán
    if gt:
        d_gt = OUT / "ghi-truoc"
        d_gt.mkdir(parents=True, exist_ok=True)
        (d_gt / "index.html").write_text(trang(
            "Tôi ghi trước, rồi kết quả ra sao — BlockPinned", trang_ghi_truoc(moi_claim), t, "..",
            meta={"mo_ta": "Mọi lần BlockPinned dán một con số hoặc một ngưỡng ra công khai "
                           "trước khi biết đáp án, kèm kết quả — cả những lần sai và những "
                           "lần chưa có kết quả.",
                  "duong": "/ghi-truoc/", "anh": "post01-card.png", "loai": "website",
                  "tieu_de_og": "Tôi ghi trước, rồi kết quả ra sao"}), encoding="utf-8")
        print(f"  ✓ ghi-truoc/  ·  {len(gt)} lần ghi trước")

    # ── sitemap + robots: điều kiện để máy tìm THẤY trang ────────────────────────
    # Thiếu hai file này thì site vẫn sống, chỉ là không ai tìm ra — đúng loại hỏng
    # KHÔNG báo lỗi. lastmod lấy từ ngày bài, không lấy giờ chạy, để hai lần dựng cùng
    # nội dung ra cùng một byte (dựng không tất định thì mọi phép so bản chép vô nghĩa).
    ngay_moi = max(f["date"] for f, *_ in bai)
    loc = [(BASE + "/", ngay_moi)]
    if gt:
        loc.append((f"{BASE}/ghi-truoc/", ngay_moi))
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
