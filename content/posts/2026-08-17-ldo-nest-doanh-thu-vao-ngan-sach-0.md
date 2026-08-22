---
title: Cơ chế mua lại LDO của Lido đã nhận 145.443,55 USD doanh thu staking trong hai ngày đầu, nhưng ngân sách dùng để mua LDO vẫn bằng 0 vì contract phân bổ chưa đọc sổ doanh thu lần nào
tieu_de_ngan: LDO: 145.443 USD đã vào, ngân sách mua vẫn là 0
reading_layout: centered
token: LDO
date: 2026-08-17
mau: 🟡
ghim: Ethereum block 25.771.902 (2026-08-17T02:46:23Z) cho bốn giá trị trạng thái; sự kiện và sổ doanh thu đọc tại block 25.768.447 (2026-08-16T15:13:47Z); giá ETH đọc tại block 25.773.271 (2026-08-17T07:21:23Z). Contract nhận doanh thu 0x6220212a33a87ed7cc386b67eb2c393974f28c38; contract phân bổ 0xaa568141c051f2d1132b110f8391f18d48e8d889.
mo_ta: Doanh thu staking đã chảy qua cơ chế mua lại LDO hai vòng và vào sổ 145.443,55 USD, nhưng contract tạo ngân sách mua vẫn ghi 0 và chưa phát một event phân bổ nào.
anh: card-ldo-nest-145k-zero.png
kenh_x: https://x.com/blockpinned/status/2089284493974856166
doc_lai: Đây là ảnh chụp trạng thái tại các block ghim, không phải một kết luận bền. Hai contract có thể đồng bộ với nhau bất cứ lúc nào sau đó. Mức giá 2.738,55 USD và 4.107,82 USD mỗi stETH chỉ đúng khi giữ nguyên tốc độ doanh thu 30 ngày là 40,0172 stETH mỗi ngày; tốc độ doanh thu tăng cũng đưa cơ chế qua mức sàn mà giá không cần đổi. Ba dự đoán chỉ được phân định theo điều kiện ghi trong từng claim, không dời mốc sau khi biết kết quả.
---

**Lido đã bật một cơ chế mới, được thiết kế để lấy phần doanh thu staking vượt một mức sàn rồi mua LDO ngoài thị trường. Hai ngày đầu, doanh thu đã thực sự bắt đầu đi qua cơ chế đó: 145.443,55 USD vào sổ. Số tiền đã trở thành ngân sách mua LDO: 0.**

Có một khác biệt quan trọng giữa "doanh thu đã vào" và "lực mua đã xuất hiện". Tới các block ghim, mới xảy ra chuyện thứ nhất.

## Hai vòng ghi nhận doanh thu đầu tiên

Trong toàn bộ log đọc tới block **25.768.447**, đây là hai vòng đầu tiên mà contract nguồn ghi nhận doanh thu. Mỗi vòng là **hai giao dịch cách nhau**, không phải một:

- **15/08 12:23:59Z** — ghi nhận **38,93775769 stETH**; **14 phút 36 giây** sau quy ra **73.084,06 USD**, ở giá **1.876,9459 USD** mỗi stETH
- **16/08 12:21:11Z** — ghi nhận **38,49207858 stETH**; **2 giờ 6 phút 12 giây** sau quy ra **72.359,48 USD**

Sổ doanh thu tích luỹ đi từ **0 lên 145.443,549059 USD**. Cộng tay hai vòng ra đúng con số đó tới chữ số thứ tám sau dấu phẩy — log và giá trị đọc thẳng từ contract là hai đường độc lập, và chúng khớp nhau.

## Nhưng tiền dừng ở contract nguồn

Đọc lại lúc **09h46 ngày 17/08 (02:46:23Z)** tại block **25.771.902**, contract phân bổ vẫn ở trạng thái trắng:

- ngân sách mua = **0**
- tổng doanh thu nó ghi nhận = **0**
- event phân bổ = **chưa phát lần nào**

Contract đó có **14 log** trong lịch sử đọc được, nhưng **0/14 là event phân bổ**; tất cả đều thuộc nhóm cấu hình hoặc kích hoạt, log mới nhất ở block **25.724.759**, tức ngày **10/08**.

Bên nguồn đã ghi nhận 145.443,55 USD. Contract tạo ngân sách mua vẫn ghi 0. Tới block đó, chưa thấy hai contract đồng bộ doanh thu với nhau.

## Và kể cả khi bước đồng bộ chạy, công thức vẫn chưa cho ngân sách dương

Tiền mua mỗi ngày bằng **( doanh thu mỗi ngày − 109.589 USD ) × 50%**, với giới hạn tối đa **50 nghìn USD mỗi ngày** và **10 triệu USD mỗi năm**. Mốc 109.589 USD mỗi ngày tương đương một mức sàn **40,0 triệu USD mỗi năm**.

Tốc độ doanh thu 30 ngày là **40,0172 stETH mỗi ngày**. Ở giá **1.909,33 USD** đọc tại block 25.773.271, con số đó thành **76.406 USD mỗi ngày**, tức khoảng **27,9 triệu USD mỗi năm** — dưới mức sàn. Với đầu vào này, phần vượt của phép tính bằng 0, nên tiền mua cũng bằng 0.

Nếu tốc độ doanh thu giữ nguyên ở mức đo được trong cửa sổ 30 ngày gần nhất, mức giá làm **phần vượt của mỗi lượt bằng 0** là **2.738,55 USD mỗi stETH**, khoảng **+43%** so với mức giá dùng trong phép đo. Ở đúng mức đó, phần thiếu đã tích lại chỉ **ngừng lớn thêm** — nó không làm ngân sách mua thành dương, vì phần đã tích vẫn phải được bù hết trước. Đây không phải một dự báo giá; nó là mức hoà vốn của **dòng** doanh thu so với mức sàn. Văn bản đề xuất gốc nêu mốc khoảng 2.700 USD; con số suy ra từ tham số on-chain là 2.738,55 USD, lệch **1,43%**. Cùng giả định đó, mức tương ứng với giới hạn 10 triệu USD mỗi năm là **4.107,82 USD**.

Điều kiện "giữ nguyên tốc độ doanh thu" là bắt buộc phải đọc kèm: doanh thu stETH mỗi ngày tăng cũng đưa cơ chế qua mức sàn mà giá không cần nhúc nhích.

## Hai chỗ dễ hiểu nhầm

Kho DAO của Lido **vẫn đang nhận LDO thật** — nhưng qua một chương trình mua khác, chi stETH trực tiếp, không đi qua cơ chế này.

Bộ máy mua của cơ chế mới **cũng đã chạy thử trọn một vòng** hôm 13/08, bằng 1,001 stETH nạp từ một ví ngoài kho. Thứ chưa xảy ra là doanh thu của Lido tự biến thành lực mua LDO qua cơ chế này.

## Ba giới hạn của chính phép đo

Rebase **không** tự quy ra USD. Hook rebase chỉ tích stETH; bước quy đổi là một giao dịch riêng, được gửi sau đó. Hai mẫu trễ 14 phút 36 giây rồi 2 giờ 6 phút 12 giây — hai mẫu, chưa đủ để gọi là một nhịp. Đọc "rebase lúc 12:2xZ nên USD vào lúc 12:2xZ" là gộp hai chủ ngữ khác nhau.

Ô ngân sách phải đọc kiểu **có dấu**. Đọc kiểu không dấu thì ngày nó âm, bạn nhận về một số dương khổng lồ trông y hệt một con số thật.

Ô doanh thu chờ hôm nay bằng 0, và hôm qua cũng bằng 0 — nhưng vì **hai lý do ngược nhau**. Trước 15/08 nó là 0 vì chưa từng có gì đi qua; nay nó là 0 vì cả hai vòng đều đã được quy đổi hết. Đọc riêng giá trị hiện tại không phân biệt được hai trường hợp; phải xem lịch sử event log mới biết vì sao nó bằng 0.

Văn bản đề xuất **không nêu cơ chế tự xoá phần thiếu hụt tích luỹ** khi doanh thu nằm dưới mức sàn kéo dài. Nhưng khoản thiếu hụt đó chưa được ghi nhận on-chain: ngân sách đúng bằng 0, không phải một số âm. Nó chỉ bắt đầu phản ánh phép tính sau khi contract phân bổ đọc tổng doanh thu lần đầu, và tới block ghim nó chưa đọc.

## Cách tự kiểm

Bốn trạng thái này đọc thẳng được trên hai contract Ethereum mainnet. Contract nhận doanh thu là `0x6220212a33a87ed7cc386b67eb2c393974f28c38`, contract phân bổ là `0xaa568141c051f2d1132b110f8391f18d48e8d889`. Chia mọi kết quả cho 1e18; số trong ngoặc là giá trị tại block 25.771.902.

- `getCumulativeRevenueUSD()` trên contract nhận doanh thu → 145443,549059
- `pendingRevenueStEth()` trên cùng contract đó → 0
- `budgetUSD()` trên contract phân bổ, kiểu int256 → 0
- `lastTotalRevenueUSD()` trên contract phân bổ → 0

Ba tham số của công thức cũng đọc thẳng được và khớp văn bản đề xuất: mức sàn 109.589, tỷ lệ dành cho mua lại 5000 điểm cơ bản, giới hạn năm 10 triệu.

## Ba dự đoán, hạn 24/08

Ghi trước khi biết kết quả:

- log phân bổ trên contract phân bổ **vẫn chưa phát lần nào**. Sai nếu nó phát.
- **có điều kiện**: nếu contract phân bổ đồng bộ được với sổ doanh thu trong cửa này, ngân sách mua vẫn nhỏ hơn hoặc bằng 0. Chỉ chấm nếu điều kiện xảy ra; nếu không xảy ra thì ghi là chưa chấm được, không tự tính là đúng.
- sổ doanh thu nhận thêm **ít nhất 6 vòng** nữa trong 8 ngày 17–24/08, tức bước quy đổi tiếp tục diễn ra gần như mỗi ngày. Sai nếu ít hơn 6.

Sai câu nào thì đăng lại câu đó tại đây, không sửa lặng.

## Cái gì bác được bài này

Nếu gọi bốn giá trị trên tại đúng block 25.771.902 mà ngân sách mua khác 0, hoặc tổng doanh thu contract phân bổ ghi nhận khác 0, hoặc đếm log của contract phân bổ ra một event phân bổ, thì phần trung tâm của bài phải rút.

Nếu cộng hai vòng doanh thu không ra đúng 145.443,549059 USD, hoặc hai vòng đó không phải hai vòng đầu tiên trong toàn bộ log của contract nguồn, phần đo doanh thu phải rút.

Nếu tốc độ doanh thu 30 ngày đo lại khác 40,0172 stETH mỗi ngày, hai mức 2.738,55 và 4.107,82 USD mỗi stETH đổi theo — chúng là hệ quả của tốc độ đó chia vào mức sàn, không phải hai con số độc lập.

## Đính chính — 22/08

Bản đăng ngày 17/08 viết: *"mức giá làm công thức bắt đầu cho ngân sách dương là 2.738,55 USD mỗi stETH"*. Câu đó dẫn sai. Nó được sửa ở trên, và câu cũ giữ nguyên tại đây.

Cơ chế có hai đại lượng khác nhau. **Phần vượt của mỗi lượt** là một dòng, tính lại mỗi lần chốt sổ. **Ngân sách mua** là một kho cộng dồn, âm được, và số âm nằm lại trong bộ nhớ contract. Mức 2.738,55 USD làm **dòng** bằng 0. Nó không làm **kho** thành dương: phần đã tích vẫn phải được bù hết trước, và ở đúng mức giá đó thì không có gì để bù.

Ngày 21/08, chuyện này thành quan sát thay vì suy luận. Một địa chỉ ngoài DAO gọi hàm phân bổ hai lần, và ngân sách mua được ghi vào bộ nhớ contract: **âm 374.848,060795 USD**.

Chỗ thứ hai do một người đọc chưa xem bài tìm ra. Cụm *"Giữ nguyên tốc độ doanh thu 30 ngày"* bị hiểu thành *"phải giữ trong 30 ngày"*. Con số 30 ngày ở đó là **cửa sổ đo** tốc độ doanh thu, không phải một điều kiện thời lượng. Câu đã viết lại cho hết chỗ hiểu hai nghĩa.

Bài này **không** nói cơ chế hỏng, và **không** nói Lido ngừng mua LDO. Nó nói đúng một chuyện: tới các block ghim, đường doanh thu chưa tạo ra đồng ngân sách mua nào.

Sai ở đâu, BlockPinned sửa ngay tại đó.

*Không phải lời khuyên đầu tư.*
