# Eval card — LogiX-VN refund agent

**Nguyễn Hữu An — 2A202604024 · 18/11/2026 · M1–M7.** Em đánh giá offline bằng MockLLM, Python 3.13.18 trong conda `lab9`, pydantic-evals 2.68.0.

## Dữ liệu và phiên bản

| Eval set | SHA | Kích thước | Spec | Baseline / run ID |
|---|---|---|---|---|
| v1 | `da70a29adb0a` | 14 item × 5 seed = 70 trial | 1.1 | [baseline_v1](../src/reports/baseline_v1.json), `E-swarm-20261118-da70` |
| v2 | `395c9495a572` | 28 item × 5 seed = 140 trial | 2.1 | [baseline_v2](../src/reports/baseline_v2.json), `E-swarm-20261118-395c` |

Seed `11,22,33,44,55`; nhãn tách riêng. V2 giữ 14 item v1 và thêm 14 item adversarial; mỗi FM bị tấn công có ≥3 item. Harness map 1.2. Mã và dữ liệu được lưu cùng commit bài nộp; [log tái lập](../src/reports/submission_validation.txt) ghi đủ cặp item/seed và không có evaluator failure.

## Core — M1–M4

[Taxonomy](failure_taxonomy.md) có 8 FM quan sát được, FM-09 với đối chứng chặn truy cập chéo principal và 5 trial công khai ghi bước sai đầu tiên. [Trace case](trace_case.md) C-002@11: event 3 ghi đè DB từ 2 thành 5 ngày; regression test đối chiếu ledger/status với `fixed`.

[Judge audit](judge_audit.md) có 6 bất đồng và đề xuất sửa rubric. Tone đạt κ/P/R = **0.757/0.857/0.800**; helpful **0.375/1.000/0.300**, bị loại. Tỷ lệ lỗi Rogan–Gladen là 0.300 trên cả hai tập replay. Tone chưa tích hợp làm metric blocking; tiền/phê duyệt chấm bằng code.

| Metric blocking v1 | Ngưỡng | Baseline | fixed | seeded_regression |
|---|---|---:|---:|---:|
| approval_bypass | = 0 | 0 | 0 | 0 |
| secret_leak | = 0 | 0 | 0 | 0 |
| refund_amount_correct | ≥0.95, không giảm có ý nghĩa | 0.9857 | 1.0000 | 0.8571 |
| pass_rate | ≥0.85, không giảm có ý nghĩa | 0.9857 | 1.0000 | 0.7143 |
| reply_amount_matches_ledger | ≥1.00 | 1.0000 (N/A) | 1.0000 | 0.7857 |

Metric theo dõi và ngưỡng đầy đủ nằm trong [spec v1](../src/config/metric_spec.yaml). Baseline thiếu event reply nên FM-08 trả True/N/A, chưa chứng minh reply được kiểm tra. [M3](m3_validation.md): detection **20/20 = 100%**, báo nhầm **0/70 = 0%**; grader proposal giải thích lỗi khi ledger cuối vẫn đúng.

Bootstrap ghép cặp theo trung bình item qua seed: percentile, 1.000 resample, RNG 2027, CI 95%, Δ = PR − baseline. [fixed](../src/reports/eval_fixed.json), run `E-fixed-20261118-da70`: Δ **+0.014**, CI **[0.000, +0.043]**, exit 0. [seeded_regression](../src/reports/eval_seeded_regression.json), run `E-seeded_regression-20261118-da70`: Δ **−0.271**, CI **[−0.500, −0.057]**, exit 1 tại refund_amount_correct, pass_rate, FM-08; sai lệch tham chiếu ≤0.01.

## Advanced — M5–M6

[Spec v2](../src/config/metric_spec_v2.yaml): pass_rate ≥0.85, refund_amount_correct ≥0.90, FM-08 ≥1.00; slice `money_movement`, `adversarial`, `denial` cùng sàn pass_rate ≥0.90, blocking và không giảm có ý nghĩa.

| Report v2 / run ID | pass_rate | pass^5 | money_movement | Gate |
|---|---:|---:|---:|---|
| baseline / `E-swarm-20261118-395c` | 0.9786 | 0.8929 | 1.0000 | exit 0, tự so |
| [fixed](../src/reports/eval_fixed_v2.json) / `E-fixed-20261118-395c` | 1.0000 | 1.0000 | 1.0000 | exit 0 |
| [honest_refactor](../src/reports/eval_honest_refactor_v2.json) / `E-honest_refactor-20261118-395c` | 1.0000 | 1.0000 | 1.0000 | exit 0 |
| [slice_regression](../src/reports/eval_slice_regression_v2.json) / `E-slice_regression-20261118-395c` | 0.9357 | 0.8929 | 0.8500 | exit 1, slice money_movement |
| [flaky_regression](../src/reports/eval_flaky_regression_v2.json) / `E-flaky_regression-20261118-395c` | 0.9143 | 0.5714 | 0.8667 | exit 1, gồm pass_hat_5 |

Slice regression vẫn trên sàn toàn tập, CI Δ **[−0.121, +0.029]**; riêng money_movement đạt 0.85 <0.90, CI slice **[−0.300, 0.000]**. Sàn slice quyết định việc chặn.

Em tính pass@k/pass^k bằng estimator tổ hợp từng item, kiểm tra miền đầu vào. A/A với seed `66,77,88,99,110` cho **Δ=0** ở mọi metric, pass^5 cùng **0.8929**. Em chọn **pass_hat_5 ≥0.80, blocking**, thấp hơn mức A/A. Với LLM thật cần nhiều lần A/A để đặt sàn dưới miền dao động bình thường.

## Expert — M7

Em bổ sung integrity cho NaN/inf, điểm grader thiếu, evaluator failure, dòng thiếu/trùng, item/seed và slice bị thay đổi; ratchet chặn bỏ rule, tắt blocking/CI hoặc nới ngưỡng trên cùng eval-set version. **4/4 trap công khai đều gate exit 1, INTEGRITY**; baseline tự so exit 0; mutation **3/3, 0 báo nhầm**. Test bổ sung kiểm tra dòng trùng và evaluator failure dù aggregate vẫn xanh. [Minh chứng cuối](../src/reports/submission_validation.txt): **121 test pass**; script tái lập là [verify_submission.py](../src/scripts/verify_submission.py).

## Trách nhiệm và giới hạn

Nguyễn Hữu An phụ trách gate, phân tích lỗi và chạy lại trước merge; không miễn trừ lỗi tiền/phê duyệt. Phạm vi pilot là claim public về giao trễ/hàng hỏng, đúng principal và approval; chưa chuyển tiền hoặc phục vụ khách hàng thật.

MockLLM, **14 item v1 / 28 item v2**, judge replay công khai và 5 seed chưa đại diện cho model/người dùng thật. Chưa có held-out; bộ chấm ẩn không có trong repo. Bug xác suất 1/3 chưa được phát hiện ổn định với 5 seed. Parser FM-08 chỉ hỗ trợ tiền VND tường minh; integrity chưa chứng minh report không bị giả mạo đồng bộ toàn bộ dữ liệu. Thêm item/đổi nhãn cần tăng eval-set version và sinh baseline mới; đổi metric/siết ngưỡng cần tăng metric-spec version.