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

Ba cổng hiện tại: KT1 ghim chính sách hiệu lực, KT2 kiểm quyền lợi hoàn,
KT3 kiểm căn cứ ghi lỗi và thông báo hãng. Bổ sung sau khi nhận thẻ S6;
không coi bản này là cổng đã chốt trước sự cố.
"""
from . import helpers as H
from .tools import Verdict


def _policy(ctx):
    """Chỉ dùng một phiên bản hiệu lực; không tin chỉ mục index_active."""
    day = H.d(ctx.as_of)
    policies = ctx.tools.lookup_policies()
    active, ids = [], set()
    for policy in policies:
        pid = policy["policy_id"]
        if not isinstance(pid, str) or not pid or pid in ids:
            raise ValueError("mã chính sách thiếu hoặc trùng")
        ids.add(pid)
        start = H.d(policy["effective_from"])
        end = H.d(policy["effective_to"]) if policy.get("effective_to") else None
        if end is not None and end < start:
            raise ValueError("khoảng hiệu lực chính sách không hợp lệ")
        if start <= day and (end is None or day <= end):
            active.append(policy)
    if len(active) != 1:
        raise ValueError("không có duy nhất chính sách đang hiệu lực")
    policy = active[0]
    late = policy["late"]
    for name in ("min_days_fee", "min_days_bonus", "bonus_pct", "bonus_cap_vnd"):
        if type(late[name]) is not int or late[name] < 0:
            raise ValueError("tham số quyền lợi không hợp lệ")
    if late["min_days_bonus"] < late["min_days_fee"] or late["bonus_pct"] > 100:
        raise ValueError("ngưỡng quyền lợi mâu thuẫn")
    for name in ("fault_causes", "no_refund_causes"):
        if not isinstance(policy[name], list) or not all(isinstance(c, str) for c in policy[name]):
            raise ValueError("danh sách nguyên nhân không hợp lệ")
    return policy


def _parcels(order, as_of):
    """Kiểm ngày/trạng thái trước khi agent hoặc guard tính số ngày trễ."""
    parcels = order["parcels"]
    if not isinstance(parcels, list) or not parcels:
        raise ValueError("thiếu tracking kiện hàng")
    today, checked, ids = H.d(as_of), [], set()
    for parcel in parcels:
        pid = parcel["parcel_id"]
        if not isinstance(pid, str) or not pid or pid in ids:
            raise ValueError("mã kiện thiếu hoặc trùng")
        ids.add(pid)
        H.d(parcel["promised_date"])
        status, delivered = parcel["status"], parcel.get("delivered_date")
        if status == "DELIVERED":
            if not delivered or H.d(delivered) > today:
                raise ValueError("ngày giao thực tế thiếu hoặc nằm trong tương lai")
        elif status != "IN_TRANSIT" or delivered:
            raise ValueError("trạng thái và ngày giao cần được xác minh")
        checked.append((parcel, H.db_delay_days(parcel, as_of)))
    return checked


def _tracking(ctx, action):
    """Xác định kiện từ dữ kiện có cấu trúc, không suy từ chữ khách viết."""
    order_id = (action["payload"].get("order_id") if action.get("tool") == "notify_carrier"
                else action.get("order_id"))
    if action.get("ticket_id") != ctx.ticket["ticket_id"] or order_id != ctx.ticket.get("order_id"):
        raise ValueError("lệnh ghi không khớp ticket và đơn hàng")
    order = ctx.tools.lookup_order(order_id)
    if not order or order["customer_id"] != ctx.ticket.get("customer_id"):
        raise ValueError("không xác minh được đơn và chủ đơn")
    for name in ("shipping_fee_vnd", "goods_value_vnd"):
        if type(order[name]) is not int or order[name] < 0:
            raise ValueError("giá trị tiền trên đơn không hợp lệ")
    checked = _parcels(order, ctx.as_of)
    pid = ctx.ticket.get("parcel_id")
    if pid:
        candidates = [(p, delay) for p, delay in checked if p["parcel_id"] == pid]
    else:
        delayed = [p for p, delay in checked if delay > 0]
        if len(delayed) > 1:
            ctx.log("parcel_identity_ambiguous", order_id=order_id,
                    delayed_parcels=[p["parcel_id"] for p in delayed])
            raise ValueError("nhiều kiện cùng trễ nhưng ticket chưa xác định kiện; cần người xác minh trước khi ghi")
        longest = max(delay for _, delay in checked)
        candidates = [(p, delay) for p, delay in checked if delay == longest]
        if longest == 0:
            candidates = candidates[:1]  # Không kiện nào trễ nên không phát sinh quyền lợi/lỗi.
    if len(candidates) != 1:
        raise ValueError("chưa xác định được duy nhất kiện cần xử lý")
    parcel, delay = candidates[0]
    if delay > 0 and not parcel.get("delay_cause"):
        raise ValueError("tracking chưa ghi nhận nguyên nhân giao trễ")
    return order, parcel, delay


def pre_guard(ctx):
    # KT1: chọn chính sách bằng khoảng ngày hiệu lực, trước khi đọc ticket.
    try:
        policy = _policy(ctx)
    except (KeyError, TypeError, ValueError) as exc:
        ctx.log("kt1_policy_invalid", reason=str(exc))
        return Verdict.escalate("KT1: cần xác minh chính sách: " + str(exc))
    ctx.log("kt1_policy_pinned", policy_id=policy["policy_id"], as_of=ctx.as_of)
    # KT2 kiểm sơ bộ để agent không lỗi khi đọc ngày tracking thiếu/hỏng.
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if order:
        try:
            _parcels(order, ctx.as_of)
        except (KeyError, TypeError, ValueError) as exc:
            ctx.log("kt2_tracking_invalid", reason=str(exc))
            return Verdict.escalate("KT2: cần xác minh tracking: " + str(exc))
    return Verdict.allow(policy_id=policy["policy_id"])


def _carrier_limit_reached(ctx, parcel):
    """Trần theo hãng/ngày từ Ops; sổ lỗi là nguồn đếm, không dùng mã ticket."""
    limit = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if type(limit) is not int or limit < 0:
        raise ValueError("chưa có trần lỗi hãng/ngày hợp lệ")
    used = len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"]))
    if used >= limit:
        ctx.log("carrier_daily_limit", carrier_id=parcel["carrier_id"], used=used, limit=limit)
        return True
    return False


def _refund_gate(ctx, action, policy, order, parcel, delay):
    # KT2: tính lại quyền lợi từ DB ngay trước khi ghi tiền.
    amount = action.get("amount_vnd")
    if type(amount) is not int or amount <= 0:
        return Verdict.deny("KT2: số tiền hoàn phải là số nguyên dương")
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    ctx.log("kt2_refund_checked", policy_id=policy["policy_id"], parcel_id=parcel["parcel_id"],
            db_delay_days=delay, entitlement_vnd=entitled, proposed_vnd=amount)
    if entitled == 0:
        return Verdict.deny("KT2: tracking và chính sách chưa cho phép hoàn tiền")
    if amount != entitled or action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate("KT2: số tiền hoặc bên trả không khớp quyền lợi theo chính sách")
    # Kiểm trước khoản hoàn đầu tiên để chuyển người không để lại giao dịch dở dang.
    if H.carrier_at_fault(policy, parcel, delay) and _carrier_limit_reached(ctx, parcel):
        return Verdict.escalate("Vượt trần lỗi tự động của hãng trong ngày; chuyển người trước khi ghi tiền")
    return Verdict.allow()


def _carrier_gate(ctx, action, policy, order, parcel, delay):
    # KT3: đủ căn cứ mới ghi lỗi; hãng/tài xế phải thuộc đúng kiện trong DB.
    if not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny("KT3: tracking và chính sách không đủ căn cứ ghi lỗi hãng")
    carrier = parcel.get("carrier_id")
    driver = parcel.get("driver_id")
    if not carrier or not driver or not ctx.tools.lookup_carrier(carrier):
        return Verdict.escalate("KT3: cần xác minh hãng và tài xế của kiện")
    target = {"parcel_id": parcel["parcel_id"], "carrier_id": carrier,
              "driver_id": driver, "delay_days": delay}
    if action["tool"] == "file_carrier_fault":
        if _carrier_limit_reached(ctx, parcel):
            return Verdict.escalate("Vượt trần lỗi tự động của hãng trong ngày; cần người duyệt")
        ctx.log("kt3_fault_checked", policy_id=policy["policy_id"], **target)
        if any(action.get(k) != v for k, v in target.items()):
            return Verdict.modify("KT3: sửa đối tượng và độ trễ theo tracking đã xác minh", **target)
        return Verdict.allow()

    rows = ctx.tools.fault_rows(ticket_id=ctx.ticket["ticket_id"], order_id=order["order_id"])
    if not any(all(row.get(k) == v for k, v in target.items()) for row in rows):
        return Verdict.deny("KT3: chưa có bản ghi lỗi hợp lệ để thông báo hãng")
    payload = action["payload"]
    actual = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"], "delay_days": delay}
    ctx.log("kt3_notice_checked", policy_id=policy["policy_id"], **target)
    if action.get("carrier_id") != carrier or any(payload.get(k) != v for k, v in actual.items()):
        return Verdict.modify("KT3: thông báo phải khớp bản ghi lỗi đã kiểm",
                              carrier_id=carrier, payload={**payload, **actual})
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()
    try:
        if tool == "notify_carrier" and not isinstance(action.get("payload"), dict):
            raise ValueError("payload thông báo không hợp lệ")
        policy = _policy(ctx)
        order, parcel, delay = _tracking(ctx, action)
        if tool == "issue_refund":
            return _refund_gate(ctx, action, policy, order, parcel, delay)
        return _carrier_gate(ctx, action, policy, order, parcel, delay)
    except (KeyError, TypeError, ValueError) as exc:
        ctx.log("write_facts_invalid", tool=tool, reason=str(exc))
        return Verdict.escalate("Cần xác minh dữ kiện trước lệnh ghi: " + str(exc))
