---
title: Dashboard báo buyback bằng 0, hợp đồng đang giữ 144.388 PENDLE
date: 2026-07-31
mau: 🟡
ghim: Ethereum · block #25.650.178 (31/07/2026 03:34:35 UTC) · cửa sổ #25.553.408 → #25.650.178 · trang dữ liệu Pendle đọc cùng lúc
mo_ta: Cột buyback của Pendle trả 0 cho hai kỳ gần nhất. Trên chain, hợp đồng buyback giữ 144.388,02 PENDLE vào qua 65 giao dịch và chưa chuyển ra — hai con số nhìn hai chặng khác nhau.
anh: card-pendle-buyback.png
kenh_x: https://x.com/blockpinned/status/2083065438943244720
---

**Trang dữ liệu của Pendle: buyback kỳ gần nhất = 0.**

**Hợp đồng buyback trên chain: 144.388 PENDLE.**

Hai con số này không mâu thuẫn. Chúng đang nhìn hai chặng khác nhau của cùng một đường tiền — và nếu chỉ đọc con số đầu, bạn sẽ kết luận sai về con số thứ hai.

Đường tiền có hai bước: hợp đồng buyback gom PENDLE qua nhiều giao dịch nhỏ, rồi chuyển phần đã gom sang sPendle trong một giao dịch. Trong **12 đợt** đo được từ 13/02 tới 17/07, cả 12 đợt đều có cấu trúc đó.

Cột trên trang dữ liệu phản ánh bước thứ hai. Bước thứ nhất thì không ai nhìn — nên đo nó.

Tại block **25.650.178** (10h34 ngày 31/07, 03:34:35 UTC), cửa sổ từ block **25.553.408**, ngay sau lần chuyển gần nhất:

- **65** giao dịch đưa PENDLE vào hợp đồng — tổng **144.388,016375**
- **0** lượt chuyển ra
- số dư hợp đồng bằng đúng vào trừ ra, **khớp tới wei**

## 144.388 PENDLE đó có thật sự được mua không?

Token nằm trong ví không tự chứng minh nó được mua. Nên mở cả 65 giao dịch ra đọc: cả 65 đều gọi **cùng một hàm** của hợp đồng đó, đều có **USDT đi ra**, **PENDLE đi vào**, và ít nhất một **sự kiện swap** trong cùng giao dịch.

Nhưng đồng thời chưa phải nhân quả. Nên nối thêm một bước: PENDLE rời một địa chỉ vừa phát sự kiện swap, rồi tới hợp đồng, trong chính giao dịch đó. Nối được **119.039,61 PENDLE — 82,44%**.

Phần **17,56%** còn lại **chưa nối được bằng phép thử này**. Nhiều khả năng vì danh sách loại pool chưa phủ hết — log của các giao dịch này chứa ít nhất sáu topic AMM mà bộ lọc bốn loại không nhận diện được — nhưng "nhiều khả năng" không phải một phép đo. Nên con số đúng để nhớ là: **ít nhất 82,44% lượng PENDLE này đến thẳng từ một lượt swap** — con số sàn, không phải toàn phần.

| phép thử | hỏi gì | kết quả |
|---|---|---|
| vòng 1 | địa chỉ **gửi** token có tự phát sự kiện swap không | **0/65** — hỏi sai chỗ: sự kiện swap do **pool** phát, người gửi là router |
| vòng 2 | trong cùng giao dịch có swap không, hợp đồng có chi tài sản khác không | **65/65** — nhưng đây mới là **đồng thời** |
| vòng 3 | PENDLE có rời một địa chỉ vừa phát swap rồi tới hợp đồng không | **82,44%** lượng · **1/65** giao dịch nối kín |

## Còn ô 0 kia đang bỏ sót cái gì

Đếm bước thứ hai từ block 0: endpoint trả về **12** lượt chuyển sang sPendle; truy vấn trang kế tiếp trả về **0** kết quả, thử ở cả cỡ trang 1.000 lẫn 50. Khoảng cách giữa các lần: **11,5–17,1 ngày**.

| ngày | block | PENDLE | cách lần trước |
|---|---|---|---|
| 13/02 | 24.447.170 | 256.295,28 | — |
| 27/02 | 24.547.032 | 173.301,79 | 13,9 |
| 13/03 | 24.647.427 | 196.891,65 | 14,0 |
| 27/03 | 24.746.717 | 140.582,29 | 13,9 |
| 10/04 | 24.846.394 | 196.115,03 | 13,9 |
| 27/04 | 24.969.306 | 287.935,30 | **17,1** |
| 08/05 | 25.051.665 | 110.443,77 | **11,5** |
| 22/05 | 25.148.172 | 142.392,18 | 13,4 |
| 05/06 | 25.249.416 | 218.235,05 | 14,1 |
| 19/06 | 25.350.280 | 131.832,08 | 14,1 |
| 03/07 | 25.449.465 | 239.840,40 | 13,8 |
| 17/07 | 25.553.407 | 149.086,56 | 14,5 |

Bảng lịch sử trên trang dữ liệu cũng có **12 ô**. Hai ô mới nhất bằng 0. **Chín** ô ghép được với một lượt chuyển on-chain theo khối lượng. **Một** ô không ghép được với lượt nào — nhãn 24/02, giá trị 203.883,65; chỗ đó tôi chưa giải thích được, và ghi ra đây thay vì bỏ qua cho bảng đẹp.

Trong chín cặp đã ghép, tính theo ngày UTC, ngày trên bảng đứng **trước** ngày chuyển **17 ngày ở tám cặp, 20 ngày ở một cặp**.

Nếu kỳ này lệch như chín kỳ kia, nhãn **14/07** ứng với một lượt chuyển rơi vào **31/07 đến 03/08**. Vậy ô 0 chưa đủ để kết luận không có PENDLE đang chờ: tại block đo, hợp đồng vẫn giữ 144.388,02 và chưa chuyển đi đâu.

Chu kỳ ngay trước có cùng chuỗi sự kiện: **63** giao dịch đưa PENDLE vào từ 14/07 tới 17/07, không lượt ra nào trong lúc gom, rồi **một** giao dịch chuyển toàn bộ phần đã gom sang sPendle — vào bằng ra, khớp tuyệt đối.

## Một câu đã bị chặn trước khi lên bài

Bản nháp viết: *"ô nhãn 30/06 hiển thị 149.086, trùng khối lượng lượt chuyển 149.086,56 ngày 17/07 sau khi làm tròn"*. Hai chỗ sai. Thứ nhất, 149.086,56 làm tròn ra **149.087**. Thứ hai, một phép đo cũ đã xếp ô 30/06 là khớp với một nguồn **khác** — tổng của đợt phân phối theo Merkle, lệch 5,4e-8 — chứ không khớp lượt chuyển, vốn lệch 0,565.

Rộng hơn: cột buyback trên trang dữ liệu **không phải một đại lượng duy nhất**. Đối chiếu 11 kỳ cho 5 kỳ gần nguồn Merkle, 2 kỳ gần lượt chuyển, 2 kỳ không phân định được. Nên bài này **không** nói cột đó "đếm" gì, và không dùng nó làm thước đo khối lượng. Nó chỉ dùng quan hệ **ngày**.

## Phép đo dừng ở đây

144.388,02 PENDLE đã vào hợp đồng và chưa chuyển sang sPendle trong cửa sổ đo. Nó **không** chứng minh lượt chuyển tiếp theo chắc chắn xảy ra — nên phải ghi trước, trước khi biết kết quả.

## Dự đoán có hạn kiểm: 04/08

Trong **11 khoảng cách** giữa 12 lượt chuyển từ 13/02 tới 17/07, khoảng dài nhất là **17,1 ngày**. Tính từ 17/07, biên đó là **03/08**.

Hết ngày **04/08**, nếu không có PENDLE nào đi từ hợp đồng buyback sang sPendle, thì dự đoán *"kỳ này không vượt khoảng dài nhất đã đo"* đã sai. Điều đó **chưa đủ** để kết luận chương trình đã dừng — nó chỉ nói kỳ này dài hơn mọi kỳ trước.

Nếu trước lượt chuyển sang sPendle mà tổng PENDLE đi từ hợp đồng tới các đích **khác** đạt 144.388,02, thì giả thuyết *"số dư đang chờ chuyển sang sPendle"* phải rút lại. Chuyển **một phần** thì chưa xác nhận được gì — khi đó phải báo riêng lượng đã chuyển, lượng còn lại và đích nhận.

Tới hạn, kết quả đăng tại đúng trang này, kể cả khi nó ngược với bài.

## Cách tự kiểm lại

Ba địa chỉ:

| vai | địa chỉ |
|---|---|
| token PENDLE | `0x808507121B80c02388fAd14726482e061B8da827` |
| hợp đồng buyback | `0x9e08C5499F953C6297a7755bcbcED383B606896b` |
| sPendle | `0x999999999991E178D52Cd95AFd4b00d066664144` |

- Mở endpoint dữ liệu sPENDLE của Pendle: trường tổng kết kỳ gần nhất đang là **0**, và hai ô mới nhất của bảng lịch sử — nhãn **28/07** và **14/07** — cũng là 0.
- Lọc chuyển khoản của token PENDLE với đích là hợp đồng buyback, từ block **25.553.408** tới **25.650.178**. Cộng lại, rồi hỏi số dư hợp đồng. Ba con số phải khớp.
- Mở bất kỳ giao dịch nào trong danh sách 65 sẽ thấy ít nhất một sự kiện swap, PENDLE vào hợp đồng và USDT ra khỏi hợp đồng, trong cùng giao dịch.

Ba cái bẫy công cụ gặp ngay trong lượt đo này, ghi ra để bạn không mất thời gian:

- Endpoint của Pendle trả **403** với thư viện mặc định; phải đặt User-Agent trình duyệt. Code nuốt lỗi sẽ in ra bảng rỗng, và bảng rỗng đọc rất giống "không có buyback nào".
- Mảng lịch sử xếp **mới trước**. Lấy hai phần tử cuối là đọc hai kỳ **cũ nhất**.
- Một nhà cung cấp RPC phổ biến chặn truy vấn log quá **10 block** ở gói miễn phí, và trả lỗi chứ không trả danh sách rỗng.

Phép đo neo vào **địa chỉ** hợp đồng. Cụm "sPENDLE buyback contract" chỉ là tên Pendle dùng trong tài liệu, không phải nhãn chain tự cung cấp.

## Ba số 0 trong bài này, và không số nào nói cái nó có vẻ nói

Ngày 28/07, đọc đúng ô 0 đó, tôi suýt viết *"buyback đã dừng thật"*. Lần đo đầu của phần "có phải mua không" trả về **0 swap**, vì nó hỏi sai chỗ phát sự kiện. Và lượt nối cuối cùng trả về **1/65**, vì bộ lọc pool chưa đủ rộng.

Cả ba số 0 đều đến từ giới hạn của câu hỏi, không từ Pendle. Bài này tồn tại vì cả ba đều bị kiểm lại trước khi thành kết luận.

Không phải lời khuyên đầu tư. Các số tại block 25.650.178 là mốc cố định, không đổi khi có block mới; số dư hiện tại có thể khác ở các block sau, và dữ liệu trên endpoint có thể được Pendle cập nhật.
