---
title: Ai đang trả protocol fee của Uniswap v4, và pool nào vẫn đang trả 0
token: UNI
date: 2026-07-30
mau: 🔴
ghim: Ethereum · block #25.643.032 (đoạn 400 block) · DualPool tại block #25.642.998 · đọc lại 30/07/2026 06:40:36 UTC
mo_ta: Trong 5.413 lượt swap của một đoạn 400 block, protocol fee được cộng vào phần người swap trả chứ không trừ khỏi pool fee. Cùng lúc, bốn pool dùng hook DualPool trả về 0.
anh: card-uni-v4-incidence.png
kenh_x: https://x.com/blockpinned/status/2082737959380418674
---

Protocol fee v4 của Uniswap đã được kích hoạt ba ngày. Nhưng trong đoạn Ethereum được đo hôm nay, không phải pool nào cũng đang thu — và bốn pool dùng hook mà Uniswap Labs công bố live hôm nay đều có protocol fee bằng **0**.

Đọc mức phí thực tính của **5.413** lượt swap trong một đoạn **400 block** trên Ethereum, kết thúc tại block **25.643.032**:

- **2.899** lượt mang một trong bốn giá trị đã được mô hình cộng thêm ghi ra trước; kiểm ngược theo từng pool hiện mới chạy trên **8 pool, 8/8 khớp**
- **328** lượt chỉ ghi nhận đúng pool fee, chưa có phần protocol fee cộng thêm

Ở một phép đo riêng, tại block **25.642.998**, registry của factory khai đúng **4** hook **DualPool**; log deploy cũng đếm ra đúng **4**. Bốn pool dùng bốn hook đó đều trả về protocol fee bằng **0**.

## Trong 8 pool đã kiểm ngược, người swap trả phần protocol fee; LP không bị trừ khỏi pool fee

Câu đang khiến một số người rút thanh khoản là: *"Protocol ăn 25% phí của LP."*

Trong đoạn 400 block trên Ethereum, với các pool không hook được kiểm, dữ liệu cho kết quả khác.

Một pool có pool fee **0,30%** và đã bật protocol fee đang thu tổng cộng **0,3499%**. Phần **0,30%** của LP còn nguyên. Phần chênh được cộng vào số người swap phải trả.

Cách kiểm không bắt đầu bằng việc nhìn dữ liệu rồi tìm lời giải thích. Với bốn mức pool fee được kiểm trong bài, hỏi hợp đồng xem protocol fee của một pool **không hook** đang được đặt ở mức nào. Sau đó tính tổng phí người swap phải trả nếu cơ chế là cộng thêm, ghi bốn đáp án ra trước — rồi mới mở dữ liệu swap.

| pool fee | protocol fee | tổng phí dự đoán | thấy trong swap thật |
|---|---|---|---|
| 0,01% | 0,0025% | **0,0125%** | 1.043 lượt / 33 pool |
| 0,05% | 0,0125% | **0,0625%** | 490 lượt / 31 pool |
| 0,30% | 0,05% | **0,3499%** | 848 lượt / 126 pool |
| 1,00% | 0,10% | **1,0990%** | 518 lượt / 98 pool |

Cả bốn giá trị ghi trước đều xuất hiện trong dữ liệu. Việc xác nhận nguyên nhân theo từng pool hiện mới hoàn tất trên **8 pool, 8/8 khớp**.

Cả bốn tổng phí quan sát được đều **lớn hơn** pool fee tương ứng. Kết quả đó không phù hợp với giả thuyết protocol fee bị trừ khỏi chính pool fee đã niêm yết.

Riêng con số **0,3499%**, thay vì **0,35%** chẵn, cũng là một dấu vết: công thức trừ đi một phần tích của hai số. Đây là kết quả đọc từ hợp đồng, không phải phép cộng nhẩm.

## Điều gì bác được cách gán 2.899 lượt cho protocol fee

Lấy bất kỳ pool nào trong **126** pool ghi giá trị **3.499** — tương ứng tổng phí **0,3499%** — trong đoạn đó. Hỏi lại hợp đồng tính phí bằng đúng bộ trường của pool, tại đúng block.

Nếu hợp đồng trả protocol fee bằng **0**, thì ở pool đó, giá trị **3.499** là pool fee của chính pool, không phải phần protocol được cộng thêm. Khi đó câu mở bài phải hạ xuống *"2.899 lượt mang giá trị trùng dự đoán"*, và không được gọi toàn bộ số đó là dấu hiệu protocol fee.

Phép kiểm này đã chạy trên **8 pool, 8/8 khớp**. **118 pool còn lại chưa chạy.** Ai chạy tiếp và tìm thấy kết quả khác, con số mở bài của bài này phải sửa.

## "25%" không phải con số bịa. Nó thuộc về phiên bản khác

Theo tài liệu của Uniswap, v2 mô tả protocol fee bằng **một phần sáu** phí LP, còn v3 có một mức bằng **một phần tư**. Trong hai cơ chế đó, phần protocol được lấy từ khoản phí vốn dành cho LP.

Người nói "25%" đang trích đúng ngôn ngữ của Uniswap. Chỗ trượt là mang cách tính đó sang v4.

Phần v2/v3 ở đây là trích nguồn. Kênh này chưa đo hai phiên bản đó trên chain bằng phương pháp vừa dùng với v4.

## Bốn pool dùng hook mới của Uniswap Labs đang thu 0

Mỗi pool v4 được nhận diện bằng một bộ trường. Một trong các trường đó là địa chỉ **hook** — hợp đồng có thể chạy kèm mỗi lần swap.

Hôm nay, Uniswap Labs công bố **DualPool** đã live. Đây là hook họ xây cùng Spark, được nêu là đích đến của **150 triệu USD** thanh khoản Spark đã chuyển sang v4 từ tháng 6.

Tại block **25.642.998**, hai đường đếm độc lập trả về cùng một tập: registry của factory khai **4** hook, log deploy của factory cũng trả về **4**. Giới hạn của phép đếm là các hook được đăng ký tại factory đó.

Bốn pool dùng bốn hook DualPool ấy đều trả về protocol fee bằng **0**.

Để đối chứng, giữ nguyên toàn bộ trường của từng pool, chỉ thay địa chỉ hook bằng địa chỉ rỗng rồi hỏi lại hợp đồng.

| pool | pool fee | protocol fee | cùng khoá, bỏ hook | swap |
|---|---|---|---|---|
| `0xda85f9c1…` USDC/USDT | 0,001% | **0** | 0,0002% | 32 |
| `0x51d00841…` | 1,00% | **0** | 0,10% | 1 |
| `0x7647d633…` | 1,00% | **0** | 0,10% | 129 |
| `0xf0ac1894…` | 1,00% | **0** | 0,10% | 27 |

Chỉ thay trường hook, kết quả chuyển từ 0 sang mức dành cho pool không hook tương ứng.

Phép kiểm thứ hai đi thẳng vào dữ liệu giao dịch: trong **189** swap của bốn pool đó, mức phí thực tính đều bằng đúng pool fee. Không swap nào ghi nhận protocol fee lớn hơn 0.

## Vì sao chưa thu — và vì sao đây không phải quy luật của mọi pool có hook

Với mỗi pool, hợp đồng chính sách chọn một trong ba mức: mức dành cho pool không hook, mức riêng đã được gán cho một hook, hoặc mức mặc định khi hook chưa được gán vào nhóm nào.

Bốn cấu hình pool dùng hook DualPool hiện rơi vào trường hợp thứ ba. Mức mặc định đang là **0**.

Hai điều kiện hiện cùng tồn tại: mức mặc định bằng 0 và DualPool chưa được gán mức protocol fee riêng. Điều đó không có nghĩa mọi pool có hook đều được miễn protocol fee — pool dùng một hook đã được gán mức riêng sẽ áp dụng mức đó.

Sáu chain đã bật protocol fee v4 sử dụng **sáu** hợp đồng chính sách có địa chỉ khác nhau nhưng đang mang cùng một bộ giá trị.

| chain | hợp đồng chính sách | block đọc lại |
|---|---|---|
| ethereum | `0x1cd822b7…a314` | 25.643.933 |
| arbitrum | `0x8f6a5a19…bd0b` | 489.208.042 |
| optimism | `0x13d9d198…2eb8` | 154.897.430 |
| base | `0xf963bdbe…ab71` | 49.302.145 |
| polygon | `0x600c29d3…6093` | 91.125.747 |
| robinhood | `0x6ee98430…3dfc` | 23.107.483 |

Lúc **13h40 ngày 30/07/2026 (06:40Z)**, mức mặc định và cấu hình phân nhóm DualPool tương ứng chưa đổi trên sáu chain đã kiểm.

## Điều gì làm kết luận về trạng thái hiện tại hết đúng

Kết luận "bốn pool dùng hook DualPool đang có protocol fee bằng 0" hết hiệu lực nếu một trong hai việc xảy ra: mức mặc định được đặt lớn hơn 0, hoặc các hook DualPool được gán một mức protocol fee lớn hơn 0.

Nếu cấu hình mới được triển khai trên đủ sáu hợp đồng chính sách, trạng thái của cả sáu chain sẽ đổi. Các kết quả tại những block đã ghi trong bài vẫn giữ nguyên giá trị lịch sử.

Vì vậy, câu hỏi cho người cầm UNI không còn là *"Fee switch đã bật chưa?"* — nó đã bật. Câu hỏi đáng theo dõi hơn là: **pool nào đang sinh protocol fee, ai trả khoản đó, và cấu hình nào vẫn đang để nó bằng 0?**

## Tự kiểm — địa chỉ, lệnh gọi, và hai lệnh kiểm lại trạng thái

Hợp đồng dùng trong bài:

- PoolManager (Ethereum) — `0x000000000004444c5dc75cb358380d2e3de08a90`
- V4FeeAdapter, nơi hỏi protocol fee của một pool — `0x89a5d5bf00a27d55c02951e49078a5c5771051db`
- Hợp đồng chính sách (Ethereum) — `0x1cd822b70a0591420f65e94b9b3a0d0b0fb3a314`
- AllowlistedFactory của DualPool, tạo tại block 25.581.749 — `0x0000000000077769c332e0d3ed8bc8e02a0ce108`

**Bốn mức phí.** Gọi `getFee((address,address,uint24,int24,address))` trên V4FeeAdapter với một PoolKey không hook (ô cuối để `address(0)`), lấy 12 bit thấp. Đơn vị là pip: 3.000 = 0,30%. Công thức trong `ProtocolFeeLibrary` là `swapFee = protocolFee + lpFee − protocolFee × lpFee / 1.000.000` — đó là lý do 500 cộng 3.000 ra **3.499**, không phải 3.500. Pool dynamic-fee (`lpFee = 0x800000`) nằm ngoài phép thử này.

**Nguồn đã deploy, không phải nhánh main trên GitHub.** `getsourcecode` của PoolManager trả `v0.8.26+commit.8a97fa7a`, chứa `calculateSwapFee` và chú thích *"swapFee is the pool's fee in pips (LP fee + protocol fee)"*.

**Bốn hook DualPool.** `allDeploymentsLength()` trả 4, và log `Deployed(address,bytes32,address,bytes,bytes32)` cũng trả 4 — cùng một tập bốn địa chỉ, cùng creation code hash `0xb63b7eea…`. Provenance kiểm hai chiều từng hook: `factory.isFromFactory(hook)` là true và `hook.factory()` bằng factory. Chủ bốn hook là bốn địa chỉ khác nhau; địa chỉ đầu trùng đúng địa chỉ đã tạo factory. Không địa chỉ nào được định danh là Spark.

**Cơ chế.** Trên hợp đồng chính sách: `isHookedNativeMathFeeOn()` trả false, `defaultFee()` trả 0, `hookFamilyId(hook)` trả 0 cho cả bốn. DualPoolHook khai bốn cờ `*ReturnDelta` đều false, tức pool native-math có hook; nhánh đó không đi qua bảng mức theo nhóm và dùng `defaultFee`.

**Hai lệnh kiểm lại trạng thái.** Gọi `defaultFee()` và `hookFamilyId(<hook>)` trên hợp đồng chính sách của bất kỳ chain nào ở bảng trên. Ra khác 0 nghĩa là cấu hình đã đổi và kết luận về trạng thái hiện tại hết đúng — các block đã ghim trong bài không vì thế mà sai.

**Control, vì sao số 0 ở trên không phải lỗi công cụ.** Control dương: `getCode(PoolManager)` trả 24.009 byte trên cả sáu chain; ra 0 thì mọi số 0 phía trên vô nghĩa. Control âm: địa chỉ rác trả `0x`, không phải 0. Đáp án biết trước: pool không hook pool-fee 0,30% phải ra 500 pip, 0,05% ra 125 pip. Archive: hỏi state ở block tương lai phải báo lỗi. Giải mã: không thấy mức chuẩn nào trong histogram nghĩa là offset trường `fee` bóc sai và mọi số sau là rác. Lượt đọc lại ngày 30/07 chạy 4/4 phép thử trên 6/6 chain.

Một ghi chú về chính lượt đó: endpoint RPC của Robinhood trả HTTP 403 với User-Agent mặc định và trả block bình thường với User-Agent trình duyệt. Không có dòng sửa đó thì Robinhood bị đọc thành "RPC hỏng", và câu "sáu chain" tụt xuống năm — một phát biểu về công cụ đội lốt phát biểu về chain.

## Bốn điều bài này không nói

**1.** **2.899/5.413** là số lượt mang giá trị trùng dự đoán, không phải số swap đã được xác nhận từng cái. Kiểm ngược theo pool hiện mới chạy 8/8. Và đây là phép đếm theo lượt, không phải theo khối lượng: một lệnh nhỏ và một lệnh lớn được tính như nhau.

**2.** **150 triệu USD** của Spark chưa được xác nhận nằm trong bốn pool đã đo. Chủ pool USDC/USDT là chính địa chỉ đã tạo factory; ba pool còn lại có ba chủ khác; thông báo được viết ở thì tương lai. Câu có thể nói hiện tại là: bốn pool đó đã tồn tại với protocol fee bằng 0 trước khi bài này xác nhận được thanh khoản Spark đi vào chúng.

**3.** Trên năm chain ngoài Ethereum, bài này mới kiểm ở tầng cấu hình hợp đồng. Chưa đo swap volume, protocol fee thực thu hoặc doanh thu phát sinh trên năm chain đó.

**4.** Không có một tỷ lệ duy nhất cho câu "protocol lấy bao nhiêu". Ở pool fee 0,30%, phần protocol chiếm khoảng **14%** tổng phí swap. Ở pool fee 0,05%, tỷ lệ đó là **20%**.

## Một ghi chú nội bộ cũ của tôi cũng viết sai đúng chỗ này

Một dòng cũ ghi *"0,05% bằng 16,7% phí LP"*. Con số **16,7%** vẫn mô tả đúng độ lớn tương đối: 0,05 chia 0,30. Nhưng cách viết đó khiến người đọc hiểu LP bị lấy mất một phần phí. Trong mẫu v4 vừa đo, cách hiểu đó không đúng.

Con số không đổi. Người chịu phí thì khác.

Không phải lời khuyên đầu tư. Phép đo bên chịu phí được chạy tại Ethereum block **25.643.032**; số DualPool tại block **25.642.998**; lượt đọc lại số hook và bốn mức phí tại block **25.643.932**, **13h40 ngày 30/07/2026 (06:40:36Z)**.
