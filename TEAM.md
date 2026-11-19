# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): Sunset
- Lớp: L3B
- Repo của bàn: K5-L3B-DAY10-Sunset-PoCtoPilotGate1
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |     Hà Phan Đại Dương      |   2A202604119   |  Sản phẩm và kinh doanh   |      Có       |
|   2 | Nguyễn Hữu An          | 2A202604024     | Kỹ sư cổng    | Không            |
|   3 |           |      |     |             |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.


## HaPhanDaiDuong-2A202604119

### Phần việc phụ trách

Sản phẩm và kinh doanh: CP3, câu 2.3 (Phiếu B/B3), câu 2.9 (B7.4), pre-mortem và quyết định v1. Dùng trợ lý AI hỗ trợ hoàn thiện toàn bộ Phiếu B và phần code/config cần cho checkpoint; không ghi các thành viên khác là đã thực hiện thao tác thay họ.

### Đóng góp cụ thể

Có sử dụng AI để đọc yêu cầu/dữ liệu/code của lab, soạn bản đồ dữ liệu và drift chính sách, giải thích ngân sách/ROI; chạy đo base, các bản cổng, prepared; hoàn thiện ba cổng, business/operations/legal, HAZOP, checklist, behavioral test và runbook. Quyết định v1 là **Cải tiến thêm**: mọi ngưỡng nền đạt nhưng chưa kiểm chứng đủ tải dồn, trần lỗi hãng/ngày và vận hành thật. Các ngưỡng và quyết định thuộc trách nhiệm của bàn, cần giải thích được khi demo.

### Bằng chứng

- Phiếu B: B0–B8 trong `templates/form-b-evaluation-gates.md`.
- Base `R-base-before-20261119-155543-b45eeb`: 20.000đ hoàn sai, 1 lỗi hãng oan.
- Prepared `R-base-prepared-20261119-155904-eae960`: 110/110 đạt, tác hại 0, chi phí 4.510đ/ticket, ROI 1,22, không ùn, không regression.
- Tiêu chí đã ký `69d355e4` (commit `1a3786d`), chốt vòng 1 `a1af532b`; 13 tests công khai OK; hai adhoc ở B7.3 đã chạy trước/sau.

### Exit ticket

Chưa điền; thành viên tự viết điều học được và điều còn chưa chắc sau khi đọc kết quả, thảo luận cùng bàn và hoàn tất buổi lab.
