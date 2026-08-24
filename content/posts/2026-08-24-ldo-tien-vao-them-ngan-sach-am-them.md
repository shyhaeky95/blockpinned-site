---
title: Cỗ máy mua LDO nhận thêm 201.494 USD doanh thu. Ngân sách lại âm thêm 63.636 USD.
tieu_de_ngan: "Tiền vào nhiều thêm, ngân sách âm sâu thêm"
reading_layout: centered
token: LDO
date: 2026-08-24
mau: 🟡
ghim: Ba lượt gọi hàm phân bổ đọc tại Ethereum block 25.803.732, 25.803.734 và 25.824.702 — tức 20h12 và 20h13 ngày 21/08, rồi 18h21 ngày 24/08/2026 giờ Việt Nam (13:12:47Z · 13:13:11Z · 11:21:35Z). Trạng thái hợp đồng, tham số và nhịp doanh thu đọc tại block 25.825.413, tức 20h43 ngày 24/08 giờ Việt Nam (13:43:47Z).
mo_ta: Cơ chế buyback LDO của Lido ghi nhận thêm 201.494 USD doanh thu trong ba ngày, nhưng ngân sách dùng để mua LDO vẫn đi từ âm 374.848 xuống âm 438.484 USD, và số lượt mua vẫn bằng 0.
anh: card-ldo-tien-vao-ngan-sach-am-them.png
kenh_x: https://x.com/blockpinned/status/2091907493190615157
doc_lai: Mốc hoà vốn không phải hằng số — nó bằng phí dự trữ mỗi ngày chia cho nhịp doanh thu, nên nhịp doanh thu đổi thì mốc đổi theo, và đổi cả hai chiều. Bài BlockPinned ngày 17/08 in mốc 2.738,55 USD; bản đo ngày 23/08 ra 2.698,82; tại block ghim của bài này nó là 2.720,91. Ba con số, một công thức, không tham số hợp đồng nào đổi.
---

**Ba ngày qua, cỗ máy buyback LDO của Lido nhận thêm 201.494 USD doanh thu staking. Tiền vào thật, vào đúng sổ của nó. Nhưng thay vì có thêm tiền mua LDO, ngân sách của cỗ máy lùi thêm 63.636 USD — xuống âm 438.484 USD.**

Không phải máy hỏng. Nó đang chạy đúng thiết kế. Và cũng chính vì thế mà mốc giá hay được nhắc tới nhất — khoảng 2.700 USD mỗi stETH — dễ bị đọc sai: chạm mốc đó **không** có nghĩa Lido bắt đầu mua LDO.

## Một phép tính giải thích trọn vẹn

Cơ chế lấy doanh thu staking, trừ đi một khoản **phí dự trữ cố định 109.589 USD mỗi ngày**, rồi chia đôi phần còn lại — một nửa thành ngân sách mua LDO.

Ba ngày phí dự trữ là 328.767 USD. Doanh thu ba ngày là 201.494 USD.

> 201.494 − 328.767 = **−127.273**, chia đôi = **−63.636**

Đúng bằng mức ngân sách lùi thêm, tới từng xu. Đây là hai ô trong hợp đồng, đọc ngay sau lượt chốt sổ thứ hai và ngay sau lượt thứ ba:

| Ô trong hợp đồng | sau lượt ② (21/08) | sau lượt ③ (24/08) | đổi |
|---|---:|---:|---:|
| tổng doanh thu đã ghi nhận | 565.371,878410 | **766.866,023026** | **+201.494,144615** |
| ngân sách dùng để mua LDO | −374.848,060795 | **−438.484,488487** | **−63.636,427692** |
| số ngày phí dự trữ đã tính | 12 | 15 | +3 |

Doanh thu không đứng yên, không chậm lại, không bị chặn ở đâu. Ngân sách vẫn lùi. Lý do nằm trọn ở vế trừ: **phí dự trữ là một cái đồng hồ chạy mỗi ngày, còn doanh thu phải chạy nhanh hơn nó.** Doanh thu chỉ cần nhỏ hơn nó là ngân sách âm sâu thêm.

Một chi tiết đáng nói ở vế trừ: hợp đồng tính phí dự trữ theo **ngày tròn và làm tròn lên**. Từ ngày bật 10/08 tới lượt chốt sổ thứ ba là 14,47 ngày; máy tính 15 ngày. Bấm sớm trong ngày không giúp gì — nó vẫn cộng trọn ngày đó vào vế trừ.

## 2.700 USD không phải mốc bắt đầu mua

Ngân sách này là một **kho cộng dồn**, không phải một dòng tính lại từ đầu mỗi ngày. Phần thiếu nằm lại trong bộ nhớ hợp đồng, và phải được bù hết trước khi mua đồng LDO đầu tiên.

Từ đó ra hai đại lượng rất khác nhau, và mốc khoảng 2.700 USD chỉ nói về cái thứ nhất:

> **Ngừng âm ≠ hết âm. Hết âm rồi mới tới lượt mua.**

Ở đúng mức giá hoà vốn, phần dư mỗi lượt bằng 0 — nên 438.484 USD kia đứng yên ở mức nó đang có và không bao giờ về 0. Mốc đó là mức **ngừng đào sâu**, không phải mức **bắt đầu mua**.

**BlockPinned cũng từng đọc sai mốc này.** Bài ngày 17/08 gọi 2.738,55 USD là mức *"ngân sách bắt đầu dương"*. Câu đó đã được đính chính ngày 22/08: đây chỉ là mốc **dòng tiền ngừng âm**, không phải lúc khoản âm đã tích biến mất.

## Vậy cần gì để cỗ máy thật sự mua?

Cỗ máy tự để lại dấu vết về giá. Mỗi lượt quy đổi doanh thu ghi cả lượng stETH lẫn số USD, nên chia hai con số ấy ra được giá stETH tại đúng lượt đó — không cần nguồn giá bên ngoài. Mười lượt gần nhất, từ 19h38 ngày 15/08 tới 20h27 ngày 24/08 giờ Việt Nam, đi từ **1.876,95 USD** lên **2.513,73 USD** mỗi stETH.

Nhịp doanh thu đo trên chín khoảng ấy là **40,2765 stETH mỗi ngày**. Chia vào phí dự trữ, mức giá làm phần dư bằng 0 là **2.720,91 USD**. Giá hiện tại còn cách mốc đó **8,24%** — tức stETH đang tiến gần mức mà khoản âm ngừng lớn thêm, chứ chưa tới mức cỗ máy mua được gì.

Giữ nhịp doanh thu như hiện tại:

| Giá stETH | Điều xảy ra |
|---:|---|
| 2.513,73 USD *(lượt quy đổi mới nhất)* | ngân sách còn lùi 4.172 USD mỗi ngày |
| **2.720,91 USD** | khoản âm ngừng lớn thêm — và đứng yên ở đó |
| 3.000 USD | khoảng **78 ngày** để bù hết khoản âm |
| 3.500 USD | khoảng **28 ngày** |
| 4.000 USD | khoảng **17 ngày** |

Đây là **độ nhạy, không phải dự báo giá**. Mỗi hàng giả định giá nhảy tới mức đó ngay hôm nay rồi đứng yên, và nhịp doanh thu giữ nguyên. Cả hai giả định đều sai trong thực tế; bảng chỉ dùng để so độ lớn giữa các nhánh, không dùng để đoán tháng nào cỗ máy mua lượt đầu.

Điều bảng nói được không phụ thuộc vào việc đoán giá: **ngừng tệ đi và bắt đầu mua là hai mốc cách nhau rất xa.** Ở 3.000 USD, dù đã cao hơn mốc hoà vốn 10,3%, cỗ máy vẫn cần khoảng 78 ngày để lấp khoản âm hiện tại.

## Cỗ máy đã được gọi ba lần. Số LDO mua được: 0.

Và đây không chỉ là phép tính trên giấy.

Lúc 18 giờ 21 phút 35 giây ngày 24/08 giờ Việt Nam (11:21:35Z), block 25.824.702, một địa chỉ gọi hàm `allocate()` của cơ chế. Đây là lần thứ ba trong bốn ngày; hai lần trước là 20h12 phút 47 giây và 20h13 phút 11 giây ngày 21/08, cách nhau 24 giây.

Cả ba lượt đều đến từ **cùng một địa chỉ** `0x64c0…ffce` — một ví thường, không có mã hợp đồng, gọi thẳng. Không phải địa chỉ của DAO, và không cần phải là: hàm này ai gọi cũng được.

Cả ba lượt đều kết thúc bằng một sự kiện **bỏ qua phân bổ**. Số lượt mua ghi nhận trong toàn bộ lịch sử hợp đồng, tính tới block ghim: **0**.

Nói cách khác: cơ chế không nằm im chờ ai đó nhớ ra nó. Nó đã được gọi ba lần, và cả ba lần đều trả lời: chưa có ngân sách để mua.

## Ngay cả khi giá tăng tiếp, quy mô buyback vẫn có giới hạn cứng

Hợp đồng mang một giới hạn cứng **10 triệu USD mỗi năm**. Ở nhịp doanh thu hiện tại, giới hạn đó bắt đầu ràng buộc từ giá stETH khoảng **4.081 USD** — trên mức ấy, giá tăng thêm không làm quy mô buyback lớn thêm theo cùng tỷ lệ.

## Bài này không nói gì

Bài này **không** nói cơ chế hỏng, cũng **không** nói doanh thu của Lido giảm hay Lido đang lỗ. Cơ chế chạy đúng thiết kế đọc được từ mã nguồn, và thiết kế đó vốn dĩ là *chưa đủ doanh thu thì không mua*. Ngân sách này chỉ đếm doanh thu staking đi qua một đường dẫn cụ thể, trừ một khoản phí dự trữ do chính DAO đặt ra — nó không phải sổ lãi lỗ của Lido, và con số 201.494 USD là phần chảy vào **cỗ máy này**, không phải mức doanh thu tăng thêm của Lido.

Bài này **không** nói Lido ngừng buyback LDO. Đây là **một trong hai** đường mua; đường còn lại là một chương trình mua thủ công chạy song song, không đi qua ngân sách nói ở đây. Bài này không đo đường đó.

Bài này **không** nói các tham số là bất biến, và cũng không nói Lido bị kẹt. Quản trị đổi được **tương lai** — hạ tỷ lệ phí dự trữ, nâng phần chia — chỉ không xoá được phần đã tích. Câu đúng là: phần đã tích thì khoá, phần sắp tới sửa được nhưng phải qua một lượt bỏ phiếu ai cũng thấy.

## Điều kiện bác bỏ

Nếu gọi hai giá trị trạng thái của hợp đồng phân bổ tại đúng block 25.825.413 mà ngân sách khác −438.484,488487 USD hoặc doanh thu khác 766.866,023026, hoặc đếm log toàn thời gian ra một sự kiện mua, thì phần trung tâm của bài phải rút.

Nếu nhịp doanh thu đo lại khác 40,2765 stETH mỗi ngày thì mốc hoà vốn và cả bảng số ngày đổi theo — chúng là hệ quả của nhịp đó chia vào phí dự trữ, không phải những con số độc lập.

## Phần kiểm chứng — cách tự kiểm

**Sự kiện.** Đếm log của hợp đồng phân bổ `0xaa568141c051f2d1132b110f8391f18d48e8d889` từ trước ngày bật tới block ghim: sự kiện chốt sổ **3**, sự kiện bỏ qua phân bổ **3**, sự kiện mua **0**. Ba giao dịch phát ra chúng đều có `from` bằng `0x64c0ff5c25925acb33d68f79ad728fd63361ffce` và cùng chữ ký hàm `0xabaa9916`, tức `allocate()`.

**Trạng thái.** Gọi `budgetUSD()` và `lastTotalRevenueUSD()` tại block 25.803.735, 25.811.745 và 25.825.413. Đọc lại một lượt nữa tại block 25.825.714, lúc 21h43 ngày 24/08 giờ Việt Nam — cả hai giá trị và số lượt mua đều không đổi. Đọc có dấu — đây là số nguyên có dấu 256 bit; đọc không dấu sẽ ra một con số khổng lồ vô nghĩa.

**Tham số**, đọc tại block ghim: phí dự trữ 109.589 USD mỗi ngày, tỷ lệ dành cho buyback 5000 điểm cơ bản, giới hạn ngày 50.000 USD, giới hạn năm 10.000.000 USD, sàn giá 0.

🔴 **Sàn giá bằng 0 là một dữ kiện, không phải chỗ trống.** Nhiều bản tóm tắt về cơ chế này nhắc tới một cổng giá ETH; trên chuỗi, ô đó đọc ra 0. Cơ chế không có cổng giá — nó chỉ có phép trừ phí dự trữ.

**Nhịp doanh thu và giá** dựng từ mười lượt ghi nhận doanh thu của hợp đồng nguồn. Mỗi lượt chở cả lượng stETH lẫn số USD, nên giá suy ra được từ chính lượt đó; nhịp lấy trên chín khoảng giữa mười lượt, không chia tổng cho một cửa sổ tự chọn.

**Bốn phép kiểm đi kèm, cả bốn đều nổ được:**

- **Ca ngược.** Nạp lại đầu vào của bảng đã dựng ngày 23/08 (khoản âm 374.848,060795 và nhịp 40,6063) phải tái lập đúng bảng cũ 61,3 · 23,0 · 14,2 ngày. Ra đúng 61,3 · 23,0 · 14,2. Không khớp thì công thức của bài này khác công thức bản trước và mọi số mới vô nghĩa.
- **Tái lập khoản âm.** Một nửa của hiệu giữa doanh thu 766.866,023026 và 15 × 109.589 phải ra đúng con số hợp đồng đang ghi. Lệch 0.
- **Cộng dồn khớp sổ.** Cộng dồn mười lượt ghi nhận doanh thu phải tái lập đúng con số hợp đồng ở **ba** mốc độc lập: 565.371,878410 sau bảy lượt, 669.904,474521 sau tám lượt, 766.866,023026 sau chín lượt. Cả ba khớp. Một mốc lệch thì tập log này không phải nguồn của sổ hợp đồng và mọi suy luận về nhịp doanh thu sai theo.
- **Hoà vốn đối chiếu nguồn chính chủ.** Mốc 2.720,91 USD tính từ phép đo của bài lệch **0,77%** so với mốc khoảng 2.700 USD mà chính tài liệu đề xuất của Lido nêu. Lệch lớn thì cách đọc định nghĩa doanh thu sai, và mọi kịch bản giá bên trên sai theo.

**Hai đường đo độc lập cho cùng một đại lượng.** Nhịp doanh thu tính từ mười lượt quy đổi ra 40,2765 stETH mỗi ngày; bản đo ngày 23/08 dựng từ một nguồn khác hẳn — các lượt trả thưởng của stETH trong cửa sổ 30 ngày — ra 40,6063. Hai đường lệch nhau **0,81%**.

**Một chỗ dễ đọc nhầm.** Mốc hoà vốn **không phải hằng số của cơ chế**. Nó bằng phí dự trữ chia cho nhịp doanh thu, nên nhịp đổi thì mốc đổi theo — và nó đổi cả hai chiều. Bài BlockPinned ngày 17/08 in 2.738,55 USD; bản đo 23/08 ra 2.698,82; tại block ghim bài này là 2.720,91. Ba con số, một công thức, không tham số hợp đồng nào đổi.

**Một dữ kiện chưa vào sổ.** Lượt quy đổi doanh thu lúc 20h27 ngày 24/08 giờ Việt Nam (13:27:47Z) — thêm 103.691,97 USD — xảy ra **sau** lượt chốt sổ lúc 18h21, nên nó chưa được tính vào con số 766.866 ở trên. Lượt gọi kế tiếp sẽ nhặt nó.

---

*Không phải lời khuyên đầu tư.*
