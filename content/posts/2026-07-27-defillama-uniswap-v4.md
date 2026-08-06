---
title: DefiLlama báo phí Uniswap v4 cao hơn 3,9 lần — và bản sửa mới chỉ chạy một chiều
token: UNI
date: 2026-07-27
mau: 🟢
ghim: Robinhood chain · block #10.808.643 → #11.671.782 (trọn ngày 16/07 UTC)
doc_lai: Cập nhật 28/07/2026 09:36 UTC — DefiLlama đã tính lại TOÀN BỘ khoảng 08→24/07. Phép đếm trực tiếp của tôi được xác nhận ở cả hai ngày ghi trước; nhận định 'cú tụt do đổi cách tính' bị chính điều bác bỏ của nó bác, và tôi rút
mo_ta: Ngày 16/07, DefiLlama báo phí Uniswap v4 trên Robinhood chain cao hơn 3,9 lần phép đếm trực tiếp trên chain. Họ đã merge bản sửa, rồi tự tính lại đúng trong khoảng tôi ghi trước.
anh: post01-card.png
kenh_x: https://x.com/blockpinned/status/2081674093368365398
---

Ngày 16/07, DefiLlama báo phí Uniswap v4 trên Robinhood chain: **$5,01M**. Tôi đếm từng swap trên chain cùng ngày: **$1,29M**. Lệch 3,9 lần.

Tôi mở issue báo họ ngày 18/07. Sáu ngày sau, DefiLlama merge bản sửa, dòng đầu ghi rõ: *"Fixes #8242"* — issue tôi đã mở.

*(Phí ở đây là phí swap người giao dịch trả cho pool — không phải phí gas, và cũng không phải phần phí giao thức mà governance Uniswap vừa bật hôm 27/07.)*

## Không phải một hệ số thổi phồng cố định

Ba ngày, ba kết quả khác nhau:

| Ngày | DefiLlama | Đếm trực tiếp | Ai đo | Tỷ lệ |
|---|---|---|---|---|
| 16/07 | $5.014.570 | $1.286.386 | tôi | **cao hơn 3,9×** |
| 20/07 | $1.355.193 | $977.586 | tôi | cao hơn 1,39× |
| 22/07 | — | — | **chính tác giả bản sửa** | **thấp hơn** 0,93× |

Có ngày số bị đội lên, có ngày bị kéo xuống. Không thể hiệu chỉnh chuỗi cũ bằng một hệ số chung. Nguyên văn trong bản sửa của họ: *"it's pure luck which direction wins"* — lệch lên hay lệch xuống là hên xui.

**Hệ quả với người đọc chart:** nếu bạn nhìn phí Uniswap v4 để đọc mức độ hoạt động, bạn có thể kết luận phí tăng hay phí sập chỉ vì cách quy đổi ra USD đã đổi — không phải vì người ta giao dịch nhiều hay ít đi.

## Vì sao sai

DefiLlama không có sẵn một con số "phí bằng USD" để đọc. Phí thu bằng token, nên với mỗi swap, adapter phải chọn một token trong cặp làm mốc quy sang USD.

Adapter v4 luôn chọn `currency0` — mà với một cặp ERC-20, `currency0` về cơ bản là **token có địa chỉ contract nhỏ hơn**, không liên quan gì tới token nào có giá đáng tin hơn. Trên Robinhood chain, một số meme token mới có địa chỉ thấp lọt đúng vào chỗ đó — thay vì WETH hoặc USDG, các core asset mà adapter có thể dùng làm mốc. Phí của những pool ấy bị quy USD theo giá meme token; cộng dồn cả ngày, tổng số lệch mạnh.

Adapter v2/v3 tránh được lỗi này vì chúng ưu tiên lấy bên core của cặp làm mốc; riêng adapter v4 chưa từng được xử lý như vậy, cho tới bản sửa 24/07.

## Vì sao chưa xong

Bản sửa chỉ chạy từ 24/07 trở đi, lịch sử trước đó chưa tính lại. Sáng 27/07 tôi kiểm tra lại chuỗi dữ liệu của họ: ngày 16/07 **vẫn trả đúng $5.014.570** — con số issue này mở ra vì nó.

**Cập nhật 28/07/2026 —** đoạn ngay trên là tình trạng lúc bài này đăng, và nó đã đổi. Sáng 28/07, ngày 16/07 trong chuỗi của DefiLlama xuống còn **$1.311.188**, rơi trong khoảng tôi ghi trước ngày 26/07. Nhưng đúng một ngày đó đổi thôi: 16 ngày còn lại trong khoảng chính họ nói sẽ tính lại (08→24/07) vẫn giữ nguyên số cũ, giống tới từng đơn vị. Trạng thái từng khẳng định của bài nằm ở [sổ claim](#so-claim) cuối trang — kể cả một chỗ tôi viết hỏng và đã thay.

Nên mọi chart phí v4 gồm cả trước lẫn sau mốc 24/07 đang **trộn hai thứ**: biến động thị trường thật, và một cú tụt do đổi cách tính. Đọc trọn cú tụt đó thành "phí sập" là đọc sai.

Tách thử hai phần đó ra — cả bảng dưới lấy từ **một lần đọc duy nhất** (27/07 06:32Z), hai ngày "sau" đều đã đóng sổ:

| | TB 17–23/07 (trước) | TB 25–26/07 (sau) | tụt |
|---|---|---|---|
| Uniswap v4 | $987.745/ngày | $501.016/ngày | **1,97×** |
| Uniswap v3 *(bản sửa không đụng tới)* | $1.459.704/ngày | $1.208.511/ngày | 1,21× |
| **v4 ÷ v3** | | | **1,63×** |

v3 tụt 1,21× trong cùng khoảng thời gian; tôi dùng nó như một proxy cho xu hướng hoạt động chung trên Robinhood chain — không phải "toàn thị trường". Sau khi trừ phần đó, chênh còn lại khoảng **1,63×**.

**Đây là ước tính ban đầu, không phải một phân rã nhân quả hoàn chỉnh.** Bốn chỗ nó có thể sai:

- toàn bộ là số của DefiLlama, không phải tôi đo trên chain
- mới có **2 ngày** dữ liệu sau bản sửa
- v3 không phải một phép so hoàn hảo: mix pool và mức phí khác v4, và số v3-Robinhood của họ đi qua Dune chứ không đọc log — nên nó so được về *xu hướng thị trường*, không so được về *đường dữ liệu*
- ngày 24/07 bị loại khỏi cả hai nhóm vì bản sửa merge vào giữa ngày

Và một giới hạn của cả bài: chuỗi dữ liệu công khai của họ chỉ trả về khoảng 27 ngày gần nhất. **Mọi câu trong bài này chỉ nói về khoảng từ 01/07 trở đi** — tôi không đọc được xa hơn, nên không nói gì về trước đó.

## Tự kiểm, không cần tin tôi

1. **Issue gốc**, kèm toàn bộ phép đo đã dán công khai trong thread: [github.com/DefiLlama/dimension-adapters/issues/8242](https://github.com/DefiLlama/dimension-adapters/issues/8242)
2. **Bản sửa:** PR #8376, commit `33e0503`, diff đúng một file `dexs/uniswap-v4.ts`
3. **Số gốc của chính DefiLlama** — lệnh dưới đây đã chạy, không phải viết cho đẹp:

```bash
curl -s 'https://api.llama.fi/overview/fees/robinhood-chain?dataType=dailyFees' | python3 -c "
import sys,json,datetime
def walk(o,out):
    for k,v in o.items():
        walk(v,out) if isinstance(v,dict) else out.setdefault(k,v)
for ts,o in json.load(sys.stdin)['totalDataChartBreakdown']:
    r={}; walk(o,r)
    if 'Uniswap V4' in r:
        print(datetime.datetime.fromtimestamp(ts,datetime.timezone.utc).strftime('%Y-%m-%d'), r['Uniswap V4'])
"
```

4. **Đếm tận gốc:** sự kiện `Swap` của PoolManager trên Robinhood chain, block 10.808.643 → 11.671.782 (trọn ngày 16/07 UTC). 931.772 swap, volume $226,6M.

## Một lỗi của chính tôi

Trong issue ban đầu, tôi gọi **sai tên** cơ chế bảo vệ v2/v3 trong codebase của họ — viết từ trí nhớ thay vì tra lại. Lỗi đó không đổi số đo hay nguyên nhân, và tôi đã [đính chính công khai trong thread ngày 26/07](https://github.com/DefiLlama/dimension-adapters/issues/8242#issuecomment-5082514404).

Không phải lời khuyên đầu tư.

## Phụ lục — cho người muốn đọc code

Cơ chế giữ adapter v2/v3 khỏi lỗi này là `addOneToken` trong `helpers/uniswap.ts`. Bản sửa v4: commit `33e0503`, +12/−5 dòng.

Phép đo 22/07 của chính tác giả bản sửa: block 15.977.411 → 16.839.577, 1.047.163 swap — hai bên đo bằng cùng một cách.

Một bẫy tôi tự dính khi dựng bài này: bản tính đầu ra tỷ lệ tụt **2,26×** — sai, vì tôi lấy trung bình trên một ngày **chưa kết thúc**. Đọc lại khi ngày đã đóng: 1,97×. **Số ở ô cuối một chuỗi theo ngày còn tự lớn lên sau khi bạn đọc nó.**
