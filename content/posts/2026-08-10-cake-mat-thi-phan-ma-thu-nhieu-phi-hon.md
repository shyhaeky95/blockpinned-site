---
title: PancakeSwap mất gần một nửa thị phần BSC trong sáu tuần, nhưng phí giao dịch trên sàn tăng 3,1 lần vì volume dời sang pool có mức phí cao gấp 100 lần
tieu_de_ngan: PancakeSwap mất gần nửa thị phần BSC, nhưng phí giao dịch lại tăng 3,1 lần
token: CAKE
date: 2026-08-10
mau: 🟡
ghim: BSC block 115.070.912 (10/08/2026 14h22 giờ Việt Nam) — ví đốt 0xceba60280fb0ecd9a5a26a1552b90944770a4a0e giữ 59.637.099,55 CAKE chưa đốt, trong đó 599.032,72 là tiền phí của tuần đang chạy. Chuỗi cycle tuần pin tại block 115.047.719; phí pool TUT/WBNB đo trong cửa sổ block 114.861.872 đến 115.053.819; allocPoint đọc tại block 115.053.639
mo_ta: Thị phần volume của PancakeSwap trên BSC đi từ 74,0% xuống 36,4% qua ba giai đoạn, trong khi phí thu được tăng 3,1 lần. Phần tới được CAKE chỉ tăng 1,4 lần.
anh: card-cake-thi-phan-phi-muc.png
kenh_x: https://x.com/blockpinned/status/2086712976091046317
doc_lai: Số của tuần đang chạy trôi cho tới lúc lệnh đốt tuần thực thi, nên nó là mức sàn chứ không phải con số cuối. Ba giai đoạn đã đóng thì giữ nguyên, với điều kiện DefiLlama không tính lại lịch sử và Dune không sửa bảng dex.trades. Giá CAKE và BNB là ảnh chụp theo giờ đã ghi.
reading_layout: centered
---

**Thị phần volume của PancakeSwap trên BSC đi một mạch từ 74,0% xuống 36,4% qua ba giai đoạn của sáu tuần. Cùng lúc đó, phí giao dịch tạo ra trên sàn tăng 3,1 lần. Hai đường này không mâu thuẫn: volume dời từ pool mức phí 0,01% sang pool mức phí 0,25% và 1%.**

Nhưng phần tới được token thì không tăng theo kịp. Gross fee tăng 3,1 lần, lượng CAKE bị đốt từ nguồn phí chỉ tăng 1,4 lần, và tỷ lệ chuyển hoá giữa hai đại lượng đó rơi từ khoảng 47% xuống 21%.

{{visual:thi-phan-phi-nguoc-huong}}

## Ba giai đoạn, đo bằng trung vị theo ngày

Trung vị chứ không phải tổng, để một ngày đột biến không kéo cả cụm. Ngày 02/08 là một ngày như vậy: phí 1.294.920 đô, gấp 2,7 lần ngày kề bên.

| trung vị/ngày | A. trước (27/06–11/07) | B. sóng khối lượng (12/07–29/07) | C. sóng phí (30/07–08/08) |
|---|---:|---:|---:|
| volume DEX cả chain BSC | 674 triệu đô | **1,02 tỷ** (+51%) | **1,77 tỷ** |
| volume PancakeSwap | 491 triệu đô | **477 triệu** (−3%) | 630 triệu |
| **thị phần PancakeSwap** | **74,0%** | **44,4%** | **36,4%** |
| phí PancakeSwap | 202.808 đô | **155.398** (−23%) | **479.026** (×3,08 so với B) |
| phí trên mỗi đô volume | 4,07 bps | 3,47 bps | **7,36 bps** |

Ranh giới không chọn cho đẹp. **12/07** là ngày volume cả chain lần đầu vượt 1 tỷ đô. **30/07** là ngày phí PancakeSwap nhảy từ 200.030 lên 447.400 trong một ngày rồi ở lại mức đó.

Giai đoạn B là ca sạch nhất của cả bài: volume cả chain tăng 51% mà phí PancakeSwap **giảm** 23%. Một đợt sóng đi qua nhà mà không để lại đồng nào.

Dải đầy đủ, không phải trung vị — thị phần **63,9–77,5%** rồi **17,5–76,9%** rồi **30,2–59,3%**; phí mỗi ngày **120.793–250.783** rồi **102.419–257.428** rồi **409.740–1.294.920**.

Ranh giới ba giai đoạn chia theo volume và phí của cả chain, **không** theo một phép phân loại token nào. Bài không đo bao nhiêu phần trăm của đợt này là token meme.

## Volume dời chỗ, không phải nhiều thêm

Trên v3 mỗi pool có một mức phí riêng, từ 0,01% cho cặp lớn tới 1% cho token biến động mạnh. Cùng một đô volume thì mức phí danh nghĩa chênh nhau tới 100 lần.

| tỷ trọng volume v3 | A. trước | B. sóng khối lượng | C. sóng phí |
|---|---:|---:|---:|
| mức 0,01% | 75,76% | **86,62%** | 80,22% |
| mức 0,05% | 21,28% | 11,56% | 10,02% |
| mức 0,25% | 2,18% | 1,34% | **7,45%** |
| mức 1,00% | 0,77% | 0,48% | **2,31%** |
| **tổng nhóm ≥ 0,25%** | **2,95%** | **1,81%** | **9,76%** |
| quy ra đô, cả giai đoạn | 146 triệu | 131 triệu | **517 triệu** |
| phí trên mỗi đô volume v3 | 3,14 bps | 2,25 bps | **5,47 bps** |

{{visual:mix-pool-doi-gia-phi}}

Ở giai đoạn B, tỷ trọng nhóm phí cao **giảm** còn 1,81% trong khi mức 0,01% tăng lên 86,62%. Volume v3 tăng 20% mà phí thu được giảm 14%. Ở giai đoạn C, tỷ trọng nhóm phí cao tăng 5,4 lần.

Câu hỏi đầu tiên phải hỏi khi một chỉ số nhảy gấp đôi đúng một ngày rồi ở đó: có phải nguồn dữ liệu vừa đổi cách tính không. Kiểm bằng v2, vì mức phí của nó cố định 0,25% nên nếu công thức đổi thì tỷ lệ phí trên volume của v2 phải đổi theo. Đo ba giai đoạn, nó đứng yên ở **25,5 rồi 26,5 rồi 25,8 bps**.

## Một pool 1% và không một CAKE emissions nào

Pool TUT/WBNB, mức phí 1%, địa chỉ `0x6dafbf0ab4fd72e2a5c0ad5a1ed277d3bf8a8d1f`. Trong 24 giờ tính tới 11h05 ngày 10/08 giờ Việt Nam, nó thu **152.288 đô phí**.

Con số này đọc thẳng từ trạng thái của pool chứ không phải volume nhân tỷ lệ: hiệu của `feeGrowthGlobal0X128` và `feeGrowthGlobal1X128` giữa hai block, nhân với `liquidity`, chia 2^128, ra **110,69 WBNB cộng 377.679 TUT**.

Tại block 115.053.639, `allocPoint` của pool này trong MasterChef v3 bằng **0**. Ở mốc đó nó không nhận CAKE emissions qua cơ chế phân bổ này. Phép thử đối chứng cùng lượt: pool USDT/WBNB mức 0,01% trả pid 137 với allocPoint 1.645, nên phép đọc không mù.

Để hình dung quy mô: cả nhánh v3 của PancakeSwap trên BSC ngày 08/08 ghi nhận 207.554 đô phí. Hai số này không cùng cửa sổ thời gian nên đừng dùng để tính tỷ trọng.

## Phần tới được CAKE

PancakeSwap gom phí rồi đốt CAKE mỗi thứ Hai. Hai tuần đã đốt xong gần nhất, đọc thẳng lượng CAKE từ các fee collector chảy vào ví đốt:

· tuần 27/07: **344.346 CAKE**
· tuần 03/08: **496.944 CAKE**

Tăng 44,3%. Quy ra tốc độ giảm cung cả năm thì được **−2,97%** và **−5,29%/năm**, so với mục tiêu PancakeSwap tự công bố là ít nhất 4%/năm.

Đừng nhân thẳng hai con số trên. Cung ròng mỗi tuần đổi bằng **hiệu** của hai dòng:

`cung ròng đổi = (CAKE mới phát ra mà không bị đốt ngay trong cùng sự kiện) − (CAKE đốt từ phí)`

· tuần 27/07: 150.871 − 344.346 = **−193.475**
· tuần 03/08: 152.180 − 496.944 = **−344.764**

Nhân 52,1786 rồi chia cho lượng CAKE lưu hành 340.269.999,51 đọc tại block 115.047.719. Vì tử số là một hiệu nên nó khuếch đại: lượng đốt tăng 1,44 lần mà tốc độ giảm cung tăng 1,78 lần.

## Tỷ lệ chuyển hoá rơi trong chính đợt phí tăng

Cùng một công thức cho cả ba tuần: lượng CAKE đốt từ phí quy ra đô, chia cho tổng gross fee của bảy ngày cùng tuần đó.

| tuần kết | burn CAKE | quy ra đô | gross fee 7 ngày | tỷ lệ |
|---|---:|---:|---:|---:|
| 20/07 | 358.571 | 504.127 | 1,19 triệu | **42,3%** |
| 27/07 | 344.346 | 481.417 | 0,94 triệu | **51,1%** |
| 03/08 | 496.944 | 701.949 | 3,29 triệu | **21,3%** |

Chỉ ba tuần đủ bảy ngày dữ liệu được đem so. Trung bình hai tuần đầu 46,7%, tuần 03/08 còn 21,3%, tức **0,46 lần**. Bỏ ngày đột biến 02/08 khỏi mẫu số thì 35,1%, tức 0,75 lần.

Mức tuyệt đối của tỷ lệ này **không dùng được**. Tử số là phần thanh toán theo tuần trên BSC, có cả perps, sau khi đã chuyển đổi; mẫu số là con số phí lý thuyết của adapter, chỉ BSC và chỉ DEX. Hai vế không cùng phạm vi, nên đừng đọc 21,3% thành "PancakeSwap giữ 21,3% phí". Cái so được là tỷ lệ đổi thế nào giữa các tuần, vì công thức giữ nguyên.

Nguyên nhân của cú rơi **chưa đo**. Ba ứng viên: phần tăng nằm ở v2 với tỷ lệ về burn khác v3; độ trễ giữa lúc thu phí và lúc mua CAKE; hoặc thay đổi ở nhánh sản phẩm phụ.

## Tuần đang chạy, kiểm được ngay lúc bạn đọc

Tính tới 13h14 ngày 10/08 giờ Việt Nam, ví đốt đã gom **599.033 CAKE** tiền phí và lệnh đốt tuần chưa chạy. Đọc lại lúc 14h22 vẫn y nguyên. Con số đó còn tăng cho tới lúc lệnh chạy, nên hãy đọc nó như một mức sàn.

Khi lệnh đốt tuần chạy, hiệu `totalSupply` trừ số dư địa chỉ đốt phải rơi xuống **không cao hơn 339.823.371,96**, và thấp hơn nữa đúng bằng phần phí gom thêm từ lúc đo tới lúc đốt.

Chỗ phải tự giới hạn: tuần đã đóng gần nhất, 496.944, vẫn thấp hơn mức trung bình **584.000 CAKE/tuần** của tháng 5 và 6, tính bằng trung bình 9 tuần đo cùng cách trong cửa sổ 04/05 đến 29/06. Lượng CAKE bị đốt từ nguồn phí mới hồi phục từ đáy gần nhất, chưa vượt được mức của hai tháng trước bằng một tuần đã chốt.

Giá CAKE trong tháng qua: **+4,7%**, đọc lúc 13h27 ngày 10/08 giờ Việt Nam.

## Cách tự kiểm

**Tỷ trọng volume theo mức phí.** Dune, bảng `dex.trades` lọc `blockchain='bnb'`, `project='pancakeswap'`, `version='3'`, nối với bảng pool sang mức phí dựng từ chính log `PoolCreated` của factory v3 `0x0bfbcf9fa4f9c56b0f40a671ad40e0805a091865`. Mức phí không lấy từ danh sách có sẵn. Ba phép thử: bảng pool sang mức phí phải trả đúng giá trị đã đọc độc lập bằng `fee()` on-chain cho ba pool (10000, 100, 100); volume của Dune chia trung vị DefiLlama ra 1,12 và 1,14 và 1,20; phí dựng lại từ tỷ trọng chia phí DefiLlama ra 1,02 và 1,04 và 1,20.

**Phí 24 giờ của pool.** Trên `https://bsc-dataseed.bnbchain.org`, đọc `feeGrowthGlobal0X128` và `feeGrowthGlobal1X128` của pool `0x6dafbf0ab4fd72e2a5c0ad5a1ed277d3bf8a8d1f` tại block 114.861.872 và 115.053.819, nhân hiệu với `liquidity`, chia 2^128. Quy về một đơn vị bằng `slot0()` của chính pool, 1 WBNB bằng 2.658,02 TUT. Công thức dùng `liquidity` một thời điểm cho cả cửa sổ, ở đây chặt vì `liquidity` chỉ đổi 0,2% trong 24 giờ.

**Emissions.** `v3PoolAddressPid(pool)` trên MasterChef v3 `0x556B9306565093C855AEA9AE92A594704c2Cd59e` trả pid 258; `poolInfo(258)` trả allocPoint bằng 0 tại block 115.053.639, trên tổng totalAllocPoint 6.526 của 588 pid.

**Ví đốt.** `balanceOf` của `0xceba60280fb0ecd9a5a26a1552b90944770a4a0e`. Tại block 115.047.719, tổng các dòng nạp vào bằng 99,999999% số dư ví, gồm collector v2 `0x0ed943ce…9706` 292.013,58 và collector v3 `0x518d9643…68a3` 268.156,08 và collector Infinity `0x75a91527…6f8e` 10.545,46, cộng hai dòng tự triệt tiêu.

**Vì sao hai ngày cuối bị loại khỏi mọi câu về phí.** Chuỗi phí theo ngày trả 0 cho nhánh AMM và AMM V3 ngày 09/08 và 10/08, trong khi cùng hai ngày đó cột volume vẫn có số. Một AMM đang chạy không thu 0 đồng phí. Đọc lại lần hai cách bảy tiếng: 08/08 và 09/08 y hệt lần đầu, riêng 10/08 có đổi. Nên mọi câu về phí theo ngày dừng ở 08/08.

**Nguồn số phụ.** Mức trung bình 584.000 CAKE mỗi tuần của tháng 5 và 6 là trung bình 9 tuần đo cùng cách, cửa sổ 04/05 đến 29/06. Giá CAKE và giá BNB lấy từ CoinGecko tại đúng giờ đã ghi.

## Cái gì bác được bài này

Nếu `feeGrowthGlobal` của pool TUT trong đúng cửa sổ block trên không ra 110,69 WBNB cộng 377.679 TUT. Nếu `poolInfo(258)` trả allocPoint khác 0 tại block 115.053.639. Nếu tỷ trọng volume ở mức 0,25% cộng 1% của giai đoạn C không cao hơn giai đoạn B ít nhất 2 lần. Nếu thứ tự ba giai đoạn của phí trên mỗi đô volume v3 không còn là giảm rồi tăng. Nếu tỷ lệ chuyển hoá của tuần 03/08 không thấp hơn trung bình hai tuần 20/07 và 27/07. Nếu tổng các dòng nạp vào ví đốt không còn bằng 99,999999% số dư ví tại block 115.047.719. Nếu sau lệnh đốt tuần này, `totalSupply` trừ số dư địa chỉ đốt cao hơn 339.823.371,96.

Sai chỗ nào thì sửa ngay tại chỗ đó.

## Bốn giới hạn

Con số 44,3% là so hai mốc tuần, không phải một xu hướng. Ba mẫu chưa đủ gọi tên, mẫu thứ tư rơi vào thứ Hai 17/08.

Bài không truy được tên thật của các venue hút phần volume còn lại ở giai đoạn B. Chúng mới có nhãn của bên tổng hợp dữ liệu, chưa ai đọc contract.

Bài không trả lời được hai đợt sóng này do đâu ra, và không đo được vì sao tỷ lệ chuyển hoá rơi.

Số của Dune và số của DefiLlama không đồng nhất phạm vi pool và cách định giá, ba tỷ số đối chiếu đều lớn hơn 1. Dùng để so hình dạng giữa ba giai đoạn, không dùng để thay số tuyệt đối của nhau.

*Không phải lời khuyên đầu tư.*
