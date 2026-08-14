# BlockPinned — site

Sổ gốc của [blockpinned.com](https://blockpinned.com). Mỗi bài đăng ở đây kèm một **sổ
claim**: từng khẳng định mang số block nó được đọc ra, một **điều bác bỏ ghi trước**
nói rõ cái gì sẽ chứng minh nó sai, và một nhật ký nối thêm khi có kết quả.

Claim bị bác **không bị xoá**. Nó đổi trạng thái và nằm nguyên trên trang.

## Vì sao repo này công khai

Kênh bán một thứ duy nhất: số nào cũng truy ngược được. Bộ sinh trang cũng phải
chịu cùng luật đó — nên nó ở đây, chạy lại được, và **cổng của nó chặn được chính tôi**.

## Dựng lại

```bash
python3 build.py            # sinh docs/ — cổng nào chặn thì KHÔNG có trang
python3 test_cong.py        # ép từng cổng phải nổ, kèm control âm
python3 preview.py          # ảnh chụp khổ hẹp + phép đo tràn tự kiểm
```

Chín mẫu visual cho bài dài và cấu hình copy-paste nằm tại [`VISUALS.md`](VISUALS.md).

`docs/` là thứ GitHub Pages phục vụ. Nó là **bản sinh ra** — sửa nội dung ở
`content/`, đừng sửa `docs/`.

## Các cổng CHẶN build

Không cổng nào chỉ cảnh báo. Cảnh báo là thứ người ta quen mắt bỏ qua.

| | Cổng | Chặn cái gì |
|---|---|---|
| ① | ngôn ngữ | từ nghề đã khai tử, và chữ tự bịa |
| ② | cấu trúc | bài thiếu một trong năm phần bắt buộc |
| ③ | claim | claim thiếu điều-bác-bỏ, thiếu block, hoặc trạng thái lạ |
| ④ | ngôi xưng | "chúng tôi" — desk này một người |
| ⑤ | đánh dấu | markdown ngoài tập con thì **nổ**, không nuốt im |
| ⑥ | thuộc tính số | toạ độ/số trong HTML sinh ra phải là số hợp lệ |
| ⑦ | xem trước | bài thiếu dòng mô tả, hoặc ảnh xem trước trỏ vào file không có |
| ⑧ | đo lại | nút "đo lại ngay" khai thiếu, hoặc claim không đo được mà không nói vì sao |
| ⑨ | hạn | ngày phân định không có mốc và ý nghĩa rõ ràng |
| ⑩ | ghi trước | kết quả hoặc nơi ghi trước bị bỏ trống |
| ⑪ | liên kết | href nội bộ không trỏ tới trang/neo có thật |
| ⑫ | fact | Fact thiếu số, block, lệnh tự kiểm hoặc khoảng cách đáng kể |
| ⑬ | bố cục | component v3 bắt buộc bị rơi khỏi HTML |
| ⑭ | visual | marker, schema, claim nguồn, hình và bảng dữ liệu không khớp một-một |

Cổng ③ là bản máy của một lỗi thật: một claim suýt đăng khi đã bị cắt mất điều
bác bỏ, mà ô tick "có điều bác bỏ?" vẫn nguyên vì nó thừa kế từ bản trước.
Người phản biện bắt được, checklist không bắt được.

## Sinh ra thế nào

Repo này là **bản mirror** sinh bằng `publish_site.py` từ kho làm việc. Đừng sửa
trực tiếp ở đây — lần sinh sau sẽ đè lên.
