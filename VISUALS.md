# Visual cho bài dài

Mỗi visual được khai **một lần** trong `*.claims.json`. Builder dùng cùng cấu hình để
dựng cả hình đọc nhanh và bảng dữ liệu gốc có thể mở ra; không chép số sang một nguồn
thứ hai.

## Cách gắn vào bài

1. Thêm object vào mảng top-level `visuals` của file `*.claims.json`.
2. Đặt đúng một marker trên một dòng riêng trong Markdown:

   ```text
   {{visual:ten-visual}}
   ```

3. Mỗi visual phải neo vào ít nhất một `claims[].id` của chính bài.
4. Chạy `python3 site/build.py --bo-cuc v3` và `python3 site/test_cong.py`.

Builder chặn id trùng, marker/config lệch, claim nguồn không tồn tại, loại hoặc màu lạ,
dữ liệu rỗng và trường hợp renderer làm rơi hình/bảng. Bản rollback D2 tự hạ visual
thành bảng đầy đủ.

## Bốn template

### `flow` — đường đi hoặc phép cân sổ

Dùng cho 2–6 chặng có hướng: tiền vào → xử lý → tiền ra, proposal → vote → thi hành.

```json
{
  "id": "money-path",
  "type": "flow",
  "eyebrow": "CÙNG MỘT CỬA SỔ",
  "title": "Tiêu đề nói điều người đọc cần thấy",
  "aria": "Mô tả đầy đủ hình cho người dùng trình đọc màn hình.",
  "caption": "Khai mốc, phạm vi và giới hạn của phép đọc.",
  "claims": ["C1"],
  "steps": [
    {"label": "ĐẦU VÀO", "value": "120", "note": "đơn vị A", "tone": "info"},
    {"label": "ĐANG GIỮ", "value": "100", "note": "tại mốc đo", "tone": "accent"},
    {"label": "ĐẦU RA", "value": "20", "note": "cùng cửa sổ", "tone": "muted"}
  ]
}
```

### `proof` — các vòng siết bằng chứng

Dùng cho 2–6 phép thử nối tiếp, nhất là khi bài đi từ câu hỏi rộng tới kết luận hẹp.

```json
{
  "id": "proof-ladder",
  "type": "proof",
  "title": "Ba vòng trả lời ba câu khác nhau",
  "aria": "Mô tả thứ tự và kết quả của từng vòng kiểm.",
  "caption": "Nói rõ vòng cuối chứng minh được tới đâu.",
  "claims": ["C2"],
  "steps": [
    {"label": "VÒNG 1", "question": "hỏi gì", "value": "0/10", "note": "vì sao chưa đủ", "tone": "bad"},
    {"label": "VÒNG 2", "question": "hỏi gì", "value": "10/10", "note": "đã biết gì", "tone": "warn"},
    {"label": "VÒNG 3", "question": "hỏi gì", "value": "84%", "note": "giới hạn còn lại", "tone": "good"}
  ]
}
```

### `timeline` — chuỗi mốc có độ lớn

Dùng cho 3–16 sự kiện. `magnitude` chỉ điều khiển chiều cao, còn `value` là chữ hiện ra.

```json
{
  "id": "event-timeline",
  "type": "timeline",
  "title": "Nhịp sự kiện qua thời gian",
  "aria": "Mô tả khoảng thời gian, số sự kiện và điểm lệch đáng chú ý.",
  "caption": "Khai rõ chiều cao biểu diễn gì và khoảng cách được tính thế nào.",
  "claims": ["C3"],
  "unit": "TOKEN",
  "events": [
    {"label": "01/01", "value": "120.000", "gap": "—", "magnitude": 120000, "tone": "info"},
    {"label": "15/01", "value": "180.000", "gap": "14 ngày", "magnitude": 180000, "tone": "info"},
    {"label": "05/02", "value": "90.000", "gap": "21 ngày", "magnitude": 90000, "tone": "warn"}
  ]
}
```

### `distribution` — phân bổ theo trạng thái

Dùng cho 2–6 nhóm cộng lại thành một tổng. `count` phải là số nguyên dương.

```json
{
  "id": "status-map",
  "type": "distribution",
  "title": "Mười hai mục không cùng một trạng thái",
  "aria": "Mô tả tổng số và số lượng trong từng nhóm.",
  "caption": "Khai quy tắc phân nhóm và điều không được suy ra.",
  "claims": ["C4"],
  "segments": [
    {"label": "đã khớp", "count": 8, "note": "theo quy tắc A", "tone": "good"},
    {"label": "chưa khớp", "count": 3, "note": "còn kiểm", "tone": "warn"},
    {"label": "không áp dụng", "count": 1, "note": "ngoài phạm vi", "tone": "muted"}
  ]
}
```

### `dai` — cùng một đại lượng, nhiều con số cùng hợp lệ

Dùng cho 2–8 giá trị **của CÙNG một đại lượng** rải trên một trục: nhiều nguồn công bố
nhiều con số, hoặc nhiều cách tính hợp lệ cho nhiều kết quả. Khác `distribution` ở chỗ
các con số **không cộng lại thành gì cả** — ép chúng thành phân bổ là nói dối về dữ liệu.

`value` phải là SỐ (vị trí trên trục tính từ nó). `hien` là chuỗi hiện ra, tuỳ chọn —
dùng khi thân bài viết `13%` mà format tự động cho ra `13,0`. Hai đầu trục phải khác nhau.

```json
{
  "id": "nam-con-so",
  "type": "dai",
  "eyebrow": "CÙNG MỘT CÂU HỎI · BỐN NGUỒN",
  "title": "Tiêu đề nói điều người đọc cần thấy",
  "aria": "Mô tả dải, hai đầu mút và từng con số cho người dùng trình đọc màn hình.",
  "caption": "Khai vì sao các con số khác nhau mà vẫn có thể cùng đúng.",
  "claims": ["C3"],
  "don_vi": "%",
  "cot": "nguồn",
  "diem": [
    {"label": "Nguồn A", "value": 13, "hien": "13", "note": "không khai mẫu số", "tone": "bad"},
    {"label": "Nguồn B", "value": 31.9, "hien": "31,9", "note": "cửa sổ 30 ngày", "tone": "info"},
    {"label": "Nguồn C", "value": 71, "hien": "71", "note": "chính họ đã sửa xuống", "tone": "warn"}
  ]
}
```

🔴 Trục chỉ chở CHẤM, chữ nằm ở danh sách bên dưới. Nhãn đặt tuyệt đối trên trục là ứng
viên tràn số một ở khổ 360px, và khi các giá trị xúm lại một chỗ thì chúng đè lên nhau
mà phép đo tràn vẫn xanh — đè nhau không phải tràn.

Màu hợp lệ: `accent`, `good`, `warn`, `bad`, `info`, `muted`. Màu chỉ giúp quét mắt;
`label`, `aria`, `caption` và bảng gốc mới là lớp mang nghĩa.

## Chọn template nào

- Có mũi tên hoặc quan hệ trước–sau rõ: `flow`.
- Có nhiều tầng kiểm và mỗi tầng sửa cách hiểu: `proof`.
- Có ngày/tháng và cần thấy nhịp hoặc ngoại lệ: `timeline`.
- Có một tổng chia thành vài trạng thái: `distribution`.
- Có nhiều con số cho CÙNG một đại lượng, không cộng lại thành tổng: `dai`.
- Chỉ có một con số hoặc bảng đã đủ rõ: không ép thành visual.

🔵 **Chỗ bộ template CÒN THIẾU, khai ra để lượt sau không phải tìm lại (12/08):** chưa
khuôn nào chở được *"cùng một chuỗi, hai cửa sổ đo, hai chiều NGƯỢC nhau"* — thứ cần một
cặp mũi tên trên cùng trục. `dai` vẽ được bốn chấm nhưng đánh rơi chiều, mà chiều mới là
điều đáng nói. Bài HYPE 12/08 để mục đó ở dạng bảng chứ không ép thành hình.

Một bài dài thường chỉ cần 2–4 visual, đặt sau đoạn đã giải thích dữ liệu. Visual tóm
tắt lập luận; nó không thay claim, caption phạm vi hay bảng kiểm.
