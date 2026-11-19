"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách hiệu lực: cần người xác minh")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if action.get("tool") == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if (not order or order["order_id"] != ctx.ticket.get("order_id")
                or order["customer_id"] != ctx.ticket.get("customer_id")
                or action.get("ticket_id") != ctx.ticket["ticket_id"] or not policy
                or not order.get("parcels")):
            return Verdict.escalate("thiếu dữ liệu hoặc sai đối tượng hoàn tiền")
        if ctx.ticket.get("parcel_id") and not any(
                p["parcel_id"] == ctx.ticket["parcel_id"] for p in order["parcels"]):
            return Verdict.escalate("kiện được yêu cầu không thuộc đơn")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        if not parcel.get("promised_date") or not parcel.get("delay_cause"):
            return Verdict.escalate("tracking thiếu ngày cam kết hoặc nguyên nhân")
        delay = H.db_delay_days(parcel, ctx.as_of)
        expected = H.entitlement_vnd(policy, order, delay, parcel["delay_cause"])
        if action.get("amount_vnd") != expected or action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("khoản hoàn không khớp quyền lợi từ tracking và chính sách")
        if ctx.tools.ledger_rows(order_id=order["order_id"]):
            return Verdict.escalate("đơn đã có khoản hoàn trong sổ cái: cần đối soát trước khi ghi tiếp")
        approval_id = action.get("approval_id")
        if approval_id or expected > policy["auto_limit_vnd"]:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
            approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            if not any(
                    a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
                    and a.get("ticket_id") == ctx.ticket["ticket_id"]
                    and a.get("order_id") == order["order_id"]
                    and a.get("customer_id") == order["customer_id"]
                    and a.get("max_vnd", 0) >= expected
                    and (not approver or a.get("approver_id") == approver)
                    for a in approvals):
                return Verdict.escalate("phê duyệt thiếu, hết hiệu lực hoặc không đúng giao dịch/người duyệt")
        else:
            cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
            spent = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                        if not r.get("approval_id"))
            if cap is not None and spent + expected > cap:
                return Verdict.escalate("vượt hạn mức hoàn tự động cho một khách trong ngày")
    if action.get("tool") == "notify_carrier":
        if not policy:
            return Verdict.escalate("không có chính sách để xác định dữ liệu được gửi hãng")
        allowed = set(policy["carrier_notice_fields"])
        payload = {k: v for k, v in action.get("payload", {}).items() if k in allowed}
        if payload != action.get("payload"):
            return Verdict.modify("chỉ gửi các trường trong danh sách cho phép của chính sách", payload=payload)
    return Verdict.allow()
