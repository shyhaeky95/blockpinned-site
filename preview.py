#!/usr/bin/env python3
"""Chụp site ở khổ ĐIỆN THOẠI + ĐO TRÀN NGANG bằng máy.

Cùng lý lẽ với template/feed_preview.py (LAUNCH.md:88: *"Kiểm bằng feed_preview.py
trước mỗi bài, đừng đoán"*). Trang này phần lớn được đọc trên điện thoại.

🔴 VÌ SAO CÓ PHÉP ĐO TRÀN: lần render đầu, một URL dài không có chỗ ngắt
(`github.com/…/issues/8242`) nong cả trang rộng ra, và MỌI dòng chữ bị cắt mất
mép phải — kể cả tiêu đề. Nhìn ảnh mới thấy. Một trang tràn ngang trên điện
thoại là trang hỏng, mà không cổng nào của build.py nhìn tới tầng hiển thị
(đúng họ với 5 ca "tầng kênh hiển thị" ở LAUNCH.md:144 — *"cả năm đều kiểm
bằng máy được"*). Nay đo bằng scrollWidth thật trong trình duyệt thật.

Chạy:  python3 site/preview.py            → cả hai hệ màu, kèm phép đo tràn
       python3 site/preview.py verdigris  → một hệ
"""
import pathlib, re, shutil, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = pathlib.Path(__file__).parent
# 🔴 ĐỌC TÊN HỆ TỪ CHÍNH build.py, không giữ bản sao. Xác 06/08/2026: site đã sang hệ
# `d2` từ commit ac0d11b, còn dòng mặc định ở đây vẫn đứng ở `benchmark` — nghĩa là
# cổng đo tràn khổ điện thoại chạy trên một hệ ĐÃ KHAI TỬ, và mọi dòng "✓ không tràn"
# nó in ra là nói về một trang không ai truy cập. Đúng cái bẫy docstring dưới cảnh báo.
sys.path.insert(0, str(SITE))
from build import HE_MAC_DINH  # noqa: E402  (phải sau SITE, vì nó dựng đường dẫn)
OUT = SITE / "out"
SHOT = SITE / "preview"; SHOT.mkdir(exist_ok=True)
BAI = "bai/2026-07-27-defillama-uniswap-v4/index.html"
# 🔴 Chrome headless trên macOS KẸP bề rộng cửa sổ ở 500px: xin --window-size=390
# thì trang vẫn dựng ở 500 (innerWidth=500), rồi --screenshot cắt lấy 390px bên
# trái ⇒ ảnh trông như chữ bị cắt mép phải TRONG KHI trang hoàn toàn bình thường.
# Đã mất một vòng vá CSS cho một lỗi không tồn tại. Chụp đúng bề rộng trang dựng;
# khổ hẹp hơn thì đo bằng do_tran() (gói overflow:auto), không đo bằng mắt.
RONG = 500
KHUNG = [("dau", BAI, 1740, None),
         ("soclaim", BAI, 1620, "so"),      # cắt riêng sổ claim, không dựa vào cuộn theo neo
         ("chu", "index.html", 1180, None),
         # 🔴 06/08: MỌI trang phục vụ đều phải nằm ở đây. Trang nào không có trong
         # danh sách này thì cổng đo tràn KHÔNG nhìn tới, và một trang hỏng ở khổ điện
         # thoại đi ra ngoài không báo gì cả. Trước lượt này chỉ có 3 khuôn: `/facts/`,
         # `/track-record/`, `/du-lieu/` chưa lần nào được đo — ba trang, không cổng.
         ("token", "token/uni/index.html", 1500, None),
         ("muctoken", "token/index.html", 1400, None),
         ("facts", "facts/index.html", 1500, None),
         ("trackrecord", "track-record/index.html", 1500, None),
         ("dulieu", "du-lieu/index.html", 1300, None)]

# 🔴 Hai cách đo SAI đã thử và bị bác, ghi lại để không ai dựng lại:
#   ① documentElement.scrollWidth — không bao giờ nhỏ hơn viewport ⇒ là chặn dưới
#      của phép đo, không phải bề rộng trang.
#   ② body{width:360px} rồi đọc body.scrollWidth — body overflow:visible thì KHÔNG
#      có hộp cuộn, nên scrollWidth trả về đúng 360 dù con có tràn. Phép đo tự kẹp
#      chính nó và báo PASS ở mọi cấu hình (luật bằng chứng của desk §2).
# Cách đúng: gói nội dung vào một div có overflow:auto — nó CÓ hộp cuộn thật, nên
# scrollWidth phản ánh tràn thật. Kèm thủ phạm rộng nhất để báo động chỉ ra chỗ sửa.
DO_TRAN = """<script>addEventListener('load',()=>{document.fonts.ready.then(()=>{
 const w=document.createElement('div');
 w.style.cssText='width:'+WW+'px;overflow:auto';
 while(document.body.firstChild) w.appendChild(document.body.firstChild);
 document.body.appendChild(w);
 let mx=0,who='';
 for(const e of w.querySelectorAll('*')){
   if(e.closest('.cuon,pre'))continue;          // vùng cuộn ngang có CHỦ Ý, không tính
   const r=e.getBoundingClientRect();
   if(r.width&&r.right>mx){mx=r.right;who=e.tagName.toLowerCase()+(e.className?'.'+String(e.className).split(' ')[0]:'')}
 }
 const f=document.fonts.check('16px Inter')&&document.fonts.check('12px "JetBrains Mono"');
 document.body.insertAdjacentHTML('beforeend','<i id=ovf>'+w.scrollWidth+'|'+WW+'|'+Math.round(mx)+'|'+who+'|'+(f?'font':'KHONG-FONT')+'</i>');
})})</script>"""


def neo_font(html: str) -> str:
    """Đổi đường font TƯƠNG ĐỐI sang đường tuyệt đối của bản dựng.

    🔴 Vì sao bắt buộc, và nó suýt lọt: từ 06/08 font được TỰ HOST, `build.py` in ra
    `url(./font/…)` (trang gốc) và `url(../../font/…)` (trang bài) — đúng cho site
    thật. Nhưng phép đo ở đây CHÉP trang sang thư mục tạm, nên hai đường đó trỏ vào
    hư không và Chrome dựng bằng font hệ thống. Bề rộng chữ khác font là khác ⇒ cổng
    sẽ đo một trang KHÔNG PHẢI trang sắp ship, y hệt cái bẫy hệ màu `benchmark` vừa
    vá cùng ngày. Marker `KHONG-FONT` ở trên là cái bắt lần sau, nếu ai đổi cách
    sinh đường dẫn mà quên chỗ này.

    🔴 Đổi bằng REGEX, không phải hai lượt `replace` cố định: bản đầu chỉ vá
    `./font/` (trang gốc) và `../../font/` (trang bài) — nên bốn trang sâu ĐÚNG MỘT
    cấp (`/facts/`, `/track-record/`, `/du-lieu/`, `/token/`) vẫn dựng bằng font hệ
    thống. Chúng lọt được vì đúng lượt thêm chúng vào `KHUNG` cũng là lượt ĐẦU TIÊN
    chúng được đo — không có bản trước để so, nên "mới" và "hỏng" trông giống nhau.
    Và marker báo hỏng khi đó cũng không hiện ra: regex đọc nó viết `(\\w+)`, mà
    `KHONG-FONT` có dấu gạch ⇒ cổng in "không đo được" thay vì "không có font".
    """
    goc = (OUT / "font").as_uri()
    return re.sub(r"url\((?:\./|(?:\.\./)+)font/", f"url({goc}/", html)


def chrome(args, timeout=150):
    return subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu",
                           "--virtual-time-budget=9000"] + args,
                          capture_output=True, text=True, timeout=timeout)


def cat_muc(html: str, cls: str) -> str:
    """Lấy riêng <section class="cls"> và giữ nguyên khuôn trang — để chụp đúng
    khối đó mà không phải cuộn theo neo (chụp full-page bỏ qua fragment)."""
    m = re.search(rf'<section class="{cls}".*?</section>', html, re.S)
    if not m:
        sys.exit(f"không tìm thấy <section class=\"{cls}\"> — khuôn đã đổi?")
    body = re.search(r'<main class="khung">(.*?)</main>', html, re.S)
    return html.replace(body.group(1), m.group(0))


def do_tran(html: str, tmp: pathlib.Path, nhan: str) -> bool:
    """🔴 macOS chặn bề rộng cửa sổ Chrome ở ~500px: xin --window-size=390 vẫn nhận
    clientWidth 500. Đo ở 500 rồi ghi "không tràn trên điện thoại" là một phép đo
    MÙ tự xưng PASS (luật bằng chứng của desk §2). Nên ép bề rộng bằng CSS
    trên chính tài liệu, và đo ở khổ HẸP NHẤT đáng lo (360px = Galaxy S/iPhone SE).

    Giới hạn còn lại, khai ra: media query vẫn đánh giá theo cửa sổ 500px, không
    theo 360px ép. Ở đây vô hại vì mọi breakpoint của site đều ≥540px nên 360 và
    500 rơi cùng một nhánh — nhưng thêm breakpoint dưới 500 thì phép đo này mù lại.
    """
    tran = False
    for w in (360, 430):
        f = tmp / f"ovf{w}.html"
        f.write_text(neo_font(html).replace(
            "</body>", f"<script>WW={w}</script>" + DO_TRAN + "</body>"), encoding="utf-8")
        r = chrome(["--dump-dom", "--window-size=520,900", f.as_uri()], timeout=90)
        m = re.search(r'<i id="ovf">(\d+)\|(\d+)\|(\d+)\|([^|]*)\|([\w-]+)</i>', r.stdout)
        if not m:
            print(f"  ⚠ {nhan} @{w}px: không đo được — phép đo MÙ, đừng đọc là 'không tràn'")
            continue
        sw, lim, mx, who = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        if m.group(5) != "font":
            sys.exit(f"🔴 {nhan} @{w}px: trang dựng KHÔNG CÓ font thật — bề rộng chữ đo được "
                     f"là của font hệ thống, không phải của bản sắp ship. Sửa neo_font().")
        if sw > lim:
            print(f"  🔴 {nhan} @{w}px: TRÀN {sw}px > {lim}px · rộng nhất: <{who}> tới {mx}px")
            tran = True
        else:
            print(f"  ✓ {nhan} @{w}px: không tràn")
    return tran


def tu_kiem(html: str, tmp: pathlib.Path) -> None:
    """Phép đo tràn phải NỔ ĐƯỢC, không thì mọi chữ 'không tràn' bên dưới là vô nghĩa.
    Hai cách đo trước đã im lặng báo PASS ở MỌI cấu hình — chỉ lộ khi ép bằng ca này."""
    xau = html.replace('<main class="khung">',
                       '<main class="khung"><p style="overflow-wrap:normal;'
                       'word-break:normal">' + "X" * 400 + "</p>", 1)
    if xau == html:
        sys.exit("🔴 không chèn được ca thử — khuôn đã đổi, phép tự kiểm mù")
    print("  · tự kiểm dụng cụ (chuỗi 400 ký tự không chỗ ngắt — PHẢI nổ):")
    if not do_tran(xau, tmp, "    control dương"):
        sys.exit("🔴 PHÉP ĐO TRÀN KHÔNG NỔ ĐƯỢC ⇒ nó không phải control. Dừng.")


def main() -> None:
    # 🔴 Bản đầu để mặc định là ["do", "verdigris"] — tức phép đo tràn chạy trên HAI hệ
    # đã khai tử và KHÔNG bao giờ chạy trên hệ đang ship. Đúng hình dạng lỗi đã ghi hai
    # lần trong hồ sơ nhận diện: "phép thử đo một cái hình khác cái hình sắp được chốt".
    # 🔴 Và nó TÁI PHÁT ngay lần đổi hệ kế tiếp (29/07 vá tay thành "benchmark"; 06/08
    # site sang "d2" mà dòng này đứng nguyên) — vì bản vá hôm đó chép một cái TÊN sang
    # đây thay vì đọc tên từ chủ của nó. Nay đọc `build.HE_MAC_DINH`: đổi hệ ở một chỗ
    # là cổng đi theo, không có lượt vá tay nào để quên.
    hes = [sys.argv[1]] if len(sys.argv) > 1 else [HE_MAC_DINH]
    tran = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        tu_kiem((OUT / BAI).read_text(encoding="utf-8"), tmp)
        for he in hes:
            cmd = [sys.executable, str(SITE / "build.py"), "--theme", he]
            b = subprocess.run(cmd, capture_output=True, text=True)
            if b.returncode:
                sys.exit(f"build hệ '{he}' hỏng:\n{b.stdout}{b.stderr}")
            for hau, duong, cao, cat in KHUNG:
                src = OUT / duong
                html = src.read_text(encoding="utf-8")
                if cat:
                    html = cat_muc(html, cat)
                    src = tmp / f"{he}-{hau}.html"
                    src.write_text(html, encoding="utf-8")
                tran += do_tran(html, tmp, f"{he}/{hau}")
                # Chrome headless dựng theo prefers-color-scheme của máy. Chụp CẢ HAI
                # nền: hệ nhận diện là "giấy audit" (nền sáng), nhưng phần lớn người
                # đọc crypto để máy ở nền tối — không được chỉ nhìn một bên rồi chốt.
                for nen in ("toi", "sang"):
                    h = html if nen == "toi" else html.replace(
                        "@media (prefers-color-scheme:dark)",
                        "@media (prefers-color-scheme:dark) and (min-width:99999px)")
                    s = tmp / f"{he}-{hau}-{nen}.html"
                    s.write_text(neo_font(h), encoding="utf-8")
                    png = SHOT / f"{he}-{hau}-{nen}.png"
                    r = chrome([f"--screenshot={png}", f"--window-size={RONG},{cao}",
                                "--force-device-scale-factor=2", s.as_uri()])
                    if not png.exists():
                        sys.exit(f"render hỏng ({he}/{hau}/{nen}): {r.stderr[-400:]}")
                    print(f"    → preview/{png.name}")
    # Dựng lại KHÔNG tham số ⇒ nhận đúng mặc định của build.py. Dòng thông báo cũ ghi
    # cứng tên một hệ; khi mặc định đổi (29/07: 'do' → 'benchmark') nó thành một câu
    # SAI mà không lệnh nào hỏng — hệt loại "file nói dối trong im lặng" của §13.
    subprocess.run([sys.executable, str(SITE / "build.py")], capture_output=True)
    print("↩︎ out/ dựng lại bằng hệ MẶC ĐỊNH của build.py")
    if tran:
        sys.exit(f"\n🔴 {tran} khung TRÀN NGANG — trang hỏng trên điện thoại, sửa trước khi xem tiếp.")


if __name__ == "__main__":
    main()
