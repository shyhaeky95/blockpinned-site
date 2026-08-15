---
title: Nếu hợp đồng thực thi được chạy, Sky mở cấu hình buyback 27,77 triệu USD mỗi năm và giao cho ví vận hành 4/6 điều chỉnh trong giới hạn tới 350 triệu USD mỗi năm
tieu_de_ngan: SKY: 27,77 triệu hay giới hạn 350 triệu USD mỗi năm?
reading_layout: centered
token: SKY
date: 2026-08-15
mau: 🟡
ghim: Ethereum block 25.760.209 (2026-08-15T11:40:59Z). Executive spell 0xB26b9d89776aa9E74ddA0e86e916413def03F59b đã lên hat, đã schedule, chưa cast; eta = 1786891307. SBE BEAM 0xc8b61d211D3D03A630Fb09199E17953a8c9749a9; ví vận hành 0x869294B42B80f99CF3Bdac0F44abddAd6cD41330 có 6 owner, threshold 4.
mo_ta: Nếu hợp đồng thực thi chạy, buyback mở ở 27,77 triệu USD mỗi năm; cùng cơ chế cho ví 4/6 điều chỉnh trong giới hạn 0–350 triệu.
anh: card-sky-sbe-beam.png
kenh_x: https://x.com/blockpinned/status/2088599713167937958
doc_lai: Đây là ảnh chụp trước khi hợp đồng thực thi được chạy. Ba con số 27,77 triệu USD buyback mỗi năm, 22,72 triệu USD thưởng USDS mỗi năm và 1,08 triệu SKY mỗi ngày được tính từ mã nguồn đã xác minh; chúng chưa phải trạng thái hiện hành. Bốn dự đoán chỉ được phân định theo điều kiện ghi trong từng claim, không dời mốc sau khi biết kết quả.
---

**Sky vừa thông qua một lá phiếu thay đổi cơ chế mua lại token của chính mình. Nếu hợp đồng thực thi được chạy đúng mã đã công bố, tiền mua SKY tăng từ 13,72 lên 27,77 triệu USD mỗi năm. Nhưng cùng lá phiếu đó còn mở một khung rộng hơn nhiều: ví vận hành 4/6 có thể điều chỉnh khoản mua lại trong giới hạn từ 0 tới 350 triệu USD mỗi năm, mỗi 30 phút một lần.**

Hai con số 27,77 và 350 triệu không phải hai dự báo cạnh tranh. Một số là cấu hình mặc định sau khi thực thi; số kia là giới hạn mà cơ chế quản trị đặt cho ví vận hành.

## Ba con số sau khi hợp đồng thực thi chạy

Mã nguồn đã xác minh chốt ba thay đổi ban đầu:

- tiền giao thức dùng để mua SKY ngoài thị trường tăng từ **13,72 lên 27,77 triệu USD mỗi năm**
- kênh trả thưởng USDS cho người stake, tắt từ tháng 11/2025, bật lại ở mức **22,72 triệu USD mỗi năm**
- lượng SKY rời kho giao thức giảm từ **3,19 xuống 1,08 triệu SKY mỗi ngày**

Đây là số tính từ chỉ thị trong mã nguồn, chưa phải trạng thái hiện hành tại block ghim. Chúng chỉ lên sổ cái nếu hợp đồng thực thi được chạy.

## Con số 27,77 triệu trở thành một cái núm

Sau khi hợp đồng được chạy, bộ ba tham số quyết định tốc độ mua lại — lượng mua mỗi lượt, tỷ lệ dành cho mua lại và khoảng cách giữa hai lượt — có thể được ví vận hành điều chỉnh mà không cần một executive vote mới và không đi qua 48 giờ chờ của GSM.

Ví đó có **6 chủ sở hữu, cần 4 chữ ký**, đọc tại block 25.760.209. Mỗi lần điều chỉnh phải cách lần trước ít nhất **1.800 giây**, tức 30 phút.

Giới hạn tốc độ lớn nhất trong mã nguồn tương đương **350 triệu USD mỗi năm**. Tỷ lệ dành cho mua lại nhận giá trị từ **0% tới 100%**. Vì vậy cùng một cơ chế có thể đưa khoản mua lại lên giới hạn, và cũng có thể đưa nó về 0.

Để có tỷ lệ so sánh, ảnh 30,1 ngày kết thúc tại block 25.700.475 cho ba mốc: thu nhập của Sky tương đương khoảng **155 triệu USD mỗi năm**; khoảng đệm của cổng buyback là **123,6 triệu USD**; khối lượng giao dịch hữu cơ trên pool Uniswap v2 SKY/USDS mà giao thức dùng để mua tương đương khoảng **144 triệu USD mỗi năm**. Mức 350 triệu bằng **2,42 lần** khối lượng của riêng pool đó.

Con số 144 triệu chỉ đo một pool, nên là mức ít nhất quan sát được chứ không phải toàn bộ thị trường SKY.

## Bốn giới hạn vẫn nằm trong tay cơ chế quản trị

Ví vận hành không có quyền tự đặt lại luật chơi:

- ví chỉ đổi tham số bên trong giới hạn; muốn đổi chính giới hạn vẫn cần executive vote
- 30 phút là khoảng nghỉ giữa hai lần đổi; mã còn đặt mức tối thiểu 300 giây giữa hai lượt mua
- ngưỡng kích hoạt phiên đấu giá không nằm trong nhóm tham số giao cho ví
- tại block ghim, địa chỉ triển khai hợp đồng không còn quyền trên hợp đồng đó

Đây vì thế không phải câu chuyện quản trị mất quyền. Cơ chế quản trị dựng hàng rào; ví vận hành được xoay các tham số bên trong hàng rào đó.

## Trạng thái lúc bài được đăng

Tại block **25.760.209**, hợp đồng thực thi đã lên \`hat\` với **7,02 tỷ SKY** ủng hộ, cao hơn hợp đồng trước **3,30 tỷ SKY**. Nó đã được schedule nhưng chưa cast. \`eta\` là 21h41 ngày 16/08 giờ Việt Nam; thời điểm sớm nhất trong khung thực thi là 21h00 ngày 17/08.

Nghĩa là lá phiếu đã qua cửa biểu quyết. Phần chưa biết là hợp đồng có được chạy đúng cửa hay không.

## Bốn dự đoán ghi trước

Bản X và reply được đăng lúc 19h12 ngày 15/08, trước khi biết kết quả. Dự đoán đầu không kèm điều kiện; ba dự đoán sau chỉ được chấm nếu hợp đồng thực thi được chạy:

1. Hợp đồng được chạy trong khoảng **21h01 ngày 17/08 tới 03h27 ngày 18/08** giờ Việt Nam, tương ứng 14:01Z–20:27Z ngày 17/08. Khoảng này suy từ 8 lá phiếu gần nhất; cả 8 đều trễ 4,584 tới 4,852 ngày tính từ ngày ghi trên hợp đồng.
2. Nếu được chạy, số thứ tự chương trình trả thưởng đi từ **15 lên 16** trong cùng giao dịch.
3. Nếu được chạy, tổng đã rút của chương trình 15 sau khi chốt nằm trong khoảng **89.167.349 tới 90.021.114 SKY**.
4. Nếu được chạy, khoảng cách giữa hai lượt trả thưởng giữ nguyên **601.200 giây**.

Không đổi khoảng dự đoán sau khi đã thấy kết quả. Nhật ký phân định sẽ được nối ngay trong sổ claim của trang này.

## Cách tự kiểm

**Ví vận hành.** Gọi \`getThreshold()\` trên \`0x869294B42B80f99CF3Bdac0F44abddAd6cD41330\` phải ra 4; \`getOwners()\` trả 6 địa chỉ.

**Giới hạn của SBE BEAM.** Mã nguồn đã xác minh nằm tại \`0xc8b61d211D3D03A630Fb09199E17953a8c9749a9\`. Đọc hàm \`set\` và các nhánh \`file\` để thấy bốn giới hạn, khoảng nghỉ 1.800 giây và mức tối thiểu 300 giây.

**Tốc độ mua hiện tại.** Gọi \`kbump()\` trên Kicker và \`hop()\` trên Splitter, rồi tính \`kbump × 86.400 ÷ hop\`.

**Pool giao thức dùng để mua.** Gọi \`pair()\` trên Flapper trả \`0x2621cc0b3f3c079c1db0e80794aa24976f0b9e3c\`; \`token0\` và \`token1\` của pool là SKY và USDS. Khối lượng 144 triệu USD mỗi năm được dựng từ log \`Swap\` của chính pool này trong ảnh 30,1 ngày.

**Trạng thái lá phiếu.** Gọi \`hat()\` trên MCD_ADM tại block ghim trả \`0xB26b9d89776aa9E74ddA0e86e916413def03F59b\`. Trên hợp đồng đó, \`eta() = 1786891307\` và \`done() = 0\`.

## Cái gì bác được bài này

Nếu mã nguồn đã xác minh không chứa các giới hạn được mô tả, hoặc ví vận hành không phải 4 trong 6 tại block ghim, phần mô tả cơ chế phải rút. Nếu hợp đồng được cast ngoài khoảng 14:01Z–20:27Z ngày 17/08, dự đoán đầu sai. Nếu hợp đồng được chạy mà số thứ tự chương trình, tổng đã rút hoặc khoảng cách trả thưởng khác ba số đã ghi, claim tương ứng sai và được sửa riêng tại chỗ.

Nếu hợp đồng không được chạy, ba dự đoán có điều kiện không được tính là đúng hay sai; chúng giữ trạng thái chờ điều kiện.

Sai ở đâu, BlockPinned sửa ngay tại đó.

*Không phải lời khuyên đầu tư.*
