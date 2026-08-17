---
title: Một nguồn tiền từng được contract của ether.fi chuyển sang ví mua lại ETHFI đã đổi đích từ ngày 14/07/2026, khi bản nâng cấp xoá hàm gom khoản đó khỏi hợp đồng, trong khi tài liệu quản trị chính chủ vẫn mô tả cơ chế cũ
tieu_de_ngan: "ETHFI: một nguồn buyback đã đổi đích từ 14/07"
reading_layout: centered
token: ETHFI
date: 2026-08-17
gio: 17:45
mau: 🟡
ghim: Ethereum block 24.135.880 → 25.772.300 (2026-08-17T04:06Z) cho toàn bộ phép quét log; mốc nâng cấp block 25.533.308 (2026-07-14T20:36Z). WithdrawRequestNFT 0x7d5706f6ef3F89B3951E23e557CDFBC3239D4E2c; PriorityWithdrawalQueue 0x35e7D6feF6f72aDd3c3e39dEc6d9CCc29e3345FA; EtherFiRedemptionManager 0xDadEf1fFBFeaAB4f68A9fD181395F68b4e4E7Ae0; eETH 0x35fA164735182de50811E8e2E824cFb9B6118ac2; ví buyback 0x2f5301a3D59388c509C65f8698f521377D41Fd0F; Upgrade Timelock 0x9f26d4C958fD811A1F59B01B86Be7dFFc9d20761.
mo_ta: Tài liệu ether.fi nói 100% phí rút eETH dùng mua lại ETHFI hàng tuần. Cơ chế đó có thật, đã chuyển 355,66 ETH sang ví buyback, và bị xoá khỏi hợp đồng ngày 14/07/2026.
anh: card-ethfi-doi-dich.png
kenh_x: https://x.com/blockpinned/status/2089359697224892552
doc_lai: Đây là ảnh chụp trạng thái tại các block ghim, không phải một kết luận bền — hợp đồng có thể được nâng cấp lại bất cứ lúc nào sau đó. Con số quy đổi 676 nghìn USD dùng một mức giá ETH duy nhất tại 16/08, không dùng giá tại từng thời điểm phát sinh; phần ETH là số đo, phần USD là phép ngoại suy. Câu về việc các kênh chính chủ chưa mô tả thay đổi này có phạm vi hẹp: phép đọc kênh công bố chỉ phủ 5 trong số 160 bài mà tài khoản tự khai. Cầu nối từ "khoản đó ở lại quỹ" tới "làm tăng giá trị mỗi share eETH" đi bằng số học của hai dòng code, không bằng một phép đo dòng tiền riêng.
---

**Tài liệu quản trị của ether.fi nói 100% doanh thu từ phí rút eETH được dùng mua lại ETHFI, theo nhịp hàng tuần. Cơ chế đó có thật trong code. Ngày 14/07/2026, một bản nâng cấp xoá hàm thực hiện nó khỏi hợp đồng. Trang tài liệu vẫn giữ nguyên câu cũ.**

Điều đáng nói không phải là một cơ chế ngừng chạy. Là một khoản tiền vẫn phát sinh đều, vẫn chảy, nhưng từ một ngày cụ thể thì chảy sang người khác — và không văn bản nào của đối tượng, trong phạm vi BlockPinned đã đọc, mô tả việc đó.

## Khoản tiền đó là gì

Khi một người rút eETH theo đường chậm, hệ thống khoá phần share tương ứng với số họ yêu cầu, rồi tới lúc trả tiền thì trả **đúng số đã yêu cầu**. Phần share ấy có thể tăng giá trị trong thời gian chờ. Khoản chênh sinh ra không thuộc về người rút.

Tài liệu quản trị của ether.fi gọi đó là *"phí implicit của lượt rút chậm"*, và xếp nó cùng một chỗ với phí của đường rút nhanh:

> *"100% of all revenue generated from eETH withdrawal fees—both implicit (delayed exits) and explicit (instant exits)—is allocated to buybacks of $ETHFI. These buybacks are executed on a weekly cadence."*

Trang đó ghi **"Last updated 1 year ago"** và tới thời điểm đo vẫn chưa được sửa.

## Đường ống cũ: gom lại rồi chuyển sang ví buyback

Ở các bản contract của `WithdrawRequestNFT` chạy tới 12/02/2026, phần chênh mỗi lượt claim được dồn vào biến `totalRemainderEEthShares`, rồi hàm `handleRemainder()` chia nó theo tham số `shareRemainderSplitToTreasuryInBps` cho biến `treasury`. Source của chính bản đó tự chú thích ngay cạnh khai báo biến:

> *"this treasury address is set to ethfi buyback wallet address"*

Gọi `treasury()` tại một block trước 14/07 trả về `0x2f5301a3D59388c509C65f8698f521377D41Fd0F` — đúng ví mà tài liệu buyback tự khai. Ở bản đang chạy, lời gọi đó **revert** — báo lỗi thay vì trả về một địa chỉ: hàm không còn tồn tại.

Đo cửa sổ 01/04 tới 14/07/2026: **68 lượt chia, 355,658 ETH** đã đi từ đường rút chậm sang ví buyback. Trong cùng cửa sổ, phần đốt bằng **0** — tức toàn bộ phần gom được đưa sang ví, không phần nào bị đốt. Cộng thêm phí của đường rút nhanh trong cùng giai đoạn là **3,783 ETH**, tổng đã về ví buyback là **359,441 ETH**, khoảng **676 nghìn USD**.

Trong đúng cửa sổ đó, phép đo **không thấy một lượt mua ETHFI nào** từ ví ấy. Lượt mua thị trường cuối cùng ghi nhận được là **01/04/2026 lúc 21:34:47Z**.

## Ngày 14/07: một giao dịch nâng cấp 26 hợp đồng

Lúc **20:36Z ngày 14/07/2026**, block `25.533.308`, một giao dịch nâng cấp **26 proxy cùng lúc**, kèm **55 lần** đổi phân quyền trên `RoleRegistry`, và chính `RoleRegistry` cũng được nâng cấp trong đó.

Sau giao dịch này, `handleRemainder()` không còn, biến `treasury` không còn, và phần chênh mỗi lượt claim được quét **ngược về quỹ**. Lần chạy cuối cùng của hàm gom là **20:25Z cùng ngày** — mười một phút trước lần nâng cấp.

Từ mốc đó tới block `25.772.300`, phép lọc log không thấy **một leg nào** đi từ ba hợp đồng rút về ví buyback. Số 0 này có nghĩa vì cùng bộ lọc, cùng cách gọi, tìm ra **11.493 leg** ở đoạn từ block `24.781.450` tới `25.533.308` — chia ra `EtherFiRedemptionManager` 11.423, `WithdrawRequestNFT` 68, `PriorityWithdrawalQueue` 2.

## Từ 14/07, khoản đó ở lại trong eETH

Thiết kế mới trả tiền cho một lượt rút bằng cách gọi `LiquidityPool.withdraw(_amount, _share)`, và hàm đó làm đúng hai việc: trừ `_amount` khỏi tổng tài sản, rồi **đốt trọn** `_share` của yêu cầu.

Tỷ giá eETH chính là tổng tài sản chia cho tổng share. Đốt trọn share mà chỉ trừ đúng số đã trả cho người rút thì mẫu số nhỏ đi nhanh hơn tử số — nên tỷ giá tăng, cho tất cả những người còn giữ eETH. Đó là toàn bộ cơ chế, không có bước nào khác.

Điều này cũng có nghĩa phần chênh **không tồn tại như một số dư riêng** để ai đó rút ra dùng: nó không phải một khoản tiền nằm ở đâu, nó là một mẫu số nhỏ đi.

Đo từ block `25.533.308` tới `25.772.300`: **98,506 ETH** — `WithdrawRequestNFT` 97,898 và `PriorityWithdrawalQueue` 0,607. Con số này đọc thẳng từ log: mỗi lượt claim, giá trị ETH của phần share bị đốt trừ đi số ETH đã trả cho người rút.

## Ba lớp im lặng, ba ngày khác nhau

Cơ chế không tắt trong một lần. Nó tắt qua ba lớp:

**12/02/2026, 19:32:18Z** — thông báo buyback cuối cùng trên `x.com/ether_fi_Fdn`, đúng kênh mà tài liệu chỉ định làm nơi công bố.

**01/04/2026, 21:34:47Z** — lượt mua thị trường cuối cùng ghi nhận được.

**14/07/2026, 20:36Z** — hàm gom bị xoá khỏi hợp đồng.

Trong các nguồn chính chủ BlockPinned đã đọc, chưa thấy văn bản nào mô tả việc đổi đích này: không có ở các lá phiếu và chủ đề diễn đàn đã kiểm tra cho đợt này, **0 trên 4** bài blog về siết bảo mật cùng giai đoạn nhắc tới, và cửa sổ 01/06 → 18/08/2026 trên kênh công bố trả về **0 bài**.

## Một khoảng lệch riêng, ở cửa sổ trước đó

Mốc **15.571.023 USD** là tổng tích luỹ cuối cùng mà kênh công bố tự ghi, ngày 12/02. Dashboard chính chủ — nơi mà đề xuất treasury 50 triệu USD chỉ định làm chỗ báo cáo công khai — hiện ghi tổng tích luỹ **16.591.121,30 USD**. Chênh lệch **1.020.098 USD**.

Vì phép đo không ghi nhận lượt mua nào sau 01/04, phần chênh này nằm trong khoảng từ thông báo cuối 12/02 tới lượt mua cuối 01/04. Đây là chênh lệch giữa **hai con số tích luỹ** từ hai nguồn, không phải tổng giao dịch được đếm trực tiếp: nó cho thấy phần mua vào cao hơn phần từng được công bố, nhưng bài này không xác định từng giao dịch nào tạo ra khoảng lệch đó.

Tài liệu cam kết công bố **mọi** lượt buyback trên kênh đó.

## Việc gỡ không phải một hành động lén

Phần này phải nói, nếu không thì mọi đoạn trên nghe nghiêm trọng quá mức thực tế.

Giao dịch nâng cấp 14/07 đi qua một ví nhiều chữ ký cần **6 trên 10** người ký, `0xcdd57d11476c22d265722f68390b036f3da48c21`, rồi qua `Upgrade Timelock` với độ trễ tối thiểu **10 ngày** — đọc `getMinDelay()` tại cả block hiện tại lẫn block ngay trước lần nâng cấp, cả hai đều trả **864.000 giây**.

Ghép từng lệnh đã lên lịch với từng lệnh đã chạy theo `id`: **86 trên 86 cặp** ghép được, độ trễ thật ngắn nhất là **978.372 giây, tức 11,32 ngày**, và **0 trên 86** cặp chạy trước mức tối thiểu. Nghĩa là lệnh nằm công khai trên chain hơn mười một ngày trước khi nó chạy.

Bản nâng cấp cũng giải một vấn đề kỹ thuật thật: source mới tự ghi rằng cách đốt cũ để lại phần dư lắt nhắt, nên nay đốt trọn rồi quét phần thừa về lại quỹ.

Nên câu đúng không phải *"gỡ lén"*. Câu đúng là: quy trình nâng cấp công khai trên chain, còn phần thay đổi về **nơi dòng giá trị đi tới** thì chưa xuất hiện trong các nguồn đã kiểm tra.

## Hai chỗ dễ hiểu nhầm

**Tiền không mất, nó đổi đích.** ETHFI mất một nguồn buyback từng được tài trợ từ khoản chênh này; phần giá trị đó nay ở lại trong eETH. Người cầm ETHFI mất một nguồn cầu từ đường này, người còn giữ eETH được thêm một khoản lợi tức.

**Đường rút nhanh không bị gỡ.** Nó vẫn thu phí, và vẫn chuyển một phần cho một ví treasury — nhưng từ 14/07 là một địa chỉ **khác** ví buyback. Bài này chỉ nói về đường rút chậm; tổng phí của đường rút nhanh trong cửa sổ 01/04 → 17/08 đo được là **38,053 ETH** trên **213.955,37 ETH** khối lượng, tức **0,0178%**.

## Ba giới hạn của chính phép đo

**Phép đọc kênh công bố chỉ phủ được một phần.** Tài khoản tự khai 160 bài; bốn cửa sổ tìm kiếm cộng lại chỉ trả về 5 bài, và đường cuộn trực tiếp cũng dừng ở đó. Cái đỡ cho kết luận không phải độ phủ, mà là phép thử hai chiều: cùng một truy vấn, cửa sổ trước 01/04 trả về 4 bài và cả 4 đều là thông báo buyback; cửa sổ sau trả về 1 bài và nó không phải buyback. Bộ lọc không mù, và cửa sổ sau không rỗng vì lý do công cụ.

**Con số USD là phép ngoại suy.** 359,441 ETH phát sinh rải ra suốt 01/04 → 14/07, còn phép quy đổi dùng một mức giá ETH duy nhất tại 16/08. Phần ETH là số đo; phần USD không phải.

**Cầu nối tới eETH đi bằng số học, không bằng phép đo dòng tiền.** Nó chặt vì phần chênh không tồn tại như một số dư — nhưng ai muốn kiểm độc lập thì đo `amountForShare(1e18)` hai bên mốc 14/07 rồi so với 98,506 ETH. BlockPinned chưa làm phép đo đó trong bài này.

## Cách tự kiểm

**Hàm còn hay không.** Gọi `treasury()` trên `WithdrawRequestNFT` `0x7d5706f6ef3F89B3951E23e557CDFBC3239D4E2c` tại một block trước và một block sau `25.533.308`. Trước: trả về `0x2f5301a3D59388c509C65f8698f521377D41Fd0F`. Sau: revert.

**Dòng tiền dừng lúc nào.** Lọc log `Transfer` của eETH `0x35fA164735182de50811E8e2E824cFb9B6118ac2` với người gửi là ba hợp đồng rút và người nhận là ví buyback. Dải `24.781.450` → `25.533.308`: 11.493 leg. Dải `25.533.308` → `25.772.300`: 0 leg.

**Timelock có được tôn trọng.** Trên `0x9f26d4C958fD811A1F59B01B86Be7dFFc9d20761`, ghép `CallScheduled` với `CallExecuted` theo `id`. Trường `delay` nằm ở word thứ 4 của data, không phải word cuối — word cuối thuộc payload `bytes`, và đọc nhầm chỗ đó cho ra những con số vô nghĩa cỡ 10⁷⁶ cho một đại lượng tính bằng giây.

**Ngày sửa cuối của tài liệu** đọc ngay trên đầu trang `etherfi.gitbook.io/gov/ethfi-buyback-program`.

## Cái gì bác được bài này

Nếu trong dải block `25.533.308` → `25.772.300` tìm được **ít nhất một** log `Transfer` eETH từ một trong ba hợp đồng rút tới ví buyback, **và** trace của giao dịch cho thấy transfer đó phát sinh từ đường xử lý phần chênh sau rút, thì câu *"đường rút chậm không còn chuyển khoản đó sang ví buyback"* phải rút lại. Vế thứ hai là bắt buộc: một transfer chỉ khớp người gửi và người nhận thì chưa tự chứng minh nó đến từ đường ấy.

Nếu tìm được **một** nguồn chính chủ nói rõ khoản chênh không còn tài trợ buyback và nay quay về quỹ, thì phần nói về việc các kênh chưa mô tả thay đổi này phải bỏ.

Nếu gọi `treasury()` trên `WithdrawRequestNFT` tại một block sau `25.533.308` mà nó trả về một địa chỉ thay vì revert, phần đo về việc hàm bị xoá phải đọc lại từ đầu.

Bài này **không** nói ether.fi ngừng mua lại ETHFI, và **không** nói có ai lấy khoản tiền đó. Nó nói đúng một chuyện: một nguồn từng chảy về ví buyback nay chảy sang chỗ khác, và tài liệu chính chủ vẫn mô tả cơ chế cũ.

Sai ở đâu, BlockPinned sửa ngay tại đó.

*Không phải lời khuyên đầu tư.*
