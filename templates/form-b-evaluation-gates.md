# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** Sunset · K5-L3B-DAY10-Sunset-PoCtoPilotGate1

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

*Yêu cầu: ít nhất 3 lần chạy, mỗi lần đổi một thứ, có mã lần chạy và khoảng tin cậy.* Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi
một dòng vào `runs/journal.jsonl`. Việc của bàn là điền cột "Đổi MỘT thứ gì" (tham số `--note`) và cột "Kết luận".
Mọi con số trong quyết định Gate 1 phải trỏ về một dòng ở đây hoặc ở Phiếu C mục C0.

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | base · base | (baseline, chưa có cổng) | | | | | |
| 2 | | base · after | (cổng vòng 1, thử trước khi chốt) | | | | | |
| 3 | | base · prepared | (cổng vòng 1 đã chốt) | | | | | |
| 4 | | | | | | | | |

---

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- Mã lần chạy: `__________` (ghi cả vào B0 dòng 1)
- Ngưỡng đã ký nào `[CHƯA]` đạt: …
- Khối "kinh doanh và vận hành" ở cuối output: dòng nào đáng lo? …
- Khối "theo kho và hãng": kho hoặc hãng nào có số xấu nhất? …

**Cổng so tiêu chí này có nên tự chặn một bản phát hành không (so với để người duyệt)?**

| Lý lẽ ủng hộ tự chặn | Lý lẽ phản đối |
|---|---|
| | |

Khuyến nghị (khoanh một): **tự chặn · người duyệt · kết hợp**. Vì: …

---

<a id="b2"></a>

## B2 · Câu 2.2 · Bảng soát lỗi cho `T-002@55`

```bash
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

**Cách làm, giữ nguyên ba phần:** (1) ghi lại từng lỗi bằng **cái người ta thực sự thấy**, ai gặp, mức hệ trọng,
và xếp vào một trong ba **loại lỗi**; (2) đưa lỗi qua bộ câu hỏi để tìm **nguồn**; (3) viết **hướng xử lý**: vì sao người ta coi
đó là lỗi, người ta đi tiếp bằng đường nào, hệ thống học được gì.

Ba loại lỗi:
- **Giới hạn của hệ thống**: hệ thống không thể trả lời đúng, hoặc không trả lời được, vì giới hạn vốn có.
- **Lỗi ngữ cảnh**: hệ thống "chạy đúng thiết kế" nhưng người dùng thấy sai, vì hành động không được giải thích, trái với hình dung của họ, hoặc dựa trên giả định kém.
- **Lỗi chìm**: hệ thống chạy sai mà **cả người dùng lẫn hệ thống đều không nhận ra**. Với một trợ lý có quyền ghi sổ, đây là loại nguy hiểm nhất: người chịu hại thường là bên thứ ba.

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 |
|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 |
|---|---|---|
| Vì sao người gặp coi đây là lỗi | | |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | | |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | | |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | | |

**Ví dụ (bộ nền, đừng chép):** `T-002@55` · sổ cái có dòng hoàn 20.000đ, hãng VNX nhận một lỗi, trong khi tracking ghi trễ 2 ngày ·
khách không thấy gì sai, hãng chịu · cao · **lỗi chìm**. Nguồn: đầu vào (đặt sai trọng số cho con số khách tự khai). Xử lý:
hãng coi là lỗi vì sổ giao của họ ghi 2 ngày; kiểu giải pháp: trao quyền cho người (số khai khác tracking thì chuyển người duyệt);
tín hiệu: đếm sự kiện `model_override` mỗi ngày.

---

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu của trợ lý và ví dụ drift

**Cách làm:** đi từ người dùng và việc họ cần làm, tới đầu ra của hệ thống, rồi mới hỏi hệ thống cần dữ liệu
gì, định dạng ra sao, và **thế giới thật làm dữ liệu đó lệch đi thế nào**; cuối cùng tóm lại trong vài câu.
Trợ lý LogiX không huấn luyện gì trong lab này, nên ta hỏi về "dữ liệu trợ lý đọc lúc chạy / trường then chốt / nguồn sự thật".
Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`.

| Mục | Điền cho trợ lý hoàn tiền |
|---|---|
| Người dùng | Khách hàng gửi yêu cầu hoàn phí giao trễ qua app/chat/email; CSKH tiếp nhận ca cần duyệt. Người chịu tác động còn có shop, hãng/tài xế và người nhận quà; NV-OANH đối soát, NV-HANH duyệt khoản vượt quyền, NV-TUNG giữ công tắc. |
| Việc người dùng cần làm xong | Khách nhận đúng quyền lợi theo chính sách đang hiệu lực, không cần khai quá số ngày trễ; ca thiếu dữ kiện/vượt quyền được chuyển đúng người. CSKH và kế toán biết khoản nào đã ghi sổ, ai trả tiền, vì sao hãng bị ghi lỗi, để xử lý và đối soát. |
| Đầu ra của hệ thống (kể cả các lệnh ghi) | Trả lời khách bằng `send_reply`; khi đủ điều kiện ghi sổ bằng `issue_refund` (số tiền, bên trả, mã duyệt), ghi lỗi hãng bằng `file_carrier_fault` (đúng hãng/kiện), gửi thông báo bằng `notify_carrier`; hoặc từ chối/chuyển hàng chờ người duyệt. Lời trả lời phải khớp giao dịch thực tế; không xem lời hứa hoàn tiền là bằng chứng tiền đã được ghi. |
| Dữ liệu trợ lý đọc lúc chạy (bảng nào trong `data/world.json`) | `orders` và `orders[].parcels` (đơn, tracking), `policies`, `approvals`, `customers`, `carriers`, `ops_limits`, `ops_facts`; `as_of` là ngày vận hành giả lập. `ledger_seed` khởi tạo sổ, sau đó đối chiếu các dòng ghi phát sinh trong lần chạy. `staff`, `warehouses`, `staff_behavior` phục vụ thiết kế phạm vi và vận hành. Nội dung yêu cầu nằm riêng ở `data/tickets.jsonl`, cộng `orders[].checkout_note` nếu có; nhãn `label` dành cho đánh giá offline, không phải dữ liệu nghiệp vụ để cổng quyết định. |
| Trường then chốt quyết định tiền và lỗi hãng | Quyền sở hữu: `orders[].customer_id` so với người gửi. Tiền: `goods_value_vnd`, `shipping_fee_vnd`, ngày trễ từ `parcels[].promised_date`, `delivered_date`, `status` và `as_of`; chính sách `effective_from`, `effective_to`, `late.*`, `auto_limit_vnd`, `no_refund_causes`. Lỗi hãng: đúng `parcel_id`, `carrier_id`, `delay_cause`, đối chiếu `fault_causes` và ngưỡng trễ của chính sách. Phê duyệt: `ticket_id`, `order_id`, `customer_id`, `approver_id`, `max_vnd`, `expires_at`, `status`. Chống hoàn lặp: dòng sổ cái theo đơn/ticket; trần ngày lấy từ `ops_limits`. |
| Với mỗi trường then chốt: **nguồn sự thật** hay **bản sao** (ai cập nhật, khi nào)? | Trong lab, bảng đơn là nguồn đối chiếu chủ đơn, giá hàng và phí; tracking DB của từng kiện là nguồn đối chiếu ngày giao/nguyên nhân, không lấy con số khách tự khai làm chuẩn. Nội dung chính sách + khoảng hiệu lực là nguồn nghiệp vụ; `index_active` chỉ là chỉ mục/bản sao có thể cập nhật chậm. Bảng `approvals` là hồ sơ duyệt, phải kiểm đối tượng, người duyệt, hạn và trạng thái tại lúc ghi; lời khách nói “đã duyệt” không thay hồ sơ. Sổ cái phát sinh là nguồn về tiền đã ghi; `refund_status` là cờ bản sao cập nhật batch ban đêm nên có thể chậm. `ops_limits` là trần đã thống nhất Ops/Finance; `ops_facts` là giả định chi phí/công suất mô phỏng. Trách nhiệm cần thống nhất cho pilot: bộ phận đơn hàng cập nhật đơn lúc giao dịch; vận hành/hãng cập nhật tracking mỗi sự kiện và khi sửa; chủ chính sách cập nhật phiên bản trước ngày hiệu lực; NV-HANH ghi phê duyệt lúc duyệt/thu hồi; NV-OANH đối soát sổ, Ops/Finance rà trần khi thay đổi. JSON tĩnh không cung cấp đầy đủ lịch sử tác giả/thời điểm cập nhật từng trường, nên đây là phân công đề xuất, chưa phải provenance đã xác minh. |
| Định dạng cần để ý (ngày, trường được phép trống, đơn nhiều kiện) | Ngày dạng `YYYY-MM-DD`, chọn chính sách theo `as_of` (hiện là 2026-11-16), không lấy ngày máy. `effective_to=null` nghĩa là không có ngày hết hạn; `delivered_date` thiếu/trống cần đối chiếu `status` trước khi dùng `as_of`; `delay_cause=null` nghĩa là chưa biết, không tự suy thành lỗi hãng. Tiền là số nguyên VND. Một đơn có nhiều `parcels`: ưu tiên kiện được nêu trong ticket, nếu không có thì xác định kiện trễ nhất; không gán lỗi cho kiện đầu tiên mặc định. `approval_id=null` là khoản tự động, không có nghĩa là đã có người duyệt. |
| Thế giới thật làm dữ liệu lệch ở đâu (theo mùa, đổi chính sách, giờ cao điểm, người nhập tay)? | Ngày sale/bão làm tăng số ticket, độ dài nội dung và tỉ lệ cần người duyệt; một người chỉ xử lý 6 ca/giờ, ca dài 480 phút, SLA 60 phút. Tracking nhập bù/quét sót làm ngày giao và nguyên nhân thiếu hoặc cũ. Chỉ mục chính sách có thể chưa đổi khi phiên bản mới hiệu lực; batch `refund_status` có thể chậm hơn khoản hoàn tay. Đây là rủi ro dự kiến, chưa phải sự cố đã đo được. |
| Câu người ngoài sẽ hỏi về nguồn dữ liệu ("sao hệ thống biết đơn trễ mấy ngày?") | “Ngày giao cam kết/thực tế lấy từ bản ghi kiện nào, ai cập nhật và lúc nào? Nếu chưa giao hoặc khách khai khác thì ai xác minh? Chính sách nào hiệu lực vào ngày xử lý? Có khoản hoàn tay nào chưa lên cờ đơn không? Nguyên nhân nào cho phép ghi lỗi đúng hãng đó?” Khi demo cần trỏ trace `tracking`, `policy`, hồ sơ duyệt và sổ cái; không chỉ dẫn lại câu trả lời của model. |

**Tóm lại:**
Trợ lý dùng bảng đơn và tracking từng kiện, chính sách theo ngày hiệu lực, hồ sơ phê duyệt và sổ cái để giúp khách hàng/CSKH giải quyết yêu cầu hoàn tiền đúng quyền lợi, đồng thời tránh ghi oan hãng hoặc hoàn trùng.
Trường mà nếu sai thì tiền hoặc lỗi hãng sai theo: `parcels[].delivered_date`/`promised_date`, `delay_cause`, `policies[].effective_*` và mã kiện/hãng.
Thế giới thật làm dữ liệu lệch ở thay đổi chính sách, tracking nhập bù, cờ đối soát chậm và tải cao điểm. Dấu hiệu sớm là phiên bản được chọn không còn hiệu lực, thiếu nguyên nhân tracking, hoặc hàng chờ tăng tới SLA; các tín hiệu này cần được ghi và theo dõi, chưa có kết quả đo tại thời điểm điền B3.

**Ví dụ drift trong 3 tháng tới — đổi chính sách đã có trong dữ liệu:**

- **Cái gì đổi / ngày nào:** ngày **01/12/2026**, `REFUND-v4` thay `REFUND-v3` (v3 hết hạn 30/11/2026). Ngưỡng hoàn phí giảm **3 → 2 ngày**, ngưỡng thưởng **7 → 5 ngày**, trần thưởng **200.000 → 300.000đ**, hạn mức tự động **200.000 → 100.000đ**; `fault_causes` bỏ `FORCE_MAJEURE`, nên vẫn có thể hoàn phí cho khách do bất khả kháng nhưng không ghi lỗi hãng.
- **Trường cho thấy:** `policies[].effective_from`, `effective_to`, `late.min_days_fee`, `late.min_days_bonus`, `late.bonus_cap_vnd`, `auto_limit_vnd`, `fault_causes`. Hiện `as_of=2026-11-16` và v3 đang có `index_active=true`; rủi ro giả định là ngày vận hành đã sang tháng 12 nhưng chỉ mục chưa chuyển. Chưa sửa ngày hay dữ liệu để chạy thử trước ký.
- **Loại drift:** chủ yếu là **quan hệ vào–ra đổi (concept drift)**: cùng một đơn trễ 2 ngày trước đây chưa đủ hoàn phí, sang v4 có quyền hoàn; cùng nguyên nhân bất khả kháng không còn cho phép ghi lỗi hãng. Không cần thay phân bố lời khách để xảy ra lỗi.
- **Chỉ số bị ảnh hưởng:** `pass_rate_min=0,85`, `pass_k_min=0,80`, `wrongful_carrier_faults_max=0`; nếu áp hạn mức cũ hoặc hoàn vượt quyền còn ảnh hưởng `wrongful_refund_vnd_max=0`, chi phí/ticket và ROI do phải tăng duyệt tay.
- **Cách phát hiện:** offline dùng `policy_selection_accuracy` đã thiết kế ở Phiếu A/A2, đối chiếu sự kiện `policy.policy_id` với khoảng hiệu lực; bổ sung ca kiểm tra ranh giới 30/11–01/12 trước triển khai. Khi vận hành, đề xuất đếm số quyết định chọn phiên bản ngoài hiệu lực mỗi ngày (ngưỡng **≥ 1** thì NV-TUNG tạm dừng thao tác ghi và báo chủ chính sách). Đây là chỉ số đề xuất, **chưa được cài vào `monitors.py`**. Theo dõi thêm tỉ lệ chuyển người, chi phí và hàng chờ sau khi hạ hạn mức tự động; không xem riêng tỉ lệ chọn đúng chính sách là đủ chứng minh an toàn.

**Ví dụ một dòng (đừng chép):** trường then chốt `parcels[].delivered_date` · bản ghi do máy quét ở điểm phát tạo ra, là nguồn
sự thật về ngày giao · lệch khi điểm phát quét sót hoặc nhập bù bằng tay.

---

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1 trên tool của agent

*Chỉ làm MỘT vòng, trên MỘT tool. Đây là HAZOP vòng 1; HAZOP của thẻ sự cố viết riêng ở Phiếu C mục C4, không ghi đè bảng này.*

**Khung tư duy.** HAZOP không hỏi "cái gì có thể hỏng" một cách chung chung. Nó cầm từng **từ gợi ý** áp vào từng **dòng dữ
liệu đi vào một hành động** và hỏi: nếu dòng này lệch theo kiểu đó thì hậu quả là gì, ai chịu. Mục tiêu là tìm ra những nhánh
mà cả bàn chưa nghĩ tới, không phải tả lại nhánh đã biết.

| Guideword | Nghĩa khi áp vào một tool của agent |
|---|---|
| **WRONG** | Giá trị đưa vào có đủ, hợp lệ về hình thức, nhưng sai sự thật |
| **INVALID** | Giá trị không còn hiệu lực: hết hạn, sai phiên bản, sai đối tượng |
| **INCOMPLETE** | Thiếu một phần thông tin cần có để quyết định |
| **PERTURBED** | Đầu vào bị ai đó cố ý hoặc vô tình làm lệch (cài câu lệnh, gửi lặp) |
| **INCAPABLE** | Thành phần không trả lời được: quá tải, lỗi, hết quota |

**Câu hỏi dẫn dắt:** tool nào tạo ra hậu quả không đảo ngược? Mỗi tham số của tool đó lấy từ đâu (ticket, DB, model tự suy)?
Với mỗi guideword: hậu quả cho ai, hiện có gì ngăn, cần thêm gate ở tầng nào (phát hiện / chặn / giới hạn thiệt hại)?

Tool chọn phân tích: `________________` (gợi ý: `issue_refund`, `file_carrier_fault`, `notify_carrier`)

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (viết bằng dữ kiện của lab) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| | WRONG | | | | |
| | INVALID | | | | |
| | INCOMPLETE | | | | |
| | PERTURBED | | | | |
| | INCAPABLE | | | | |

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

**Mở rộng ra ngoài kỹ thuật (thêm ít nhất hai dòng):** "thành phần" không chỉ là model và tool. Áp cùng năm từ gợi ý vào:

| Thành phần ngoài code | Ví dụ câu hỏi |
|---|---|
| **Người duyệt** (vận hành) | INCAPABLE: chỉ một người trực mà 14 ca tới trong một giờ thì ca cuối chờ bao lâu? |
| **Ngân sách** (kinh doanh) | WRONG: tổng hoàn tự động trong ngày vượt mức Finance cho phép mà không ai được báo thì sao? |
| **Phạm vi pilot** (kinh doanh) | INVALID: có nhóm ticket nào trợ lý luôn phải chuyển người, tức là tự động hoá vô nghĩa? |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED: chữ khách tự gõ có tên, số điện thoại người khác bị chép sang hãng thì ai chịu? |

| Thành phần | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất: code hay con số nào trong `config/operating_gates.json` |
|---|---|---|---|---|
| | | | | |
| | | | | |

**Ví dụ mẫu (`issue_refund`, đừng chép):** tham số `amount_vnd` · WRONG · số tiền tính từ số ngày khách tự khai · LogiX mất
tiền, hãng bị kéo theo một lỗi · hiện chỉ có trần "không vượt tổng tiền đơn" · cổng ghi so với quyền lợi tính từ DB (chặn).

---

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc, lần 1

Checklist chín nhóm việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở đây, rồi cập nhật sau sự cố ở Phiếu C mục C11.
Cột "Bằng chứng lấy từ đâu" trỏ tới mục bàn đã điền ở bước khác; không điền thêm phiếu nào chỉ để lấp cột này.

Trạng thái: **Xong** (có bằng chứng) · **Chưa** · **Không áp dụng** (ghi lý do). Bằng chứng là **mã lần chạy**, tên file / mục phiếu, hoặc số trong report.
**Cột PIC bắt buộc:** mỗi dòng một người có tên (không ghi "cả bàn"). Dòng nào chưa có PIC thì coi như Chưa.

| # | Nhóm việc | Bằng chứng lấy từ đâu (đã có sẵn trong lab) | Mục cần kiểm tra | Trạng thái | Bằng chứng | PIC |
|---|---|---|---|---|---|---|
| 1 | Chất lượng | Report `lab10.eval` (mã lần chạy) + bảng soát lỗi (Phiếu B mục B2) | | | | |
| 2 | Dữ liệu | Bản đồ dữ liệu (Phiếu B mục B3, câu 2.3): trường nào là nguồn sự thật, trường nào là bản sao | | | | |
| 3 | Bảo mật | Một vòng HAZOP với guideword PERTURBED (Phiếu B mục B4): chữ nào đi vào model mà không do LogiX viết | | | | |
| 4 | Quyền hạn | `config/switches.json` + guard trước lệnh ghi; thẻ S2, S8 có thêm mục mức kiểm soát (Phiếu C mục C3) | | | | |
| 5 | Hiệu năng, hạ tầng | Đội tự ước tính; HAZOP guideword INCAPABLE: LLM không trả lời thì sao; số người duyệt và số ca mỗi giờ | | | | |
| 6 | Chi phí | Khối "kinh doanh và vận hành" của report: chi phí mỗi ticket so với làm tay, ROI, tiền LLM ticket đắt nhất; `config/operating_gates.json` mục `business` | | | | |
| 7 | Vận hành | Runbook (Phiếu B mục B7.5–B7.6) + `config/operating_gates.json` mục `operations` (PIC, người duyệt, số người trực, điều kiện dừng, kênh báo tin) + metric trong `monitors.py` | | | | |
| 8 | Con người, pháp lý | Bên thứ ba (hãng, tài xế, shop, người nhận quà, người đứng tên duyệt); `config/operating_gates.json` mục `legal`; thẻ S6, S7, S8 có mục riêng ở Phiếu C mục C3 | | | | |
| 9 | Quyết định | Câu tiêu chí (Phiếu A mục A4) + hash Bản tiêu chí đã ký + quyết định Gate 1 (Phiếu B mục B8, Phiếu C mục C12) | | | | |

Ô "Chưa" có rủi ro cao → chuyển thành một dòng Risk register (Phiếu C mục C10).

---

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa (khoảng 8–10 phút, cả bàn)

*Mọi bàn làm pre-mortem ở vòng 1, TRƯỚC khi biết sự cố, để chọn 2–3 cổng phòng ngừa sẽ dựng. Ở vòng 2 bàn mở lại phần này ở
Phiếu C mục C1 (bút khác màu).*

**Khung tư duy.** Hỏi "có rủi ro gì không" thì ai cũng dè dặt. Nói "nó đã hỏng rồi, vì sao" thì mọi người được phép nói ra
điều mình vẫn lo. Làm im lặng trước, đọc sau, để ý kiến của người nói to không lấn át.

**Đề bài (đọc to):** *"Ba tháng sau pilot, LogiX phải tắt trợ lý hoàn tiền ở cả hai depot. Chuyện gì đã xảy ra?"*

1. **2 phút, im lặng:** mỗi người viết 2 lý do, mỗi lý do một dòng.
2. **2 phút:** đọc vòng tròn, mỗi lượt một lý do, không bình luận. Gộp lý do trùng.
3. **2 phút:** xếp từng lý do vào một **lăng kính**. Lăng kính nào còn trống thì cả bàn viết thêm ít nhất một lý do cho nó.
4. **2 phút:** chọn 2–3 lý do sẽ biến thành **cổng phòng ngừa** ngay hôm nay (code trong `guards.py` hoặc con số trong
   `config/operating_gates.json`). Lý do còn lại → Risk register.

Bốn lăng kính (bắt buộc đủ cả bốn; dự án AI hay chết ở ba lăng kính sau hơn là ở lăng kính đầu):

| Lăng kính | Câu hỏi gợi ý trên LogiX |
|---|---|
| **Kỹ thuật** | Model tin nhầm cái gì? Dữ liệu nào thiếu, cũ, lệch? Lệnh ghi nào không đảo ngược được? |
| **Kinh doanh** | Mỗi ticket tốn bao nhiêu so với làm tay? Một ngày hoàn tối đa bao nhiêu? Nhóm ticket nào không thể có lời? |
| **Con người và vận hành** | Ai duyệt, mấy người, mỗi giờ được mấy ca? Lượng việc tăng gấp ba thì sao? Nhân viên có tin trợ lý không? |
| **Pháp lý** | Dữ liệu cá nhân của ai rời hệ thống? Bên thứ ba nào bị ghi lỗi, bị trừ tiền mà không được hỏi? |

**Đóng góp của vai Sản phẩm và kinh doanh:** mới chuẩn bị dòng kinh doanh dưới đây; các lăng kính còn lại chờ cả bàn bổ sung, chưa coi là pre-mortem đã hoàn tất hoặc đã thống nhất 2–3 cổng.

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được hôm nay? (trace / data / config nào) | Thành cổng phòng ngừa nào (code hay config) / hay vào risk register |
|---|---|---|---|
| | Kỹ thuật | | |
| Pilot đã tốn hơn làm tay vì phí máy, công duyệt và phí trực; ngân sách hoàn tự động đã bị sử dụng quá mức mà Finance không được báo kịp. | Kinh doanh | `ops_limits`: ngân sách hoàn 2.000.000đ/ngày, máy 1.500đ/ticket; `ops_facts`: làm tay/duyệt 10.000đ, phí trực 30.000đ/người/ca. Cần report đúng cấu hình cả bàn để kiểm thực tế. | Đề xuất cổng business tại B7.4: trần hoàn 2.000.000đ/ngày, ngân sách đọc 900đ, ROI tối thiểu 0,25; giữ phạm vi all/100% cho lần đánh giá ban đầu. Sau khi các vai hoàn tất, kiểm tổng chi phí/ticket, ROI và từng phân khúc trước quyết định v1. |
| | Con người và vận hành | | |
| | Pháp lý | | |

---

<a id="b7"></a>

## B7 · Khối 2B · Cổng phòng ngừa (phút 85–105)

### B7.1 · Câu 2.6 · 2–3 cổng phòng ngừa trong `lab10/guards.py`

Mỗi cổng ứng với một dòng pre-mortem (B6) hoặc một dòng HAZOP (B4). Viết trong `pre_guard(ctx)` (trước khi trợ lý đọc ticket)
hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Thử bằng:

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m unittest discover -s tests
```

| # | Cổng (hàm và nhánh, ví dụ `write_gate` khi `tool == "issue_refund"`) | Ứng với dòng nào ở B6 / B4 | Chặn điều gì, dựa vào nguồn sự thật nào | Mã lần chạy `base · after` | Ca đang đúng nào bị hỏng? (phải là "không") |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### B7.2 · Câu 2.7 · Hai bước tránh rò rỉ dữ liệu

Bàn đang chỉnh cổng tới khi 22 ticket bộ nền xanh hết. Nêu 2 bước cụ thể để không "chỉnh trên chính bộ dùng để chấm"
(gắn với bộ nền, gói sự cố, bài kiểm tra ẩn):

1. …
2. …

### B7.3 · Câu 2.8 · Một behavioral test

- Tính chất (một câu): …

```bash
python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx
```

| Ticket hiểm | Nội dung ticket (`--adhoc`) | `--order` · `--customer` | Kết quả (dán dòng `SỔ CÁI` / `LỖI HÃNG` / `GỬI HÃNG`) | Tính chất giữ được? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

Giữ hai ticket này cho phần demo.

### B7.4 · Câu 2.9 · Cổng kinh doanh (`config/operating_gates.json` mục `business`)

Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`.

**Người chuẩn bị:** Hà Phan Đại Dương · Sản phẩm và kinh doanh.

**Trạng thái:** đã điền riêng mục `business` trong `config/operating_gates.json`; đây là phần chuẩn bị của vai sản phẩm, **chưa ký/chốt cổng vòng 1 và chưa quyết định v1**. `operations`, `legal` và cổng code chờ các vai tương ứng thực hiện. Chưa có báo cáo đánh giá cho cấu hình cả bàn hoàn chỉnh; không dùng kết quả từ lần làm vượt phạm vi trước đó làm bằng chứng cho bản hiện tại.

| Khoá | Giá trị bàn đặt | Lý do (một câu, có số) |
|---|---|---|
| `business.daily_refund_cap_vnd` | `2000000` (VND/ngày) | Bằng ngân sách Finance trong `ops_limits.daily_auto_refund_budget_vnd=2.000.000đ/ngày`; khoản tự động làm vượt trần chuyển người duyệt, còn giới hạn 300.000đ/khách/ngày cần kỹ sư kiểm riêng, không suy là đã có chỉ nhờ đặt trần tổng. |
| `business.cost_budget_per_ticket_vnd` | `900` (VND tại bước kiểm ngân sách đọc) | Từ trần máy `ops_limits.max_llm_cost_per_ticket_vnd=1.500đ`, dành `2 × 200đ` cho kiểm chính sách có một lần thử lại, `100đ` xác nhận và `100đ` ghi chú theo `ops_facts.llm_cost`, còn `900đ` cho phần trước đó; agent chỉ kiểm ngân sách trước lượt đọc nên vẫn cần đo tiền máy tối đa, và khoản dự phòng ghi chú chỉ dùng nếu vai vận hành bật tính năng này. |
| `business.pilot_scope` (all / warehouse / percent) | `{"mode": "all", "warehouses": [], "percent": 100}` | Đánh giá ban đầu trên 100% của 22 ticket nền, giữ cả 4 kho HN/HCM/DN/CT có trong dữ liệu để không loại phân khúc khó khi chưa có bằng chứng; với sức duyệt 6 ca/giờ/người theo `ops_facts`, cần vai vận hành xác nhận công suất trước khi cho chạy thật. |
| `business.roi_min` | `0.25` | Khớp tiêu chí CP2 hiện có: làm tay `10.000đ/ticket` theo `ops_facts`, tổng chi phí mục tiêu tối đa `8.000đ/ticket` thì ROI `(10.000 − 8.000) / 8.000 = 0,25` khi hoàn sai bằng 0; không hạ ROI để hợp thức hóa cấu hình chưa đạt. |

**Cách giải thích và đọc số khi cả bàn đã có kết quả:**

- Trần hoàn ngày và ngân sách đọc là cổng con số được hệ thống thực thi sẵn; phạm vi xác định ticket được đưa vào trợ lý. `roi_min` chỉ tạo cảnh báo trong report, không tự chặn lệnh ghi. Cổng code của kỹ sư mới kiểm đúng nghiệp vụ từng hành động; đặt ngân sách không chứng minh tiền hoặc lỗi hãng đã đúng.
- **900đ** là ngân sách kiểm trước bước đọc, **1.500đ** là trần tiền máy/ticket của Finance, **8.000đ** là ngưỡng tổng chi phí/ticket của CP2. Tổng chi phí gồm máy + công duyệt/kiểm lại + phí trực; khi tính tiết kiệm/ROI, report còn trừ tiền hoàn sai. Không dùng riêng tiền máy để tuyên bố pilot có lời.
- Ví dụ lập kế hoạch từ dữ liệu, chưa phải kết quả đo: 1 người trực có sức danh nghĩa `6 × 480 / 60 = 48` ca/ca, phí `30.000đ/ca`; nếu xử lý đủ 22 ticket thì riêng phí trực khoảng `30.000 / 22 = 1.364đ/ticket`. Số người trực thực tế và phương án giờ cao điểm do vai Vận hành và pháp lý quyết định.
- Sau khi các vai hoàn tất và kỹ sư chạy đo, đối chiếu tổng chi phí `≤8.000đ/ticket`, ROI `≥0,25`, máy tối đa `≤1.500đ/ticket`, hoàn tự động `≤2.000.000đ/ngày`, coverage >0 và tác hại đúng ngưỡng CP2. Xem cả kho/hãng có số xấu nhất; chỉ đề nghị thu hẹp khi phạm vi nhỏ hơn đã được đo lại, không dùng phạm vi 0 làm cách sửa.

### B7.5 · Câu 2.10 · Cổng con người, vận hành, pháp lý + Runbook phần 1–3

Điền `config/operating_gates.json` mục `operations` và `legal` (PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ,
thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có
nguyên nhân trong tracking). Rồi viết runbook dưới đây **khớp với các con số đó**.

*Runbook là tờ giấy người trực ca cầm lúc 23h khi có chuyện. Nó trả lời: nhìn con số nào, ngưỡng nào thì làm gì, ai được quyết.
Phần 1–3 và mục Giờ cao điểm viết ở vòng 1. Phần 4–5 viết ở vòng 2 (Phiếu C mục C11). Mọi con số phải khớp `config/operating_gates.json` và report.*
*Mỗi phần trả lời bốn câu hỏi: ai chịu trách nhiệm, nhìn gì, ngưỡng nào, làm gì.* **Người viết (vai Vận hành và pháp lý):** ______

#### Runbook 1 · Ai chịu trách nhiệm

| Vai | Tên / mã nhân viên (lấy từ `data/world.json` → `staff`) | Được quyền làm gì | Liên lạc qua kênh nào |
|---|---|---|---|
| PIC của trợ lý (một người) | | | |
| Người duyệt đứng tên các khoản vượt hạn mức | | | |
| Người giữ công tắc tắt từng thao tác ghi | | | |
| Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | | | |

Số người trực duyệt mỗi ca: ___ · Mỗi giờ duyệt được: ___ ca · Phạm vi pilot: ______ (tất cả / kho nào / bao nhiêu phần trăm)

#### Runbook 2 · Nhìn con số nào, ngưỡng nào thì làm gì

Mỗi dòng một tín hiệu. Cột "Lấy ở đâu" phải là một dòng trong report của `lab10.eval` / `lab10.grade` hoặc một chỉ số trong `lab10/monitors.py`.

| Tín hiệu | Lấy ở đâu | Bình thường | Ngưỡng VÀNG → việc làm | Ngưỡng ĐỎ → việc làm | Ai quyết |
|---|---|---|---|---|---|
| Thời gian chờ người duyệt lâu nhất | | | | | |
| Số ca bị ùn | | | | | |
| Chi phí mỗi ticket so với làm tay | | | | | |
| Tổng tiền hoàn tự động trong ngày so với trần | | | | | |
| Tiền hoàn sai | | | | | |
| Lỗi ghi oan cho hãng / lộ dữ liệu cá nhân (pháp lý) | | | | | |
| (tín hiệu riêng của bàn) | | | | | |

#### Runbook 3 · Điều kiện dừng và cách dừng

- Dừng một phần (tắt một thao tác ghi, thu hẹp phạm vi) khi: …
- Dừng hẳn khi: …
- Cách dừng, từng bước (công tắc nào trong `config/switches.json`, dòng nào trong `config/operating_gates.json`): …
- Từ tín hiệu đỏ đến lúc dừng xong tối đa ____ phút; người bấm: ____
- Khi đã dừng, ticket đang chờ đi đâu, ai xử lý: …
- Điều kiện để bật lại, ai ký: …

### B7.6 · Giờ cao điểm (bắt buộc với thẻ S4; các thẻ khác nên có)

Lượng ticket có thể dồn gấp ba trong một giờ (ngày sale, sau bão). Viết trước, khi chưa biết sự cố.

| Câu hỏi | Trả lời (có số, có tên) |
|---|---|
| Giờ cao điểm là khi nào, bao nhiêu ticket mỗi giờ (dựa vào `ops_facts`)? | |
| Ai trực giờ cao điểm, mấy người (khớp `operations.reviewers_on_shift`)? | |
| Ngưỡng nào thì **gọi thêm người** (hàng chờ bao nhiêu ca, chờ lâu nhất bao nhiêu phút)? Ai gọi? | |
| Ngưỡng nào thì **thu hẹp** phạm vi (khoá `business.pilot_scope`) hoặc **tắt** một thao tác ghi (`config/switches.json`)? Ai quyết? | |
| Thêm người thì chi phí mỗi ticket và ROI thay đổi thế nào (đọc report)? | |

---

<a id="b8"></a>

## B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 (phút 105–115)

**Chưa ký/chốt vòng 1, chưa có quyết định v1.** Vai Kỹ sư cổng và Vận hành/pháp lý chưa hoàn tất phần việc nên các ô dưới đây để chờ cả bàn. Sản phẩm và kinh doanh sẽ đối chiếu số đo, chi phí/ROI, ngưỡng CP2 và phân khúc xấu nhất để chuẩn bị quyết định sau khi có bản cổng hoàn chỉnh. Chưa chọn một trong bốn quyết định, chưa ghi PIC ký và chưa thực hiện các lệnh chốt/commit bên dưới.

Làm đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

**Khung tư duy.** Gate 1 "đạt" khi **quyết định khớp bằng chứng và khớp tiêu chí đã ký trước**. Tiếp tục, Thu hẹp, Cải tiến
thêm, Dừng đều có thể là quyết định đạt. Quyết định không đạt là quyết định mà con số trong report không đỡ được.
Chỉ chọn Tiếp tục khi mọi chỉ số bắt buộc đều đạt.

Ba câu tự vấn trước khi viết: (1) Rủi ro còn lại có chấp nhận được như hiện trạng không? (2) Cần thêm biện pháp nào, tốn
bao nhiêu thời gian? (3) Có phần nào của dự án không nên làm tiếp?

| | **v1** (phút 105–115, TRƯỚC khi nhận thẻ sự cố) |
|---|---|
| Commit ký tiêu chí (message `Sign acceptance criteria`; hash commit, tuỳ chọn) | |
| Hash chốt cổng vòng 1 (8 ký tự lệnh `lab10.checkpoint` in ra, tuỳ chọn) | |
| Mã lần chạy dùng làm bằng chứng | bộ nền, mốc base: ________ · bộ nền với cổng vòng 1 (prepared): ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Đọc khối "theo kho và hãng" ở cuối output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt phần nào, vì sao | |
| Nếu Cải tiến thêm: giả thuyết cụ thể + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Một bằng chứng còn thiếu (thứ bộ nền chưa đo được) | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

Xong v1 thì lưu và đẩy một bản (sau mốc này không sửa cột v1):

```bash
git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md
git commit -m "LAB 10: chốt cổng vòng 1, quyết định v1"
git push -u origin main
```
