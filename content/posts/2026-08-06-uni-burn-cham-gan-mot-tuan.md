---
title: Biểu đồ UNI burn trên Ethereum đang chậm gần một tuần so với Robinhood Chain
token: UNI
date: 2026-08-06
mau: 🟡
ghim: Robinhood Chain block #29.174.972 · Ethereum block #25.690.453, đọc 15h58 ngày 06/08/2026 (08:58Z)
mo_ta: Robinhood Chain đã huỷ 340.000 UNI ở nguồn, nhưng trên Ethereum mới 44.000 tới địa chỉ đốt. Chênh lệch nằm ở hai hàng chờ, và một trong hai đo được là 6,44–7,41 ngày.
anh: card-rh-burn-cham-mot-tuan-muc.png
kenh_x: https://x.com/blockpinned/status/2085288243067748407
---

**Biểu đồ UNI burn trên Ethereum đang chậm gần một tuần so với Robinhood Chain.**

Gần 10 ngày, Robinhood Chain huỷ **340.000 UNI** bản Robinhood. Trên Ethereum mới **44.000** tới địa chỉ đốt — **12,9%**. Còn **296.000** chưa qua cầu.

Uniswap đốt UNI bằng phí giao dịch. Trên Robinhood Chain, contract `Firepit` gom đủ ngưỡng rồi huỷ **2.000 UNI** bản Robinhood và phát một **lệnh rút** về Ethereum. UNI gốc chỉ rời lưu thông khi lệnh đó được thực thi ở đầu kia.

Quét từ block đầu tới nay: **170 lượt huỷ**, và **cả 170 lệnh rút đều nhắm địa chỉ đốt** — đọc từng thông điệp, không suy từ mẫu. Trên Ethereum, mới **22 lệnh** được thực thi.

Phần chênh **296.000 UNI** đã bằng **24,3%** toàn bộ lượng UNI Uniswap đốt trong tháng 7.

## Vì sao lệch: hai hàng chờ, không phải một

**Hàng chờ thứ nhất — gom đủ ngưỡng.** Khoảng cách giữa hai lệnh rút liên tiếp: nhanh nhất **0 phút**, trung vị **71 phút**, chậm nhất **1.682 phút** (~28 giờ). Đây chưa phải tuổi của phí: phí vào `TokenJar` rồi mới quy đổi thành UNI, đoạn đó bài chưa đo.

**Hàng chờ thứ hai — chờ được thực thi.** Calldata của lệnh thực thi mang sẵn thời điểm lệnh được phát ở đầu Robinhood, nên ghép cặp được chính xác mà không cần giả định thứ tự. Giải mã cả 22 lượt:

· nhanh nhất **6,44 ngày**
· trung vị **6,76 ngày**
· chậm nhất **7,41 ngày**

Khớp cửa sổ khiếu nại chuẩn của một rollup Arbitrum.

## Nhưng chờ đủ tuổi chưa đủ — còn phải có người chọn lượt đó

Lệnh rút **đầu tiên** (Robinhood block 20.678.587, 27/07 10:59:00Z) mang số thứ tự **679**.

Quét toàn bộ lịch sử thực thi của cầu — **601 lượt**, số thứ tự 0 → 796 — thì **679 không có mặt**, trong khi **678 và 680 đều đã thực thi**. Các số chưa thực thi quanh đó: 679 · 682–687 · 689 · 693 · 699.

Không phải chưa tới lượt. Nó bị **nhảy qua**.

Nên 296.000 UNI chưa về **không phải đều đang chờ đúng quy trình**. Một phần đã đủ tuổi mà vẫn nằm im, vì mỗi lượt cần có người gọi lệnh thực thi trên Ethereum và trả gas. Cả **22/22** lượt đã về đều do **cùng một địa chỉ** gọi lệnh đó — cũng là địa chỉ gọi lệnh bật protocol fee cho các pool Robinhood Chain mà bài đã đối chiếu.

## Điều này đổi cách đọc một biểu đồ

Lượng UNI đốt hiển thị hôm nay phản ánh các **lệnh rút** được phát khoảng một tuần trước — còn **phí** tạo ra lượng UNI đó có thể đã phát sinh sớm hơn nữa.

Burn theo ngày không phải thước đo thời gian thực của hoạt động giao dịch. Nó là kết quả của hai hàng chờ trên, cộng thêm quyết định của người thực thi.

**Vì vậy, một cột burn tăng hôm nay chưa nói hoạt động hôm nay tăng.** Nó có thể chỉ là lượng phí cũ vừa vượt qua cả hai hàng chờ. Năm lệnh phát rải rác trong tám tiếng ngày 27/07 cùng được đóng tại **một** thời điểm ngày 03/08.

Và một ngày không có burn từ Robinhood cũng chưa nói được chain đó ngừng tạo phí.

## Địa chỉ và cách tự kiểm

· cầu Robinhood Chain trên Ethereum — `0x85001cc4867c5e1c22da4b79bb8852b9e2a06da0`
· gateway đối ứng phía Robinhood Chain — `0xfd9b17206278c16ddaacf6ac8f05dbf97edcb31e`
· `Firepit` trên Robinhood Chain — `0x7a8f74c2585f84c781f951b7f2ff21337d5b630b`, ngưỡng 2.000 UNI
· token bản Robinhood — `0xf177d86a28b520e3e396e4f3b96cd8e72d7dabd8`
· UNI trên Ethereum — `0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984`
· outbox — `0xf0ce991ea4a0d2400a4ab49b20ae333f6dce3de9`
· địa chỉ gọi lệnh thực thi cả 22 lượt — `0x2cf8e5b175aa29c1fdf0e9fe572735c78eacce43`

Gọi `counterpartGateway()` của gateway trên Ethereum, rồi gọi cùng hàm đó trên địa chỉ trả về bằng RPC công khai của Robinhood Chain: hai kết quả phải trỏ ngược về nhau. Rồi đọc log `Transfer` của UNI tới địa chỉ đốt, lọc địa chỉ gửi là gateway, trong Ethereum block **25.671.175 → 25.690.453**: phải ra **22 dòng × 2.000 UNI**.

## Chưa đo

· hai địa chỉ gửi khác chưa rõ thuộc chain nào — `0x2216958c…09a9` (20.000 UNI) và `0xa9bbe51b…fb00` (4.000 UNI)
· 105 lượt thực thi khác có đích là gateway này nhưng đưa tài sản đi chỗ khác
· đoạn phí nằm trong `TokenJar` trước khi thành UNI

## Điều gì bác được các con số trên

· hai gateway không trỏ ngược về nhau, hoặc lệnh rút không ghi đích là địa chỉ đốt ⇒ phép gán chain mất giá trị, mọi câu gán 44.000 UNI cho Robinhood phải rút. **22 lượt và 44.000 UNI từ địa chỉ đó vẫn đứng.**
· tổng 22 dòng không ra 44.000 UNI ⇒ con số 44,00% sai
· trong khoảng đo có địa chỉ khác gửi hơn 44.000 UNI tới địa chỉ đốt ⇒ câu "địa chỉ gửi lớn nhất" sai
· hai địa chỉ chưa rõ chain hoá ra cùng một chain và tổng vượt 44.000 ⇒ thứ hạng ở cấp chain phải viết lại

*Không phải lời khuyên đầu tư. Số đọc tới Robinhood block 29.174.972 và Ethereum block 25.690.453.*
