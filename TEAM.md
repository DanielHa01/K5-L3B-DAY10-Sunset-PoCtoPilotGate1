# Team · Sunset

## Thông tin nhóm

- Nhóm: Sunset · Lớp: L3B.
- Repo: `K5-L3B-DAY10-Sunset-PoCtoPilotGate1` · nhánh `main` · thẻ S6 (commit nhận thẻ `528560a`).
- GitHub API ngày 19/11/2026: Public, `fork=false`, không có parent. Repo đúng tên nhưng chưa đáp ứng yêu cầu tạo fork của CP1; giữ nguyên lịch sử và báo Coach, không tạo lại repo để che sai lệch. Nguồn: [metadata repo](https://api.github.com/repos/DanielHa01/K5-L3B-DAY10-Sunset-PoCtoPilotGate1).

## Thành viên

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --- | --- | --- | :---: |
| 1 | Hà Phan Đại Dương | 2A202604119 | Sản phẩm và kinh doanh | Có |
| 2 | Nguyễn Hữu An | 2A202604024 | Kỹ sư cổng | Không |
| 3 | Lê Bá Nguyên | 2A202604100 | Vận hành và pháp lý | Không |
| 4 | Nguyễn Văn Tuấn | 2A202604121 | Kỹ sư đánh giá và theo dõi | Không |

## Cách ghi nhận đóng góp

Đối chiếu `git log` và nội dung `git show`, không chia đều theo số commit. AnnNguy3n là Nguyễn Hữu An; tuannguyen-cell là Nguyễn Văn Tuấn; DanielHa01 là Hà Phan Đại Dương; lbNGuyen06 là Lê Bá Nguyên. Git còn hiển thị tên Nguyễn Hữu An, Le Nguyen và MSSV trưởng nhóm `2A202604119`.

Các phần kỹ thuật ở `5cc3c6d`, `632c0eb` và hồ sơ `8c2cf52` dùng danh tính commit của Dương nhưng An–Dương cùng làm theo xác nhận của nhóm; không quy toàn bộ cho người tạo commit. Các commit hoàn thiện CP3–CP5 trong lượt này dùng danh tính Git sẵn có của trưởng nhóm và có Codex hỗ trợ đọc code, chạy kiểm tra, sửa cổng/monitor, đối chiếu minh chứng và biên soạn báo cáo. Đây là công việc hỗ trợ chung, không tự chia thành bốn đóng góp độc lập. Các ngưỡng ký không đổi; trần mới thực thi lấy từ `ops_limits`.

## NguyenHuuAn-2A202604024

### Phần việc phụ trách

Kỹ sư cổng; Phiếu A câu 1.3, 1.5–1.6; phần kỹ thuật B0–B2, B6, B7.1–B7.3; `lab10/guards.py`.

### Đóng góp cụ thể

- Đưa PRD/eval card Lab 9 vào repo; thiết kế `policy_selection_accuracy`, tham gia viết tiêu chí trước ký. Baseline đo 80/80 ca tới bước policy đúng phiên bản; 30 ca dừng sớm đếm riêng.
- Cùng Dương phân tích `T-002@55` và triển khai KT1 ghim policy hiệu lực, KT2 đối chiếu quyền lợi từ tracking, KT3 kiểm đúng kiện/hãng/tài xế. Chuẩn bị hai ticket hiểm và kiểm thêm hai ticket do vai đánh giá đề xuất. Ba cổng được bổ sung sau nhận S6, không nhận là chuẩn bị trước sự cố.
- Mục cá nhân trước đó đã ghi sử dụng Codex cho đọc repo, đối chiếu trace/số liệu, soạn báo cáo và kiểm tra CP3. Lượt hoàn thiện S6 và báo cáo này tiếp tục có AI hỗ trợ chung như phần trên.

### Bằng chứng

`c314476` (tài liệu Lab 9), `734fb64` (metric), `e8d3bb0` (A3–A4/tiêu chí); phần cùng làm: `5cc3c6d`, `632c0eb`, `8c2cf52`. Bộ nền sau tích hợp `R-base-after-20261119-171327-6fd875`: 110/110, 0 hoàn sai/ghi oan/PII, 4.202đ/ticket, ROI 1,38. CP4 hỗ trợ chung: `442180a`, Phiếu C C2/C7–C9.

### Exit ticket

- Điều rút ra: 109/110 lượt đúng vẫn có 20.000đ hoàn sai và một lỗi hãng oan; phải kiểm dữ kiện trước lệnh ghi, không dựa riêng vào tỉ lệ đúng.
- Điều còn chưa chắc: guard đối chiếu được DB nhưng chưa bảo vệ khi chính tracking nguồn sai hoặc nhiều worker dùng trạng thái khác nhau.

## HaPhanDaiDuong-2A202604119

### Phần việc phụ trách

Trưởng nhóm, Sản phẩm và kinh doanh; mục tiêu, tiêu chí, cổng business, quyết định Gate 1 và theo dõi việc nộp.

### Đóng góp cụ thể

- Ghi mục tiêu hệ thống, ký/commit/push tiêu chí; ghi A5 và nhận đúng S6. Commit ký được push trước các lần đánh giá còn lưu trong nhật ký.
- `a34f841` cập nhật phần business/Phiếu B. Cùng An hoàn thiện các phần kỹ thuật nêu ở bảng ghi nhận; hồ sơ CP3 ghi rõ bản chốt muộn và v1 Cải tiến thêm, không che commit revert.
- Phần báo cáo cá nhân và tổng hợp quyết định trong lượt này có AI hỗ trợ từ commit/report. Không suy ra toàn bộ code trong các commit mang MSSV trưởng nhóm do Dương làm một mình.

### Bằng chứng

`706a8ea` (A1), `1a3786d` (ký), `48118c9` (A5), `528560a` (S6), `a34f841` (business/B), `8c2cf52` (hồ sơ CP3 cùng làm). Reflog push tiêu chí 15:52:44; lần đo sớm nhất còn nhật ký 16:01:01 GMT+7. V2 và căn cứ Dừng ở Phiếu C C12.

### Exit ticket

- Điều rút ra: máy cho phép cân nhắc Tiếp tục về số đo không thay điều kiện giữ nguyên bản chốt; quyết định phải xét cả tiêu chí và lịch sử thực hiện.
- Điều còn chưa chắc: Coach sẽ xử lý thế nào với snapshot bị gỡ/thay và repo Public không phải fork; chưa có xác nhận ngoại lệ.

## LeBaNguyen-2A202604100

### Phần việc phụ trách

Vận hành và pháp lý; A1/A2 phía bên thứ ba, B4/B5, B7.5–B7.6, operations/legal và runbook.

### Đóng góp cụ thể

- Viết mục tiêu của người đối soát/người duyệt và telemetry không nhãn; HAZOP notify_carrier, checklist 9 nhóm có PIC.
- Điền người phụ trách, SLA, stop_conditions, bảo vệ recipient_contact/customer_note và yêu cầu nguyên nhân tracking; viết runbook/giờ cao điểm và bàn giao số nền.
- Báo cáo cá nhân và cập nhật runbook/risk register CP4–CP5 có AI hỗ trợ biên soạn trong lượt chung; chưa có bằng chứng diễn tập dừng, thiết lập kênh cảnh báo hoặc liên hệ hãng thật.

### Bằng chứng

Git author Le Nguyen: `44e1c0b` (A1/A2), `5039e3c` (HAZOP), `47aab38` (operations/legal, runbook), `d6c8a20` (số nền), `c4af866` (checklist), `4851194` (PIC). Các cập nhật sau sự cố ở Phiếu C C10–C11.

### Exit ticket

- Điều rút ra: chuyển người chỉ an toàn khi có công suất và trách nhiệm rõ; một người duyệt 6 ca/giờ không có nghĩa chịu được mọi cụm tải dồn.
- Điều còn chưa chắc: số người dự phòng có thẩm quyền, độ trễ phát hiện/dừng và công suất thực tế chưa được xác minh bằng diễn tập/pilot.

## NguyenVanTuan-2A202604121

### Phần việc phụ trách

Kỹ sư đánh giá và theo dõi; baseline, trace, hồi quy, behavioral test và lưu minh chứng.

### Đóng góp cụ thể

- Tái lập baseline, ghi B0–B1 và phân tích trace B2; chuẩn bị hai cách diễn đạt mới để kiểm việc khách tự khai độ trễ không thay tracking.
- Kiểm chứng bản tích hợp, lưu report trước/sau, trace và nhật ký trong `docs/evidence/quality-engineer-20261119/`. Không coi bộ nền xanh là đã kiểm S6 hoặc test ẩn.
- Báo cáo cá nhân và kiểm tra cuối trong lượt chung có AI hỗ trợ. Hai monitor mới cùng các lượt chạy S6 ở `442180a` là phần hoàn thiện chung, không tự gán riêng cho Tuấn chỉ vì tên vai.

### Bằng chứng

Git author tuannguyen-cell: `94a6f69` (baseline/trace), `725370c` (B7.2/ticket mới), `80afa6f` (kiểm tích hợp và lưu minh chứng). Baseline `R-base-before-20261119-163228-80bad3`; after `R-base-after-20261119-172751-ab9e95`: 110/110, không ca mới hỏng, 13/13 test công khai đạt.

### Exit ticket

- Điều rút ra: phải giữ mã lần chạy và hash code/config để biết kết quả thuộc bản nào; các lần chạy lại không đổi code không phải các thí nghiệm sửa mới.
- Điều còn chưa chắc: PASS-VISIBLE chưa chứng minh qua test ẩn, ngày đổi chính sách hoặc dữ liệu và tải thực tế khác mock.

## Kết quả chung và việc còn lại

| Mục | Trạng thái có bằng chứng |
|---|---|
| CP1–CP2 | Đủ 4 thành viên, có PRD/eval card, test công khai đạt; tiêu chí giữ nguyên và push trước lần đo sớm nhất còn nhật ký. Repo Public nhưng không phải fork, cần Coach xử lý. |
| CP3 | Có nội dung kỹ thuật và v1 Cải tiến thêm; bản khóa đầu bị revert rồi thay sau nhận S6. `a686572` bổ sung đối chiếu, không chốt lại hoặc sửa v1. Chưa xác nhận đạt thứ tự bắt buộc. |
| CP4 | `442180a`; grade `R-S6-grade-20261119-194303-8584c7`: PASS-VISIBLE, S6 60/60, base 110/110, 0 hoàn sai/ghi oan/PII, 0 ca ùn; hai monitor đạt. Test ẩn chưa chạy. |
| CP5 | V2 Dừng pilot tự động theo C12; ba câu và submission.json đồng bộ bốn thành viên. Hồ sơ nộp được gom bằng check_submission --collect; trạng thái kiểm cuối theo lệnh, không coi đủ thành phần là đủ điểm. |
| Cần người thực hiện | Dương trao đổi Coach về fork/bản chốt; nhóm trình bày demo và giải thích ngưỡng; từng thành viên nộp link LMS. Chưa có bằng chứng các thao tác này đã hoàn thành. |

Đây là báo cáo từ repo và kết quả mô phỏng. Không ghi đã gửi thông báo hãng, thu hồi khoản hoàn/phạt, ký triển khai hoặc chạy pilot với khách thật.
