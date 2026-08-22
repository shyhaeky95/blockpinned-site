# SKY kiếm tiền như thế nào — và token SKY nhận gì?

**Sky có thể tạo ra rất nhiều doanh thu. Nhưng nắm SKY không có nghĩa bạn sở hữu một phần doanh thu đó.**

Khoảng cách giữa hai câu này là thứ quan trọng nhất cần hiểu về SKY.

Muốn hiểu nó, đừng bắt đầu từ staking, buyback hay tokenomics. Hãy bắt đầu từ cỗ máy kinh tế phía dưới.

Bỏ hết tên riêng đi, Sky làm một việc khá quen thuộc:

> **Phát hành một stablecoin, dùng tài sản phía đối diện để kiếm lợi suất, rồi cố kiếm nhiều hơn chi phí phải trả để giữ stablecoin đó tồn tại.**

Đó là business.

Nhưng từ lúc business kiếm được tiền tới lúc một người giữ SKY nhận được lợi ích, dòng giá trị còn phải đi qua nhiều tầng khác.

### Bản đồ của cả bài

Nếu chỉ nhớ một hình, nhớ bốn tầng này:

> **① Business** — Sky kiếm được bao nhiêu.
> **② Chính sách vốn** — số đó được giữ lại hay đem phân bổ.
> **③ Governance** — phần dành cho token rộng bao nhiêu.
> **④ Kho SKY** — token thực sự được lấy từ đâu để trả.

Business chạy tốt ở tầng ① **không tự động** có nghĩa nhiều giá trị hơn sẽ chảy xuống tầng ④.

Phần còn lại của bài chỉ là phóng to bốn tầng đó.

**Một quy ước của bài, nói trước để đọc cho đúng.** Các số **mức dễ trôi** — quy mô bảng cân đối, doanh thu, số SKY trong kho, tốc độ hiện hành — có chủ ở **bảng ảnh chụp cuối bài**, kèm ngày và block. Thân bài chỉ giữ những con số cần để giải thích **một cơ chế** hoặc **một sự kiện lịch sử**, và luôn gắn mốc.

Số trong bảng cũ đi **không** làm phần giải thích cơ chế phía trên sai. Nhưng nếu **chính cơ chế** đổi ở mức material thì Primer cũng phải được cập nhật — bài này đã phải làm đúng việc đó một lần, và mục 4 kể lại.

---

## 1. Cỗ máy bắt đầu từ một nghĩa vụ $1

Với người dùng, USDS là một stablecoin được thiết kế để giữ giá quanh $1.

Với Sky, mỗi USDS tồn tại đồng nghĩa hệ thống có thêm một **nghĩa vụ**: phải duy trì đủ tài sản và thanh khoản để người dùng tiếp tục tin đồng tiền đó đáng $1.

Phía bên kia nghĩa vụ ấy là tài sản.

Người dùng có thể đưa stablecoin vào hệ thống. Người khác thế chấp ETH hoặc stETH để vay. Các cấu trúc tài sản thực đưa tín phiếu kho bạc và tín dụng vào. Những đơn vị như Spark, Grove hay Obex mang vốn của hệ thống đi triển khai.

Cơ chế kinh tế không thay đổi:

**Sky có một phía phải trả tiền, và một phía phải kiếm tiền.**

Nếu tài sản kiếm được nhiều hơn chi phí của phía nghĩa vụ, Sky có spread dương. Đó là nguồn economics của toàn bộ hệ thống.

Ở ảnh chụp cuối bài, quy mô stablecoin đã ở cỡ mười tỷ đô, đối diện là một bảng cân đối lớn hơn số đó.

### Nhưng "bảng cân đối" của Sky có nhiều tầng

Hai chi tiết phải biết trước khi đọc bất kỳ con số nào của Sky.

**Thứ nhất, con số supply gồm cả USDS và DAI** — di sản từ MakerDAO. Đem nó so thẳng với lượng USDS đọc trên chain sẽ tạo ra một khoảng lệch không hề tồn tại.

**Thứ hai, mở sổ kế toán lõi ra, bạn không phải lúc nào cũng nhìn thấy tài sản cuối cùng.** Khi Sky cấp vốn cho Spark hay Grove, thứ nằm trong sổ lõi là **một khoản phải thu đối với đơn vị đó** — một IOU — chứ không phải trái phiếu, stablecoin hay khoản vay mà đơn vị ấy đang nắm. Tài sản cơ sở nằm thêm một tầng bên ngoài.

Đo trực tiếp ngày 17/07/2026: **48,9% lượng backing nhìn từ sổ lõi nằm dưới dạng IOU của các Star.**

Điều đó **không** có nghĩa gần một nửa hệ thống không được bảo chứng. Nó có nghĩa:

> **Sổ lõi cho biết Sky đang có claim đối với ai. Muốn biết tài sản cuối cùng là gì, phải đi tiếp vào danh mục của từng đơn vị đó.**

Vì vậy một câu kiểu *"Sky được back 100%"* chưa nói được nhiều, nếu người viết không nói rõ họ đang đo ở tầng nào.

---

## 2. Sky kiếm tiền bằng spread — và phần lớn doanh thu bị tiêu trước khi thành lợi nhuận

Spark cho vay trên thị trường crypto. Grove triển khai vốn vào tín dụng và tài sản thực. PSM nắm stablecoin dự trữ. Các vault crypto thu lãi từ người vay dùng ETH và stETH làm thế chấp.

Tên gọi khác nhau, nhưng về kinh tế chúng làm cùng một việc: **biến bảng cân đối của Sky thành tài sản sinh lợi.**

Sky cũng phải trả tiền để huy động vốn. Khoản lớn nhất — bỏ xa mọi khoản khác — là **lợi tức trả cho người giữ stablecoin**, đặc biệt sUSDS. Đó là **chi phí vốn** của hệ thống. Cộng thêm chi phí tích hợp, vận hành, và tổn thất tín dụng khi một khoản vay không đòi được.

Hình dạng của một quý điển hình, và đây là tỉ lệ đáng nhớ hơn con số:

**Khoảng 63 xu trong mỗi đô doanh thu gộp đã được dùng hết trước khi Sky chạm tới Net Protocol Revenue.** Biên còn lại quanh **37%**.

Và đây là cái vạch quan trọng nhất trong bài:

> **Trên Net Protocol Revenue là business.** Sky kiếm tiền và chịu chi phí để tạo ra nó.

> **Dưới Net Protocol Revenue là phân bổ vốn.** Hệ thống quyết định làm gì với phần economics đã tạo ra.

Nhớ được cái vạch này thì gần như mọi con số tài chính của Sky vào đúng chỗ.

Lợi tức trả cho người giữ sUSDS nằm **trên vạch** — đó là chi phí để business vận hành. Buyback SKY và thưởng staking nằm **dưới vạch** — đó là cách economics được phân bổ **sau khi** business đã tạo ra Net Revenue. Chính hệ thống báo cáo của Sky phân biệt hai tầng này.

Không phải chuyện trình bày. **Trừ thưởng staking một lần trong chi phí rồi trừ tiếp khi tính phân bổ là đếm cùng một dòng tiền hai lần.**

---

## 3. Một kỳ kế toán có thể làm business trông tăng hoặc giảm mạnh

Sky có một đặc điểm khiến các con số theo tháng và theo quý rất dễ bị đọc sai.

Một phần lớn economics từ Spark, Grove, Obex **không được ghi nhận liên tục**. Nó đi qua **Monthly Settlement Cycle** — ngày chốt sổ giữa Sky và các cánh tay triển khai vốn. Business vẫn tạo ra economics trong tháng, nhưng khoản đó chỉ lên P&L khi kỳ settlement chạy.

Độ trễ không đều — sáu kỳ gần nhất chạy từ khoảng **4 tới 33 ngày**. Hệ quả: **có tháng hứng một kỳ settlement, có tháng hứng hai.** Một tháng trông mạnh gần gấp đôi tháng sau nó có thể chỉ là một tháng chứa hai lần chốt sổ. *(Chuỗi sáu kỳ gần nhất: lớp kiểm chứng.)*

Cùng cơ chế đó chạy ở cấp quý, và nó đẻ ra **ba con số cùng đúng cho cùng một quý**:

| cách so | kết quả |
|---|---:|
| với cùng kỳ năm trước | **+10,5%** |
| với quý liền trước | **−13,6%** |
| cùng cơ sở — sau khi bù nhịp chốt sổ | **+0,5%** |

Ba con số đó trả lời ba câu hỏi khác nhau. Muốn biết **xu hướng nền giữa hai quý liền nhau**, con số phù hợp là **+0,5%** — gần như đi ngang.

Nên nếu bạn đọc ở đâu đó rằng *"doanh thu Sky quý này giảm 13,6%"*, con số ấy không sai. Nó chỉ chưa trừ đi một cái lịch.

Với Sky luôn phải tách hai câu hỏi: **business đã tạo ra bao nhiêu economics?** và **kế toán đã ghi bao nhiêu vào kỳ này?** Monthly Settlement Cycle chỉ trả lời câu thứ hai. **Nó là một cơ chế chốt sổ, không phải một mảng kinh doanh.**

---

## 4. Business kiếm được tiền chưa có nghĩa SKY nhận được tiền

Đến đây Sky vẫn có thể được nhìn giống một tổ chức tài chính. Từ đây trực giác cổ phiếu bắt đầu hỏng.

**SKY không phải cổ phiếu của Sky.** Nếu Net Protocol Revenue tăng 50%, không có một quyền pháp lý hay một công thức cố định nào khiến người giữ SKY tự động nhận thêm 50%.

Sau Net Revenue còn một tầng phân bổ vốn, viết sẵn trong **Atlas** — bộ luật thành văn của giao thức:

```text
Net Revenue
 ├─ 20%  →  Security & Maintenance
 │           chia đôi: Core Council 10% + Fortification Foundation 10%
 └─ 80%  →  "Step 2 Capital"
```

Nhưng 80% đó cũng chưa phải tiền của người giữ token. Nó tiếp tục đi qua chính sách vốn — và chỗ này Atlas thiết kế **hai chế độ**.

### Hai chế độ, và cái ngòi giữa chúng

**Chế độ 1** chia Step 2 Capital làm hai nhánh: một nhánh dành cho người stake SKY, và **quỹ đệm chống sốc** của hệ thống. Các bậc sâu hơn của thác không chạy. Bản thân Atlas gọi cơ chế thưởng của chế độ này là **tạm thời** — nguyên văn *"short-term SKY staking rewards **pending the full implementation** of the Sky Treasury Management Function"*. Tức chế độ 1 được viết ra để một ngày nào đó nhường chỗ.

**Chế độ 2** giữ một phần vào quỹ đệm, phần còn lại đi qua **ba** nhánh: mua SKY trả cho staker · thưởng **USDS** cho staker · và một nhánh mà văn bản gọi là *"buyback and burn"*.

Ngòi chuyển giữa hai chế độ không phải một con số thị trường. Nó là **một trạng thái của chính cỗ máy**: khi lượng SKY cấp cho chương trình thưởng đi tới cạn.

**Và ngòi đó đã nổ.** Ngày 07/08/2026, Core Facilitator của Sky xác nhận trên forum quản trị rằng điều kiện *"đã đạt"*. Tham số lên chain ngày **17/08** — một giao dịch, và nó đổi cùng lúc năm thứ. Bảng cuối bài ghi đủ.

Nhớ hình dạng này, đừng nhớ ngày: **chế độ là thứ Atlas viết sẵn; chuyển chế độ là một sự kiện quản trị; và nó không cần business thay đổi gì.**

### Quỹ đệm — nơi phần lớn lợi nhuận thực sự ở lại

**Ở chế độ 1, quỹ đệm là nơi phần lớn economics sau vạch được giữ lại.** Tài liệu gọi nó bằng **hai cái tên cho cùng một đại lượng** — *"Aggregate Backstop Capital"* và *"Sky Reserves"*; nguồn tự đặt dấu bằng, nên gặp cả hai tên thì **đừng cộng lại**. Atlas đặt cho nó một mốc gọi là *Turbo-Fill Floor*.

Nói gọn: **business tạo lợi nhuận → phần lớn dùng để làm bảng cân đối khoẻ hơn**, giống một tổ chức tài chính đang tăng vốn dự phòng.

**Với một điều kiện phải nói ngay, nếu không con số đó bị đọc quá tốt.** Quỹ đệm **không** phải một đống tiền mặt chờ sẵn để hấp thụ lỗ. Bóc nó ra — phép bóc gần nhất chạy ngày 10/08 — thì phần lớn là **vốn đã cấp vào chính các Star**, nhãn của chính đối tượng là *illiquid*, cộng với phần đệm ở sổ lõi **đang âm**. Con số tổng dương **là vì** phần vốn illiquid được cộng ngược vào.

⇒ *"Quỹ đệm đang đầy dần"* và *"khả năng hấp thụ lỗ đang tăng"* là **hai câu khác nhau**; bài này chỉ đo được câu thứ nhất.

---

## 5. Staking SKY dùng hai cái thước khác nhau

Đây là chỗ dễ nhầm nhất, và nhầm ở đây kéo theo nhầm về cả mô hình.

Phần thưởng staking **có** liên hệ với kết quả kinh doanh của Sky. Nhưng token dùng để trả phần thưởng **không phải SKY mua bằng chính Net Revenue vừa tạo ra**.

Có ba bước, và ba bước đó không dùng chung một túi tiền:

| bước | ai làm | lấy từ đâu |
|---|---|---|
| **phân bổ** | thác Atlas | một phần Step 2 Capital được dành cho nhánh staking |
| **định cỡ** | công thức | kết quả kinh doanh quyết định phần thưởng lớn cỡ nào |
| **cấp nguồn** | kho giao thức | **SKY thật sự trả ra lấy từ kho**, không phải từ economics vừa kiếm |

> **Net Revenue quyết định phần thưởng nên lớn cỡ nào. Kho quyết định token thực tế lấy từ đâu.**

**Và giữa hai bước đó còn một biến mà rất ít người biết: một con số phải được CHỌN.** Quy mô tính bằng đô, nhưng thứ trả ra là token — nên phải chia cho một mức giá SKY. **Không có oracle, không có công thức giá.** Atlas ghi thẳng mức đó do Core Facilitator xác định, tham vấn cố vấn rủi ro, rồi đưa lên chain bằng một cuộc bỏ phiếu.

Nghĩa là **APY staking bạn nhìn thấy phụ thuộc một phần vào một phán đoán của người**, không chỉ vào kết quả kinh doanh.

Và điều này không phải lý thuyết. Dòng vest cấp SKY cho chương trình thưởng là **một dòng cụ thể, có số thứ tự, thay được bằng một cuộc bỏ phiếu**. Ngày 17/08, đúng chuyện đó đã xảy ra: dòng cũ bị đóng, dòng mới mở với tổng **nhỏ hơn gần ba lần**.

Business không cần thay đổi gì. Tốc độ token rời kho vẫn giảm xuống còn khoảng một phần ba, chỉ bằng một quyết định.

---

## 6. SKY chạm vào economics bằng những đường nào?

Đây là lúc token bước vào câu chuyện. Tách rõ ba chủ thể:

| | |
|---|---|
| **Sky Protocol** | economics từ business |
| **người chỉ giữ SKY** | **không** có khoản chi trả tự động nào từ Net Protocol Revenue |
| **người stake SKY** | tham gia các chương trình phân phối riêng |

Câu trả lời gọn nhất là một bảng — từng đường một, kèm trạng thái **tại lần đọc gần nhất, 20/08**:

| đường về tay ai đó | trạng thái tại lần đo |
|---|---|
| **mua SKY trên thị trường mở** | đang chạy |
| **thưởng staking bằng SKY** | đang chạy — token lấy từ **kho**, không lấy từ doanh thu vừa kiếm |
| **thưởng staking bằng USDS** | bắt đầu chảy từ **17/08** |
| **nhánh gọi là "buyback and burn"** | điều khoản đã có hiệu lực từ 17/08 — nhưng tổng cung **chưa giảm một wei** |
| **người chỉ giữ SKY, không stake** | không có đường trực tiếp; chỉ hưởng gián tiếp qua lực mua của buyback |

Điểm quan trọng: **đừng đếm số cơ chế tồn tại — hãy nhìn cơ chế nào thực sự đang chảy.** Đếm số dòng trong cột trái là đếm **thiết kế**.

Và cũng đừng gọi cả ba đường đang chảy là *"chia lợi nhuận"*. Chúng có ba nguồn khác nhau: buyback dùng USDS mua SKY trên sàn · thưởng staking bằng SKY lấy token có sẵn trong kho · thưởng USDS thì được **đúc lúc trả**.

---

## 7. Buyback của Sky là một cái cổng, không phải một đường ống

Đây là đường trực tiếp nhất chạm tới **cả** người stake lẫn người chỉ giữ SKY.

Nhưng buyback không hoạt động theo kiểu `Sky kiếm thêm $1 → tự động dùng một phần cố định mua SKY`.

Governance đặt tham số cho cỗ máy. Khi điều kiện kế toán cho phép **và** có người kích hoạt, hệ thống dùng USDS mua SKY trên thị trường mở.

**Được phép mua** và **đã có một khoản tiền được phân bổ để mua** không phải cùng một câu. Toàn bộ khác biệt giữa hiểu đúng và hiểu sai mô hình này nằm ở chỗ đó.

Tháng 3/2026, một quyết định quản trị đổi đồng thời **lượng mỗi lượt** (10.000 → 6.000 USDS) và **khoảng cách tối thiểu giữa hai lượt** (2.880 → 13.787 giây) — cùng một spell. Chỉ đổi tham số, tốc độ buyback khác hẳn.

Đó là lý do **doanh thu tăng không đủ để suy ra lực mua SKY tăng**. Business có thể kiếm thêm rất nhiều mà lực mua dành cho SKY không đổi, nếu cái cổng không mở rộng.

### Một chỗ rất dễ đọc quá tay

Cỗ máy này tạo USDS để đi mua, nên rất dễ đọc thành *"Sky in tiền để bơm token của chính mình"*. **Đừng đọc như vậy.**

Nó chạy bên trong hệ thống kế toán của Sky: khi hạn mức được dùng để tạo USDS cho buyback, hệ thống **đồng thời ghi nhận một khoản nghĩa vụ tương ứng** — tiền và nợ sinh ra cùng một lúc, trong một hạn mức đã được quản trị **cấp phép trước**.

Đây là **chi tiêu trong một hạn mức đã được cấp phép**, không phải một cục tiền xuất hiện mà không có vế đối ứng. Cùng tính chất đó áp cho nhánh thưởng USDS đúc-lúc-trả ở mục trên.

---

## 8. Buyback này không phải burn

Cỗ máy buyback mua SKY ngoài thị trường rồi đưa token về **kho giao thức**. Không có bước huỷ token — và không phải kiểu *"chưa đốt, sau sẽ đốt"*: trong thiết kế của nó, đường đốt không tồn tại.

Điều đó **không** làm buyback vô nghĩa: lệnh mua vẫn là **cầu thật trên thị trường**, và nó chạm tới **mọi** người đang giữ SKY. Chỉ chặng kho → staker mới là chuyện riêng của người stake.

Nhưng economics khác hẳn một buyback-and-burn: token đã mua **vẫn tồn tại** và có thể được dùng lại.

Vì vậy phải tách hai khái niệm hay bị gọi lẫn:

- **token inflation** — `totalSupply` tăng;
- **float expansion** — token đã tồn tại trong kho quay trở lại lưu thông.

Nếu 100 SKY nằm trong kho rồi được trả cho staker: `totalSupply` vẫn là 100, không token nào được mint, nhưng lượng token cạnh tranh ngoài thị trường tăng lên.

Và phải nói chính xác cái nào đổi: **float expansion không làm tỷ lệ sở hữu của bạn trên `totalSupply` thay đổi** — không mint thì mẫu số đứng yên. Thứ nó làm là tăng áp lực cung. Hai chuyện khác nhau, và gọi nhầm tên là chỗ dễ bị bắt nhất.

---

## 9. Hai dòng kéo ngược nhau, và phải nhìn cùng lúc

Kho SKY có hai dòng chảy ngược chiều:

> buyback hút SKY từ thị trường **vào** kho, đều đặn từng lượt nhỏ;
> staking đưa SKY từ kho **trở lại** lưu thông, theo từng cục lớn.

Chỉ nhìn buyback sẽ thấy cung đang bị hút vào. Chỉ nhìn phân phối staking lại thấy token đang bị đẩy ra. **Bức tranh đúng là net của cả hai dòng.**

Và cái kho **không chảy đều**. Tiền ra thành **từng cục, gần một tuần một cục**; giữa hai cục, số dư chỉ **đi lên**, vì buyback vẫn mua vào. Nghĩa là số dư **nhảy bậc chứ không trượt dốc**, và một lần đọc rơi ngay **trước** một cục sẽ cao hơn hẳn một lần đọc rơi ngay sau. *(Chu kỳ đo được chính xác tới giây, và hai hằng số dựng ra nó: lớp kiểm chứng.)*

⇒ Một con số *"kho còn bao nhiêu"* chỉ có nghĩa khi bạn biết mình đang đứng ở đâu trong tuần. Muốn so thì so **cùng pha**, hoặc đọc mức rút trung bình một tuần trọn.

Trong cửa sổ đo ghi ở bảng cuối bài, **dòng ra lớn hơn dòng vào**.

---

## 10. Governance đổi được đường value capture mà không đổi business

SKY tựa lên ít nhất **ba nhóm giả định**, và chúng **hỏng được riêng từng cái**.

**Business.** Tài sản phải tiếp tục kiếm nhiều hơn chi phí huy động stablecoin. Nếu lợi suất tài sản giảm trong khi Sky vẫn phải trả cao để giữ USDS hấp dẫn, spread co lại — **không cần hack, depeg hay bất kỳ sự kiện kịch tính nào**. Đây là rủi ro rất giống ngân hàng.

**Bảng cân đối.** Gần một nửa backing nhìn từ sổ lõi là claim lên các Star; tài sản cuối cùng nằm thêm một tầng bên ngoài. Nếu người vay hoặc đối tác gây lỗ, khoản lỗ đánh thẳng vào vốn của hệ thống. Hệ thống càng lớn thì chất lượng đối tác ở tầng đó càng material.

**Governance của value capture.** Đây là giả định dễ bị bỏ qua nhất. Business có thể tốt hơn, bảng cân đối có thể an toàn, **mà phần economics chạm tới token vẫn giảm** — vì cái cổng giữa hai tầng là một tập tham số do governance kiểm soát.

Ngày 17/08/2026 là ví dụ rõ nhất: **một giao dịch** đổi cùng lúc chế độ phân bổ, tỉ lệ chia, nhịp buyback, cỡ dòng vest và cỡ cục rút kho. Cùng một business. Cùng một cái kho. Bảng cuối bài ghi đủ năm dòng.

Và có một chi tiết làm giả định ba cụ thể hơn hẳn: **từ 17/08, ba cái núm quan trọng nhất của cỗ máy buyback — lượng mỗi lượt, khoảng cách giữa hai lượt, tỉ lệ chia — không còn đi qua cuộc bỏ phiếu nữa.** Chúng chuyển sang một hợp đồng mà một ví đa chữ ký vận hành gọi thẳng: không spell, không 48 giờ chờ. Mã chỉ chặn tỉ lệ mua SKY không vượt 100%; **nó không có sàn**. Tới lần đọc gần nhất quyền đó **chưa được bấm lần nào** — nhưng nó tồn tại.

⇒ **Cùng một business, cùng một bảng cân đối, mà phần chạm tới token vẫn đổi được.** Đó là hình dạng của value capture ở SKY.

---

## 11. Còn *"buyback and burn"* thì sao?

Atlas có một nhánh mang đúng cụm từ đó, và cái tên gây hiểu sai — chính nguồn nói ra điều ấy.

Bản mô tả cơ chế viết thẳng: **không có một burn function nào được gọi trong quá trình đó**; phần này được thực hiện bằng **non-issuance** — tức không phát token ra khỏi kho, chứ không phải huỷ token đã tồn tại.

Tới lần đo gần nhất, `totalSupply` **không giảm**.

Một người bảo trì kho mã của Atlas thì nói phần đó *sẽ được đốt ở một cuộc bỏ phiếu sau*. **Hai lời giải thích chính chủ mô tả cùng một khoản theo hai cách khác nhau.** Bài này không chọn thay bạn.

Điều đo được chỉ là:

> **tới lần kiểm tra, số SKY mua về chưa làm `totalSupply` giảm.**

Nếu trạng thái đó đổi, đây là một trong những câu đầu tiên của bài phải sửa. Ai đọc *"buyback and burn"* thành *"nguồn cung sẽ bắt đầu co lại"* đang đọc thêm một thứ không có trong cơ chế.

---

## 12. Kể lại SKY trong 30 giây

Sky phát hành stablecoin. Phía đối diện là một bảng cân đối sinh lợi. Tài sản kiếm nhiều hơn chi phí giữ stablecoin thì Sky tạo ra Net Revenue.

Nhưng Net Revenue **không tự động thuộc về người giữ SKY**.

Sau business còn một tầng phân bổ vốn. Phần lớn economics được giữ lại để củng cố bảng cân đối; một phần đi vào buyback và các chương trình staking. Phần đó rộng hay hẹp phụ thuộc vào **governance và những tham số đổi được**.

Và token dùng để trả thưởng staking lấy từ **một cái kho hữu hạn**, không phải trực tiếp từ doanh thu vừa kiếm.

> **Business quyết định Sky có bao nhiêu economics.**
> **Chính sách vốn quyết định giữ lại bao nhiêu.**
> **Governance quyết định phần dành cho token rộng bao nhiêu.**
> **Kho quyết định SKY thực tế được lấy ra từ đâu.**

Đó là bốn tầng của cỗ máy. Và đó là lý do của câu cuối cùng:

> **Business của Sky và value capture của SKY là hai câu hỏi khác nhau.**

Khoảng cách giữa hai thứ đó chính là phần phải đo.

---

## Ảnh chụp để kiểm lại

> Cơ chế ở trên đổi chậm. **Những con số dưới đây đổi được bằng một giao dịch.**

> Bài không cố làm bảng này evergreen, và không được viết lại khi bảng cũ đi. Nó được viết cho một thời điểm, và thời điểm đó ghi ngay đây. Muốn biết hôm nay khác gì, chạy lại mấy lệnh ở cuối bài — chúng trả về con số của **lúc bạn bấm**.

**Tài chính — quý II/2026** *(báo cáo của Sky, số tới 30/06/2026)*

| | |
|---|---:|
| Stablecoin lưu hành *(USDS + DAI)* | ~$10,04B |
| Protocol Collateral | $12,32B |
| Gross Protocol Revenue | **$107,35M** |
| ba nhóm segment: Primes | $58,15M |
| — Stablecoins & PSM | $34,60M |
| — Crypto Vaults | $13,48M |
| Chi phí *(chủ yếu lợi tức trả sUSDS)* | ~$67,26M |
| **Net Protocol Revenue** | **$40,09M** |
| biên Net Revenue | **37,3%** |
| Net Protocol Surplus | $33,29M |
| Sky Reserves cuối quý | ~$82,40M / Turbo-Fill Floor $150M |
| — chuyển vào quỹ đệm trong quý | $29,87M |

*Ba dòng segment cộng lại ra **$106,23M**, hụt **$1,12M** so với Gross Protocol Revenue. Báo cáo không tách phần chênh đó ra, và bài này **không suy** nó là gì — ghi ra để bạn cộng thấy lệch thì biết lệch ở đâu.*

**Chi phí — 2026 tính tới báo cáo** *(khác kỳ với bảng trên: luỹ kế năm, không phải quý)*

| | |
|---|---:|
| Chi phí trực tiếp *(chủ yếu lợi tức trả sUSDS)* | **$118,96M** |
| Chi phí tích hợp | $16,88M |
| Vận hành *(trên vạch)* | $2,63M |
| An ninh & bảo trì *(dưới vạch)* | $21,49M |

*`Net Protocol Surplus` **không** phải `Net Protocol Revenue` trừ đi một khoản duy nhất — đó là một chỉ tiêu khác Sky báo cáo sau các khoản dưới vạch. Bài này không dựng câu nào lên hiệu của hai số đó.*

**On-chain — block 25.700.475 · 07/08/2026**

| | |
|---|---:|
| Tổng cung SKY | 23.462.665.147 |
| đang stake | 17.326.759.910 |
| trong kho giao thức | **70.452.586** |
| lượng bán được ngay | 3,91B SKY = **16,66%** tổng cung |
| tỉ lệ chia: mua SKY / thưởng USDS | **100% / 0%** |
| khoảng cách tối thiểu giữa hai lượt | 13.787 giây |
| khoảng cách **thực tế** trong cửa sổ đo | ~13.836 giây |
| buyback 30,11 ngày | $1,128M / 188 lượt |
| buyback thực thi | **~$37.468/ngày** *(mức tối đa theo tham số: ~$37.601)* |
| buyback / khối lượng tự nhiên trên Uniswap V2 | **9,48%** — cận trên cho câu hỏi toàn thị trường |
| chế độ phân bổ | **chế độ 1** |
| kho theo thời gian | 147,26M *(30/06)* → 105,75M *(24/07)* → **70,45M** *(07/08)* |

*Ba mốc kho là ba **mức**, không phải một **đường đi** — chúng cách nhau khoảng hai tuần trên một chu kỳ rút hằng tuần.*

*Vì sao hai con số buyback lệch nhau: hợp đồng chỉ chặn gọi **sớm** hơn `hop`, không chặn gọi **muộn**. Tham số vì vậy là một **mức tối đa**, không phải một lịch chạy đảm bảo — nên mọi lượt đo thực tế phải nằm dưới nó.*

**Đã đổi sau ảnh chụp — cast 17/08/2026, block 25.775.271**

Một giao dịch, năm thứ đổi cùng lúc:

| | ngày 07/08 | từ 17/08 |
|---|---:|---:|
| chế độ phân bổ | chế độ 1 | **chế độ 2** |
| tỉ lệ chia: mua SKY / thưởng USDS | 100% / 0% | **55% / 45%** |
| khoảng cách tối thiểu giữa hai lượt | 13.787 giây | **3.748 giây** |
| dòng vest cấp SKY cho chương trình thưởng | 286.714.697 SKY / 90 ngày | **96.903.706 SKY / 90 ngày** |
| cỡ cục rút kho | ~22M SKY | **~7,5M SKY** *(cùng nhịp 601.200 giây)* |

Lượng mỗi lượt không đổi ($6.000), nên lượng rút khỏi quỹ đệm đi từ **~$37.601/ngày** lên **$138.314/ngày** — tách thành **$76.073** mua SKY và **$62.241** thưởng USDS.

---

## Điều gì sẽ làm bức tranh trên sai?

Bài này không yêu cầu bạn tin BlockPinned. Nó phải có cách bị bác — ba cách rẻ nhất:

- **Nếu SKY mua lại thực sự bị đốt** thì `totalSupply` phải giảm sau một kỳ phân bổ. Đọc ở hai block, nó không giảm.
- **Nếu người chỉ giữ SKY có dòng tiền tự động** thì phải tồn tại một contract trả value chỉ dựa trên số dư, không cần stake. Chưa tìm ra cái nào.
- **Nếu thưởng staking được trả bằng doanh thu vừa kiếm** thì token trả cho staker phải rời khỏi một địa chỉ đang giữ doanh thu. Truy ngược thì nó rời **kho**; còn nhánh USDS thì được **đúc lúc trả**.

*Các phép kiểm còn lại nằm ở lớp dưới.*

---

# 🔎 Lớp kiểm chứng

> **Từ đây trở xuống là phần dành cho người muốn tự đo lại, không phải phần để hiểu Sky.** Câu chuyện đã hết ở trên. Nếu bạn muốn bắt lỗi bài này, đây là chỗ có đủ đồ nghề.

## Bảng điều-bác-bỏ đầy đủ

| câu | sai nếu |
|---|---|
| **SKY mua lại không bị đốt** | trace giao dịch buyback cho thấy SKY mua được đi vào một đường đốt thay vì về kho |
| **Người chỉ hold SKY không có dòng tiền tự động** | tồn tại một contract trả value chỉ dựa trên việc một địa chỉ đang giữ SKY, không cần stake |
| **Thưởng staking bằng SKY lấy token từ kho** | contract thưởng bắt đầu mint SKY mới, hoặc lấy token từ một nguồn khác |
| **Float tăng được trong khi tổng cung đứng yên** | phân phối từ kho đồng thời làm `totalSupply` giảm tương ứng |
| **Gần một nửa backing trong sổ lõi là IOU của các Star** | đọc trực tiếp các vault allocator cho thấy tài sản cuối cùng nằm ngay trong sổ lõi |
| **Buyback bằng ~9,48% khối lượng tự nhiên trên Uniswap V2** | đo lại cùng cửa sổ 30,11 ngày ra tỉ lệ khác, hoặc số lượt khác 188 |
| **"Sky Reserves" và "Aggregate Backstop Capital" là MỘT đại lượng** | tìm được một văn bản chính chủ định nghĩa chúng thành hai quỹ tách biệt, với hai số dư khác nhau tại cùng một mốc |
| **Kho ra thành từng cục rời rạc mỗi 601.200 giây, không phải dòng chảy đều** | đọc số dư kho ở nhiều ngày liên tiếp mà thấy nó giảm đều, thay vì đứng yên rồi tụt một nhát |
| **Nhánh "buyback and burn" chưa làm giảm cung** | `totalSupply()` đọc ở hai block trước và sau một kỳ phân bổ cho ra hai số khác nhau theo chiều giảm |
| **Buyback tạo USDS kèm một khoản nghĩa vụ ghi cùng lúc** | đọc sổ tại hai block quanh một lượt buyback mà chỉ thấy phía tài sản đổi, không thấy phía nghĩa vụ |

## Một chỗ bài cố ý không dùng

**"Lộ trình 15 ngày runway."** Có hai văn bản khác nhau hay bị nhắc chung. **Atlas** — bộ luật của giao thức — viết chế độ thứ hai với ngòi là *trạng thái của chính cỗ máy* (SKY cấp cho chương trình thưởng đi tới cạn). Còn **bản cập nhật tài chính hằng tháng**, tức publisher chứ không phải Atlas, mô tả một lộ trình theo giai đoạn với ngòi bằng chữ *"when native SKY reserves eventually reach 15 days of runway"* và **một tỉ lệ chia khác hẳn**. Khác nguồn, khác ngòi, khác tỉ lệ — gộp hai cái là lỗi phổ biến nhất khi đọc Sky. Lộ trình theo giai đoạn đó **không được nhắc lại ở bốn kỳ cập nhật liên tiếp** sau khi công bố, nên bài không dựng câu nào lên nó.

## Sáu kỳ settlement gần nhất

Đây là chuỗi đứng sau câu *"có tháng hứng một kỳ, có tháng hứng hai"* ở mục 3.

| kỳ báo cáo | chốt sổ | vào P&L |
|---|---|---|
| Nov–Dec 2025 *(hai tháng)* | 02/02/2026 | tháng 2 — **$37,27M** |
| Jan 2026 | 02/03/2026 | tháng 3 |
| Feb 2026 | 30/03/2026 | tháng 3 — tổng **$32,42M** |
| Mar 2026 | 27/04/2026 | tháng 4 — **$16,03M** |
| Apr 2026 | ~04/05/2026 | tháng 5 — **$20,53M** |
| May 2026 | 22/06/2026 | tháng 6 — **$21,59M** |

Tháng 2 và tháng 3 mạnh gần gấp đôi tháng 4 **không** vì business co lại: tháng 2 chứa settlement của hai tháng cuối 2025, tháng 3 chứa hai kỳ, tháng 4 chỉ chứa một.

## Nhịp rút kho, chính xác tới giây

Cục thưởng rời kho theo một cái đồng hồ **601.200 giây — bảy ngày trừ đúng một giờ**, trong khi cửa sổ trả thưởng của chính cái farm nhận tiền là **604.800 giây**. Hai hằng số nằm ở **hai contract khác nhau**, lệch đúng **3.600**, nên mỗi tuần đợt chi **trôi sớm thêm một giờ**. Đó là lý do một lần đọc số dư kho chỉ có nghĩa khi bạn biết mình đang đứng ở đâu trong tuần.

## Chạy lại bằng chính máy của bạn

```text
# Tỉ lệ chia hiện tại
Splitter.burn()          # phần đi mua SKY (phần còn lại sang thưởng USDS)
Splitter.hop()           # khoảng cách tối thiểu giữa hai lượt, tính bằng giây

# SKY nằm trong kho giao thức
SKY.balanceOf(0xBE8E3e3618f7474F8cB1d074A26afFef007E98FB)

# Tổng cung — đọc tại hai block bất kỳ, phải bằng nhau
SKY.totalSupply()

# Nhịp rút kho: hai hằng số nằm ở HAI contract khác nhau, lệch đúng 3.600 giây
CRON_REWARDS_DIST_JOB.intervals(REWARDS_DIST_LSSKY_SKY)   # 601200 = 7 ngày − 1 giờ
REWARDS_LSSKY_SKY.rewardsDuration()                       # 604800 = 7 ngày trọn

# Ngưỡng cho phép buyback chạy
Kicker.kbump()
Kicker.khump()           # khai int256 — ÂM được, tức cấp phép chạy khi đang thâm hụt
```

Địa chỉ contract nên resolve lại từ Chainlog tại thời điểm kiểm, đừng chép từ trí nhớ.

**Cơ chế có thể sống nhiều tháng. Tham số và số dư thì đổi được trong một giao dịch.** Đó là lý do BlockPinned tách hai thứ này ra.

*Không phải lời khuyên đầu tư. Số on-chain chốt tại block 25.700.475 trừ chỗ ghi mốc khác; số tài chính lấy từ báo cáo quý II/2026 và các công bố công khai của Sky.*

@BLOCKPINNED
