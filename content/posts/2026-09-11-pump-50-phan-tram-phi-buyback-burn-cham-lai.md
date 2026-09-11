---
title: Pump.fun vẫn dành 50% phí cho buyback, nhưng tốc độ burn giảm 36%
tieu_de_ngan: "Nửa phí vẫn đi buyback, nhịp burn PUMP giảm 36%"
phu_de: "Cấu hình buyback vẫn ở 50% tại mốc đo. Con số này xác định cách chia phí, không ấn định số PUMP sẽ được mua và burn."
reading_layout: centered
token: PUMP
date: 2026-09-11
gio: "16:29"
mau: "🟡"
ghim: "Dòng phí và cấu hình đọc trên Solana tới slot 445.942.667; giao dịch kiểm cách chia phí tại slot 445.934.392, lúc 23h54 ngày 10/09/2026 giờ Việt Nam (16:54:20Z). Chuỗi doanh thu, dailyHoldersRevenue và burn kết thúc ngày 09/09/2026."
mo_ta: "Pump.fun vẫn tách 50% phí gộp sang buyback trong giao dịch đã kiểm, nhưng nhịp burn bảy ngày chỉ còn 144,10 triệu PUMP mỗi ngày — thấp hơn 36,1% so với trung bình 30 ngày."
anh: card-pump-50-phan-tram-burn-giam-36.png
doc_lai: "dailyHoldersRevenue là giá trị USD của lượng PUMP tại ngày burn, không phải USD thực chi trên DEX. Các số 45,75%, 43,55% và giá PUMP ngụ ý chỉ dùng để tái lập số học, không phải ba bằng chứng độc lập giải thích nguyên nhân burn giảm."
---

**Tại mốc BlockPinned kiểm tra, Pump.fun vẫn tách một nửa phí gộp sang buyback. Nhưng lượng PUMP bị burn mỗi ngày lại giảm mạnh.**

Trong bảy ngày kết thúc 09/09, nhịp burn chỉ còn **144,10 triệu PUMP mỗi ngày**. Trung bình 30 ngày kết thúc cùng mốc là **225,58 triệu**. Chênh lệch: **−36,1%**.

Sai lầm dễ mắc là coi hai con số này phải đi cùng nhau. **Tỉ lệ 50% cho biết phí được chia thế nào; nó không cho biết mỗi ngày có bao nhiêu USD thực sự được đem đi swap, mua ở giá nào và burn vào lúc nào.**

## 50% không chỉ nằm trong lời công bố

Cấu hình hiện tại của Pump.fun ghi `buyback_basis_points = 5000`: một nửa phí gộp đi vào tám buyback vault, nửa còn lại đi vào tám ví nhận phí thường.

BlockPinned kiểm theo hai đường.

Trong một giờ ngày 09/09, cả 16 địa chỉ đều có dòng tiền. Tám ví thường nhận tổng **247.162.676.113 lamports**; tám buyback vault nhận **247.162.620.490 lamports**. Phần buyback bằng **49,999994374%** phí gộp.

Một giao dịch khác được đọc trực tiếp bằng RPC. Phí gộp là **3.966.585 lamports**; ví thường tăng **1.983.293**, buyback vault tăng **1.983.292**. Cộng hai số đúng bằng phí của giao dịch, tới từng lamport.

Ở một giao dịch gom tiền khác, đủ tám vault được chuyển về cùng ví burn. Tổng SOL và WSOL ghi trong tám event khớp số dư đến từng đơn vị.

Các phép kiểm này xác nhận cấu hình 50% đang được thực thi **tại các mốc đã đo**. Dữ liệu không ủng hộ cách giải thích rằng cấu hình buyback đã bị hạ tại những mốc đó. Nó không phải bản replay của mọi giao dịch trong cả giai đoạn.

## 50% không khóa số token burn

Về kinh tế, lượng token mua được phụ thuộc vào số USD thực chi và giá khớp lệnh:

> **PUMP mua được = USD thực chi trên DEX ÷ giá khớp lệnh**

Cấu hình chia phí chỉ nằm ở đầu đường tiền. Muốn nối nó với lượng token burn, còn phải chứng minh tiền được đưa lên DEX khi nào, khớp ở giá nào và token được burn ở thời điểm nào.

Trong dữ liệu hiện có, `dailyHoldersRevenue` không phải USD thực chi. Từ tháng 05/2026, chuỗi này ghi **giá trị USD của lượng PUMP tại ngày burn**. Vì thế, khi viết lượng burn dưới dạng doanh thu × tỉ lệ giá trị USD của lượng burn trên doanh thu ÷ giá bình quân ngụ ý, ba thành phần của phép tính thay đổi như sau:

| Biến | trung bình 30 ngày | trung bình 7 ngày | thay đổi |
|---|---:|---:|---:|
| doanh thu | 1.904.207 USD/ngày | 1.396.283 USD/ngày | **−26,7%** |
| giá trị USD của lượng burn / doanh thu | 45,75% | 43,55% | **−4,8%** |
| giá PUMP bình quân ngụ ý từ cùng chuỗi | 0,0038622 USD | 0,0042201 USD | **+9,3%** |
| PUMP burn | 225,58 triệu/ngày | 144,10 triệu/ngày | **−36,1%** |

Ba tỉ số trên tái lập về mặt số học tỉ số burn:

> **0,733 × 0,952 ÷ 1,093 = 0,638**

Tỉ số burn đo trực tiếp là **0,6388**. Chênh lệch **0,00035** đến từ việc các hệ số trong phép nhân đã được làm tròn.

Đây là một **phép kiểm tính nhất quán**, không phải bằng chứng độc lập rằng ba biến đã gây ra mức giảm burn. Giá bình quân ngụ ý được suy ra từ chính giá trị USD và lượng PUMP burn; do đó không thể dùng phép nhân trên để xếp hạng nguyên nhân. Trong ba tỉ số, doanh thu có mức thay đổi số học lớn nhất, nhưng dữ liệu này chưa chứng minh nó là đóng góp nhân quả lớn nhất.

## Bằng chứng DEX nói được gì

USD thực chi được đo theo một đường khác: cộng `amount_usd` tại các lượt swap của những ví buyback trên `dex_solana.trades`.

Tới thời điểm dữ liệu DEX dừng ở 23:59:58Z ngày 09/09, các giao dịch nhìn thấy được cho thấy chương trình đã chi ít nhất **446,54 triệu USD** để mua **164,16 tỷ PUMP**. Lượng mua này bằng **99,41%** lượng burn ghi trong cùng sổ. Đây chỉ là mức ít nhất đo được: phép đo không nhìn thấy giao dịch OTC hoặc giao dịch ngoài tập dữ liệu nếu có.

Phép đo DEX lũy kế xác nhận có hoạt động buyback quy mô lớn. Nhưng dữ liệu đã đóng chưa có chuỗi USD thực chi và giá khớp lệnh độc lập cho đúng hai cửa sổ bảy ngày và 30 ngày. Vì vậy bài này không dùng số lũy kế để giải thích nguyên nhân của riêng nhịp giảm gần nhất.

Kết luận đủ bằng chứng là:

> **Một tỉ lệ buyback cố định không tạo ra một nhịp burn cố định.**

Muốn giải thích nhịp burn giảm bằng hoạt động thị trường, cần ghép theo ngày số USD thực chi, giá khớp lệnh và lượng token sau đó được burn. Chỉ nhìn phần trăm phí hoặc số token burn chưa đủ.

## 50% hôm nay cũng không phải lời hứa bất biến

Có hai quyền khác nhau: **quyền đổi tỉ lệ buyback** và **quyền điều khiển nơi tiền từ tám vault được gom tới**.

Cấu hình 5.000 điểm cơ bản hiện do một Squads multisig ba trên bốn kiểm soát, không có timelock. Trong lịch sử đã đo, cấu hình từng được đổi hai lần trong cùng ngày 28/04: lên 10.000 rồi xuống 5.000.

Với quyền gom tiền, tám vault hiện cùng dùng một địa chỉ on-curve làm authority. IDL công khai không nêu một địa chỉ nhận cố định; BlockPinned chưa giải ngược bytecode để loại trừ hoàn toàn khả năng chương trình có thêm kiểm tra lúc chạy.

Con số 50% vẫn đúng tại mốc đo. Nhưng theo quyền quản trị hiện tại, multisig có thể thay đổi cấu hình đó.

## Điều bài này chưa biết

Bài này đo được cấu hình 50% tại các mốc kiểm, nhịp burn bảy ngày thấp hơn 30 ngày và lượng mua DEX lũy kế tới mốc dữ liệu. Bài **chưa xác định nguyên nhân** của mức giảm burn gần nhất, cũng chưa đo được vì sao doanh thu giảm.

Cửa sổ bảy ngày nằm bên trong cửa sổ 30 ngày; đây là so nhịp gần nhất với nền dài hơn, không phải hai giai đoạn rời nhau. Dữ liệu tổng 50% theo địa chỉ là một giờ từ indexer. Giao dịch RPC chỉ dùng để kiểm trực tiếp cách phí được chia trong một giao dịch, không phải replay toàn bộ một giờ hay toàn bộ giai đoạn.

## Phần kiểm chứng — cách tự kiểm

**Cấu hình và đường phí.** Đọc account `Global` tại `slot 445.942.667`: `buyback_basis_points = 5000`, tám địa chỉ nhận phí thường và tám buyback vault không giao nhau. Ở giao dịch `slot 445.934.392`, decode `TradeEvent`, rồi so với thay đổi số dư trước/sau: **3.966.585 = 1.983.293 + 1.983.292**.

**Dòng tiền một giờ.** Cộng inflow của đúng 16 địa chỉ trong cửa sổ 09/09 00:00–01:00Z. Tám ví thường phải ra **247.162.676.113 lamports**, tám buyback vault **247.162.620.490**, tổng **494.325.296.603**; buyback chia phí gộp ra **49,999994374%**.

**Nhịp burn.** Cộng lệnh `burn` và `burnChecked` theo ngày trên `tokens_solana.transfers`, chặn hai đầu thời gian. Bảy ngày kết thúc 09/09 phải ra **144.097.375,50 PUMP/ngày**; 30 ngày phải ra **225.578.810,86**. Cộng toàn lịch sử tới thời điểm dữ liệu dừng ra **165.137.872.788,42 PUMP**.

**Kiểm tra số học.** Lấy `dailyRevenue`, `dailyHoldersRevenue`, giá bình quân ngụ ý và lượng burn cho cùng hai cửa sổ. Tỉ số bảy ngày chia 30 ngày cho **0,733 × 0,952 ÷ 1,093 = 0,63844**; tỉ số burn trực tiếp là **0,63879**. Nếu độ lệch tuyệt đối vượt **0,001**, bảng hoặc phép tính phải sửa. Đây không phải kiểm chứng nhân quả.

**Mua DEX lũy kế.** Cộng `amount_usd` và `token_bought_amount` của đúng các ví buyback, qua hai giai đoạn đã ghim và tới thời điểm dữ liệu dừng. Kết quả phải ra ít nhất **446.540.728,31 USD** và **164.164.054.283,05 PUMP**; lượng PUMP mua chia lượng trong sổ burn là **99,4103%**.

**Điều bác bỏ.** Claim 50% sai nếu giao dịch tại đúng slot đã ghim không đóng được phí gộp về hai thay đổi số dư hoặc phần buyback lệch ngoài **±2 điểm phần trăm**. Claim burn chậm **36,1%** sai nếu chạy lại đúng cửa sổ và hai đầu thời gian mà một trong hai nhịp lệch quá **0,01%**. Claim mua DEX lũy kế sai nếu chạy lại cùng phạm vi mà USD, PUMP hoặc tỉ lệ phủ lệch quá **0,01%**.

*Không phải lời khuyên đầu tư.*
