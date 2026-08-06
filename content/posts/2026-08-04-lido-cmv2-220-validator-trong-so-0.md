---
title: 220 validator đã nạp, trọng số phí của module vẫn đúng 0,0000 ETH
token: LDO
date: 2026-08-04
mau: 🟡
ghim: Ethereum block #25.680.251 · hàng chờ deposit đọc tại consensus slot 14.917.257, 15h11 ngày 04/08/2026 (08:11Z)
mo_ta: Module staking mới của Lido có 220 validator đã nạp tiền thật, nhưng số dư đi vào công thức chia phần thưởng vẫn bằng 0 — và số 0 đó đúng theo cách trường dữ liệu được thiết kế.
anh: card-cmv2-220.png
kenh_x: https://x.com/blockpinned/status/2084586520129024148
---

**220 validator đã gửi tiền thật vào module staking mới của Lido. Số dư đi vào công thức phân bổ phần thưởng của module đó vẫn đúng 0,0000 ETH.**

Sáu ngày trước, BlockPinned ghi nhận module này có 43 node operator, **0 validator đã nạp** và số dư oracle báo về là 0 ETH. Một trong hai con số đã đổi.

Nếu bạn dùng riêng số dư oracle để hỏi "module mới đã được dùng chưa", số 0 kia sẽ đọc thành "chưa ai dùng". Chỗ sai không nằm ở số 0. Nó nằm ở việc dùng số dư oracle để kết luận module đã nhận deposit hay chưa — trong khi trường này loại tiền đang chờ kích hoạt.

## Số 0 này phù hợp với cách trường số dư được thiết kế

Trong công thức phân bổ phần thưởng giữa các staking module mà bài này kiểm, trọng số lấy từ **số dư do oracle báo về**, không lấy từ số validator. Contract không tự tính số dư ấy: oracle đọc dữ liệu ở tầng đồng thuận của Ethereum rồi đưa con số vào báo cáo on-chain. Và phần chú thích ngay tại trường dữ liệu đó trong source contract ghi rõ — tiền đang chờ kích hoạt bị loại khỏi số dư báo cáo.

Trong 10 lượt báo cáo gần nhất tính tới Ethereum block **25.680.251**, con số oracle thật sự đưa vào cho module mới đều là **0 gwei**. Bốn lượt trong số đó xảy ra **sau** khi số validator đã nạp của module đạt 220.

Nói cách khác: ETH của 220 validator đã được gửi, nhưng chưa đi vào số dư oracle. Vậy tại thời điểm đo, nó đang ở đâu?

## 220 validator đó đang nằm trong hàng chờ kích hoạt

Và quy mô của hàng chờ mới là chỗ đáng nhìn.

Tại consensus slot **14.917.257**, lúc 15h11 ngày 04/08 (08:11Z), hàng chờ gửi tiền của Ethereum có **39.020 lượt, chở 2.521.416 ETH**. Trong cùng ảnh chụp, Lido Core — bốn staking module, không tính stVaults — chiếm **52,13% số lượt** nhưng **25,82% lượng ETH**.

Hai con số cho cùng một chỗ đứng, chênh nhau gấp đôi. Lý do đo được: tại cùng slot đó, cả **20.343 lượt** mà phép lọc credential nhận diện là Lido Core đều mang đúng **32,0 ETH**, trong khi phần còn lại của mạng có lượt mang tới **1.920 ETH**.

Cả hai con số đều đúng. Đại lượng cần dùng thì phụ thuộc câu hỏi: số lượt, hay lượng ETH. Hàng chờ này được xử lý theo lượng ETH — nên để đo phần tiền đang đứng chờ của bốn module Lido Core, tỉ lệ là **25,82%**.

Hỏi về **toàn bộ Lido** thì con số cao hơn, và nó là mức tối thiểu: stVaults tự đặt credential riêng nên nằm ngoài phép lọc. Một stVault đã đo có 5 lượt / **5.090 ETH** trong hàng — cộng riêng nó đã thành **26,02%**, và chưa quét hết stVaults.

Phép lọc có nhìn sót lượt lớn không? Tại cùng slot đó, truy vấn trả **1.648** lượt lớn hơn 32 ETH trên toàn hàng chờ (thường gặp 1.920 · 1.888 · 1.024 · 1.800) và **0** lượt như vậy trong 20.343 lượt được nhận diện là Lido Core.

Hàng dài đến mức nào: cũng tại slot đó, lượt đứng đầu **đã chờ 50,23 ngày** và vẫn chưa tới lượt. 220 validator của module mới nằm rải trong dải vị trí **38.145–38.846** trên tổng 39.020 lượt.

## Và đây là cái bẫy thật sự của việc đếm validator

**Credential** — đoạn dữ liệu gắn với mỗi validator, quy định nơi rút tiền và loại validator — của module mới thuộc loại khác ba module cũ. Và chính loại đó quyết định **mức ETH tối đa** được tính cho một validator: loại cũ **32 ETH**, loại module mới dùng **2.048 ETH**.

Nghĩa là mức ETH tối đa của một validator loại mới bằng 64 validator loại cũ. Lấy số validator để suy ra lượng ETH mà không xét loại credential và mức nạp, quy mô ước tính có thể lệch tới ngần ấy lần.

Cụ thể, với ngưỡng 1% tổng số dư Lido Core — **87.030,64 ETH**: giả định validator loại mới đều được nạp đủ 2.048 ETH thì cần **43** cái, thay vì **2.720** validator loại 32 ETH.

Cùng một cột mốc, số validator cần thiết chênh khoảng **63,3 lần**. Khác biệt đến từ loại credential, từ mức nạp mà bạn giả định, và từ việc phải làm tròn lên số validator nguyên đủ để vượt ngưỡng.

## Tự kiểm lại

Số tầng thực thi ghim tại Ethereum block **25.680.251**, đọc lại được bằng RPC có hỗ trợ trạng thái lịch sử tại đúng block đó:

- số dư module mới **0,0000 ETH**
- validator đã nạp **220**, key sẵn sàng nạp **3.059**
- mức ETH tối đa của hai loại credential: **32** và **2.048**

Số hàng chờ đọc tại consensus slot **14.917.257** lúc 15h11 ngày 04/08; endpoint dùng ở đây chỉ trả trạng thái hiện tại nên không gọi lại được chính ảnh chụp đó.

Mốc BlockPinned ghi trước từ 29/07 không đổi: tới **18/09**, nếu số dư module mới vẫn dưới 1% tổng số dư Lido Core thì hạ mức ưu tiên theo dõi. Nó vẫn được kiểm bằng số dư module. Bài này không rút mốc đó và cũng không đoán trước kết quả. Một biến quan trọng là tốc độ hàng chờ xử lý lượng ETH đứng trước 220 validator này, trong một hàng mà lượt đứng đầu đã đợi 50,23 ngày tại ảnh chụp trên — nhưng không phải biến duy nhất: kết quả còn phụ thuộc lượng deposit mới, mức ETH thực nạp trên mỗi validator, và phân bổ giữa các module.

Bài này đo tiền **đang ở đâu**, không đo tiền **đến từ đâu**. Việc 220 validator này được tạo bằng tiền mới hay bằng tiền dịch sang từ ba module cũ là một câu hỏi khác, cần phép đo khác, và không câu nào trong bài trả lời nó.

*Không phải lời khuyên đầu tư. Số tầng thực thi đo tại Ethereum block 25.680.251; số hàng chờ đọc tại consensus slot 14.917.257, lúc 15h11 ngày 04/08/2026 (08:11Z), và sẽ đổi.*
