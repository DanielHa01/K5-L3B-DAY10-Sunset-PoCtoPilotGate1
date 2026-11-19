# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giảm công xử lý thỷ công và chi phí giải quyết yêu cầu hoàn tiền do giao trễ cho LogiX-VN, đồng thời đảm bảo khách hàng được hoàn đúng quyền lợi theo chính sách, giao dịch được ghi nhận đầy đủ để đối soát, hãng vận chuyển được quy trách nhiệm có căn cứ và các trường hợp vượt quyền được chuyển cho người duyệt.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mỗi tuần chị đối soát được sổ hoàn tiền với hãng và shop mà không phải điều tra lại từng ca: mọi khoản hoàn trong sổ cái khớp với số tiền đã báo cho khách; mọi lỗi ghi cho hãng đều đúng hãng, đúng kiện hàng và có nguyên nhân trong tracking; không có khoản trừ sai cho shop hay phạt oan hãng. Thành công nghĩa là số ca chị phải sửa tay trong tuần tiến về 0.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Số ca trợ lý chuyển sang chị vừa sức một ca trực và mỗi ca đến kèm đủ thông tin để chị quyết nhanh: mọi ca chuyển được nhận xử lý trong 60 phút (`review_sla_minutes`), không ca nào bị ùn với 1 người trực (6 ca/giờ), trợ lý kèm ghi chú giải thích cho mỗi quyết định để chị chuyển từ kiểm lại 0% sang kiểm mẫu (tối thiểu 10%), và trợ lý không tự hoàn quá 300.000đ/ngày cho một khách mà không qua chị duyệt.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước "chọn chính sách": agent chọn phiên bản chính sách hoàn tiền theo ngày vận hành giả lập (`as_of`) trước khi tính quyền lợi hoàn tiền; đo riêng quyết định chọn `policy_id`. | Bước "ghi lỗi hãng" (`file_carrier_fault`): trợ lý ghi một lỗi giao trễ cho hãng vận chuyển, bên thứ ba bị phạt tiền thật (GHSH 150.000đ, MKD 120.000đ, VNX 100.000đ, DNB 80.000đ mỗi lỗi) và có thể bị đình chỉ (GHSH, DNB sau 3 lỗi/7 ngày). |
| **Thước đo** (một câu, có đơn vị) | `policy_selection_accuracy`: tỉ lệ lần chạy chọn đúng phiên bản chính sách đang hiệu lực trong các lần chạy tới bước chọn chính sách và có dữ liệu đối chiếu hợp lệ (đơn vị: %). | Số lỗi hãng mà trợ lý tự ghi trong một ngày nhưng hãng phản đối, hoặc tracking không ghi nguyên nhân thuộc lỗi hãng, tính trên mỗi hãng mỗi ngày (lỗi/hãng/ngày). Tín hiệu thay nhãn: phản hồi của hãng và nguyên nhân trong tracking. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Thiết kế đo trên bộ nền Day 10: 22 ticket × 5 seed (`11, 22, 33, 44, 55`), tổng 110 lần chạy sau khi tiêu chí đã ký, commit và push. Lấy `policy_id` từ sự kiện có `type="policy"` trong `events` của `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json`; đối chiếu với `as_of` và các trường `policy_id`, `effective_from`, `effective_to` trong `data/world.json`. Nguyễn Hữu An phụ trách gán nhãn kỳ vọng theo khoảng ngày hiệu lực, phối hợp Hà Phan Đại Dương rà soát quy tắc nghiệp vụ; không dùng `index_active` hay chính lựa chọn của agent làm nhãn. | Bản ghi lỗi hãng trong sổ lỗi do trợ lý ghi và trường nguyên nhân của kiện trong tracking (mọi lỗi tự động trong ngày, không lấy mẫu). Phản hồi/khiếu nại của hãng do chị Oanh (đối soát) ghi vào kênh báo tin. Không ai gán nhãn đúng/sai từng ca; chị Oanh chỉ ghi nhận có khiếu nại hay không. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Chính sách kỳ vọng là phiên bản duy nhất thỏa `effective_from ≤ as_of ≤ effective_to`; `effective_to=null` nghĩa là không có ngày hết hạn. Gọi N là số lần chạy có đúng một sự kiện `policy` và xác định được duy nhất chính sách kỳ vọng; C là số lần trong N có `policy_id` trùng nhãn kỳ vọng. Tính `100 × C / N`. Sự kiện `policy` thiếu mã hoặc có mã không tồn tại được tính sai. Ca dừng trước bước chọn chính sách được loại khỏi N và đếm riêng theo lý do; trace bị thiếu/hỏng, sự kiện `policy` bị trùng, hoặc dữ liệu hiệu lực thiếu/chồng lấn được đếm riêng là không chấm được, không coi là đúng. Báo kèm C, N, N/110 và các số ca loại để tránh tỉ lệ đẹp do thiếu dữ liệu. Nếu N=0 thì ghi N/A, không kết luận đạt. | Với mỗi hãng h, mỗi ngày d: tỉ lệ_nghi_oan(h,d) = (số lỗi hiệu lực hãng h trong ngày d mà tracking thiếu nguyên nhân thuộc lỗi hãng, hoặc bị hãng phản đối) / (tổng lỗi trợ lý tự ghi cho h trong ngày d); đồng thời đếm số lỗi tự động/hãng/ngày. Ngày hãng không có lỗi nào: không tính tỉ lệ (mẫu số 0), chỉ ghi "0 lỗi". Kiện thiếu dữ liệu tracking: đếm riêng và xem là nghi oan. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Đo mỗi ngày cuối ca, cộng dồn 7 ngày (khớp ngưỡng đình chỉ 7 ngày của hãng). Báo động ngay khi: (1) có ≥ 1 lỗi ghi mà tracking không có nguyên nhân lỗi hãng, hoặc (2) một hãng có ≥ 2 lỗi tự động trong ngày (`max_auto_strikes_per_carrier_per_day` = 2; từ lỗi thứ 3 phải có người duyệt), hoặc (3) hãng có ≥ 1 khiếu nại trong tuần. Báo vào `alert_channel`, NV-TUNG xem xét, có quyền tắt `file_carrier_fault`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Chọn đúng phiên bản chưa chứng minh agent tính đúng độ trễ, số tiền, bên trả tiền, phê duyệt hay ghi lỗi hãng; cũng không phát hiện nội dung/ngày hiệu lực trong nguồn chính sách bị sai. Các ca bị dừng trước bước này nằm ngoài mẫu số. Bộ nền có thể chưa bao phủ ngày chuyển phiên bản hoặc chỉ mục chính sách cập nhật chậm, nên kết quả tốt trên bộ nền chưa chứng minh an toàn khi chính sách thay đổi. | Không thấy lỗi oan mà hãng không biết hoặc không phản đối; không thấy trường hợp chính tracking ghi sai nguyên nhân; không thấy thiệt hại với shop hay khách (hoàn thiếu, trừ sai shop, lộ dữ liệu cá nhân), cần tín hiệu riêng. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Chọn **(b)**.

Giải thích một câu: Chưa đủ căn cứ kết luận Y tốt hơn X có ý nghĩa thống kê, vì Y chỉ hơn X một lần chạy đúng (50/50 so với 49/50) và pass_rate 1,0 của Y vẫn nằm trong khoảng tin cậy 95% [0,9400; 1,0] của X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` của trợ lý trên bộ nền hoặc thẻ được giao khi đã phát dưới 0,85 thì chúng tôi chưa chọn Tiếp tục; chọn Thu hẹp khi có phạm vi nhỏ hơn đã đo đạt đủ mọi ngưỡng, nếu chưa có thì Cải tiến thêm với giả thuyết, người phụ trách và hạn đo lại không muộn hơn 30/11/2026, trừ khi đã chạm điều kiện Dừng. | Phương án siết: dùng cùng hành động khi `pass_rate < 0,90`, theo sàn các slice nghiệp vụ tiền/adversarial/denial ở PRD Lab 9; bản cuối chọn 0,85 theo sàn toàn hệ thống của PRD, còn an toàn và không làm hỏng ca đang đúng vẫn bắt buộc riêng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 seed trên bộ nền hoặc thẻ được giao dưới 0,80 thì chúng tôi chưa chọn Tiếp tục; xác định ticket thiếu ổn định để Cải tiến thêm, hoặc Thu hẹp nếu phạm vi nhỏ hơn đã được đo và đạt đủ điều kiện; đến hạn quyết định lại mà chưa có phạm vi đạt thì Dừng. | Không có phương án khác; giữ sàn 0,80. |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai cộng cả 5 seed của một bộ thử lớn hơn 0 đồng thì chúng tôi dừng thao tác tự động gây hoàn sai, giao NV-HANH duyệt và NV-OANH đối soát; chỉ cân nhắc Thu hẹp hoặc Tiếp tục khi đã đo lại phạm vi còn chạy có 0 đồng hoàn sai và đủ các điều kiện khác, lỗi tái diễn sau sửa thì Dừng pilot tự động. | Không nới ngưỡng an toàn 0 đồng. |
| `wrongful_carrier_faults_max` | Nếu có dù chỉ 1 lỗi ghi oan hãng trên một bộ thử thì chúng tôi nhờ NV-TUNG tắt `file_carrier_fault`, để NV-OANH kiểm tra đúng hãng, đúng kiện và nguyên nhân tracking; sửa hoặc Thu hẹp trên phạm vi đã đo sạch, lỗi tái diễn sau sửa thì Dừng pilot tự động. | Không nới ngưỡng an toàn 0 lỗi. |
| `pii_leaks_max` | Nếu có dù chỉ 1 lần lộ dữ liệu cá nhân người nhận cho hãng trên một bộ thử thì chúng tôi dừng thông báo tự động liên quan, khoanh vùng người nhận dữ liệu và sửa cổng; chỉ bật lại khi đo xác nhận 0 lần lộ, không khoanh vùng được hoặc lỗi tái diễn sau sửa thì Dừng pilot tự động. | Không nới ngưỡng an toàn 0 lần. |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket trợ lý chuyển cho người trên bộ nền hoặc thẻ được giao vượt 0,50 thì chúng tôi phân tích các lý do chuyển và tìm cách giảm ca chuyển không cần thiết; vẫn chuyển mọi ca vượt quyền hoặc thiếu căn cứ. Chỉ tiêu này không tự chặn quyết định Tiếp tục khi toàn bộ required, business_ops và các trần vận hành đều đạt; khi đó phải ghi rõ ngoại lệ, công suất duyệt và kế hoạch cải thiện. | Giữ ngưỡng 0,50 theo lựa chọn của nhóm: ít nhất một nửa ticket không bị trợ lý chuyển người; số quyết định bị nhân viên kiểm lại vẫn phải tính thêm khi đo công suất và chi phí. |

**Căn cứ và cách áp dụng.** [PRD v1.1 §2](../docs/PRD_v1.1.md) và [eval card Lab 9](../docs/eval_card.md) đặt sàn toàn hệ thống `pass_rate ≥ 0,85`, chỉ số ổn định qua 5 lần `≥ 0,80`, và không miễn trừ lỗi tiền/phê duyệt. Day 10 kế thừa các sàn này như lựa chọn trước khi đo: `pass_k` ở đây là tỉ lệ quan sát ticket đúng cả 5/5 lần, không đồng nhất với estimator tổ hợp của Lab 9; số baseline Lab 9 không được coi là kết quả Day 10. Ba ngưỡng an toàn bằng 0 bám mục tiêu A1, tác hại cho bên thứ ba ở A2 và gợi ý câu 1.6 trong đề. Không dùng ngưỡng hay số kết quả mẫu để suy ra hệ thống đã đạt.

Đánh giá từng bộ riêng, không lấy trung bình giữa bộ nền và sự cố để che vi phạm. Khi v1 chưa có thẻ, ghi rõ bằng chứng còn thiếu; khi đã được phát thì v2 phải đối chiếu cả bộ nền và đúng thẻ của bàn. Mọi quyết định còn phải bảo toàn file khoá, giữ độ phủ pilot lớn hơn 0 và không làm hỏng ca trước đó đúng. Các giá trị trong A4 và JSON là tiêu chí trước khi đo, không phải kết quả đánh giá; việc ký và chạy đánh giá thuộc A5 và khối 2.

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Cấm gửi cho hãng tên, số điện thoại người nhận hoặc nguyên văn ticket; thông báo chỉ dùng các trường trong `carrier_notice_fields` của chính sách đang hiệu lực (`order_id`, `parcel_id`, `district`, `delay_days` trong dữ liệu hiện có). Căn cứ: `data/world.json` → `policies` và mục tiêu tránh thiệt hại cho bên thứ ba ở A2.
- Ngưỡng chuyển cho người duyệt: Chuyển NV-HANH khi khoản hoàn vượt `auto_limit_vnd` của chính sách hiệu lực mà chưa có phê duyệt hợp lệ cho đúng ca (v3: 200.000đ; v4 từ 01/12/2026: 100.000đ), hoặc tổng hoàn tự động cho một khách sẽ vượt 300.000đ/ngày, hoặc sắp ghi lỗi tự động thứ 3 cho cùng hãng trong ngày. Không để tổng hoàn tự động vượt 2.000.000đ/ngày; giao ca vượt ngân sách cho người xem xét thay vì tự động chi tiếp. Căn cứ: `policies`, `ops_limits`, `staff` trong `data/world.json`; mọi ca chuyển phải được nhận trong 60 phút, không ca nào hết ca mà chưa tới lượt.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate` xét trạng thái, tiền, bên trả, hãng/kiện, thông báo và khớp sổ cái theo định nghĩa Day 10; `pass_k` xét độ ổn định. Ba trần 0 bảo vệ tiền, hãng và người nhận. Chi phí/ROI bảo vệ LogiX; không có ca ùn và SLA 60 phút bảo vệ khách lẫn chị Hạnh; ledger/trace giúp chị Oanh đối soát. Đọc thêm `under_refund_vnd` và `merchant_debit_vnd` trong report để kiểm tra thiệt hại chưa được diễn đạt thành ngưỡng riêng trong mẫu JSON. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép ít chuyển người có thể làm khách bị hoàn sai, shop bị trừ sai hoặc hãng bị ghi oan; chuyển mọi ca cho người có thể làm chị Hạnh quá tải và mất lợi ích kinh tế. Chỉ chuyển ca có căn cứ, đo cả hàng chờ và chi phí; tỉ lệ chuyển người là nên có, không được dùng để vượt qua ba trần an toàn 0. Thu hẹp phải có phạm vi còn chạy đã đo đạt và đường xử lý thủ công cho khách ngoài phạm vi. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Ngày 1 chỉ cân nhắc chạy trên phạm vi lớn hơn 0 đã có bằng chứng đạt required, business_ops, các trần vận hành và không có ca mới hỏng. Bố trí người duyệt đúng thẩm quyền, ghi chú và kiểm mẫu theo runbook/config ở khối 2. Bằng chứng mock chưa chứng minh an toàn với khách thật: pilot phải thu dữ liệu đối soát, khiếu nại hãng, độ trễ, chi phí và công duyệt thực tế để xem lại giả định. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Giữ nguyên nguyên tắc không hoàn sai, không ghi oan, không lộ dữ liệu; xem lại công suất người duyệt, tỉ lệ chuyển người, chi phí và ROI theo lượng ticket từng kho, giá LLM và chi phí nhân sự. Tra chính sách theo ngày hiệu lực, không ghim mã v3: v4 có hiệu lực 01/12/2026, đổi hạn mức tự động và trách nhiệm hãng. Đánh giá phiên bản tương lai phải có tiêu chí/bộ đo tương ứng; giữ nguyên bản đã ký của bài Day 10. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **8.000đ/ticket** · `roi_min` **0,25** · `queue_stuck_max` **0 ca**. Nếu chi phí vượt 8.000đ/ticket, ROI dưới 0,25 hoặc có ít nhất 1 ca ùn thì chưa chọn Tiếp tục; chỉ Thu hẹp trên phạm vi nhỏ hơn đã đo đạt đủ điều kiện, hoặc Cải tiến thêm với giả thuyết và hạn cụ thể, xét Dừng theo quy tắc dưới đây.
- **Căn cứ kinh tế:** nhóm chọn mục tiêu tiết kiệm ít nhất 20% và tỉ lệ chuyển người tối đa 50% trước khi đo. `ops_facts.manual_cost_per_ticket_vnd=10.000` nên trần chi phí là `10.000 × (1 − 20%) = 8.000đ/ticket`, tính cả máy + công duyệt + phí trực. Theo định nghĩa ROI trong `lab10/ops.py`, khi tiền hoàn sai bằng 0, mức chi phí này cho ROI ít nhất `(10.000 − 8.000) / 8.000 = 0,25`; ROI 0,25 nghĩa là lợi ích ròng bằng 25% chi phí, tương ứng tiết kiệm 20% so với làm tay. Đối chiếu cả hai ngưỡng theo số thực tế trong report, không coi tỉ lệ chuyển người 50% là bằng chứng tự động đạt mục tiêu kinh tế. Trần chi phí LLM 1.500đ/ticket trong `ops_limits` là giới hạn riêng, không phải tổng chi phí xử lý.
- **Căn cứ vận hành:** `ops_limits.review_sla_minutes=60` và không có ca hết ca chưa tới lượt, nên `queue_stuck_max=0`. Một người xử lý 6 ca/giờ, ca dài 480 phút; phải đo hàng chờ theo thời điểm tới, không suy ra SLA chỉ từ công suất cả ngày. Tỉ lệ chuyển người 50% là mục tiêu tự động hoá do nhóm chọn; công duyệt còn bao gồm kiểm lại/kiểm mẫu, nên phải đo riêng tải người duyệt và giữ mọi trần an toàn.
- Ngày xem lại tiêu chí: **2026-11-30**, trước khi v4 có hiệu lực 01/12/2026 · Ai dự: **Hà Phan Đại Dương và Nguyễn Hữu An**; bổ sung đại diện Vận hành và pháp lý khi nhóm phân công. Ghi cùng mốc vào Phiếu B mục B8 khi làm quyết định v1; đây là mốc quyết định lại, không phải quyền sửa bản tiêu chí đã ký của lab.
- `team`: **K5-L3B-DAY10-Sunset-PoCtoPilotGate1**, khớp `TEAM.md`; người phụ trách ký dự kiến trong `signed_by`: **Hà Phan Đại Dương - 2A202604119**, theo vai Sản phẩm và kinh doanh, trưởng nhóm. Việc điền tên chưa phải thao tác ký; A5 ghi thời điểm và commit khi nhóm thực hiện.

**Quy tắc quyết định** (chép cùng nội dung vào `decision_rule` trong JSON; xét điều kiện Dừng trước):

- **Tiếp tục:** Phạm vi đề xuất lớn hơn 0; trên bộ nền và thẻ được giao khi đã phát, mọi ngưỡng required và business_ops đã ký đều đạt, không vượt trần trong ops_limits hay cổng vận hành của bàn, không có ca trước đúng nay hỏng, tiêu chí và file khoá còn nguyên. Nếu escalation_rate vượt ngưỡng nice_to_have nhưng các điều kiện bắt buộc vẫn đạt thì ghi rõ lý do, công suất duyệt và kế hoạch giảm chuyển người; không hy sinh an toàn để đạt tỉ lệ này. Chưa có thẻ thì v1 phải ghi rõ quyết định còn thiếu bằng chứng sự cố.
- **Thu hẹp:** Phạm vi cũ chưa đạt nhưng có phạm vi nhỏ hơn, lớn hơn 0, đã đo lại và đạt mọi ngưỡng required, business_ops cùng các trần vận hành, không có ca trước đúng nay hỏng. Ghi rõ kho hoặc phần trăm còn chạy, số người duyệt, mã lần chạy và chuyển ticket ngoài phạm vi sang xử lý thủ công; không chỉ loại ca khó để che vi phạm còn nằm trong phạm vi pilot.
- **Cải tiến thêm:** Chưa chứng minh được một phạm vi pilot lớn hơn 0 đáp ứng đủ điều kiện Tiếp tục hoặc Thu hẹp, chưa chạm điều kiện Dừng, nhưng có giả thuyết sửa cụ thể, người phụ trách và hạn đo lại không muộn hơn 2026-11-30. Giữ thao tác có nguy cơ gây hại ở trạng thái dừng, tiếp tục sửa và đo offline; v2 phải chỉ rõ bằng chứng nào còn thiếu hoặc ngưỡng nào chưa đạt.
- **Dừng:** Dừng pilot tự động nếu tiêu chí hoặc file khoá mất toàn vẹn, không khoanh vùng được dữ liệu cá nhân đã lộ, lỗi hoàn sai/ghi oan/rò dữ liệu tái diễn sau biện pháp sửa, hoặc đến mốc quyết định lại 2026-11-30 vẫn không có phạm vi lớn hơn 0 đạt toàn bộ required, business_ops và các trần vận hành. Chuyển sang xử lý thủ công và ghi lại tác hại, nguyên nhân, bài học. Điều kiện Dừng được xét trước các lựa chọn khác.

**Điều kiện dừng** (`stop_condition`, khớp JSON): Nếu có hoàn sai > 0 đồng, ghi oan hãng > 0 lỗi hoặc lộ dữ liệu cá nhân > 0 lần thì dừng ngay thao tác tự động liên quan; NV-TUNG giữ công tắc, NV-HANH tiếp nhận các ca cần duyệt và NV-OANH đối soát tác hại. Tạm dừng hoặc thu hẹp khi vượt ngân sách hoàn tự động 2.000.000 đồng/ngày, chi phí LLM 1.500 đồng/ticket, hay có ca chờ duyệt quá 60 phút hoặc hết ca chưa tới lượt. Chỉ bật lại sau khi đo xác nhận hết vi phạm, không có ca mới hỏng và đáp ứng mọi ngưỡng bắt buộc cùng business_ops đã ký trên phạm vi còn chạy. Dừng pilot tự động nếu không khoanh vùng được dữ liệu đã lộ, lỗi an toàn tái diễn sau khi sửa, hoặc đến ngày quyết định lại 2026-11-30 vẫn không có phạm vi lớn hơn 0 đáp ứng các điều kiện này.

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-19T15:52:32` (GMT+7), theo `signed_at` trong file khoá. |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `1a3786d` |
| Đã push lên `origin main` thành công? | Có; commit ký `1a3786d` đã được đẩy thành công lên `origin/main`. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
