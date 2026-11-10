# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Lưu Nhật Nam
- MSSV: 2A202603243
- Email: niuzoh@gmail.com
- Lớp: 2A
- Link repo bài làm: 
- Link Colab đã chạy: https://colab.research.google.com/drive/1OSpQcVHMhEhEw3eIfFQagId7mYIrF0B7?usp=sharing

## 2. Schema và mini guideline

Xem [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Mình áp dụng đúng schema 4 lớp (`0 car`, `1 truck`, `2 bus`, `3 van`), mỗi xe một box ôm sát phần thân nhìn thấy, không gán mô tô, người, biển báo, phản chiếu.

Ba ca mơ hồ đã quyết định:

1. `drive_009`: xe cỡ lớn dạng hộp dễ nhầm giữa `van` và `bus`. Quyết định: gán `van`, trừ khi xe dài và có dãy cửa sổ liên tục thì gán `bus`.
2. `drive_032`: (a) xe ở làn bên kia dải phân cách, nhỏ và bị cột trụ che một phần: không gán; (b) xe nhỏ bị cắt bởi mép trên ảnh: gán `car`, cạnh box chạm đúng mép ảnh.
3. `drive_045`: nhiều xe rất nhỏ gần đường chân trời: gán `car` nếu vẫn nhìn rõ hình dạng xe trên làn chính, bỏ qua nếu chỉ là vệt sáng hoặc đèn xe.

Phần cần giảng viên làm rõ: (i) tiêu chí đo được để phân biệt `van` và `bus` (schema chỉ mô tả bằng lời); (ii) phạm vi gán nhãn, cụ thể có gán xe ở làn ngược chiều hoặc rất nhỏ/xa hay không.

## 3. Annotation và self-QC

- Số file nhãn train: 50 (notebook xác nhận `OK: 50 train + 10 eval` khi clone repo).
- Kết quả checker và lỗi đã xử lý: lần chạy `check_yolo_labels.py` đầu tiên không đạt vì sai và thiếu label nhiều.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: drive_001-020
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa: kiểm tra và dán lại các bbox. Lỗi phát hiện sau khi có gold được ghi ở mục 4.
- Commit khóa nhãn ban đầu: **[ĐIỀN: mã commit (hash) của bản nhãn ban đầu đã push; nếu không có commit riêng thì ghi rõ "không có commit riêng cho bản khóa ban đầu"]**

## 4. Gold QC và rework

| Chỉ số | Trước sửa (lần chấm đầu) | Sau sửa (lần chấm cuối) |
|---|---:|---:|
| TP | 453 | 598 |
| FP | 689 | 23 |
| FN | 200 | 55 |
| Precision | 0.3967 | 0.963 |
| Recall | 0.6937 | 0.9158 |
| F1 | 0.5047 | 0.9388 |
| mean_iou_of_matches | 0.7286 | 0.8421 |
| passed | false | True |

Kết quả cuối nằm ở [outputs/annotation_evaluation.json](../../outputs/annotation_evaluation.json).

Diễn biến các lần chấm (ngưỡng đạt: F1 ≥ 0.80 và mean IoU ≥ 0.70):

| Lần | Số box của tôi (gold: 653) | TP | FP | FN | Precision | Recall | F1 | mean IoU |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1142 | 453 | 689 | 200 | 0.397 | 0.694 | 0.505 | 0.729 |
| 2 | 778 | 423 | 355 | 230 | 0.544 | 0.648 | 0.591 | 0.761 |
| 3 | 705 | 424 | 281 | 229 | 0.601 | 0.649 | 0.624 | 0.854 |
| 4 (sau khi đổi ID lớp) | 705 | 523 | 182 | 130 | 0.742 | 0.801 | 0.770 | 0.857 |

Rework:

- **Lần 1 → 3: bớt box thừa.** Lần 1 tôi vẽ 1142 box so với 653 của gold (FP 689). tôi dùng `diff_labels.py` để liệt kê từng box thừa, sai lớp, lệch hoặc sót kèm số dòng, lớp và vị trí, và ảnh overlay (`--draw`) để đối chiếu. Các ảnh nhiều lỗi nhất lúc đầu: `drive_003`, `002`, `030`, `006`, `043`, `001`. Sau khi xóa box thừa, FP giảm xuống 281 nhưng TP không tăng (453 → 424), cho thấy chỉ bớt box thì không đủ.
- **Lần 3 → 4: phát hiện lỗi ID lớp, không chỉ suy từ FP/FN.** tôi ghép box theo vị trí, bất kể lớp, và lập ma trận nhầm lớp: 422 box đúng vị trí và đúng lớp, 118 box đúng vị trí nhưng sai lớp. Sai lớp theo quy luật xoay vòng, ba lớp hiếm không có box nào đúng: gold `van` bị gán `bus` (52/54), gold `truck` bị gán `van` (32/46), gold `bus` bị gán `truck` (16/20), trong khi `car` đúng. Điều này khớp với việc task CVAT tạo label theo thứ tự `car, bus, van, truck` (khác schema `car, truck, bus, van`) nên CVAT xuất ID lệch.  Quyết định sửa: đổi ID bằng `remap_classes.py` (1→2, 2→3, 3→1), có sao lưu bản gốc. Kết quả: TP 424 → 523, F1 0.624 → 0.770.
- **Sau lần 4 đến lần cuối:** xóa box ở drive_050, 009, 024, 045; sửa các box nhầm lớp car↔truck để tối ưu đầu ra.

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Google Colab, GPU Tesla T4 (14.9 GB), Ultralytics 8.4.208, Python 3.13.16, Torch 2.14.1+cu130.
- Các tham số thay đổi so với notebook nếu có và lý do: không đổi tham số; chỉ đặt `REPO_URL` trỏ tới repo của em. Cấu hình giữ nguyên: `yolo26n.pt`, `epochs=50`, `imgsz=640`, `batch=-1` (AutoBatch chọn 45), `seed=20260909`.
- Đường dẫn best checkpoint trong phiên chạy: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (không đưa vào repo).

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0.683 |
| Recall | 0.610 |
| mAP50 | 0.632 |
| mAP50–95 | 0.376 |

Theo từng lớp (10 ảnh eval, 113 instance):

| Lớp | Instance (số ảnh) | P | R | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|---:|
| car | 94 (10) | 0.777 | 0.840 | 0.892 | 0.588 |
| truck | 5 (5) | 0.353 | 0.600 | 0.435 | 0.316 |
| bus | 2 (2) | 0.825 | 0.500 | 0.495 | 0.297 |
| van | 12 (6) | 0.778 | 0.500 | 0.706 | 0.302 |

Bằng chứng: ảnh dự đoán trên 10 ảnh eval ở [assets/eval_predictions/visuals/](assets/eval_predictions/visuals/) (ví dụ [drive_058.jpg](assets/eval_predictions/visuals/drive_058.jpg)), confusion matrix và các đường cong ở [assets/yolo26_runs/vehicle_eval/](assets/yolo26_runs/vehicle_eval/), log train theo epoch ở [assets/yolo26_runs/vehicle_annotation/results.csv](assets/yolo26_runs/vehicle_annotation/results.csv).

**Trả lời bốn câu hỏi cuối notebook**

**1. Lớp nào recall thấp nhất? Ảnh nào minh họa?**

`van` và `bus` cùng có recall thấp nhất (R = 0.50). `bus` chỉ có 2 instance (2 ảnh) nên một lần sót đã kéo recall về 0.50, không đủ để kết luận; tôi phân tích `van` (12 instance, 6 ảnh; P = 0.778, mAP50–95 chỉ 0.302). Ở conf 0.25, model chỉ dự đoán `van` ở 2 ảnh (`drive_053`, `drive_058`), trong khi gold có `van` ở 6 ảnh, nên bỏ sót hoàn toàn `van` ở ít nhất 4 ảnh.

Ảnh minh họa `drive_058`.

Nguyên nhân có thể: mất cân bằng lớp và xe van có dáng hộp nên dễ lẫn với `bus`, `truck`, `car`.

**2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?**

Kết quả của em: mAP50 = 0.632 nhưng mAP50–95 = 0.376 (car 0.892 → 0.588; van 0.706 → 0.302). mAP50 chỉ cần IoU ≥ 0.5, còn mAP50–95 tính đến IoU 0.95, nên chênh lệch lớn nghĩa là model tìm đúng xe và đúng lớp nhưng **box chưa khít**. Cần kiểm trên box: độ khít của cạnh (lệch tâm, rộng hay hẹp hơn box gold), đặt box dự đoán cạnh box gold của cùng xe, và xem lỗi tập trung ở xe nhỏ/xa, xe bị che hoặc cắt rìa.

Nguyên nhân có thể: chỉ có 50 ảnh train; xe nhỏ và xa nên lệch vài pixel làm IoU tụt mạnh (train ở 640 px); xe bị che hoặc cắt rìa khó xác định ranh giới. Nhãn train của tôi khớp gold khá tốt, vì vậy chất lượng nhãn có lẽ không phải nguyên nhân duy nhất, nhưng chưa thể loại trừ hoàn toàn.

**3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ?**

Schema phân biệt `car`, `truck`, `bus`, `van` chỉ bằng mô tả, chưa có tiêu chí đo được. Dữ kiện: (a) khi chấm nhãn với gold, sau khi sửa ID lớp còn khoảng 18 box đúng vị trí nhưng sai lớp (ước tính từ ma trận nhầm lớp sau khi áp ánh xạ ID, khớp với kết quả lần chấm 4), chủ yếu `car` ↔ `truck` (khoảng 11 box), tiếp đến `bus` ↔ `truck` (khoảng 3), còn `van` ↔ `bus` chỉ vài box; (b) ở model, `truck` có precision thấp nhất (0.353) và `van` chỉ đạt recall 0.50, cho thấy các lớp xe cỡ lớn dễ lẫn nhau và lẫn với `car`. tôi đã bổ sung tiêu chí (độ dài thân, dãy cửa sổ liên tục, cabin tách khỏi thùng hàng) vào `GUIDELINE_MINI.md`.

Ngoài ra, lỗi thứ tự label trong CVAT là lỗi quy trình chứ không phải lỗi guideline: nó làm ID bị lệch, được phát hiện qua gold QC và sửa bằng `remap_classes.py`.

**4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?**

Eval đo model trên dữ liệu chưa từng thấy. Đưa vào train thì model học đáp án của chính các ảnh đó: chỉ số bị thổi phồng, không phản ánh khả năng tổng quát hóa, và không còn tập để phát hiện overfitting (nguy hiểm khi chỉ có 50 ảnh train).

Trong notebook, `data.yaml` trỏ `val` tới 10 ảnh eval, nên chúng được dùng làm validation sau mỗi epoch để tính mAP và chọn `best.pt` (mAP50 dao động từ khoảng 0.20 ở đầu lên 0.63 ở giữa quá trình train rồi về 0.60 ở epoch 50). Vì vậy chúng không phải test set độc lập, và mAP50 = 0.632 có thể hơi lạc quan.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Chấm nhãn lần đầu | F1 chỉ 0.505, FP 689 (vẽ 1142 box so với 653 của gold) | Dùng `diff_labels.py` liệt kê box thừa/sai lớp/sót, xóa box thừa | F1 lên 0.624 nhưng TP không tăng |
| Gold QC | 118 box đúng vị trí nhưng sai lớp theo quy luật xoay vòng | Lập ma trận nhầm lớp, đổi ID lớp bằng `remap_classes.py` (1→2, 2→3, 3→1) | TP 424 → 523, F1 0.770 |
| `check_yolo_labels.py` | Báo lỗi "cần đúng 5 giá trị" ở 50 dòng do file `train.txt` của CVAT lẫn trong thư mục nhãn | Xóa `train.txt` khỏi `dataset/labels/train` | checker đã đạt** |



## 7. Tự đánh giá theo rubric

Em chưa đối chiếu chi tiết với [RUBRIC.md](../../RUBRIC.md). Theo `SUBMISSION.md`:

- Đã có: 50 file nhãn train, `GUIDELINE_MINI.md`, notebook đã chạy trên Colab với metrics và ảnh dự đoán trên 10 ảnh eval, bốn câu trả lời phân tích, số liệu trước/sau rework.
- Còn cần xác nhận: kết quả gold QC cuối (`passed`) và các số **[ĐIỀN]** ở mục 3, 4, 5; checker nhãn đã đạt sau khi xóa `train.txt`; nhãn và `outputs/annotation_evaluation.json` đã xuất hiện trên GitHub; không có gold hay file `.pt` trong repo.
- Hạn chế: tập eval chỉ 10 ảnh (`bus` 2 instance, `truck` 5 instance) nên chỉ số theo lớp nhiễu; eval cũng dùng làm validation nên không phải test set độc lập.

## 8. Công cụ AI và tài liệu tham khảo

Công cụ AI: Claude.

Nguồn ngoài repo: CVAT online (app.cvat.ai) để gán nhãn; thư viện Ultralytics YOLO và checkpoint `yolo26n.pt` theo notebook; Google Colab; bộ ảnh là tập con ảnh giao thông CCTV (nguồn gốc UA-DETRAC, giấy phép CC-BY-4.0) theo ghi chú dữ liệu trong README.
