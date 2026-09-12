---
title: 13 mốc trong 360 ngày: tỉ giá sENA không đổi một chữ số
tieu_de_ngan: 13 mốc trong 360 ngày: tỉ giá sENA không đổi một chữ số
phu_de: Vault có hơn một tỷ ENA không đồng nghĩa người stake đang được trả. Thứ cần nhìn là một share đổi được bao nhiêu tài sản.
reading_layout: centered
token: ENA
date: 2026-09-11
gio: "22:43"
mau: 🟡
ghim: 13 mốc tháng trên Ethereum, từ block 23.225.778 (26/08/2025) tới block 25.804.000 (21/08/2026); cửa sổ đúng 360 ngày.
mo_ta: Tại 13 mốc tháng, convertToAssets(1e18) của sENA cùng trả 1,018269352422694832 ENA; trong toàn cửa sổ, vault phát 0 RewardsReceived. Lợi suất tích luỹ trong tỉ giá vault là 0,0000%.
anh: card-ena-stake-360-ngay-ti-gia-khong-tang.png
doc_lai: Bài đo lợi suất tích luỹ trong tỉ giá vault sENA, không đo lời lỗ do giá ENA. Tỉ giá được đọc tại 13 mốc; bài không khẳng định trạng thái liên tục ở mọi block giữa các mốc.
---

**Tại 13 mốc trong cửa sổ 360 ngày, `totalAssets()` và `totalSupply()` của sENA thay đổi nhưng một share vẫn đổi được đúng `1,018269352422694832` ENA.**

Không phải gần bằng. Không phải làm tròn rồi trùng. Chuỗi số giống nhau tới từng chữ số.

Trong cùng cửa sổ, vault sENA phát **0** event `RewardsReceived`. Lợi suất tích luỹ trong tỉ giá vault sENA ở cửa sổ này: **0,0000%**.

Trong cùng 360 ngày, sUSDe lại ghi nhận **1.076** lượt `RewardsReceived`, tổng **157.063.738,58 USDe**. Tỉ giá của nó tăng **4,4118%**, tương đương APY **4,4744%**.

Đường đo vẫn bắt được phần thưởng ở sUSDe. Riêng qua vault sENA trong cửa sổ này, `RewardsReceived` bằng 0 và tỉ giá đầu–cuối không đổi.

## Vault to ra không có nghĩa người cũ có lãi

sENA là một vault theo chuẩn ERC-4626. Khi gửi ENA vào, người dùng nhận share sENA. Có hai cách làm lượng ENA trong vault tăng, nhưng chỉ một cách tạo lợi suất cho người đã ở đó.

Cách thứ nhất là có người mới gửi tiền. Tài sản trong vault tăng, nhưng số share cũng tăng theo. Miếng bánh lớn hơn và số phần chia cũng nhiều hơn; mỗi phần không đáng giá hơn.

Cách thứ hai là bơm phần thưởng vào vault mà không phát thêm lượng share tương ứng. Khi đó, mỗi sENA đổi được nhiều ENA hơn. Tỉ giá `convertToAssets(1e18)` phải đi lên.

Đó là lý do chỉ nhìn `totalAssets` hoặc câu “hơn một tỷ ENA đang stake” là chưa đủ. Con số quyết định là **một share đổi được bao nhiêu tài sản**.

Tại 13 mốc đã ghim, `totalAssets()` và `totalSupply()` thay đổi nhưng `convertToAssets(1e18)` vẫn bằng **1,018269352422694832 ENA**.

Hai giao dịch của Safe `0xdedc…fe96` cho thấy cái bẫy này. Calldata gọi `deposit(uint256,address)` vào sENA: [giao dịch thứ nhất](https://etherscan.io/tx/0xeead913589bf23fc2f6ec18c982f90190a6b8a5787c061cc90bfea1465e61100) nạp **375 triệu ENA** và mint **368.271.910,676472335089129713 sENA**; [giao dịch thứ hai](https://etherscan.io/tx/0x57a2e397c0baefdb3b30e922b75a9e5eb6cf6f194cdeff90dd14f3ea8c2d3a70) nạp **270 triệu ENA** và mint **265.155.775,687060081264171394 sENA** cho cùng Safe. Đây là **645 triệu ENA tiền gửi nhận share**, không phải `transferInRewards`.

## Đặt cạnh sUSDe, số 0 mới có nghĩa

sUSDe là đối chứng dương cho riêng hai đường đọc dùng trong bài: tỉ giá vault và event `RewardsReceived`.

Ngày 26/08/2025, một sUSDe đổi được **1,1918154 USDe**. Đến ngày 21/08/2026, con số là **1,2443953**. Mức tăng tích luỹ **4,4118%** trong 360 ngày tương đương APY **4,4744%**.

Chuỗi event kể cùng một câu chuyện: **1.076** `RewardsReceived`, tổng **157,06 triệu USDe**. Một đường đo độc lập — các `Transfer` từ rewards distributor vào sUSDe — khớp với tổng event.

sENA cho kết quả khác trong đúng phạm vi đo: cùng một tỉ giá tại 13 mốc và 0 `RewardsReceived` trong toàn cửa sổ.

## Doanh thu của sản phẩm không tự động thuộc về token

Đây là chỗ dễ nhầm nhất khi định giá token của một protocol có sản phẩm sinh doanh thu.

USDe có cơ chế đưa phần thưởng về người giữ sUSDe; hai tín hiệu on-chain trong bài đều ghi nhận dòng đó. Điều này chưa tự chứng minh doanh thu của sản phẩm trở thành dòng tiền của holder ENA.

Trong cửa sổ bài này đo, chưa thấy phần thưởng đi vào tỉ giá sENA qua hai dấu hiệu đã kiểm: APY **0,0000%** và **0** `RewardsReceived`. Trong phép quét burn trên Ethereum dùng cho bài này, tính tới block **25.804.000**, `totalSupply` ENA là **15 tỷ** tại mọi mốc đã ghim và số `Transfer` tới địa chỉ 0 là **0**.

Ở đường protocol mua rồi giữ ENA, bảy địa chỉ đã biết ngoài Safe nạp ENA vào sENA không nhận ENA trong cửa sổ. Kết quả chỉ áp dụng cho tập địa chỉ này; một địa chỉ thực thi chưa được nhận diện sẽ không hiện trong phép quét.

Vì vậy, không thể lấy kết quả này để phủ nhận doanh thu của Ethena hay mọi nguồn lợi nhuận của người giữ ENA. Bài này không đo biến động giá ENA.

Câu đủ bằng chứng là:

> **Tại 13 mốc trong cửa sổ 360 ngày, lợi suất tích luỹ trong tỉ giá vault sENA là 0,0000%; trong toàn cửa sổ, sENA ghi nhận 0 `RewardsReceived`.**

Đó là hai tài sản khác nhau và hai dòng tiền khác nhau. Doanh thu ở cấp sản phẩm không thể tự động coi là dòng tiền thuộc về holder khi định giá ENA, nếu chưa chỉ ra đường tiền đó đi tới holder.

## Tỉ giá đầu kỳ không phải APY của kỳ đo

Một sENA đổi được hơn một ENA có thể tạo cảm giác vault đã sinh lời. Nhưng tỉ giá đầu cửa sổ đã ở **1,018269352422694832** và cuối cửa sổ vẫn đúng bằng số đó.

Phần hơn **1,8%** là di sản có từ trước ngày đo đầu tiên. Nó không phải lợi suất được tạo ra trong 360 ngày này. Lấy tỉ giá cuối kỳ trừ mốc 1 rồi gọi toàn bộ phần chênh là “APY hiện tại” sẽ cộng cả lịch sử cũ vào năm nay.

Phép tính đúng là lấy tỉ giá cuối kỳ chia tỉ giá đầu kỳ, rồi annualize theo đúng số ngày. Ở đây hai tỉ giá bằng nhau, nên kết quả là **0,0000%**.

## Điều bài này chưa nói

Bài này không kết luận cơ chế chia phí cho ENA sẽ không bao giờ được bật. Nó chỉ ghi một cửa sổ lịch sử đã đóng: từ 26/08/2025 tới 21/08/2026.

Bài cũng không nói mọi holder ENA đều có kết quả bằng 0. Người mua ENA có thể lời hoặc lỗ do giá; người dùng có thể nhận incentive ở một sản phẩm khác. Đại lượng được đo ở đây hẹp hơn: **lợi suất tích luỹ trong tỉ giá sENA**.

Cuối cùng, không có event không tự nó đủ để kết luận không có phần thưởng. Bài dùng hai tín hiệu: event bằng 0 trong toàn cửa sổ **và** tỉ giá share bằng nhau tại 13 mốc. Phép đo không loại trừ một dao động nằm trọn giữa hai mốc rồi bị bù ngược trước mốc kế tiếp.

## Phần kiểm chứng — cách tự kiểm

**Tỉ giá sENA.** Gọi `convertToAssets(1000000000000000000)` trên sENA [`0x8bE3…B3b9`](https://etherscan.io/address/0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9) tại 13 block: `23.225.778`, `23.440.545`, `23.654.963`, `23.869.204`, `24.082.969`, `24.297.975`, `24.512.902`, `24.727.885`, `24.943.138`, `25.158.467`, `25.373.633`, `25.588.759`, `25.804.000`. Mỗi lần phải trả đúng `1018269352422694832` wei ENA, tức **1,018269352422694832 ENA**.

**Event.** Quét `RewardsReceived` của sENA từ block 23.225.778 tới 25.804.000: kết quả phải bằng **0**. Chạy cùng bộ quét trên sUSDe phải ra **1.076 event** và tổng **157.063.738,58 USDe**; đây là control dương cho đường đọc log.

**Phân biệt 645 triệu ENA nạp vào với phần thưởng.** Hai tx cần kiểm là [`0xeead…1100`](https://etherscan.io/tx/0xeead913589bf23fc2f6ec18c982f90190a6b8a5787c061cc90bfea1465e61100) tại block `23.734.992` và [`0x57a2…3a70`](https://etherscan.io/tx/0x57a2e397c0baefdb3b30e922b75a9e5eb6cf6f194cdeff90dd14f3ea8c2d3a70) tại block `24.994.185`. Giải mã payload `multiSend(bytes)` phải thấy lần lượt `approve` rồi `deposit(375000000 ENA, Safe)` và `approve` rồi `deposit(270000000 ENA, Safe)`. Receipt phải có `Transfer` mint từ địa chỉ 0 tới Safe lần lượt `368271910676472335089129713` và `265155775687060081264171394` wei sENA. `convertToAssets(1e18)` tại block ngay trước và block chứa mỗi tx đều trả `1018269352422694832` wei ENA.

**Tập địa chỉ nhận ENA.** Ngoài Safe nạp vào sENA, phép quét cho đường protocol mua rồi giữ dùng đúng bảy địa chỉ: payout fund [`0x71e4…3a87`](https://etherscan.io/address/0x71e4f98e8f20c88112489de3dded4489802a3a87), Reserve Fund [`0x2b5a…d4d5`](https://etherscan.io/address/0x2b5ab59163a6e93b4486f6055d33ca4a115dd4d5), dev multisig [`0x3b0a…1862`](https://etherscan.io/address/0x3b0aaf6e6fcd4a7ceef8c92c32dfea9e64dc1862), Safe thứ năm [`0xa075…c344`](https://etherscan.io/address/0xa07591b02fbd07d03df21ed9a574f058bf45c344), timelock 24h [`0xe8dc…7c94`](https://etherscan.io/address/0xe8dc0fab349ea169283c48ccfd09d797e6db7c94), guard [`0x74ab…8d29`](https://etherscan.io/address/0x74abe7805541c28f31953b3cda9711dc96278d29) và rewards distributor [`0xf2fa…b439`](https://etherscan.io/address/0xf2fa332bd83149c66b09b45670bce64746c6b439). Quét `Transfer` ENA đi vào từng địa chỉ từ block `23.225.778` tới `25.804.000`; cả bảy phải bằng 0. Kết quả chỉ áp dụng cho tập bảy địa chỉ đã biết, không phủ định mọi địa chỉ có thể tồn tại.

**Burn.** Đọc `ENA.totalSupply()` tại 13 block trên và quét `Transfer` của ENA [`0x57e1…6061`](https://etherscan.io/address/0x57e114b691db790c35207b2e685d4a43181e6061) tới `0x0000000000000000000000000000000000000000` từ block 0 tới `25.804.000`. Kết quả cần là **15.000.000.000 ENA** ở từng mốc và **0** log tới địa chỉ 0.

**Điều bác bỏ.** Claim trung tâm sai nếu bất kỳ một trong 13 block đã ghim trả `convertToAssets(1e18)` khác `1018269352422694832` wei ENA, hoặc quét cửa sổ ra một `RewardsReceived` trên sENA. Claim đối chứng sai nếu một trong hai đường không tái lập được: mức tăng tỉ giá **4,4118%**, hoặc **1.076** `RewardsReceived` với tổng **157.063.738,58 USDe**.

*Không phải lời khuyên đầu tư.*
