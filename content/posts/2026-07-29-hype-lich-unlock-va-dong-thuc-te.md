---
title: Lịch unlock không phải lượng HYPE thực sự đi vào lưu hành — ledger thấp hơn mô hình 29–38 lần
token: HYPE
date: 2026-07-29
mau: 🟢
ghim: KHÔNG neo được block — HyperCore trả state hiện tại · ảnh chụp 09h38–10h18 ngày 29/07/2026 · ledger khép 6.004.521 HYPE withdrawal về đúng 0
mo_ta: Mô hình dùng 9,92 triệu HYPE mỗi tháng; ledger chính thức chỉ cho 259.866–347.176 HYPE rời bucket. Thấp hơn 29–38 lần, và sai lệch đó làm mô hình cung đổi dấu.
anh: post04-card.png
kenh_x: https://x.com/blockpinned/status/2082365873952604576
---

Lịch unlock có thực sự cho biết bao nhiêu HYPE đi vào lưu hành? Tôi từng tin vậy.

| | Lượng |
|---|---|
| Mô hình | **9,92 triệu HYPE/tháng** |
| Ledger thực tế | **259.866–347.176 HYPE/tháng** rời bucket |

Hai thứ đó không phải một.

## Con số 9,92 triệu đến từ đâu, và ledger nói gì

9,92 triệu là giả định từng được đưa vào mô hình từ phần core contributors — gần 1% tổng cung mỗi tháng. Lịch sử chính thức trên địa chỉ khớp với bucket đó chỉ cho thấy:

- bình quân toàn kỳ: **259.866 HYPE/tháng**
- 180 ngày gần nhất: **347.176 HYPE/tháng**

Dòng thực tế chỉ bằng **2,62–3,50%** giả định — thấp hơn **29–38 lần**.

Đây không phải sai số làm tròn. Nó làm mô hình cung **đổi dấu**: nếu 9,92 triệu là dòng thật, float HYPE tăng khoảng 111,5 triệu token/năm; thay bằng ledger đã đo, cùng mô hình cho float **giảm** 0,67–4,47 triệu HYPE/năm tại ảnh chụp hiện tại.

Một bên là lượng được mô hình hoá theo lịch. Bên kia là lượng HYPE thực sự rời bucket. **Phân bổ trên giấy không tự động trở thành token đã đi vào lưu hành.**

## Phép tính

**Δfloat = staking rewards vào float + phần gốc rời bucket − Assistance Fund mua − HYPE bị huỷ thật**

Khoảng kết quả rộng vì doanh thu buyback đang giảm:

| Mẫu số doanh thu | Δfloat |
|---|---|
| trung bình ba tháng đầy đủ | **−3,25 … −4,47 triệu**/năm |
| trailing 30 ngày | **−0,67 … −1,89 triệu**/năm |

Cả hai còn âm, nhưng biên 30 ngày rất mỏng.

## "Rời bucket" vẫn chưa có nghĩa là "đã bán"

Ledger khép được 6,00 triệu HYPE withdrawal: 1,08 triệu quay lại staking, 4,93 triệu chuyển tới 101 địa chỉ, ví gốc bán trực tiếp 3 HYPE. Trong 91 địa chỉ đã đủ 30 ngày, lượng bán **tối đa có thể gán** theo thời gian bằng **0,2839%** số chúng nhận — vẫn chỉ là mức tối đa, không phải bằng chứng token vừa nhận đã bị bán.

Vì vậy mô hình dùng 3,118–4,166 triệu HYPE/năm như lượng **có thể** vào float, không gọi nó là áp lực bán cùng ngày.

## Kết luận "float đang co" cũng không phải một định luật

Nó phụ thuộc giá, doanh thu dành cho holders và lượng HYPE bị huỷ thật. Đầu vào huỷ thật hiện mới được ngoại suy từ **9,79 ngày**; tốc độ các đoạn con phân tán **106,2%**. Nếu Assistance Fund ngừng mua, mô hình lập tức đổi sang float **tăng** 6,46–7,69 triệu HYPE/năm.

Điều bài này bác không phải *"HYPE sẽ không lạm phát"*. Nó bác phép đánh đồng: **lịch unlock = lượng token thực tế đi vào lưu hành.**

## Phụ lục — bucket core contributors

Địa chỉ genesis 23,8%: `0x43e9abea1910387c4292bca4b94de81462f8a251`

Từ lịch sử chính thức của Hyperliquid, sổ khép về đúng 0:

| Dòng | HYPE |
|---|---|
| withdrawal | 6.004.521 |
| − re-deposit | 1.078.488 |
| − chuyển first-hop | 4.926.027 |
| − bán trực tiếp | 3 |
| − còn ở spot | 3 |
| **= còn lại** | **0** |

4.926.027 HYPE được chuyển qua 202 transfer tới 101 địa chỉ. Trong 91 địa chỉ đã đủ 30 ngày: nhận **4.474.027 HYPE**, sell sau lúc nhận tính theo mức tối đa có thể gán **12.702,78 HYPE**, tỉ lệ **0,2839%**.

Mười địa chỉ nhận trong tháng 7 còn chưa đủ thời gian quan sát, nên không được gộp với nhóm 91 địa chỉ rồi gọi là mẫu hoàn chỉnh.

**Ba endpoint phải tách, đừng đọc thay nhau:**

- `delegatorHistory` — principal delegate, undelegate và withdrawal
- ledger transfer — token đi tới địa chỉ nào
- `userFillsByTime` — lệnh đã khớp trên orderbook

Một transfer không phải một sell. Một withdrawal khỏi staking cũng chưa phải token đã vào orderbook.

## Phụ lục — mô hình netflow, ảnh chụp 29/07

**Δfloat = E_float + V − AF − B**

- `E_float` = 4.355.580–4.533.358 HYPE/năm
- `V` = 3.118.397–4.166.110 HYPE/năm
- `AF` = holders revenue chia giá HYPE
- `B` = 1.013.912 HYPE/năm trong phép tính hiện tại

`B` là đầu vào yếu nhất: ngoại suy từ 27.183,16 HYPE bị huỷ trong 9,79 ngày, bốn đoạn con phân tán 106,2%. Không được đọc `B` như một nhịp đã biết.

**Hai mẫu số doanh thu — không được chọn một rồi giấu một:**

| Mẫu số | Doanh thu/năm | Δfloat tại giá 54,543 đô | Giá hoà vốn |
|---|---|---|---|
| ba tháng lịch đầy đủ 04–06/2026 | 596.216.586 đô | −4.471.064 … −3.245.573 | 77,58–92,29 đô |
| trailing 30 ngày | 455.702.524 đô | −1.894.857 … −669.366 | 59,29–70,54 đô |

**Kiểm giá mua của Assistance Fund:** trong 43 quan sát ngày×cặp, giá AF trả nằm trong biên giá ngày ở **43/43**. Premium có trọng số +0,0858%, median ngày +0,0079%. Chênh lệch giữa giá trả trung bình 30 ngày và spot hiện tại chủ yếu đến từ giá HYPE giảm trong cửa sổ, không phải trượt giá.

**Counterfactual:**

- Assistance Fund ngừng mua: **+6.460.065 … +7.685.557** HYPE/năm
- giả định 9,92 triệu HYPE/tháng là đúng: **+111,45 … +111,63 triệu** HYPE/năm

## Tự kiểm, và giới hạn của nguồn

State HYPE được đọc qua Info API và precompile live. **RPC mặc định của Hyperliquid nhận block tag nhưng trả state hiện tại**, nên block number không neo được các số live ở trên — đó là lý do trang này ghim bằng cửa sổ giờ thay vì bằng block, và mọi số phụ thuộc giá sẽ tiếp tục đổi.

Chuỗi lịch sử `delegatorHistory`, `delegatorRewards` và ledger là đường lịch sử **do chính Hyperliquid công bố**; chúng vẫn là nguồn tự công bố, không phải node archive độc lập. Muốn tự kiểm: gọi ba endpoint trên cho đúng địa chỉ genesis ở trên, cộng lại theo bảng khép sổ, rồi so tốc độ rời bucket với con số 9,92 triệu/tháng.

Không phải lời khuyên đầu tư. Số sống là ảnh chụp 09h38–10h18 ngày 29/07/2026 (giờ Việt Nam).
