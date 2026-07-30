---
title: Lido đổi cách chia phí ở module mới — nhưng gần 5 ngày sau, số dư được báo cáo vẫn là 0 ETH
date: 2026-07-29
mau: 🟡
ghim: Ethereum · block #25.637.121, timestamp 29/07/2026 07:53:59 UTC
mo_ta: Module mới của Lido đổi chia phí từ 350/650 sang 400/600 bp. Nhưng tại block 25.637.121 nó có 0 ETH reported balance, nên bảng phí mới đang có trọng số bằng 0.
anh: post05-card.png
kenh_x: https://x.com/blockpinned/status/2082421671152218340
---

Lido vừa nâng cấp Staking Router v3. CMv2 đổi cách chia phí — nhưng gần 5 ngày sau, số dư được báo cáo vẫn là **0 ETH**.

Đây là snapshot tại Ethereum block **25.637.121** — không phải kết luận về mọi block kể từ ngày upgrade.

## Hai bảng phí, đọc từ contract chứ không từ slide

Trong bản nâng cấp này, StakingRouter có thêm module thứ tư: **Curated Module v2 (CMv2)**. Điểm kinh tế dễ bị bỏ qua là CMv2 dùng một cách chia phí khác module cũ.

Ở hai module đang được so sánh, 10% phần thưởng staking được chia giữa operator và treasury. Lido tổ chức validator thành các staking module; mỗi module có tỷ lệ chia riêng.

| Mỗi 100 ETH phần thưởng | CMv1 (cũ) | CMv2 (mới) |
|---|---|---|
| operator — bên vận hành validator | 3,50 ETH | **4,00 ETH** |
| treasury — quỹ của DAO | 6,50 ETH | **6,00 ETH** |
| tổng | 10% | 10% |

Với mỗi 100 ETH phần thưởng được phân bổ theo CMv2 thay vì CMv1, operator được thêm 0,5 ETH, còn treasury bớt 0,5 ETH. Hai bảng phí này đọc trực tiếp từ StakingRouter tại block đo.

*(Các tỷ lệ trên là phần trăm trực tiếp của phần thưởng, không phải phần trăm của riêng khoản phí 10%.)*

## Nhưng đổi trong contract chưa đồng nghĩa đã có ETH tạo trọng số

Tại block đo, CMv2 có:

| Trạng thái | Giá trị |
|---|---|
| registered operators | **43** |
| depositable keys | 0 |
| deposited validators | 0 |
| reported balance | **0 ETH** |

43 operator cho thấy đã có người đăng ký vận hành. **Nó không có nghĩa stake đã di cư.** Bốn trạng thái này phải đọc riêng — operator đăng ký là một chuyện, còn biến đi vào công thức gộp fee là *reported balance*.

Tỷ lệ fee chung được tính theo balance của từng module: module giữ nhiều ETH hơn thì bảng phí của module đó có ảnh hưởng lớn hơn. CMv2 có 0 ETH reported balance, nên **tại block đo, bảng phí mới có trọng số bằng 0** trong phép tính này.

## Điều gì xảy ra khi ETH bắt đầu chuyển sang CMv2

StakingRouter trả tỷ lệ phân bổ treasury gộp tại block đo là **6,2085170404%** phần thưởng staking. Đây là tỷ lệ **trong công thức**, không phải số ETH thực tế đã được chuyển vào treasury.

Giữ nguyên tổng balance và fee của các module khác, rồi chỉ dịch balance từ CMv1 sang CMv2:

| Kịch bản chuyển | Treasury | Giảm |
|---|---|---|
| 0% | 6,2085% | — |
| 25% | 6,0962% | 1,81% |
| 50% | 5,9839% | 3,62% |
| 75% | 5,8717% | 5,43% |
| **100%** | **5,7594%** | **7,23%** |

**Con số −7,23% không phải doanh thu Lido vừa mất.** Đó là kết quả của một bài toán giả định: toàn bộ balance hiện tại của module cũ chuyển sang bảng phí mới, trong khi các yếu tố còn lại giữ nguyên.

Với người nắm LDO, đây là một cược tăng trưởng: DAO nhường 0,5 ETH trên mỗi 100 ETH phần thưởng cho operator. Giữ các yếu tố khác không đổi, quy mô phần thưởng tương ứng phải tăng **ít nhất 8,33%** mới bù được phần treasury giảm từ 6,50 xuống 6,00 ETH.

Người nắm LDO **không** tự động nhận khoản fee này. Tác động tới holder đi qua sức khoẻ DAO treasury, không phải một khoản trả trực tiếp.

Thực tế có thể đi theo hướng khác: nếu CMv2 hút thêm ETH mới và số ETH đó tạo đủ phần thưởng, treasury có thể nhận tỷ lệ thấp hơn trên mỗi ETH phần thưởng nhưng vẫn thu nhiều ETH hơn về tổng lượng. Muốn biết treasury thực nhận bao nhiêu ETH, phải đo phần thưởng phát sinh theo từng module trong kỳ.

Thông báo ngày 27/07 của Lido nói về lợi ích kinh tế cho operator và khả năng tuỳ chỉnh phí. Hai bảng số cụ thể ở trên đến từ StakingRouter.

## Phụ lục — địa chỉ và getter

| | Địa chỉ |
|---|---|
| StakingRouter | `0xfddf38947afb03c621c71b06c9c70bce73f12999` |
| CMv1 — curated-onchain-v1 | `0x55032650b14df07b85bf18a3a3ec8e0af2e028d5` |
| CMv2 — curated-onchain-v2 | `0xda5f930ce326eb5205085d66c72a4e79d60cb8c1` |

Share của CMv1 tại block đo: **89,8307%** số dư validator được báo cáo qua các module.

Trạng thái CMv2 đọc bằng `getStakingModuleSummary(4)` và `getModuleValidatorsBalance(4)`.

Tỷ lệ gộp đọc bằng `getStakingFeeAggregateDistribution()`. Bản `…E4Precision()` chỉ trả 6,20%; bài dùng bản đầy đủ rồi mới làm tròn. **Getter này trả một tỷ lệ phân bổ, không đo lượng ETH đã chuyển vào treasury.**

## Phụ lục — kiểm thêm số 0

Bốn contract consolidation và top-up được kiểm:

| Contract | Địa chỉ |
|---|---|
| ConsolidationGateway | `0x17be979344f2c2cc806229a532d92f8742c10462` |
| TopUpGateway | `0x3fc2c71579d80790aaa3fc7be8b66ac39dc57374` |
| ConsolidationBus | `0xd907ce33b4be423823d1cffe80bd147e8b8554c8` |
| ConsolidationMigrator | `0x9dc70b5a4f4f5e4af9058c983d560564f031f1d7` |

Trên Ethereum, cùng bộ lọc trả **0/0/0/0** log trong dải block 25.603.297–25.637.121. Mở rộng từ block 0 đến block đo trả **8/14/11/8** — tức công cụ và bộ lọc chạy được, số 0 kia là về dải block chứ không phải về công cụ. Kết quả này chỉ kiểm loại log đã chọn, không đại diện cho mọi hoạt động của bốn contract.

## Khi nào phải đo lại

- Balance được báo cáo của CMv2 đổi khỏi 0.
- DAO thay fee của CMv2.
- Tổng balance hoặc cơ cấu balance giữa các module thay đổi.

Đây là **trigger cập nhật**, không phải cách bác snapshot cũ.

*Ngưỡng dừng theo dõi: đến 18/09/2026, nếu CMv2 vẫn dưới 1% tổng balance module, BlockPinned hạ mức ưu tiên theo dõi chủ đề này trong năm 2026. Đây là quyết định biên tập, không bác bỏ snapshot tại block đo.*

## Tự kiểm

Gọi lại cùng các getter ở **đúng block 25.637.121**. Nếu kết quả khác **43 registered operators, 0 depositable keys, 0 deposited validators hoặc 0 ETH reported balance** — chỉ cần một trong bốn số khác đi — thì phép đo này sai.

Bảng giả định dựng lại được bằng chính hai bảng phí và share 89,8307%: chỉ dịch balance từ CMv1 sang CMv2 theo từng mức 0/25/50/75/100%, giữ mọi module khác không đổi.

Không phải lời khuyên đầu tư. Mọi số động đo tại Ethereum block 25.637.121, timestamp 29/07/2026 07:53:59 UTC.
