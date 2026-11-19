# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Sunset
- Lớp: L3B
- Repo của bàn: K5-L3B-DAY10-Sunset-PoCtoPilotGate1
- Thẻ sự cố đã bốc (S1–S8): S6

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |     Hà Phan Đại Dương      |   2A202604119   |  Sản phẩm và kinh doanh   |      Có       |
|   2 | Nguyễn Hữu An          | 2A202604024     | Kỹ sư cổng    | Không            |
|   3 | Lê Bá Nguyên | 2A202604100 | Vận hành và pháp lý | Không |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenHuuAn-2A202604024

### Phần việc phụ trách

Em phụ trách vai Kỹ sư cổng. Em thiết kế phép đo offline ở câu 1.3, tham gia làm câu 1.5–1.6 của Phiếu A và bổ sung phần kỹ thuật ở Phiếu B: đo kết quả, đọc trace, phân tích lỗi, viết cổng và thử các ticket mới. File code chính em làm là `lab10/guards.py`; kết quả được ghi ở B0–B2, phần kỹ thuật B6 và B7.1–B7.3. Em cũng đưa PRD v1.1 và eval card của Lab 9 vào `docs/` để nhóm dùng làm tài liệu chung.

### Đóng góp cụ thể

- Ở Phiếu A, em thiết kế `policy_selection_accuracy` để kiểm tra agent có chọn đúng chính sách theo ngày hiệu lực hay không. Em tham gia đọc kết quả có khoảng tin cậy và viết tiêu chí chấp nhận trước khi nhóm ký.
- Em đối chiếu trace `T-002@55` với tracking và chính sách: đơn thực tế trễ 2 ngày nhưng agent dùng 5 ngày khách tự khai, dẫn tới hoàn sai 20.000đ và ghi oan hãng một lỗi. Em ghi lại bước sai đầu tiên và hai tác hại này trong Phiếu B. Với phép đo chọn chính sách, có 80/80 ca tới bước chọn chính sách dùng đúng phiên bản; 30 ca dừng sớm được thống kê riêng, không tính là chọn đúng.
- Em viết ba cổng trong `guards.py`: KT1 ghim chính sách đang hiệu lực; KT2 tính lại quyền lợi từ tracking trước khi hoàn tiền; KT3 kiểm đúng kiện, hãng, tài xế và căn cứ ghi lỗi trước khi ghi hoặc gửi thông báo cho hãng. Khi dữ kiện thiếu hoặc chưa xác định được đối tượng, cổng chuyển sang người xử lý.
- Em viết hai ticket mới để thử trường hợp khách khai quá số ngày trễ hoặc yêu cầu bỏ qua chính sách. Cả hai đều không phát sinh khoản hoàn, lỗi hãng hay thông báo hãng sai. Sau khi ghép bài, em chạy thêm hai ticket do bạn phụ trách đánh giá chuẩn bị.
- Em ghép ba cổng với phần `operations` và `legal` do bạn trong nhóm bổ sung rồi kiểm tra lại. Bộ nền đạt 110/110 lượt chạy, không có ca trước đúng nay hỏng; hoàn sai và lỗi hãng oan đều về 0, dữ liệu cá nhân bị lộ vẫn bằng 0. Chi phí là 4.202đ/ticket, ROI 1,38 và không có ca bị ùn. Kết quả kiểm tra 13 test công khai được ghi ở B7.1.

Ba cổng hiện tại được bổ sung sau khi nhóm nhận thẻ S6. Khi hoàn thiện CP3, em bổ sung số liệu bàn giao runbook, phép thử một/hai người duyệt và snapshot kỹ thuật `32d5efc2` lúc 2026-11-19T17:44:46 GMT+7. Bộ nền prepared vẫn đạt 110/110; nhóm ghi v1 là Cải tiến thêm. Em ghi rõ đây là bản chốt muộn, chưa có xác nhận Coach về điều kiện trước sự cố. Phần đánh giá S6 và monitor mới thuộc công việc tiếp theo; phần rà soát nhãn nghiệp vụ vẫn cần bạn Dương xác nhận trực tiếp.

Em dùng Codex để hỗ trợ đọc repo, đối chiếu trace và số liệu, soạn nội dung báo cáo, đề xuất ngưỡng cảnh báo có lý do và chạy các kiểm tra ghi ở hồ sơ CP3. Các ngưỡng/quy trình bổ sung là phương án cho bài mô phỏng, em cần giải thích được khi demo.

### Bằng chứng

| Nội dung | Bằng chứng |
|---|---|
| Đưa tài liệu Lab 9 vào repo | Commit `c314476`: `docs/PRD_v1.1.md`, `docs/eval_card.md` |
| Thiết kế phép đo và tham gia viết tiêu chí | Commit `734fb64`, `e8d3bb0`; Phiếu A mục A2–A4 |
| Đo chọn chính sách và phân tích lỗi | Commit `5cc3c6d`; Phiếu B mục B0–B2 |
| Ba cổng KT1–KT3 và behavioral test | Commit `632c0eb`; `lab10/guards.py`, Phiếu B phần kỹ thuật B6 và B7.1–B7.3 |
| Mốc base dùng để đối chiếu | `R-base-before-20261119-160603-b45eeb`; trace `T-002@55` |
| Kết quả sau khi ghép code và config của nhóm | `R-base-after-20261119-171327-6fd875`; report và trace trong `runs/`, số liệu ở B0 dòng 5 và B7.1 |

Bằng chứng bổ sung CP3: `docs/evidence/cp3-20261119/`, report `R-base-prepared-20261119-174446-6e5a09`, snapshot `32d5efc2` và `docs/cp3-report.md`.

### Exit ticket

**Điều em học được:** tỉ lệ đúng cao chưa đủ để quyết định cho chạy thử. Baseline đúng 109/110 lượt nhưng một lượt sai đã làm phát sinh tiền hoàn sai và ghi oan hãng. Em hiểu rõ hơn vì sao cần kiểm tra ngay trước lệnh ghi bằng dữ kiện từ tracking và chính sách, thay vì chỉ sửa cách model trả lời.

**Điều em còn chưa chắc:** các cổng hiện tại sẽ xử lý được đến đâu khi tracking ở nguồn đã sai hoặc lượng ca cần người duyệt dồn vào giờ cao điểm. Bộ nền đang xanh nhưng dữ liệu mock chưa đủ để kết luận về hai tình huống này; em cần kiểm chứng thêm qua S6 và các phép thử tiếp theo.
