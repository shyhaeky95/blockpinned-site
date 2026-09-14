---
title: 138 lượt bỏ phiếu Morpho: 72,5% có một địa chỉ giữ quá bán số phiếu đã bỏ
phu_de: Trong tập proposal đã đóng tới 01/07/2026, top-1 giữ hơn nửa số phiếu đã bỏ ở 100 lượt. Nhưng Snapshot không tự ràng buộc Safe 5/9.
reading_layout: centered
token: MORPHO
date: 2026-09-13
gio: "22:27"
mau: "🟡"
ghim: Snapshot Hub API · space morpho.eth · 138 proposal đã đóng từ 15/10/2022 tới 01/07/2026, đọc ngày 11/08/2026. Cấu trúc thực thi đọc tại Ethereum block 25.608.961 (25/07/2026).
mo_ta: Trong 138 lượt bỏ phiếu Morpho đã đo, 72,5% có một địa chỉ giữ quá bán số phiếu đã bỏ. Phiếu tập trung, nhưng vote Snapshot không tự ký được giao dịch.
anh: card-morpho-72-phan-tram-phieu-qua-ban.png
doc_lai: Tập dữ liệu dừng ở 01/07/2026, không phải toàn bộ proposal tới ngày đăng. Top-1 là một địa chỉ bỏ phiếu và có thể gộp quyền được uỷ quyền; bài không gán danh tính. Tỉ lệ turnout dùng mẫu số cung desk chưa neo block nên chỉ đọc như bậc độ lớn. Trạng thái Safe là ảnh chụp tại block 25.608.961.
---

**Một đề xuất được thông qua thường trông giống một quyết định của cộng đồng. Nhưng trước khi đọc kết quả, có một câu hỏi đơn giản hơn: ai giữ số phiếu đã bỏ?**

BlockPinned đọc từng phiếu của **138 proposal đã đóng** trong space `morpho.eth`, từ MIP1 ngày 15/10/2022 tới MIP132 ngày 01/07/2026. Kết quả: **100 lượt, tương đương 72,5%, có một địa chỉ giữ hơn 50% số phiếu đã bỏ.**

Đây không phải câu “một ví nắm quá bán nguồn cung MORPHO”. Mẫu số ở đây là **số phiếu thực sự xuất hiện trong từng proposal**. Và một địa chỉ Snapshot có thể đang mang voting power được nhiều người uỷ quyền.

## 100 lượt có top-1 quá bán

Nếu xếp người bỏ phiếu theo voting power trong từng proposal, địa chỉ đứng đầu giữ trung vị **59,9%** số phiếu đã bỏ. Mức thấp nhất là **20,1%**; cao nhất **96,7%**.

| Cách đọc 138 proposal | Kết quả |
|---|---:|
| top-1 giữ hơn 50% phiếu đã bỏ | **100/138 = 72,5%** |
| trung vị phần của top-1 | **59,9%** |
| khoảng thấp nhất → cao nhất | **20,1% → 96,7%** |
| 12 lượt đầu → 12 lượt mới nhất | **60,3% → 59,0%** |

Con số cuối đáng chú ý vì nó gần như đứng yên. Sau gần bốn năm, trung vị top-1 của 12 lượt mới nhất chỉ thấp hơn **1,3 điểm phần trăm** so với 12 lượt đầu. Tập trung voting power không cho thấy một xu hướng cải thiện rõ trong tập đã đo.

## Turnout thấp không phải một ca lẻ

Một đợt từng bị gọi là turnout thấp là MIP131: **4.341.024 voting power**, tương đương **0,663%** nếu chia cho mốc circulating 654,773 triệu MORPHO mà desk ghi nhận. Nhưng khi đặt cạnh toàn bộ 138 lượt, nó xếp **75/138** từ thấp lên — gần đúng giữa phân phối.

Trung vị của cả tập là **0,626%** theo cùng mẫu số. Nói cách khác, MIP131 không phải một ngoại lệ; nó khá gần nhịp thường của space này trong phép đo.

Phần turnout có một giới hạn lớn: nguồn cung lưu hành 654,773 triệu là số desk ghi nhận, không neo block và không phải lịch sử supply tại từng ngày proposal. Nếu dùng mẫu số “unlocked” 326,755 triệu hoặc nguồn cung chuẩn 1 tỷ, riêng MIP131 lần lượt thành **1,329%** hoặc **0,434%**. Ba phép chia đều đúng về số học; chúng trả lời bằng ba định nghĩa khác nhau.

Vì vậy, claim mạnh của bài không nằm ở một mẫu số cung đang tranh chấp. Nó nằm ở tỉ lệ **top-1 trên chính số phiếu đã bỏ** trong từng proposal — đại lượng đã tự chuẩn hoá.

## Không phải câu chuyện “signer thao túng mọi vote”

BlockPinned cũng đặt 23 khoá từng giữ vai signer của tám Safe Morpho cạnh lịch sử Snapshot. Có ít nhất một signer tham gia ở **43/138 proposal**. Trong nhóm 43 lượt đó, phần voting power của signer có trung vị chỉ **0,02%**.

Nhưng phần đuôi lại khác hẳn: **12 lượt** có một signer đứng đầu và một mình giữ quá bán; mức cao nhất là **92,26%** ở MIP53.

Hai con số cùng đúng. Signer phần lớn không bỏ phiếu với sức nặng đáng kể, nhưng đã có một nhóm nhỏ proposal mà một signer tự quyết được kết quả trên tầng Snapshot. Dữ liệu không ủng hộ câu kể đơn giản rằng signer luôn điều khiển mọi vote — cũng không cho phép bỏ qua 12 ngoại lệ rất lớn.

## Một lá phiếu không ký được giao dịch

Đây là chỗ dễ kể sai nhất.

Snapshot là tầng bỏ phiếu off-chain. Còn giao dịch được thực thi bởi Safe on-chain. Tại Ethereum block **25.608.961**, Safe quản trị của Morpho có **9 signer, cần 5 chữ ký**, không có module, không có guard và bản Safe v1.3.0 không có timelock.

Điều đó có nghĩa kết quả Snapshot **không tự biến thành giao dịch**, cũng không có cơ chế on-chain buộc 5/9 signer phải thi hành đúng kết quả vote. Một delegate giữ quá bán phiếu Snapshot vẫn không vì thế mà ký được một giao dịch.

Câu đúng phải giữ cả hai nửa:

> **Tầng bỏ phiếu tập trung, còn tầng thực thi không bị ràng buộc bằng code với tầng bỏ phiếu.**

Việc một proposal đã được thi hành đúng theo kết quả vote là bằng chứng về hành vi ở proposal đó. Nó không biến thành một bảo đảm kỹ thuật cho proposal kế tiếp.

## Điều này thay đổi cách đọc governance

Với holder, hai câu hỏi nên được tách riêng.

Câu thứ nhất là **tính chính danh**: turnout ra sao, voting power tập trung tới đâu, top-1 có thể quyết kết quả hay không?

Câu thứ hai là **quyền thực thi**: ai giữ signer, ngưỡng chữ ký bao nhiêu, có timelock, guard hoặc module nào ràng buộc giao dịch hay không?

Chỉ nhìn proposal “passed” sẽ bỏ qua câu thứ hai. Chỉ nhìn Safe 5/9 sẽ bỏ qua việc tiếng nói trên Snapshot đang tập trung tới mức nào. Bài này không kết luận một proposal cụ thể là tốt hay xấu; nó chỉ cho thấy hai tầng governance của Morpho phải được định giá như hai rủi ro khác nhau.

## Điều bài này chưa biết

BlockPinned không gán danh tính cho các voter nặng nhất. Một địa chỉ có thể đại diện cho một người, một tổ chức hoặc voting power do nhiều người uỷ quyền. Đồ thị delegation và lịch sử thay đổi strategy của space chưa được bóc, nên bài không chuyển “một địa chỉ” thành “một chủ sở hữu hưởng lợi”.

Tập 138 proposal dừng ở 01/07/2026. Nó không đại diện cho các proposal mới hơn ngày đó. Trạng thái Safe cũng chỉ đúng tại block đã ghim; signer và module có thể thay đổi sau mốc đo.

## Phần kiểm chứng — cách tự kiểm

**Tập proposal.** Gọi Snapshot Hub API cho space `morpho.eth`, trạng thái `closed`, phân trang 20 proposal. Phép đo nhận bảy trang; trang cuối ngắn hơn 20, tổng **138**. MIP131 phải xuất hiện với `scores_total` **4.341.023,7267** và quorum **500.000**.

**Voting power.** Với từng proposal, lấy mọi phiếu cùng trường `voter` và `vp`. Tổng `vp` phải khớp `scores_total` của API ở cả 138 lượt. Sắp xếp giảm dần, lấy top-1 chia tổng phiếu; kết quả phải cho **100/138** lượt trên 50%, trung vị **59,8676%**, thấp nhất **20,1499%**, cao nhất **96,7279%**.

**Nhịp theo thời gian.** Sắp proposal theo thời điểm, lấy trung vị top-1 của 12 lượt đầu và 12 lượt cuối trong tập cố định. Kết quả phải lần lượt là **60,3%** và **59,0%** sau khi làm tròn một chữ số.

**Signer.** Đối chiếu voter với tập 23 khoá signer đã đọc on-chain. Phải có signer xuất hiện ở **43/138** proposal; **12 lượt** có signer đứng top-1 và quá bán; mức cao nhất **92,26%**.

**Tầng thực thi.** Tại block 25.608.961, gọi `getOwners()`, `getThreshold()`, danh sách module và guard của Safe `0xcBa28b38103307Ec8dA98377ffF9816C164f9AFa`. Kết quả phải là **9 owner, threshold 5, module rỗng, guard rỗng**, phiên bản **1.3.0**.

**Điều bác bỏ.** Claim tập trung sai nếu chạy lại đúng 138 proposal mà số lượt top-1 quá bán khác 100 hoặc trung vị khác 59,8676% ngoài sai số làm tròn. Claim về quan hệ vote–execution sai nếu tại đúng block đã ghim tồn tại một module, guard, timelock hoặc đường on-chain khác buộc Safe thi hành kết quả Snapshot.

*Không phải lời khuyên đầu tư.*
