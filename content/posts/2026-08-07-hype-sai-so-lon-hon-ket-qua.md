---
title: Áp dụng nhất quán định nghĩa cung lưu thông của chính báo cáo, phát hành ròng HYPE quý II đổi từ +890.000 sang −412.960
token: HYPE
date: 2026-08-07
mau: 🟡
ghim: KHÔNG CÓ BLOCK — HyperCore đọc qua Info API, HyperEVM không phục vụ trạng thái lịch sử. Ảnh chụp wall-clock 07/08/2026. Ví 0x43e9abea1910387c4292bca4b94de81462f8a251 giữ 241.150.943,99 HYPE trong nonCirculatingUserBalances; circulatingSupply 299.024.976,59; totalSupply 999.049.594,42
mo_ta: Một báo cáo quý kết luận cung HYPE nở thêm 890.000 token trong quý II. Áp dụng nhất quán chính định nghĩa circulatingSupply mà báo cáo dùng thì cùng phép tính ra −412.960.
anh: card-hype-doi-dau-muc.png
kenh_x: https://x.com/blockpinned/status/2085611015794995577
doc_lai: Đại lượng trôi theo thời gian là lượng lưu thông và tỉ trọng stake của ví. Tổng của quý đã đóng giữ nguyên, với điều kiện dữ liệu lịch sử của API không bị sửa và cùng phương pháp trích xuất được dùng lại.
---

**Một báo cáo quý kết luận cung token HYPE tăng thêm 890.000 trong quý II. Áp dụng nhất quán chính định nghĩa `circulatingSupply` mà báo cáo dùng thì cùng phép tính đó ra −412.960 — và riêng phần bị cộng không nhất quán, 1.311.093, đã lớn hơn kết luận 1,47 lần.**

Nếu bạn lấy phát hành ròng của một quý làm đầu vào cho mô hình cung, thì với quý này đầu vào đó nhỏ hơn sai số của chính nó.

## Chỗ phép tính hỏng

Hyperliquid trả staking emissions cho người stake HYPE. Một phần chảy vào ví `0x43e9abea…`, thuộc nhóm địa chỉ mà Hyperliquid loại khỏi `circulatingSupply`. Token đã được phát hành, nhưng chừng nào còn nằm ở một địa chỉ thuộc danh sách loại-trừ thì chưa được tính vào lưu thông.

Chỗ dễ hỏng: ví này **có** chuyển token ra ngoài. Nên không thể chỉ loại lượng chảy vào — phải đo đủ hai chiều, và phải kiểm cả địa chỉ nhận.

Trong quý II, tổng staking emissions **2.419.166 HYPE**; báo cáo in **2,41 triệu**, lệch **0,38%**. Trong đó **1.311.093** chảy vào ví, bằng **54,20%**.

Chiều ngược lại, cùng quý: ví chuyển ra **1.288.966 HYPE** qua **58 lệnh**, tới **29 địa chỉ khác nhau**. Đối chiếu từng địa chỉ với danh sách loại-trừ tại thời điểm đo: **0/29** nằm trong danh sách đó. Theo phân loại hiện tại của API, lượng rời ví đã đi vào lưu thông và phải được cộng lại.

Về chiều đi vào: ngoài **1.311.093** được ghi nhận dưới dạng **thưởng staking tích luỹ** — bản ghi tích luỹ, không phải một lệnh chuyển tiền — không có lệnh chuyển token nào khác đi vào ví trong cùng quý.

Phép tính, giữ nguyên mọi con số khác của báo cáo:

· emissions tới những người stake khác: 2.419.166 − 1.311.093 = **1.108.073**
· cộng lượng rời ví: **+1.288.967**
· tổng thêm vào lưu thông: **2.397.040**
· trừ phần rút khỏi lưu thông, số của báo cáo: **−2.810.000**

⇒ **−412.960 HYPE**, tương đương **−0,5524%/năm** trên nền lưu thông **299.024.977** đo cùng lúc.

## Kết quả vẫn âm khi bỏ phần dữ liệu kém chắc nhất

Trong **2.810.000** rút khỏi lưu thông: phần mua lại của quỹ **2.770.208**, phần huỷ token **39.792**.

Phần huỷ là chỗ kém chắc nhất, và lý do nằm ở phép đo **của BlockPinned** chứ không phải của báo cáo: khi BlockPinned đo lượng huỷ, kết quả chênh tới **106%** tuỳ khoảng thời gian chọn để đo. Vì đúng lý do đó, BlockPinned đã tự rút một kết luận về lượng huỷ từng viết ra.

Bỏ hoàn toàn **39.792** đó ra, kết quả vẫn là **−373.168 HYPE**. Dấu âm không treo vào phần kém chắc nhất.

## Vì sao có thể nói ví này đã bị loại khỏi cung quý II

BlockPinned không có snapshot trực tiếp của danh sách loại-trừ tại từng ngày trong quý II. Nhưng có một phép kiểm từ chính số liệu báo cáo.

Hyperliquid tính `circulatingSupply` bằng tổng cung, trừ phần chưa phát hành, rồi trừ số dư các ví trong danh sách loại-trừ. Báo cáo dùng nền lưu thông khoảng **299 triệu**, trong khi riêng ví này giữ khoảng **241 triệu**. Giữ nguyên các thành phần còn lại, nền khoảng 299 triệu **chỉ phù hợp** với việc số dư ví đã bị loại; nếu không loại, nền phải vào khoảng **540 triệu**.

Nói đúng mức: đây là **suy luận từ phép trừ số dư**, không phải snapshot lịch sử trực tiếp. Nhưng nó cho thấy điểm không nhất quán trong cùng một phép tính — **số dư** của ví bị loại khỏi lưu thông, còn **emissions chảy vào chính ví đó** lại được cộng vào.

## Dòng 1,3 triệu HYPE không phải hiện tượng một lần

Endpoint `delegatorRewards` trả **587 bản ghi thưởng theo ngày liên tiếp, không thiếu ngày nào**, từ 29/12/2024 tới 07/08/2026. Cộng theo quý: quý I/2025 **1.303.294** · quý II/2025 **1.327.384** · quý III/2025 **1.336.732** · quý IV/2025 **1.351.753** · quý I/2026 **1.289.617** · quý II/2026 **1.311.093**. Sáu quý nằm trong khoảng **1.289.617–1.351.753**, chênh **4,82%**.

Phạm vi phải nói rõ: chuỗi này chỉ chứng minh **lượng thưởng chảy vào ví dao động trong khoảng hẹp**. BlockPinned chỉ có một báo cáo quý II/2026 để kiểm phép tính, nên nó **không** chứng minh các báo cáo trước cũng mắc cùng lỗi.

BlockPinned từng đặt giả thuyết rằng phần này tăng dần theo thời gian. Dữ liệu bác giả thuyết đó: quý I/2026 còn thấp hơn quý IV/2025. Lượng stake của ví chỉ tăng **1,26%** trong sáu quý; lượng chuyển ra bám sát lượng nhận vào.

## Đây không phải bất đồng về hướng

Ngay đoạn kế tiếp, báo cáo cũng cho rằng cung đang siết vì ETF và kho bạc doanh nghiệp hút khoảng **7 triệu** token. Bất đồng nằm ở **phép tính phát hành ròng**, không ở hướng.

Và vì lượng thưởng vào ví đã nằm quanh 1,3 triệu trong sáu quý, có một phép kiểm chuẩn bị trước được: nếu báo cáo quý III giữ nguyên cách tính và ví vẫn bị loại khỏi lưu thông, dòng cần kiểm đầu tiên sẽ vào khoảng **1,3 triệu**.

## Cách tự kiểm

Mọi lời gọi dưới đây là `POST https://api.hyperliquid.xyz/info` với `Content-Type: application/json`. Không cần khoá API.

· **Phân loại ví** — `{"type":"tokenDetails","tokenId":"<tokenId của HYPE>"}`. Trường `nonCirculatingUserBalances` là danh sách cặp [địa chỉ, số dư]; `circulatingSupply` và `totalSupply` cùng lượt. Lấy `tokenId` bằng `{"type":"spotMetaAndAssetCtxs"}`.
· **Thưởng vào ví** — `{"type":"delegatorRewards","user":"0x43e9abea1910387c4292bca4b94de81462f8a251"}`. Cộng `totalAmount` theo quý. Kiểm chuỗi có thiếu ngày không bằng ba số phải bằng nhau: số bản ghi, số ngày phân biệt, độ dài khoảng thời gian.
· **Khoản rời ví và địa chỉ nhận** — `{"type":"userNonFundingLedgerUpdates","user":"0x43e9abea…","startTime":…,"endTime":…}`, quét theo từng tháng để không chạm giới hạn số dòng trả về. Đối chiếu từng `destination` với danh sách loại-trừ ở trên.
· **Tổng staked** — `{"type":"validatorSummaries"}`, cộng trường `stake` rồi chia `1e8`.

🔴 **Không có block number, và đó là tính chất của nguồn chứ không phải thiếu sót của bài.** Endpoint RPC công khai mặc định của Hyperliquid cho HyperEVM — một endpoint, và là endpoint duy nhất được kiểm — không trả trạng thái lịch sử đáng tin cho các lời gọi đã thử: gọi `eth_call` cùng một block number hai lần cách 20 giây ra hai giá trị khác nhau; gọi ở block tương lai vẫn trả số thay vì báo lỗi; và tài liệu chính thức ghi *"not supported at this time on the default RPC implementation"*. Endpoint trả phí của bên thứ ba chưa kiểm. Vì vậy mọi số ở đây là ảnh chụp theo giờ đồng hồ, không phải trạng thái neo vào block.

Dữ liệu đầu vào đến từ API do chính Hyperliquid công bố — **một nguồn**, không phải hai nguồn độc lập. Phần số học thì tự kiểm được.

*Không phải lời khuyên đầu tư.*
