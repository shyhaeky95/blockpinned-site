---
title: Mỗi $100 phí swap trên Robinhood Chain, Uniswap ghi nhận $14,64
token: UNI
date: 2026-07-31
mau: 🔴
ghim: Robinhood Chain · block #22.006.019 → #22.867.791 (trọn ngày UTC 29/07/2026) · giá quy đổi lấy tại 23:59:59 UTC 29/07
mo_ta: Đo trọn một ngày UTC trên Robinhood Chain: mỗi $100 phí swap thì $85,36 ở lại với người cấp thanh khoản, $14,64 về giao thức. Và v4 lấy tỷ lệ thấp nhất trong ba phiên bản.
anh: card-uni-100usd.png
kenh_x: https://x.com/blockpinned/status/2083199069892272255
---

Uniswap đã bật thu phí trên Robinhood Chain. Câu hỏi ai cũng hỏi là giao thức lấy được bao nhiêu — nhưng chưa thấy nơi nào tách ra.

Đo trọn một ngày UTC, mỗi **$100** người dùng trả phí swap:

**$85,36** ở lại với người cấp thanh khoản.
**$14,64** Uniswap ghi nhận là phí giao thức.

## Phiên bản mới nhất lấy tỷ lệ thấp nhất

Trong $100 phí đó, v4 chiếm **$23,76** — gần một phần tư. Nhưng v4 chỉ nộp về **$1,85**, tức **7,81%**. Cùng lúc, v2 nộp **16,67%** và v3 nộp **16,78%**.

Nếu bạn đang là LP hoặc đang giữ UNI, khác biệt đó đổi hai thứ ngược nhau. Với LP thì v4 dễ chịu hơn — ở v2 và v3, phí giao thức **trừ vào phần LP**; ở v4 nó **cộng thêm** vào phí người swap trả, nên LP vẫn nhận đủ. Với người giữ UNI thì ngược lại: dòng tiền càng dồn sang v4, phần chảy về giao thức càng mỏng.

Lý do là cơ chế, không phải chính sách. Ở v2 và v3, phí giao thức là một **phân số của phí pool** — một phần sáu, hoặc một phần tư. Ở v4 nó không phải phân số, mà là một **mức tối đa 0,1%**. Khi đã chạm mức đó, pool thu phí càng cao thì phần giao thức càng chiếm tỷ trọng nhỏ. Với pool fee 1% và protocol fee 0,1%, giao thức nhận khoảng **9%** trên tổng 1,1% mà người swap trả — không phải 16,7%.

Tỷ lệ thấp không tự nó là xấu, và bài này không đo được chiều đó. Nếu v4 nộp theo tỷ lệ như v2 và v3 **mà nền phí giữ nguyên**, mỗi $100 sẽ có thêm khoảng **$2,11** về giao thức. Nhưng nền phí có giữ nguyên hay không thì chưa ai đo: một lát mỏng của cái bánh to hơn vẫn có thể là nhiều tiền hơn. Muốn trả lời phải đo thị phần v4 qua nhiều ngày — bài này chỉ có một ngày.

## Ba thứ phải đo để ra được $14,64

**Một — không phải pool nào cũng bật.** Tính theo giá trị phí, **92,9%** phát sinh ở pool đã bật. Còn **$7,15** trên mỗi $100 phát sinh ở pool chưa bật, giao thức nhận **$0**.

Trong đó có một nhóm đáng chỉ tên: **30 pool v4 sinh phí nhiều nhất** ngày hôm đó có **15 pool gắn hook, và cả 15 đều không bật** protocol fee. 15 pool còn lại trong nhóm không gắn hook.

**Hai — pool đã bật lấy tỷ lệ khác nhau.** Đọc thẳng trên chain, không lấy từ tài liệu: **328.376 pool v3 khai một phần sáu**, **5.564 pool khai một phần tư**.

**Ba — tỷ lệ của v4 phải tính từ từng giao dịch**, vì nó phụ thuộc mức phí của chính pool đó. Bình quân gia quyền theo phí của các pool v4 đã bật: **7,81%**.

Áp chung một tỷ lệ một phần sáu cho tất cả — cách làm ở bản nháp đầu — cho ra con số cao hơn **5,69%** so với phép cộng theo cấu hình từng pool.

## Còn burn thì sao

Trong **$14,64** giao thức ghi nhận, **$9,80** đã xuất hiện dưới dạng UNI đem burn trong cùng ngày.

Phần chênh **không nằm trong kho** — đã kiểm: dòng vào và dòng ra của contract giữ tiền khớp nhau tới từng xu trên phần định giá được, tồn ròng bằng **0**. Nó ở đâu thì chưa nói được, và bài này không đoán.

Điều đáng biết hơn con số đó là **cách burn xảy ra**: phí giao thức **không mua UNI**. Phí vào contract giữ tiền dưới dạng các token khác nhau, rồi **bất kỳ ai** cũng có thể nộp **2.000 UNI** để lấy ra tối đa 20 asset trong đó — và số UNI ấy bị burn. Người đi gom chỉ làm khi có lời. Burn của UNI không tự động.

## Tự kiểm lại

Ba số gốc, mọi tỷ lệ ở trên đều quy ra từ đây. Trong khoảng block **22.006.019 → 22.867.791** của Robinhood Chain, đúng một ngày UTC:

- người dùng trả tổng **$2.521.197** phí swap
- giao thức ghi nhận **$369.178**
- UNI đem burn **62.000 UNI**, tương đương **$247.122**

Tách theo phiên bản: v2 trả $198.383 → ghi nhận $33.064 · v3 trả $1.723.902 → ghi nhận $289.353 · v4 trả $598.913 → ghi nhận $46.762.

Các số đếm on-chain đọc lại lúc nào cũng ra như vậy; các số USD dùng giá cuối ngày UTC 29/07.

Bài này thay cho bài đăng ngày 29/07 đã được gỡ khỏi cả hai kênh cùng ngày, sau khi điều kiện tự bác bỏ in kèm nó xảy ra.

## Điều gì sẽ bác bỏ bài này

Nếu một phép dựng độc lập — đọc từng log Swap cùng cấu hình protocol fee của đúng pool tại đúng block — cho tỷ lệ v4 lệch quá 2 điểm phần trăm so với **7,81%**, thì câu "phiên bản mới nhất lấy tỷ lệ thấp nhất" phải sửa công khai.

Không phải lời khuyên đầu tư. Các số đếm on-chain tại khoảng block 22.006.019 → 22.867.791 là mốc cố định, không đổi khi có block mới. Các số USD phụ thuộc nguồn giá cuối ngày UTC 29/07 và sẽ khác nếu dùng giá tại từng lượt swap.
