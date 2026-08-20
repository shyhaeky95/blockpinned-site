---
title: Horizon thiếu lợi suất — hay chưa được mở đủ chỗ để lớn?
tieu_de_ngan: "Horizon thiếu lợi suất — hay chưa được mở đủ chỗ để lớn?"
reading_layout: centered
token: AAVE
date: 2026-08-20
mau: 🟡
ghim: Mọi số on-chain đo tại Ethereum block 25.792.601 (2026-08-20T00:00:00Z), node lưu trữ. Chuỗi lãi vay và dư nợ dựng từ 61 mẫu theo ngày 21/06→20/08; chuỗi NAV dựng từ 31 mẫu ngày và kiểm chéo bằng hai cửa sổ 30 ngày độc lập. Giá lấy từ oracle của chính Aave tại cùng block, không dùng nguồn giá ngoài.
mo_ta: Một quỹ tín dụng xin vào Aave Horizon với lý do collateral hiện tại chưa đủ hấp dẫn. Đo lại: chênh lệch dương đã có — thứ đáng nhìn nằm ở hạn mức.
anh: card-2026-08-20-horizon-tran-collateral.png
kenh_x: https://x.com/blockpinned/status/2090399953688657926
doc_lai: Bài KHÔNG chứng minh hạn mức cấp vốn là nguyên nhân khiến dư nợ giảm — mắt xích collateral nào sinh bao nhiêu dư nợ, cách hạn mức bao xa, và bỏ hạn mức thì dư nợ tăng bao nhiêu vẫn chưa nối được. Cũng chưa có bằng chứng có người muốn gửi thêm nhưng bị hạn mức chặn: chưa thấy giao dịch gửi bị từ chối vì hạn mức, chưa thấy hạn mức nâng rồi được lấp ngay. Chưa pin block của lệnh đổi hạn mức nên không nói được cắt hạn mức và rút tiền cái nào trước. Chưa đọc eMode, nên tham số LTV nền có thể bị nhóm eMode ghi đè. Ba quỹ nhóm tích luỹ sạch có chia cổ tức hay không thì không đọc được từ chuỗi — nếu có, mức tăng NAV đo được chỉ là mức tối thiểu — con số thật chỉ có thể cao hơn.
---

Một quỹ tín dụng lợi suất cao đang xin vào Aave Horizon với một lập luận khá đơn giản:

**Lợi suất cao hơn → người ta có thêm lý do đem tài sản đi thế chấp để vay.**

Nhưng dữ liệu đang chạy đặt ra một câu hỏi khác.

Chi phí vay GHO: **3%/năm**.
Một số collateral hiện tại đã tích luỹ **3,17–3,73%**.

Vậy mà trong cùng cửa sổ đó, dư nợ Horizon vẫn giảm **25%**.

Và có một chi tiết lạ hơn:

• một tài sản đã nằm sát **100% hạn mức collateral được phép nhận** gần một tháng;
• một tài sản khác có hạn mức đúng **1 đơn vị**.

Vậy Horizon thực sự đang thiếu lợi suất —

**hay chưa có đủ chỗ để lớn?**

Dưới đây là số đo, và cả những chỗ số đo **chưa** cho phép kết luận.

*(Bối cảnh: ngày 18/08, Securitize nộp hồ sơ xin đưa HINC vào Horizon — tài sản đầu tiên đi qua cổng mới, sau khi Aave Labs bỏ mô hình tự quyết niêm yết từ 14/08. Lý do duy nhất hồ sơ đưa ra: "when collateral yields sit close to or below the stablecoin borrow rate, borrowing is a liquidity operation rather than a carry trade.")*

## ① Với hai đồng chở 97,6% dư nợ, chênh lệch đã dương

Người vay ở Horizon dùng gì, đo @ blk 25.792.601:

| | dư nợ | phần |
|---|---:|---:|
| RLUSD | $87.129.093 | **76,8%** |
| GHO | $23.529.736 | **20,7%** |
| USDC | $2.776.709 | 2,4% |

**RLUSD + GHO = 97,6%.** Nên hai đồng đó là chỗ đáng soi.

Lãi vay GHO: **3,0000%** — không phải ảnh chụp, đo 61 mẫu ngày từ blk 25.362.242 tới 25.792.601, **biên độ đúng 0 pp**. RLUSD trung bình cửa sổ: **2,5707%**.

**Mức tăng NAV quy năm** của bộ thế chấp — đọc bằng oracle của chính Aave, blk 25.577.369 → 25.792.601. Đây là *mức tăng NAV quan sát được*, không phải một con số lợi suất do quỹ công bố:

| | NAV tăng /năm | trên GHO 3,0000% | hình dạng |
|---|---:|---:|---|
| **USTB** | 3,7292% | **+0,73 pp** | 🟢 lãi tích luỹ |
| **JTRSY** | 3,5827% | **+0,58 pp** | 🟢 lãi tích luỹ |
| **USYC** | 3,1722% | **+0,17 pp** | 🟢 lãi tích luỹ |
| JAAA | 5,0551% | +2,06 pp | 🟡 mức tích luỹ tự trôi |
| USCC | 3,2346% | +0,23 pp | 🔴 có mark-to-market |
| ACRED | 5,6847% | +2,68 pp | 🔴 có mark-to-market |

**Sáu trên sáu vượt.** Với RLUSD còn rộng hơn.

Ba dòng 🟢 là ba dòng chở luận điểm, và chúng là nhóm **sạch nhất**: **0/30 ngày âm** (lãi tích luỹ không đi lùi), mẫu *22 ngày tăng / 8 ngày đứng* trùng khít số ngày làm việc, và **hai cửa sổ 30 ngày độc lập lệch ≤0,25 pp**.

Ba dòng còn lại thì **không**: `ACRED` có **3 ngày âm** và hai cửa sổ cho **2,27% → 5,68%** — lệch **3,41 pp**. Nên con số to nhất bảng chính là con số **không được gọi là lợi suất**; nó là mức tăng NAV của đúng cửa sổ này.

⇒ Trên mức tăng NAV on-chain quan sát được, **chênh lệch so với chi phí vay đã dương** — nên **thiếu chênh lệch dương không tự nó giải thích được** việc Horizon chưa tạo ra dư nợ bền.

*(Với USDC — 2,4% dư nợ, trung bình cửa sổ 5,1232% — chỉ ACRED dương. Nói cho đủ. Một tài sản thứ bảy, mGLOBAL, bị loại khỏi bảng: NAV của nó đổi **1 lần trong 30 mẫu ngày**, nên mọi con số quy năm từ hai đầu là artifact lưới mẫu.)*

## ② Nhưng dư nợ vẫn giảm

Trong đúng cửa sổ đó: **$152.210.256 → $113.435.537 = −25,47%** (blk 25.433.938 → 25.792.601).

Nên chuyện không phải "hồ sơ nói sai". Chuyện là **triệu chứng họ mô tả có thật, còn lời giải họ đưa ra không đủ.**

## ③ Số ví đi vay không giảm

Giao tập địa chỉ có dư nợ ở hai đầu cửa sổ:

| | đầu | cuối | **ở lại** | rời | mới |
|---|---:|---:|---:|---:|---:|
| Toàn market | **26** | **26** | **21 (81%)** | 5 | 5 |

**21 trên 26 ví ở lại cả cửa sổ.** Năm rời, năm vào, tổng giữ nguyên.

Dư nợ giảm một phần tư **không đi cùng** với việc số vị thế giảm.

🔴 **Nhưng đây là câu về SỐ ĐỊA CHỈ, không phải về TIỀN.** Tôi đo sự hiện diện của địa chỉ, chưa đo **phần giá trị** mà 5 ví rời đi mang theo — chúng có thể là những vị thế rất lớn. Nên câu đúng dừng ở: *số ví đi vay không giảm*. Muốn nói *"phần lớn tiền ở lại"* thì phải đo dư nợ của riêng 5 ví đó tại đầu kỳ, và tôi **chưa làm**.

## ④ Nhưng trước khi hỏi thêm lợi suất, có một thứ khác cần nhìn: chỗ để lớn

Đọc bitmap `configuration` @ blk 25.792.601:

| | đã gửi | hạn mức cấp vốn | **% hạn mức** |
|---|---:|---:|---:|
| **mGLOBAL** | **29.999.999** | **30.000.000** | **100,0%** |
| GHO | 59.930.592 | 60.000.000 | 99,9% |
| JAAA | 24.576.930 | 30.000.000 | 81,9% |
| USTB | 5.775.210 | 8.000.000 | 72,2% |

**mGLOBAL thiếu đúng một đơn vị là chạm hạn mức** — chạm 30.000.000 vào 25/07 rồi giữ nguyên **26 ngày liền**.

Đó là hình dạng của **một reserve đã dùng hết capacity mà quản trị cho phép**. *(Tôi không nói có cầu đang xếp hàng phía sau — chưa thấy giao dịch gửi bị chặn vì hạn mức, chưa thấy hạn mức nâng rồi được lấp ngay. Chỉ nói: chỗ trống đã hết.)*

Và trong cùng cửa sổ, hạn mức bị đổi trên **4/11** reserve:

| | 01/07 | 21/07 |
|---|---:|---:|
| USCC | 15.000.000 | **3.000.000** |
| USYC | 10.300.000 | **5.000.000** |
| JTRSY | 10.000.000 | **5.000.000** |
| mGLOBAL | 50.000.000 | **30.000.000** |

Riêng USCC đi từ $92,9M xuống $19,8M — **một mình chiếm 81%** cú rơi $90,3M phía tiền gửi. *(Chưa pin block lệnh đổi hạn mức, nên không nói cắt hạn mức **gây ra** rút tiền. Chỉ nói: cùng một khoảng.)*

## ⑤ Và tài sản có spread rộng nhất thì gần như bị khoá từ cấu hình

**ACRED** — +2,68 pp, cao nhất bảng — có **0 đơn vị** được gửi vào, và **0 log `Transfer` trong toàn bộ lịch sử aToken**.

Tôi suýt viết "yield cao nhất mà chẳng ai dùng".

Rồi đọc tham số:

> **`ACRED.supplyCap = 1`.** Một đơn vị. Khoảng $1.110.
> `active = True` · `frozen = False` · `paused = False` · LTV 66% / LT 76%.

Niêm yết đầy đủ. Không đóng băng. Và hạn mức cấp vốn đặt ở **một đơn vị** — không đổi ở cả 5 mốc đo.

**Hồ sơ đang đề xuất thêm lợi suất để tạo cầu, trong khi tài sản có spread rộng nhất của chính Horizon chỉ được phép nhận đúng một đơn vị.**

## ⑥ Venue này thật ra to cỡ nào

- **26 ví** — toàn bộ bên đi vay.
- **30 vị thế** trên cả 8 tài sản thế chấp.
- Trong **$59,93M GHO** "được gửi vào": **$59,84M** ở `HorizonGhoDirectMinter` và Collector — thanh khoản **do chính DAO cấp qua facilitator**, không phải bên thứ ba mang vào. GHO từ bên ngoài: **≈$91K**.
- Ở hai trên ba đồng vay, **ba ví nắm >99,9%** dư nợ.

## Kết

HINC vẫn có thể giúp Horizon lớn lên.

Nhưng dữ liệu hiện tại **không ủng hộ câu chuyện đơn giản rằng chỉ cần thêm lợi suất**. Chênh lệch dương đã tồn tại ở hai đồng chở 97,6% dư nợ. Còn ở một số tài sản thế chấp, **khả năng mở rộng đang bị giới hạn ngay từ cấu hình quản trị**.

Câu hỏi đáng hỏi trước khi bỏ phiếu không phải *"lợi suất đã đủ hấp dẫn chưa"*, mà là ***"thị trường này đã được phép lớn chưa"***.

## Điều gì làm bài này sai

- Nếu nối được mắt xích **collateral nào sinh bao nhiêu dư nợ → cách hạn mức bao xa → bỏ hạn mức thì dư nợ tăng bao nhiêu**, và kết quả cho thấy hạn mức **không** ràng buộc — phần ④ đổ. Tôi **chưa** nối được mắt xích đó.
- Nếu **eMode** ghi đè LTV nền — một phần cách đọc ④ phải sửa. Tôi **chưa đọc eMode**.
- Nếu pin được block lệnh đổi hạn mức và nó nằm **sau** lúc tiền rút — cắt hạn mức là hệ quả, không phải ràng buộc.
- Nếu lãi vay GHO rời mức 3,0000% — bảng ① phải đo lại.
- Nếu ba tài sản nhóm 🟢 **có phân phối cổ tức** trong cửa sổ — NAV rơi ngày chốt và số đo là **mức tối thiểu**. Không đọc được từ chain.

---

## Cách tự kiểm

Mọi số neo tại Ethereum block **25.792.601**. RPC công khai, không cần khoá.

```
B=0x1899059; R=https://eth.drpc.org
q(){ curl -s $R -H 'content-type: application/json' -H 'user-agent: Mozilla/5.0' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"eth_call\",\"params\":[{\"to\":\"$1\",\"data\":\"$2\"},\"$B\"]}"; }

q 0xAe05Cd22df81871bc7cC2a04BeCfb516bFe332C8 \
  0x35ea6a7500000000000000000000000040d16fc0246ad3160ccc09b8d0d3a2cd28ae6c2f
```

Đó là `getReserveData(GHO)` trên pool Horizon. `word4 ÷ 1e27` ra **3,0000%** — chi phí vay GHO. `word0` là bitmap cấu hình: bit 0–15 là LTV, bit 56 hoạt động, bit 57 đóng băng, bit 116–151 là hạn mức cấp vốn. Đổi tham số địa chỉ sang `0x17418038ecf73ba4026c4f428547bf099706f27b` là ACRED, đọc ra hạn mức **1**, LTV **6600**, hoạt động **1**, đóng băng **0**.

Số đã gửi vào từng tài sản, `aToken.totalSupply()`:

```
q 0xc293744ffbcf46696d589f5c415e71bc491519cd 0x18160ddd   # ACRED → 0
q 0x4e58a2e433a739726134c83d2f07b2562e8dfdb3 0x18160ddd   # USTB  → 5.775.210.165.081 (6 chữ số thập phân)
```

Lệnh thứ hai là **kiểm chống mù, và nó bắt buộc**: nếu nó không ra khác 0 thì số 0 của ACRED là câu về công cụ chứ không phải về thế giới. Hai kiểu hỏng trông y hệt số 0, gặp thật khi dựng bài: block viết sai thành block tương lai thì trả rỗng, và endpoint công cộng chạm giới hạn tần suất thì cũng trả rỗng — chạy lại là ra.

---

*Không phải lời khuyên đầu tư. Đây là phân tích dữ liệu công khai; người viết không nắm giữ vị thế trong các tài sản được nhắc tới tại thời điểm viết. Mọi số đo tại block nêu trong bài và thay đổi theo thời gian.*
