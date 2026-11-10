# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe con chở người cỡ nhỏ: sedan, hatchback, SUV, taxi, xe bán tải (cabin nhỏ). | Thân thấp, thường 1 hàng ghế trước và 1 hàng sau. Xe bán tải vẫn tính là `car`, không tính `truck`. |
| `truck` | Xe tải chở hàng và xe đầu kéo: có cabin riêng và thùng hàng phía sau, thân cao và dài hơn xe con. | Phân biệt với `van`: `truck` có cabin tách khỏi thùng hàng; `van` là một khối liền. |
| `bus` | Xe buýt và minibus chở khách: thân dài, nhiều cửa sổ dọc thân, chiều cao lớn. | Phân biệt với `van`: `bus` dài hơn nhiều, có dãy cửa sổ liên tục; `van` ngắn hơn, dáng hộp. |
| `van` | Xe van và minivan chở hàng hoặc chở người: thân dạng hộp liền một khối, cao hơn xe con nhưng ngắn hơn xe buýt. | Không có cabin tách rời như `truck`; nhỏ hơn `bus` rõ rệt. |

Thứ tự ID dùng trong nhãn: `0 = car`, `1 = truck`, `2 = bus`, `3 = van` (đúng schema của bài).

## Quy tắc chung

- Box bám sát vật thể nghĩa là: cạnh box chạm vào phần thân xe nhìn thấy được, không lấy thêm mặt đường, bầu trời hay xe bên cạnh. Mỗi xe một box riêng, kể cả cùng lớp. Hai xe chồng nhau thì vẽ hai box trên phần nhìn thấy của từng xe.
- Vật thể bị che khuất: vẫn gán box quanh phần nhìn thấy được, nếu từ phần đó nhận diện được lớp.
- Vật thể bị cắt bởi rìa ảnh: gán box và cho cạnh box chạm đúng rìa ảnh; không đoán phần nằm ngoài khung.
- Vật thể rất nhỏ/mơ hồ: chỉ gán khi nhìn rõ hình dạng xe và xác định được lớp. Nếu chỉ còn mảnh quá nhỏ hoặc không chắc lớp thì không tự đoán, không gán, và ghi lại ở bảng dưới.
- Xe đang đỗ vẫn gán theo loại xe. Không gán: người đi bộ, xe đạp, mô tô/xe máy, biển báo, đèn giao thông, phản chiếu trong kính/gương, hình xe trên bảng quảng cáo.


## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_009` | Xe cỡ lớn dạng hộp ở phía trên ảnh, dễ nhầm giữa `van` và `bus`. | Gán `van`, trừ khi xe dài và có dãy cửa sổ liên tục thì gán `bus`. | Schema ghi `van` gồm minivan chở người, còn `bus` là xe buýt lớn/minibus. Dùng độ dài thân và dãy cửa sổ để phân biệt. |
| `drive_032` | Xe ở làn đường bên kia dải phân cách (góc trên bên phải), bị cột trụ và dải phân cách chắn một phần, kích thước nhỏ. | Không gán. | Ở xa, nhỏ và bị che, không xác định chắc lớp nên theo quy tắc không tự đoán; giữ nhất quán chỉ gán xe trên làn đường chính phía trước camera. |
| `drive_032` | Xe nhỏ bị cắt bởi mép trên của ảnh. | Gán `car`, cạnh trên của box chạm đúng mép ảnh. | Quy tắc vật thể bị cắt khung: box chạm rìa, không đoán phần nằm ngoài ảnh. |
| `drive_045` | Nhiều xe rất nhỏ gần đường chân trời, cao chỉ khoảng 20 px. | Gán `car` nếu vẫn nhìn rõ hình dạng xe trên làn đường chính; bỏ qua nếu chỉ là vệt sáng hoặc đèn xe. | Còn nhận diện được lớp thì theo quy tắc vẫn gán; không xác định được thì không đoán. |
