---
title: Whitepaper MiCA của QNT nói không thể tạo thêm token. Contract vẫn mint được 27,5 triệu
tieu_de_ngan: QNT — tài liệu nói không tạo thêm được, contract còn 27,5 triệu
phu_de: Gọi thử tại block hôm nay, đường phát hành của crowdsale QNT vẫn đi được. Cái chặn duy nhất là một chữ ký — và khoá đó đã 2.656 ngày không ký gì.
reading_layout: centered
token: QNT
date: 2026-09-15
gio: "22:15"
mau: "🟡"
ghim: Ethereum block 25.983.552 · 21h46 ngày 15/09/2026 giờ VN (14:46:47Z). Hạn mức phát hành đo tại block 25.800.559 (21/08/2026). Whitepaper MiCA do Bitstamp Europe soạn, công bố 15/06/2026, tải và ghim sha256 ngày 15/09/2026.
mo_ta: Tài liệu MiCA của QNT viết nguồn cung tối đa là 14.881.364 token. Contract crowdsale vẫn còn hạn mức phát hành 27.502.628,462 QNT, và lời gọi vẫn chạy được hôm nay.
anh: card-qnt-tran-mint-mot-chu-ky.png
doc_lai: eth_call kiểm logic contract tại một block; nó không nói gì về ý định của ai, và không kiểm gas, nonce hay số dư ETH của một giao dịch thật. Ai đang cầm khoá owner là câu hỏi chưa có câu trả lời công khai, nên quãng im lặng không phải một bảo đảm. Hạn mức 27.502.628,462 QNT đo tại block 25.800.559; lượt đọc 15/09 xác nhận nhánh presale vẫn chặn đúng chỗ đã tính, không đo lại toàn bộ state.
---

**Một tài liệu công bố theo MiCA cho QNT, đang sống trên web hôm nay, viết nguyên văn: *"The maximum supply of QNT is capped at 14,881,364 tokens, and no additional tokens can be created beyond this limit."* Contract crowdsale của QNT — verified công khai từ 2018, chưa bao giờ bị thay — còn hai đường phát hành, và phần chưa dùng của chúng cộng lại là 27.502.628,462 QNT — bằng 184,81% chính con số đó.**

Câu hỏi tự nhiên là: đường ấy còn chạy được không, hay chỉ là mã chết còn sót trong một contract cũ?

BlockPinned gọi thử nó bằng `eth_call` tại Ethereum block **25.983.552** — 21h46 ngày 15/09/2026 giờ VN (14:46:47Z). Lời gọi **thực thi được**. Cùng lời gọi đó phát từ một address khác thì **revert**. Nên thứ đang đứng giữa 27,5 triệu QNT và sổ cung không phải một trạng thái đã khoá. Nó là một chữ ký.

## 14.881.364 không phải một con số trong code

Contract token QNT khởi tạo với hằng số **45.467.000**. Đó là con số duy nhất ở tầng "tổng cung" mà code có, và nó không còn được dùng làm gì: `totalSupply()` trả về nó như một hằng số chết, không cộng trừ theo mint hay burn.

Cung thật dựng từ event: **608 log `Transfer` từ địa chỉ 0** trong năm 2018, tổng **24.431.259,0318 QNT**. Trong đó **9.550.880,5019 QNT** hiện nằm ở chính địa chỉ token contract — nơi không có đường nào đưa tiền ra.

| Đại lượng | Giá trị | Nguồn |
|---|---:|---|
| hằng số trong contract | 45.467.000 QNT | `totalSupply()` |
| cung phát hành dựng từ 608 log mint | 24.431.259,0318 QNT | event 2018 |
| nằm ở chính token contract | 9.550.880,5019 QNT | `balanceOf(token)` |
| hiệu của hai dòng trên | **14.880.378,53 QNT** | phép trừ |
| "max supply" thị trường và tài liệu MiCA dùng | **14.881.364 QNT** | aggregator + whitepaper |

Hai dòng cuối lệch **0,0066%**. Con số mà mọi mô hình cung của QNT đang dùng làm mẫu số là **kết quả một phép trừ trên trạng thái năm 2018** — nó không phải một giới hạn do code cưỡng chế.

## Hai đường phát hành vẫn còn dư hạn mức

Bên trong `Crowdsale` có hai lối đi tới `token.mint()`, và cả hai đều nằm sau `onlyOwner`. Hạn mức trong bảng dưới là lượng tối đa mà mỗi đường còn được phép phát hành — con số này do chính code kiểm, mỗi lần gọi một lần:

| Đường | Hạn mức còn lại | Điều kiện |
|---|---:|---|
| `recordPresalePurchase` → `transferTokens` | **6.466.887,494 QNT** | chỉ cần owner — không cần ETH, không cần bật cờ sale nào |
| `enableSale` → `buyTokens` → `transferTokens` | **21.035.740,968 QNT** | cần bật `inSale`, mà `enableSale()` cũng là `onlyOwner`; ETH nạp vào được `_forwardFunds` trả lại chính owner trong cùng giao dịch |
| **Tổng** | **27.502.628,462 QNT** | **= 184,81% của 14.881.364** |

Phần 6.466.887,494 QNT nằm trong **cả hai** hạn mức: lúc `endPresale()` chạy năm 2018, phần presale chưa bán được cộng sang hạn mức bán thường, nhưng hạn mức presale thì không bị trừ đi. Hai hạn mức được kiểm **độc lập** trong code, nên tổng ở trên là giới hạn kỹ thuật, không phải phép cộng trùng.

Chi tiết đáng chú ý: *"tắt sale ngày 25/06/2018"* không phải renounce. `inSale = false` là một biến, và hàm bật nó lại vẫn còn đó.

## Không chỉ trên giấy: gọi thử tại block hôm nay

Đọc source rồi kết luận "đường này chạy được" là một lập luận về **code**. Câu kế tiếp rẻ hơn nhiều người tưởng: gọi thử.

`eth_call` cho phép đặt trường `from` tuỳ ý. Nó thực thi đúng bytecode tại đúng block, **không cần khoá riêng, không broadcast, không đổi một byte state nào**. Tại block 25.983.552, phát từ address đang giữ `crowdsale.owner()`:

| Lời gọi | Kết quả |
|---|---|
| `recordPresalePurchase(0x…d00d, 1 QNT)` | thực thi được |
| `recordPresalePurchase(0x…d00d, 6.000.000 QNT)` | thực thi được |
| `transferTokens()` | thực thi được |
| `enableSale()` | thực thi được |
| `recordPresalePurchase(0x…d00d, 9.000.000 QNT)` — vượt hạn mức | **revert** |
| **cùng lời gọi đầu tiên, `from` = một address ngẫu nhiên** | **revert** |

Dòng cuối là trụ của cả phép đo, không phải các dòng "thực thi được" ở trên. Nếu một address lạ cũng gọi được thì `onlyOwner` không hề được kiểm, và mọi kết quả dương phía trên vô nghĩa. Dòng áp chót cũng phải nổ được: 6 triệu QNT đi qua còn 9 triệu bị chặn, tức hạn mức presale đang chặn **đúng chỗ** phép tính đã chỉ ra.

## Cái chặn duy nhất là một chữ ký, và nó đã im 2.656 ngày

`crowdsale.owner()` trả về một address có `eth_getCode` dài **0 byte** — một khoá thường, không phải multisig, không phải timelock, chưa renounce.

| Khoá giữ `owner()` | Đọc tại block 25.983.552 |
|---|---|
| `eth_getCode` | 0 byte |
| nonce | 817 |
| nonce cuối 2018 (block 6.988.615) | 777 |
| giao dịch **gửi** cuối cùng | block 7.918.253 · 08/06/2019 |
| giao dịch **gửi** sau mốc đó | 0 |
| giao dịch **nhận** sau mốc đó | 2 — 16/02/2024 và 11/12/2024 |
| số dư ETH | 0,3814 ETH |

Bốn mươi giao dịch cuối cùng của khoá này nằm trọn trong nửa đầu năm 2019, rồi dừng hẳn. Tính tới block đã ghim, nó **không ký gì trong 2.656 ngày, khoảng 7,27 năm**.

Khoảng im lặng đó không làm hạn mức phát hành nhỏ đi một wei nào — hạn mức là **state của contract**, không phải hoạt động của khoá. Cái nó đổi là câu hỏi. Không phải *"họ có định mint thêm không"*, mà ***"khoá đời 2018 ấy giờ ai cầm"***. Đó là câu BlockPinned không trả lời được, và cũng không tìm thấy nguồn công khai nào trả lời.

## Điều này đổi cách đọc gì

Mọi mô hình cung của QNT — kể cả bảng trong tài liệu MiCA — dùng 14.881.364 làm mẫu số và ngầm giả định con số ấy được code giữ. Phép đo trên nói giả định đó không có trong code.

Nếu dùng hết hạn mức còn lại, cung phát hành thành **51.933.887,49 QNT** — vượt cả hằng số 45.467.000 trong chính contract, vì `mint()` không kiểm hằng số đó. Nói cách khác, ngay cả con số lớn nhất mà contract từng khai cũng không phải một giới hạn.

## Điều bài này không nói

Không có dòng nào ở trên là bằng chứng ai đó **định** mint thêm. Phép đo trả lời đúng một câu: đường đi có mở không, tại block nào. Nó cũng không đo được ai đang giữ khoá. Quãng im lặng bảy năm **không** phải một bảo đảm, và cũng không phải dấu hiệu sắp có chuyện — nó là một câu chưa có lời đáp.

Tài liệu MiCA nói trên do **Bitstamp Europe soạn** với vai nhà cung cấp dịch vụ, không phải do Quant tự soạn. Câu trích thuộc về **tài liệu đó**, không phải một phát ngôn của công ty. BlockPinned cũng không đặt tên cho address giữ `owner()`: trong hồ sơ này nó là *"address giữ owner của crowdsale"*, không hơn.

Cuối cùng, `eth_call` kiểm logic contract. Nó không kiểm gas, nonce hay số dư ETH ở mức một giao dịch thật.

## Phần kiểm chứng — cách tự kiểm

Ba địa chỉ, tất cả verified công khai: token `0x4a220e6096b25eadb88358cb44068a3248254675` · crowdsale `0x398e41ac3d5972b4bac2320cd130c7a25ca446f7` · khoá giữ owner `0xf5e38bbedc78efea055e0c56035adb320e64c4bc`.

**Khoá và trạng thái.** Tại block 25.983.552: `owner()` của crowdsale phải trả về đúng address thứ ba ở trên; `eth_getCode` của nó phải là `0x`; `eth_getTransactionCount` phải là **817**. Đọc cùng hàm đó tại block 6.988.615 phải ra **777** — nếu nó cũng trả 817 thì phép đọc đang lấy `latest` chứ không lấy theo block, và mọi kết luận về im lặng phải bỏ.

**Im lặng.** Lấy danh sách giao dịch của khoá, lọc `from` bằng chính nó. Giao dịch gửi cuối cùng phải là `0x6fe94d15fbdb0d877881bc7cc840f7ca8e9e5774fb9c7ac6db65dccc9a656e77` tại block **7.918.253**, và số giao dịch gửi phải bằng đúng nonce **817** — hai con số này khớp thì danh sách không sót dòng nào. Một danh sách rỗng và một câu truy vấn hỏng trông giống hệt nhau, nên phải thấy lại đúng giao dịch cuối này rồi mới tin con số 0 ở trên.

**Đường mint.** `eth_call` tới crowdsale với `from` đặt bằng address giữ owner, tại block 25.983.552: `recordPresalePurchase(address,uint256)` với 1 QNT và với 6.000.000 QNT phải trả về bình thường; với 9.000.000 QNT phải revert; `transferTokens()` và `enableSale()` phải trả về bình thường. Đổi `from` thành một address bất kỳ khác thì lời gọi đầu tiên phải revert.

**Cung.** Tổng 608 log `Transfer` có `from` bằng địa chỉ 0 phải ra 24.431.259,0318 QNT; `balanceOf` của chính địa chỉ token phải ra 9.550.880,5019 QNT.

**Điều bác bỏ.** Kết luận của bài sai nếu, tại block đã ghim: `owner()` trả về một contract chứ không phải address 0 byte code, hoặc quyền đã được renounce; hoặc lời gọi `recordPresalePurchase` từ owner revert; hoặc lời gọi đó từ một address lạ **không** revert; hoặc nonce của khoá lớn hơn 817, tức nó đã ký thêm sau 08/06/2019. Bất kỳ điều nào trong số đó đúng thì câu tương ứng ở trên phải rút.

*Không phải lời khuyên đầu tư.*
