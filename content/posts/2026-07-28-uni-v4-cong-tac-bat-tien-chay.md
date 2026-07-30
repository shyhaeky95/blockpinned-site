---
title: Uniswap bật thu phí v4 — chỉ số giảm 53% sau một đêm, và nó không phải bộ đếm
date: 2026-07-28
mau: 🟡
ghim: Ethereum · cửa sổ 10,97 giờ ghim block hai đầu #25.624.853 → #25.628.131 (21h50 ngày 27/07 → 08h48 ngày 28/07, tức 14:50Z → 01:48Z)
kenh_x: https://x.com/blockpinned/status/2082128396382023921
---

Uniswap vừa bật thu phí v4. Một chỉ số phí của v4 trên Ethereum đã giảm 53% sau một đêm — **mức giảm đó không chứng minh doanh thu giảm.** Trang này ghim lại hơn 30 giờ đầu bằng bốn lần đo trực tiếp, và vì sao chỉ số kia sắp bị đọc ngược.

*(Mọi giờ là giờ Việt Nam, UTC để trong ngoặc.)*

## Bốn lần đo, bốn mốc thời gian

Hai đề xuất #99 và #100 được thực thi lúc 14h16 ngày 27/07 (07:16Z) — cả 8 cấu hình thu phí lật đúng đích như calldata đã ghim trước.

| # | Lúc | Đo được |
|---|---|---|
| 1 | 15h28 ngày 27/07 (08:28Z) | phí tích luỹ **bằng 0** trên toàn bộ 11 cặp chain–token |
| 2 | 21h51 ngày 27/07 (14:51Z) | **10/11 cặp khác 0** — lần đầu quan sát được số dư phí khác 0 |
| 3 | 08h48 ngày 28/07 (01:48Z) | Ethereum: ETH **−53%**, USDC **−61%** |
| 4 | 21h05 ngày 28/07 (14:05Z) | cùng một chain, hai token đi **hai hướng ngược nhau** |

Lượt đầu bằng 0 không phải lỗi đo: lúc đó mới 10 pool được bật thu phí, và cả 10 chưa có giao dịch nào kể từ lúc bật.

Lượt hai chạy lại đúng phép đo đó, đúng bộ cặp đó:

| Chain | Số dư phí |
|---|---|
| Ethereum | 0,4018 ETH + 207,88 USDC |
| Arbitrum | 0,0288 ETH + 21,92 USDC |
| Optimism | 0,0091 ETH + 21,51 USDC |
| Base | 0,000027 ETH (USDC còn 0 — cặp duy nhất) |
| Polygon | 66,48 POL + 22,31 USDC |

## Ai bật pool, và mẫu số nào mới đúng

Cùng buổi chiều, số pool được bật nhảy từ 10 lên **36.523** trong chưa đầy 8 giờ, qua 273 giao dịch trên Ethereum — và cả 273 giao dịch đó đều có `tx.from` là **một** địa chỉ (`0x2cf8e5b1…ce43`), gọi thẳng adapter phí.

Mẫu bật pool không phải quét toàn bộ: trong 36.523 pool đã bật khi đó, chỉ **2 pool gắn hook**, trong khi hook chiếm 23,56% số pool v4 trên Ethereum — nhóm mà chính sách hiện tại cho thu 0 phí. Vậy muốn tính tỉ lệ phủ theo chính sách hiện tại, mẫu số phải loại đúng nhóm đó:

| Mẫu số | Pool | Độ phủ |
|---|---|---|
| toàn bộ pool từng mở | 112.527 | 32,60% |
| **loại 26.512 pool gắn hook** | **86.015** | **42,65%** |

Đối chiếu tại block 25.628.131 cho 36.684 pool trùng nhau giữa danh sách không-hook và danh sách đã bật.

Sau đó nhịp bật pool giảm mạnh: từ 22h06 ngày 27/07 (15:06Z, 36.523 pool) đến 09h24 ngày 28/07 (02:24Z, blk 25.628.338) thêm 170 pool, rồi tới 21h35 ngày 28/07 (14:35Z, blk 25.631.951) thêm 103 pool nữa. Tổng 23,5 giờ thêm 273 pool — so với 36.523 pool trong 7,7 giờ của đợt đầu.

## Cái bẫy: đó là SỐ DƯ, không phải bộ đếm

Chỉ số tích luỹ phí của v4 — hàm `protocolFeesAccrued` trên PoolManager — không phải bộ đếm cộng dồn. Nó là **số dư**: phần phí còn nằm trong hợp đồng, chưa ai thu về kho.

Lượt ba: trên Ethereum số dư tụt từ 0,4018 xuống 0,1887 ETH (−53%) và 207,88 xuống 80,72 USDC (−61%). Trong đúng cửa sổ đó có giao dịch từ hai địa chỉ gọi hàm chuyển phí về kho — hàm công khai, ai gọi cũng được — và cùng cửa sổ đó vẫn có **4.382,57 đô phí mới chảy vào**. Mức giảm vì vậy không đọc được thành phí đã ngừng phát sinh.

Hai địa chỉ chuyển phí không trùng địa chỉ bật pool; chừng đó chưa đủ kết luận chúng thuộc những chủ thể khác nhau. Bốn chain còn lại cùng lúc vẫn đi lên, và trong cùng cửa sổ không thấy giao dịch chuyển phí nào trên bốn chain đó.

Lượt bốn thì ngay trong một chain nó cũng tách đôi:

| Cặp | Trước → sau |
|---|---|
| Ethereum ETH | 0,1887 → 0,0159 (**−92%**) |
| Ethereum USDC | 80,72 → 142,11 (**+76%**) |
| Arbitrum ETH | 0,0497 → 0,0048 (−90%) — cửa sổ này Arbitrum cũng có giao dịch chuyển phí |
| Optimism · Base · Polygon | vẫn đi lên |

Cùng một loại số dư, trên cùng một chain, trong cùng một buổi chiều, hai token đi hai hướng ngược nhau — và không hướng nào tự nó là doanh thu.

## Đo đúng thì đo thế nào

Số dư chỉ nói còn lại bao nhiêu, nên phải cộng thêm phần đã bị lấy đi mới ra phần đã sinh ra. Với từng token, trên cùng một hợp đồng, sau khi cộng đủ các giao dịch chuyển phí:

**phí phát sinh trong cửa sổ = (số dư sau − số dư trước) + tổng đã được chuyển khỏi hợp đồng**

Cửa sổ đầu tiên khép được là **10,97 giờ**, block ghim hai đầu 25.624.853 → 25.628.131, riêng Ethereum **4.382,57 đô**:

| Token | USD |
|---|---|
| ETH | 2.117,64 |
| USDC | 817,49 |
| LINK | 569,29 |
| USDT | 448,72 |
| *cộng 6 loại nữa* | |

Đây là **mức sàn**: mới định giá được 10/28 loại token — 18 loại còn lại có lượng thật nhưng chưa quy đô được — và mới 1/6 chain quy được ra tiền. Là con số gần *"doanh thu v4"* nhất trang này đo được, không phải chính nó.

## Phạm vi — nói đủ để không ai đọc quá tay

- **Không được nhân thành con số năm.** Đây là một cửa sổ 11 giờ ngay trong đợt triển khai, khi độ phủ còn đang đổi từng giờ.
- **Phần giá trị cuối cùng quy về UNI vẫn chưa tách được riêng cho v4.** Phí của v2, v3 và v4 vào chung một kho — trên rổ định giá được, v4 chiếm 17,71% giá trị dòng vào kho trong những giờ đầu — rồi kho mới được dùng để mua và đốt UNI, và bước đó chưa đo được.
- **Robinhood chưa nằm trong con số đô.** 118.221 pool đã được bật ở đó, nhiều nhất trong sáu chain, và 168 lượt thu phí trên 47 loại token — nhưng ở đó không có nguồn giá neo theo block nên chỉ đọc được bằng đơn vị token. Địa chỉ nói trên có mặt ở cả sáu chain, nhưng riêng Robinhood mới truy được người gửi của 400 trong 786 lượt bật (397 lượt là của nó); 386 lượt còn lại chưa biết ai, nên **không** được đọc thành *"một địa chỉ bật 118 nghìn pool"*.

## Tự kiểm

Số lượng token, giao dịch và block đọc từ hợp đồng v4 và log on-chain; phần quy ra đô dùng một nguồn giá riêng, đọc tại đúng block chốt cửa sổ.

1. **Hợp đồng PoolManager v4 trên Ethereum:** `0x000000000004444c5dc75cB358380D2e3dE08A90`
2. **Đọc `protocolFeesAccrued(địa_chỉ_token)` hai lần cách nhau vài giờ.** Nếu nó đi xuống trong lúc pool vẫn giao dịch, bạn đã tự chứng minh nó không phải bộ đếm chỉ tăng.
3. **Đối chiếu log `FeesCollected`** trong cùng cửa sổ, để xem phần giảm có đúng là số dư đã rời hợp đồng không.
4. **Số pool được bật:** đếm log `ProtocolFeeUpdated` từ block 25.622.594 — block thực thi đề xuất #99.

Không phải lời khuyên đầu tư. Cửa sổ đo: 15h28 ngày 27/07 → 21h05 ngày 28/07 giờ Việt Nam (08:28Z 27/07 → 14:05Z 28/07), block ghim theo từng phép đo.
