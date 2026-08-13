---
title: Một market Morpho định giá chỗ thế chấp 269,78 đô thành 269.782.183.315.703 đô vì hai ô decimals của oracle được khai 8/8 trong khi hai token thật là 18/6
tieu_de_ngan: 269 đô tài sản thế chấp, oracle đọc thành 269 nghìn tỷ đô
token: MORPHO
date: 2026-08-13
mau: 🟡
ghim: Ethereum block 25.656.287 (31/07/2026 23:58:59Z, tức 06h58 ngày 01/08 giờ Việt Nam). Market USDC/PAXG 0x8eaf7b29…06c9, LLTV 91,5%, oracle 0xdd1778f7…1101. Tham số constructor giải từ giao dịch tạo oracle 0x1adb1aa3… tại block 20.640.779. Giá feed đọc tại block chốt: PAXG/USD 4.527,35690715 và USDC/USD 0,99982398.
mo_ta: Giá thật của chỗ thế chấp là 269,78 đô. Con số giao thức dùng để quyết định thanh lý là 269.782.183.315.703 đô. Hai thang đơn vị lệch nhau đúng một nghìn tỷ lần.
anh: card-morpho-oracle-thang.png
kenh_x: https://x.com/blockpinned/status/2087842291696406808
doc_lai: Hai con số giá là ảnh chụp tại block chốt; block khác cho giá khác. Vế lệch 10¹² thì không đổi vì nó nằm trong tham số cố định lúc tạo oracle. Bài đo một market, một chain, một block — chưa quét còn bao nhiêu market khác có oracle lệch thang. Vế "không địa chỉ nào ở cả hai bên" chưa loại được khả năng nhiều địa chỉ cùng một chủ.
---

**Có một thị trường cho vay trên Morpho mà giao thức đang nhìn vào và thấy một vị thế cực kỳ an toàn. Chỗ thế chấp đứng sau khoản vay đó, tính theo giá thật, đáng 269,78 đô. Con số mà giao thức dùng để quyết định thanh lý là 269.782.183.315.703 đô.**

Một nghìn tỷ lần chênh lệch. Không phải làm tròn, không phải bug hiển thị — hai con số này ra từ hai thang đơn vị khác nhau, và giao thức chỉ biết một trong hai.

Vấn đề nằm ở chỗ: con số sức khoẻ mà bạn nhìn vào để quyết định có bỏ tiền vào một thị trường cho vay hay không là con số **được tính ra**, chứ không phải **đo được**. Ở đây phép tính đó chạy sai thang — mà nhìn vào thì không thấy gì bất thường.

## Oracle phải quy hai thứ về cùng một thang trước khi so được

Morpho Blue không tự biết giá. Mỗi thị trường trỏ tới một oracle trả lời đúng một câu: *một đơn vị tài sản thế chấp đáng bao nhiêu đơn vị tài sản đi vay.*

Để trả lời được, oracle phải đưa **số lượng token** và **giá từ feed** về **cùng một thang đơn vị**, rồi mới so được giá trị thế chấp với khoản nợ. Blockchain không lưu "1,5 PAXG" mà lưu một số nguyên rất dài, nên số chữ số quy đổi — thứ token khai ra dưới tên **decimals** — là tham số oracle phải nhận lúc được tạo.

Ở oracle của thị trường này, decimals được khai bằng tay và khai lệch, nhưng contract vẫn trả về giá bình thường; sai lệch đó không tự làm phép đọc giá thất bại.

## Khai một đằng, thật một nẻo

Giải mã tham số từ giao dịch tạo oracle tại block 20.640.779: decimals của tài sản thế chấp khai **8**, của tài sản đi vay khai **8**.

Đọc từ chính hai token: **PAXG 18** và **USDC 6**.

PAXG bị khai **thiếu 10** chữ số decimals, còn USDC bị khai **thừa 2**. Trong công thức quy thang của oracle, hai sai lệch này cộng lại tạo chênh lệch **12 chữ số**.

Hệ số quy thang oracle đang dùng, đọc on-chain, là **10³⁶**. Dựng lại bằng công thức trong mã nguồn đã verify của chính loại oracle này, với decimals thật thì nó phải là **10²⁴**. Giá trị thế chấp vì vậy bị đọc cao gấp **10¹²**.

## Giao thức thấy gì

Thế chấp còn lại trong thị trường là **0,059578845182231419 PAXG** — khoảng sáu phần trăm một ounce vàng token hoá, đáng **269,78 đô**.

Tỷ lệ vay trên thế chấp mà giao thức đọc được tại block chốt: **0,00000384**. Ngưỡng thanh lý của thị trường: **91,5%**. Tại block chốt, giao thức vì vậy đọc vị thế này như cực kỳ xa ngưỡng thanh lý — ở đúng trạng thái tại block đó, khoảng cách số học tới ngưỡng là **238.240 lần**.

Trên Ethereum, từ lúc thị trường được tạo đến block 25.656.287, phép đếm sự kiện thanh lý cho ra **0 lượt**.

## Thế còn con số một tỷ đô trên sổ?

Khoản nợ ghi trên sổ của thị trường này là **1.036.144.267,44 đô**. Con số đó **không phải** quy mô thiệt hại.

Thị trường nằm ở mức sử dụng 100% và lãi suất chạm mức tối đa của mô hình, nên phần lãi dồn theo thời gian. Nhưng lãi chỉ **vào sổ mỗi lần có người chạm vào thị trường** — con số trên là số đã ghi ở lần chạm gần nhất, 18h43 ngày 05/06/2026 (11:43:35Z), tức đứng yên **56 ngày** trước block chốt.

Đối soát toàn bộ lịch sử dòng vốn: số tiền thật đã rời tay người cho vay là **95.013,24 đô**; **1.036.049.254,20 đô** còn lại là lãi ghi sổ — **99,991%**.

Hai con số phải đọc cạnh nhau: **1.036.144.267,44 đô trên sổ** và **95.013,24 đô vốn gốc thật**, cách nhau **10.905 lần**.

Vậy phần chênh giữa 95.013,24 đô vốn gốc và 269,78 đô thế chấp là gì? Đó là **phần vốn gốc hiện không được tài sản thế chấp bảo đảm tương xứng**. Bài này chưa gọi nó là khoản lỗ đã thực hiện — người vay vẫn có thể trả nợ bằng nguồn khác.

## Không phải bug của Morpho core — đây là mặt trái của market permissionless

Morpho Blue cho phép tạo thị trường cho vay theo mô hình permissionless: ở cấp giao thức không có bước phê duyệt tập trung cho từng market mới. Đó là một lựa chọn thiết kế, và nó có hai mặt — bên được là cặp tài sản và **oracle** do chính người tạo thị trường chọn, không phải chờ ai xét duyệt; bên mất là sổ cái sẽ ghi trung thực một tham số hỏng, và ghi rất lâu.

Tham số sai là của người tạo thị trường đó. Bài này không nói gì về ý định và không đặt tên ai — nó chỉ đọc những con số nằm sẵn trên chain.

## Cách tự kiểm từng số

Mọi số đọc tại **block 25.656.287** — 06h58 ngày 01/08/2026 giờ Việt Nam (31/07 23:58:59Z), chain Ethereum. Thị trường `0x8eaf7b29…06c9`, oracle `0xdd1778f7…1101`.

Bốn thứ đọc thẳng từ oracle:

- `BASE_FEED_1()` trả `0x7c4561bb…c0c`, `latestAnswer` **4.527,35690715** (PAXG/USD, 8 decimals)
- `QUOTE_FEED_1()` trả `0xc5774412…88d`, `latestAnswer` **0,99982398** (USDC/USD, 8 decimals)
- `SCALE_FACTOR()` trả **10³⁶**
- tham số constructor, giải mã từ giao dịch `0x1adb1aa3…` tại block 20.640.779: `baseTokenDecimals = 8` và `quoteTokenDecimals = 8`

Giá oracle dùng là base chia quote: `4.527,35690715 / 0,99982398` = **4.528,153952808773** USDC mỗi PAXG. Phải chia cho feed thứ hai — chỉ nhân với feed đầu sẽ ra 269,73, lệch 0,02% và không khớp giá on-chain.

Giá trị thế chấp thật: `0,059578845182231419 × 4.528,153952808773` = **269,78218** USDC. Giá trị giao thức dùng: `269.782.183.315.703,145327` USDC — đúng số trên nhân 10¹².

Công thức quy thang, lấy từ mã nguồn đã verify: `SCALE_FACTOR = 10^(36 + quoteTokenDec + quoteFeedDec − baseTokenDec − baseFeedDec)`. Với tham số đã khai (8 và 8) ra **10³⁶**, khớp đúng số đọc on-chain; với decimals thật (6 và 18) ra **10²⁴**.

Tỷ lệ vay trên thế chấp: `1.036.144.267,436096 / 269.782.183.315.703,145` = **0,0000038407** so với ngưỡng **0,915**, tức khoảng cách tới ngưỡng là **238.240 lần**.

Tách sổ khỏi vốn gốc: đối soát toàn bộ lịch sử dòng vốn gốc và phần lãi ghi sổ của thị trường cho vốn gốc ròng **95.013,238325**, lãi ghi sổ **1.036.049.254,20**, tổng khớp sổ **1.036.144.267,436096**. Trường `lastUpdate` của thị trường bằng **1780659815**, tức 05/06/2026 11:43:35Z.

Sổ cái sự kiện toàn bộ lịch sử thị trường đến block chốt: `Supply` **19**, `Withdraw` **13**, `Borrow` **12**, `Repay` **6**, `SupplyCollateral` **9**, `WithdrawCollateral` **2**, `Liquidate` **0**. Phép đếm dừng khi trang cuối ngắn hơn giới hạn 1.000 bản ghi mỗi trang, tức đã cạn chứ không bị cắt.

## Một chỗ bài này chưa trả lời được

Thị trường có **7 địa chỉ cấp vốn** và **8 địa chỉ đi vay**; không địa chỉ nào xuất hiện ở cả hai tập. Dữ liệu này loại được vòng tự vay bằng **cùng một địa chỉ**, nhưng **chưa loại được nhiều địa chỉ cùng một chủ**. Muốn đóng vế đó cần dữ kiện ở tầng chủ thể — nguồn nạp chung, đích rút chung, hoặc quan hệ điều khiển — và bài này không có dữ liệu đó.

## Thao tác mang về

Trước khi tin con số sức khoẻ hay tỷ lệ vay của một thị trường cho vay permissionless: đọc hệ số quy thang của oracle mà thị trường đó trỏ tới, đọc decimals thật của hai token, rồi so hai cái với nhau.

Ba lời gọi. Ở ca này, chúng biến một vị thế được giao thức đọc là "khoẻ" thành **95.013,24 đô vốn gốc thật đứng sau 269,78 đô tài sản thế chấp** — trong khi dòng sổ vẫn hiện 1.036.144.267,44 đô.

Và một câu rộng hơn: permissionless không làm phần thẩm định biến mất — nó đẩy phần đó ra khỏi core protocol.

*Không phải lời khuyên đầu tư.*
