"""Tái lập phép thử nhân sự CP3; chỉ dùng bộ nền và hàng chờ tổng hợp.

Chạy từ repo: python3 docs/evidence/cp3-20261119/ops-study.py
Không sửa dữ liệu đề/config. Các kết quả what-if không phải report eval chính thức.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from lab10 import guards, ops
from lab10.eval import code_hash, run_suite, summarize
from lab10.world import load_suite


def queue_case(world, gates, arrivals):
    trials = [
        {"seed": 11, "ticket_id": f"OPS-STUDY-{i:03d}",
         "status": "escalated", "arrive_min": minute, "ledger": []}
        for i, minute in enumerate(arrivals)
    ]
    ops.attach_queue(trials, world, gates)
    return {
        "trials": len(trials),
        "capacity_per_hour": ops.capacity_per_hour(world, gates),
        "queue_wait_max_min": max(t["queue_wait_min"] for t in trials),
        "queue_stuck": sum(t["queue_stuck"] for t in trials),
        "waits_min": [t["queue_wait_min"] for t in trials],
    }


def main():
    world, tickets = load_suite("base")
    config = json.loads((ROOT / "config/operating_gates.json").read_text())
    switches = json.loads((ROOT / "config/switches.json").read_text())
    cases = {}
    for reviewers in (1, 2):
        gates = ops.merged(copy.deepcopy(config))
        gates["operations"]["reviewers_on_shift"] = reviewers
        # null tự tính từ số người × 6 ca/giờ; không giữ trần công suất của 1 người.
        gates["operations"]["review_capacity_per_hour"] = None
        trials = run_suite(world, tickets, guards, switches, gates=gates)
        summary = summarize(trials)
        operating = ops.summarize_ops(trials, world, gates)
        cases[str(reviewers)] = {
            "reviewers_on_shift": reviewers,
            "base": {
                **{k: summary[k] for k in
                   ("trials", "pass_rate", "pass_k", "failed",
                    "wrongful_refund_vnd", "wrongful_carrier_faults", "pii_leaks")},
                "ops": operating,
            },
            "burst_14_at_2min": queue_case(world, gates, [2 * i for i in range(14)]),
            "sustained_14_per_hour_for_8h": queue_case(
                world, gates, [60 * hour + 2 * i for hour in range(8) for i in range(14)]),
        }
    result = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_code_config_hash": code_hash(),
        "kind": "what_if_not_official_eval_run",
        "method": {
            "base": "22 ticket × 5 seed; chỉ thay số người trực 1 → 2 trong bộ nhớ",
            "burst": "14 ca cần người duyệt, đến cách nhau 2 phút trong 26 phút",
            "sustained": "Lặp cụm 14 ca mỗi giờ suốt 8 giờ; mọi ca đều cần người duyệt",
            "queue_model": "Dùng nguyên hàm ops.attach_queue: một hàng chờ với công suất gộp",
            "limits": "Dữ liệu giả; không chứng minh tên người dự phòng, ca trực thật hay tải khách thật",
        },
        "cases": cases,
    }
    output = Path(__file__).with_name("ops-study.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for count, row in cases.items():
        o = row["base"]["ops"]
        print(json.dumps({
            "reviewers": count, "base_cost_per_ticket_vnd": o["cost"]["cost_per_ticket_vnd"],
            "base_roi": o["cost"]["roi"], "base_queue": o["queue"],
            "burst": {k: v for k, v in row["burst_14_at_2min"].items() if k != "waits_min"},
            "sustained": {k: v for k, v in row["sustained_14_per_hour_for_8h"].items() if k != "waits_min"},
        }, ensure_ascii=False))
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
