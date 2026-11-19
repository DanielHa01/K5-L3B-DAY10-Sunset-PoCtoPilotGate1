# Báo cáo bổ sung CP3 · Nhóm Sunset · 19/11/2026

Nhóm em đã bổ sung nội dung Phiếu B, config vận hành, phép thử nhân sự, snapshot kỹ thuật và quyết định v1 **Cải tiến thêm**. Bộ nền đạt các ngưỡng đã ký. Tuy vậy, bản chốt hiện tại được tạo **sau khi nhận S6**, nên hồ sơ này không chứng minh CP3 đã hoàn thành đúng thứ tự trước sự cố; chưa có xác nhận Coach chấp nhận ngoại lệ này.

## 1. Thứ tự thực tế và giới hạn của mốc prepared

| Sự kiện | Bằng chứng |
|---|---|
| Ký tiêu chí | Commit `1a3786d`, `signed_at=2026-11-19T15:52:32`, hash `69d355e4`; file vẫn giữ nguyên |
| Bản chốt cũ | Commit `0149d25` lúc 16:06:09 GMT+7, sau đó bị revert bởi `b02baf6` lúc 16:09:36 |
| Nhận S6 | Commit `528560a`, 16:31:27 GMT+7 |
| Bổ sung KT1–KT3 | Commit `632c0eb`; code ghi rõ được bổ sung sau nhận S6 |
| Hoàn thiện operations và đo lại | `R-base-after-20261119-174422-6e5a09` |
| Chốt kỹ thuật bổ sung | `taken_at=2026-11-19T17:44:46` GMT+7, hash `32d5efc2` |
| Đo prepared bổ sung | `R-base-prepared-20261119-174446-6e5a09` |

Nhóm em giữ thời gian thực và các commit cũ, không sửa timestamp hoặc ghi bản mới thành bản trước sự cố. Snapshot bổ sung dùng để cố định code/config trước các sửa tiếp theo ở CP4. Mức chuẩn bị trước khi biết thẻ không được suy từ kết quả của snapshot này. PIC Hà Phan Đại Dương cần trao đổi Coach về cách ghi nhận điều kiện thời gian; báo cáo không ghi việc trao đổi đó đã xảy ra.

## 2. Phạm vi đã làm

| Mục | Nội dung và kết quả |
|---|---|
| B0–B3 | Giữ các lần chạy và phân tích `T-002@55`, phép đo chọn chính sách, bản đồ dữ liệu và drift. Phần xác nhận trực tiếp của Dương về quy tắc gán nhãn chưa được giả định là đã có |
| B4–B5 | Có HAZOP kỹ thuật/ngoài kỹ thuật và checklist 9 nhóm có PIC; các rủi ro chưa xử lý giữ trạng thái Chưa |
| B6 | Bổ sung đủ kỹ thuật, kinh doanh, con người/vận hành, pháp lý; đánh dấu nội dung bổ sung sau nhận S6 |
| B7.1–B7.4 | Giữ KT1–KT3, behavioral test, cổng business và legal; không xử lý riêng theo ID ticket |
| B7.5 | Điền kênh cảnh báo mô phỏng, người nhận phản ánh, ngưỡng vàng/đỏ, thời hạn dừng, người cho bật lại và đường xử lý ca tồn |
| B7.6 | Đo what-if một/hai người và tải dồn; số người trực thực tế trong config vẫn là 1 |
| B8 | Ghi v1 Cải tiến thêm, ba bằng chứng, phân khúc xấu nhất, người phụ trách và hạn đo lại |
| Hồ sơ phụ trợ | Mục cá nhân An, ghi S6 và lưu ý mốc muộn ở Phiếu C, thông tin nhóm và decision_v1 trong submission.json |

`submission.json` chưa có decision_v2 và ba dòng cuối vì đó là CP5, chưa được đo/kết luận. Monitor mới và đánh giá S6 thuộc CP4. Không chạy gom bài để trình bày CP4/CP5 như đã hoàn thành.

## 3. Kết quả máy đo

| Chỉ số | Base trước cổng | Prepared bổ sung |
|---|---:|---:|
| Lượt đúng | 109/110 | 110/110 |
| pass_rate | 0,9909 | 1,0000; CI 95% [1,0; 1,0] |
| pass^k | 0,9545 | 1,0000 |
| Hoàn sai | 20.000đ | 0đ |
| Lỗi ghi oan hãng | 1 | 0 |
| Lộ PII | 0 | 0 |
| Chi phí/ticket | 4.203đ | 4.202đ |
| ROI | 1,34 | 1,38 |
| Chờ lâu nhất / ca ùn | 0 phút / 0 | 0 phút / 0 |
| Chuyển người | 22,73% | 22,73% |
| Phạm vi | 100% | 100% |
| Tiền máy lớn nhất | 670đ | 670đ |
| Hoàn tự động nhiều nhất/ngày mô phỏng | 155.000đ | 155.000đ |

Base dùng `R-base-before-20261119-160603-b45eeb`; prepared dùng `R-base-prepared-20261119-174446-6e5a09`. Gate đối chiếu đủ required, business_ops, nice-to-have; không có ca mới hỏng, không có dòng vượt trần trên bộ nền. 13/13 test công khai đạt. Tiêu chí và các file khóa theo manifest còn nguyên, snapshot verify đạt.

Các con số này không thay đánh giá S6, test ẩn hoặc thử với người thật. Trong phân khúc kho xác định được, DN có chi phí cao nhất 4.586đ/ticket. Nhóm `?` (không tra được đơn/kho) tốn 10.359đ/ticket và chuyển người 100%; không gọi đây là kho thật hoặc bỏ nó để che chi phí.

## 4. Căn cứ cho phương án vận hành

- Cảnh báo chờ từ **30 phút**, bằng nửa SLA; dừng nhận tự động từ **45 phút**, hoàn tất thao tác trong **5 phút từ phát hiện**, còn 10 phút đệm trước 60 phút. Chưa có số đo độ trễ từ lúc lỗi xảy ra đến lúc phát hiện.
- Cảnh báo chi phí **6.400đ/ticket**, máy **1.200đ/ticket**, hoàn ngày **1.600.000đ**, là 80% các trần 8.000đ, 1.500đ và 2.000.000đ. Các trần đã ký không đổi. ROI dưới 0,50 cần rà soát, dưới 0,25 phải dừng phạm vi chưa đạt.
- `gate1-ops-sunset` là tên nhật ký cảnh báo quy ước trong bài mô phỏng; chưa có bằng chứng đã thiết lập kênh thật. Config không tự gửi cảnh báo hoặc thực thi mọi câu stop_conditions; người trực thực hiện runbook.
- NV-TUNG giữ công tắc và ký bật lại sau kiểm chứng; NV-HANH duyệt/nhận ca và phản ánh người nhận hàng; NV-OANH đối soát hãng/shop. Nhân viên thứ hai chưa được dữ liệu xác nhận danh tính/quyền, nên chỉ là phương án what-if.

Phép thử nhân sự chỉ thay số người trong bộ nhớ, giữ nguyên dữ liệu đề/config:

| Phép thử | 1 người, 6 ca/giờ | 2 người, 12 ca/giờ |
|---|---:|---:|
| Bộ nền: chi phí/ticket | 4.202đ | 5.565đ |
| Bộ nền: ROI | 1,38 | 0,80 |
| Cụm 14 ca cách 2 phút: chờ lớn nhất | 104 phút | 39 phút |
| Cụm 14 ca: ca ùn | 6 | 0 |
| 14 ca/giờ kéo dài 8 giờ: chờ lớn nhất | 664 phút | 109 phút |
| 14 ca/giờ kéo dài: ca ùn | 104 | 47 |

Thêm người tăng phí trực 30.000đ/ca. Hai người giải được cụm dồn thử nghiệm nhưng không đủ cho tải 14 ca/giờ kéo dài. Khi không bố trí được người hợp lệ hoặc chờ đạt 45 phút, NV-TUNG dừng nhận tự động, NV-HANH xử lý ca tồn; không coi chuyển tất cả sang thủ công là tự giải quyết công suất.

## 5. Quyết định và việc tiếp theo

**Cải tiến thêm; tiếp tục sửa và đo offline, chưa mở pilot.** Bộ nền đạt nhưng thiếu kết quả S6, kiểm tra trần lỗi hãng/ngày, telemetry thực tế, quyền của nhân viên dự phòng và xác nhận thủ tục mốc chốt muộn. Chưa có căn cứ chọn Tiếp tục hoặc một phạm vi Thu hẹp đã đo đủ.

- Nguyễn Hữu An: kiểm S6, tối thiểu hai lỗi khác nguồn, monitor mới, regression và nguồn tracking từng kiện; giữ nguyên snapshot vừa chốt.
- Lê Bá Nguyên: kiểm quy trình cảnh báo/dừng, đối soát bên thứ ba, rủi ro PII và phương án công suất; không ghi diễn tập thật đã hoàn thành khi mới có mô phỏng.
- Hà Phan Đại Dương: rà quy tắc gán nhãn nghiệp vụ, tổng hợp kinh tế/quyết định và làm rõ với Coach mốc muộn.

Hạn xem kết quả tiếp theo: **10:00 GMT+7 ngày 20/11/2026**, không vượt mốc 30/11/2026 đã ký. Trong thời gian này công tắc on chỉ phục vụ lab giả lập, không biểu thị quyền thực hiện giao dịch cho khách thật.

## 6. Bằng chứng và tái lập

Toàn bộ report thật, nhật ký, trace và log kiểm tra ở [evidence CP3](evidence/cp3-20261119/). `run-index.json` ghi các mã lần chạy; `ops-study.py` tái lập phép thử nhân sự. Các phép what-if được ghi riêng, không gán mã eval giả.

```bash
python3 -m unittest discover -s tests
python3 -m lab10.criteria verify
python3 -m lab10.checkpoint verify
python3 docs/evidence/cp3-20261119/ops-study.py
```

Không chạy lại lệnh chốt. Khi sửa ở CP4, chỉ sửa bản gốc guards/config/monitors được phép; snapshot và tiêu chí đã ký giữ nguyên. Report cũ của máy khác có hash CRLF, report LF trên máy này có hash khác; không sửa hash báo cáo để làm cho khớp. Hai report cuối CP3 cùng hash `6e5a09`, khớp code/config hiện tại.

Các ngưỡng và bản ghi bổ sung được soạn với hỗ trợ Codex, có căn cứ từ số liệu mock và phép đo đính kèm. Nhóm cần giải thích các lựa chọn này lúc demo; báo cáo không thay xác nhận của Coach hoặc phê duyệt chạy thật.
