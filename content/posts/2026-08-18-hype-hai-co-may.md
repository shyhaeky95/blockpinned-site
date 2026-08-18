---
title: Hyperliquid — 51% volume không còn là crypto, nhưng chỉ tạo ~12% doanh thu về holder
tieu_de_ngan: "Hai Hyperliquid trong cùng một sàn: 51% volume, 12% doanh thu"
reading_layout: centered
token: HYPE
date: 2026-08-18
mau: 🔴
ghim: KHÔNG CÓ BLOCK — HyperCore đọc qua Info API, RPC công khai của Hyperliquid không phục vụ trạng thái lịch sử. Ảnh chụp theo giờ đồng hồ ngày 18/08/2026, quét 494 công cụ trên 11 perp dex, nến ngày từ 01/08/2025. Tháng lịch đủ 2026-07: tổng khối lượng perp 224.233.021.320 đô, phần không phải crypto 114.741.983.929 đô.
mo_ta: Quá nửa khối lượng perp của Hyperliquid trong tháng 7 không còn đến từ crypto, nhưng phần đó chỉ mang về khoảng một phần tám doanh thu cho người giữ token.
anh: card-hype-hai-co-may.png
doc_lai: Tỉ lệ thu về của phần không phải crypto suy từ cơ chế phí Hyperliquid tự công bố, không phải từ sổ thu tiền thực tế; ba cách đo độc lập cho dải 11 tới 27 phần trăm và bài lấy đầu thấp. Trạng thái chế độ giảm phí mới đọc được tại một thời điểm, chưa có chuỗi lịch sử, nên không kết luận tỉ lệ này đang tăng hay đang giảm. Danh sách công cụ là danh sách đang niêm yết tại thời điểm đo, nên mọi tổng theo lớp là mức thấp nhất tái dựng được, không phải tổng lịch sử tuyệt đối.
---

Trên Hyperliquid, hợp đồng perp tham chiếu giá SpaceX đã chạy gần **20 tỷ đô** khối lượng kể từ khi lên sàn tháng 5.

Nhưng SpaceX chỉ là một mảnh của chuyện lớn hơn.

**Trong tháng 7/2026, hơn một nửa volume perp của Hyperliquid không còn đến từ crypto.**

Câu hỏi quan trọng hơn là: **phần tăng trưởng mới đó có giá trị với HYPE giống phần kinh doanh crypto cũ không?** Câu trả lời ngắn: **không, và chênh lệch rất lớn.**

## Hyperliquid đã đổi hình

Tháng 7/2026, tổng volume perp đo được trên Hyperliquid là **224,23 tỷ đô**. Chia theo loại tài sản: crypto **48,83%** · cổ phiếu **29,29%** · hàng hóa **9,96%** · chỉ số **9,37%** · công ty chưa niêm yết **2,22%** · ngoại tệ **0,09%** · chưa xếp được lớp **0,24%**.

Cộng lại, phần không phải crypto chiếm **51,17%**. Một năm trước, tháng 8/2025, tỷ lệ này chỉ khoảng **0,1%**.

Cần nói rõ: đây không phải cổ phiếu hay quyền sở hữu tài sản thật. Đó là hợp đồng perp lấy giá của TSLA, vàng, S&P 500, SpaceX làm tham chiếu. Người giao dịch không sở hữu cổ phần Tesla hay SpaceX.

Sự mở rộng này cũng không đến từ một cú listing duy nhất. Vàng xuất hiện cuối tháng 12/2025. Dầu đầu tháng 1/2026. S&P 500 tháng 3. SpaceX tháng 5. Một số công cụ mới tiếp tục được đưa lên trong tháng 7. Đo theo tuần cũng không cho thấy một cú nhảy duy nhất tạo ra toàn bộ kết quả: nhóm công cụ lớn nhất duy trì khoảng **7,2–18,3 tỷ đô volume mỗi tuần** trong bốn tháng gần đây.

**Nếu vẫn đọc Hyperliquid như một sàn perp crypto đơn thuần, bạn đang bỏ qua khoảng một nửa hoạt động của nó.** Nhưng đó mới chỉ là nửa đầu câu chuyện.

## Một đô volume không còn bằng một đô volume

Hyperliquid có một chế độ gọi là **growth mode**, bật riêng cho từng công cụ. Khi bật, phần phí protocol giữ lại giảm còn khoảng một phần mười mức thông thường. Nói đơn giản: đây là cách hy sinh phần thu về trên mỗi giao dịch để market mới cạnh tranh hơn.

Ở thời điểm đo ngày 18/08, growth mode đang phủ khoảng **95,94% volume non-crypto**. Ở nhóm crypto của sàn chính: **0%**.

Theo phép tính dựa trên cơ chế phí hiện tại, **mỗi $1 volume non-crypto chỉ tạo khoảng 13,65% phần giá trị về holder so với $1 volume crypto trên sàn chính.** Chia nhỏ theo lớp thì cổ phiếu **11,70%**, chỉ số **11,23%**, công ty chưa niêm yết **10,46%**, hàng hóa **17,07%**. Hàng hóa trả cao nhất, đúng vì đó là lớp bật growth mode ít nhất (**92,15%** so với 98–99% ở các lớp còn lại) — cùng một sàn, lớp nào bật cờ ít hơn thì trả nhiều hơn.

Ghép với tỷ trọng volume tháng 7: **khoảng 51% volume của Hyperliquid chỉ tương ứng khoảng 11,7% doanh thu về holder.**

Có ba giới hạn cần đặt ngay cạnh con số 11,7%.

**Thứ nhất**, đây là phép tính từ cơ chế phí công bố × volume, không phải sổ thu tiền thực tế. Có ba cách ước lượng độc lập và chúng cho khoảng **11% đến 27%**; con số 11,7% lấy từ đầu thấp. Kể cả dùng cách cao nhất đo được từ báo cáo bên thứ ba, phần doanh thu của mảng mới cũng chỉ lên khoảng **15%**, vẫn kém rất xa tỷ trọng volume 51%.

**Thứ hai**, trạng thái growth mode mới chỉ được đọc tại một thời điểm. Chưa có chuỗi lịch sử, nên không thể nói "capture đang giảm". Bài này chỉ nói: ở thời điểm đo, cấu hình đang như vậy.

**Thứ ba**, growth mode là một công tắc, không phải đặc tính cố định. Nó đã từng được tắt thật trên vài công cụ. Nếu được tắt trên các market lớn, phần phí protocol có thể tăng lên ngay — phần doanh thu bị bỏ lại hôm nay không nhất thiết mất vĩnh viễn. Nhưng người giữ HYPE cũng không quyết định khi nào công tắc đó được tắt.

## Hai cỗ máy kinh tế trong cùng một sàn

Một bên là crypto: chưa tới một nửa volume tháng 7, nhưng giữ lại economics cao hơn nhiều trên mỗi đô giao dịch. Bên kia là cổ phiếu, hàng hóa, chỉ số và pre-IPO: đã lớn hơn về volume, tăng từ gần như bằng 0 lên hơn một nửa hoạt động chỉ trong khoảng một năm, nhưng hiện mang về ít hơn nhiều trên mỗi đô volume. Trên dashboard, chúng được cộng lại. Với HYPE, chúng không nên được đọc như nhau.

Vì vậy, bài này không kết luận gì về định giá. Nó là một câu khác:

**Tổng volume của Hyperliquid đang trở thành một mẫu số ngày càng kém để suy trực tiếp economics của HYPE.** Hai phần volume trông giống hệt nhau trên biểu đồ, nhưng không mang cùng lượng giá trị về token.

Hyperliquid cũng không giấu chuyện này. Danh sách market và trạng thái growth mode đều đọc được công khai. Điểm đáng chú ý không nằm ở việc dữ liệu bị che. Nó nằm ở chỗ **con số headline vẫn đúng, nhưng cách dùng con số đó để hiểu HYPE đã bắt đầu sai mẫu số.**

## Phần phương pháp — bản X không chứa đoạn này

Info API của Hyperliquid không có trường nào khai một công cụ thuộc lớp tài sản gì. Nghĩa là nếu chỉ dựa vào việc đọc tên ký hiệu rồi tự xếp lớp, thì toàn bộ phần đầu bài đứng trên trí nhớ của người viết về mã chứng khoán. Đó là một loại sai lầm không có cách nào tự phát hiện, vì kết quả vẫn trông hoàn toàn nhất quán.

Nên phép đo dùng thêm một đường thứ hai, không cần biết ký hiệu là gì: tỉ lệ khối lượng cuối tuần so với ngày thường. Một công cụ bám theo thị trường đóng cửa cuối tuần sẽ sụt hẳn vào thứ Bảy và Chủ nhật; một công cụ crypto thì không.

Đường một, xếp lớp theo ký hiệu, cho **51,17%**. Đường hai, đo hành vi cuối tuần và không dùng tên, cho **53,70%**. Hai đường không dùng chung giả định nào, và chúng trỏ cùng một chỗ.

Đường hai còn bắt được một lỗi thật của đường một. Ở lượt đo đầu, bảng tra ký hiệu để **21,4%** khối lượng ở nhóm chưa xếp được lớp, đủ để kết luận rơi vào vùng không phân định. Nhưng nhóm ấy có tỉ lệ cuối tuần **13,3%**, thấp hơn cả nhóm cổ phiếu đã nhận diện. Tức nó gần như chắc chắn là tài sản TradFi mà người viết chưa tra ra tên. Bổ sung bảng tra, không đụng ngưỡng phán quyết đã đặt trước, kéo nhóm chưa xếp được xuống **0,24%**.

Một phép kiểm cuối, và nó có thể đã nổ. Bộ phân loại được đem áp lên sàn crypto chính của Hyperliquid, nơi chắc chắn 100% là crypto. Nó dán nhãn TradFi cho **0,0919%**, đủ nhỏ để tin bộ phân loại không loạn. Nếu con số đó lớn, cả phần đầu bài phải bỏ.

## Điều gì sẽ bác bỏ bài này?

Nếu growth mode được tắt trên phần lớn các market non-crypto lớn, chênh lệch economics giữa hai nhóm sẽ co lại và tổng volume sẽ trở thành mẫu số có ý nghĩa hơn. Cái này kiểm được: mỗi công cụ có mốc thời gian đổi cờ gần nhất, đọc công khai. Và nếu một phép phân loại độc lập khác cho thấy phần non-crypto tháng 7 thấp hơn **40%**, thì luận điểm đầu tiên của bài này không còn đứng.

Một lưu ý về cách đọc mọi con số ở trên: chúng **không neo được vào block number**. RPC công khai của Hyperliquid không phục vụ state lịch sử, nên đây là ảnh chụp theo giờ đồng hồ chứ không phải theo block. Và các tỷ lệ theo lớp chỉ tính trên danh sách công cụ **còn niêm yết tại thời điểm đo** — công cụ đã bị gỡ không xuất hiện trong universe hiện tại, nên **51,17% là mức thấp nhất có thể tái dựng từ danh sách hôm nay.**

## Tự kiểm, không cần tin bài này

Hai lệnh dưới đây chạy được ngay, không cần key.

**Một — mảng mới là gì, và growth mode đang bật bao nhiêu.**

Gọi Info API của Hyperliquid, hỏi danh sách công cụ của perp dex tên `xyz`:

`{"type":"meta","dex":"xyz"}`

Đọc lúc 18/08: **114 công cụ**, trong đó **110 bật growth mode**, tức **96,5% tính theo đầu mục**. Mười tên đầu tiên trả về: XYZ100, TSLA, NVDA, GOLD, HOOD, INTC, PLTR, COIN, META, AAPL.

*(Lưu ý đơn vị: 96,5% này đếm theo số công cụ. Con số 95,94% trong bài đếm theo khối lượng, hai mẫu số khác nhau và tình cờ gần nhau.)*

**Hai — mảng mới đã lớn cỡ nào so với sàn chính.**

Gọi `metaAndAssetCtxs` hai lần, một lần không tham số (sàn chính) và một lần với `dex` là `xyz`, rồi cộng trường `dayNtlVlm` của từng công cụ.

Đọc lúc 18/08: sàn chính **2,84 tỷ đô/24h**, `xyz` **4,23 tỷ đô/24h**. Tức riêng `xyz` chiếm **59,8%** tổng hai bên.

Con số này **cao hơn** số 51,17% trong bài, và đó là chuyện bình thường: **59,8% là ảnh chụp 24 giờ**, còn 51,17% là **cả tháng 7 lịch đủ**. Một ngày không phải một tháng, đừng thay số này vào số kia.

Số 0 trong phép đo này có nghĩa vì bộ đếm không mù: cùng cách gọi ấy trả về khối lượng khác 0 cho cả hai bên.

*Không phải lời khuyên đầu tư. Số đo tại thời điểm ghi trong bài và có thể đã thay đổi.*
