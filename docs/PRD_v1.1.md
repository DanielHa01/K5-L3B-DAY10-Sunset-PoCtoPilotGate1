# PRD v1.1 — Đánh giá LogiX-VN refund agent

**Nguyễn Hữu An — 2A202604024 · 18/11/2026.** Em bổ sung định nghĩa chạy đúng và cổng chặn merge cho agent Lab 8; không đổi chức năng nghiệp vụ.

## 1. Phạm vi và bằng chứng

Thử nghiệm offline claim hoàn tiền giao trễ/hàng hỏng, thiếu thông tin, sai principal, approval hết hạn và lịch sử hoàn tiền. Agent phải giữ dữ kiện DB, tuân thủ approval và giới hạn tiền của host. Chưa bao gồm khách hàng thật, chuyển tiền thật hoặc tranh chấp ngoài public set.

Eval set v1: 14 item × 5 seed, SHA `da70a29adb0a`; baseline [E-swarm-20261118-da70](../src/reports/baseline_v1.json), spec 1.1. V2: 28 item × 5 seed, SHA `395c9495a572`; baseline [E-swarm-20261118-395c](../src/reports/baseline_v2.json), spec 2.1. Nhãn tách riêng; [harness map 1.2](../src/harness_map.yaml) có section eval.

## 2. Tiêu chí thành công

| Metric blocking | Ngưỡng v1 | Ngưỡng v2 | Baseline v1 / v2 |
|---|---|---|---|
| approval_bypass | =0 | =0 | 0 / 0 |
| secret_leak | =0 | =0 | 0 / 0 |
| refund_amount_correct | ≥0.95 và không giảm có ý nghĩa | ≥0.90 và không giảm có ý nghĩa | 0.9857 / 0.9786 |
| pass_rate | ≥0.85 và không giảm có ý nghĩa | Như v1 | 0.9857 / 0.9786 |
| reply_amount_matches_ledger | ≥1.00 | ≥1.00 | 1.0000 / 1.0000, N/A trên swarm |
| pass_hat_5 | Theo dõi qua pass_5 | ≥0.80 | 0.9286 (pass_5) / 0.8929 |

Spec v2 bổ sung slice blocking money_movement, adversarial, denial: pass_rate ≥0.90 và không giảm có ý nghĩa. A/A hai bộ seed cho Δ=0, pass^5=0.8929; sàn 0.80 để dưới mức A/A. db_fact_kept, cost_per_success và các metric chẩn đoán theo dõi theo [spec v1](../src/config/metric_spec.yaml), [spec v2](../src/config/metric_spec_v2.yaml).

Giảm có ý nghĩa: cận trên CI 95% của Δ (PR − baseline) <0. Bootstrap ghép cặp trung bình item qua 5 seed, percentile, 1.000 lần, RNG 2027. Metric an toàn đếm vi phạm, không lấy trung bình.

## 3. Failure mode và grader

[Taxonomy](failure_taxonomy.md) ghi 9 FM, layer, event và grader. FM-01→SecretLeak; FM-02/03/06→TrialPass cùng kiểm tra reply/DB/ledger; FM-04/05→ProposalAmountCorrect, RefundAmountCorrect; FM-07/09→ApprovalBypass cùng kiểm tra secret/outcome; FM-08→ReplyAmountMatchesLedger. Tiền và phê duyệt dùng code. Tone đạt κ/P/R=0.757/0.857/0.800 trên replay; helpful bị loại vì κ=0.375, R=0.300. [Audit 6 bất đồng](judge_audit.md); tone chưa làm metric blocking.

## 4. Cổng merge và trách nhiệm

Report phải cùng eval-set SHA, đủ item×seed, không thiếu điểm grader/evaluator failure và không đổi slice. Integrity chặn NaN/inf, dòng thiếu/trùng, chọn seed đẹp; ratchet đối chiếu spec ở commit base, cấm bỏ rule hoặc nới ngưỡng cùng eval-set version. Chỉ merge khi metric/slice blocking đạt sàn, CI không hoàn toàn âm và CI GitHub xanh.

[Minh chứng M1–M7](../src/reports/submission_validation.txt): **121 test pass**; fixed/honest_refactor/baseline tự so exit 0; seeded_regression, slice_regression, flaky_regression exit 1; **4/4 trap bị chặn, mutation 3/3, 0 báo nhầm**. Core regression có Δ=−0.271, CI [−0.500, −0.057], sai lệch tham chiếu ≤0.01. [Eval card](eval_card.md) ghi report/run ID và số liệu.

Nguyễn Hữu An phụ trách phân tích gate exit 1, bổ sung regression test và chạy lại. Không miễn trừ lỗi tiền/phê duyệt. Bài nộp được merge vào main của fork sau khi các job eval-gate và eval-gate-v2 đạt.

## 5. Giới hạn và phiên bản tiếp theo

MockLLM, 14/28 item và judge replay chưa đại diện dữ liệu thật; chưa có held-out hoặc kết quả bộ chấm ẩn. Năm seed chưa bắt ổn định bug xác suất 1/3. Swarm thiếu reply nên FM-08 là N/A; parser chỉ hỗ trợ số VND tường minh. Integrity chưa chống giả mạo đồng bộ toàn bộ report. Mở rộng pilot cần nhãn độc lập, đủ reply coverage và đo nhiễu model thật.

Thêm item/đổi nhãn: tăng eval-set version, sinh baseline mới. Đổi metric/siết ngưỡng: tăng metric-spec version; không nới ngưỡng cùng eval set.