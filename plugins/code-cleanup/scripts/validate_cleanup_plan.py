#!/usr/bin/env python3
"""Validate cleanup inventory coverage and completion gates."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "## 1. 运行控制",
    "## 2. 范围与排除项",
    "## 3. 文件覆盖表",
    "## 4. 候选队列",
    "## 5. 功能基准验证",
    "## 6. 批次记录",
]

REQUIRED_CONTROL = [
    "状态",
    "功能基准版本",
    "范围基准状态",
    "清理范围",
    "扫描基线",
    "扫描终点",
    "总文件数",
    "已审文件数",
    "覆盖率",
]

FILE_STATUSES = {"unreviewed", "reviewed-clean", "candidate", "blocked", "removed"}
CANDIDATE_STATUSES = {"candidate", "ready", "active", "done", "blocked", "declined"}
TERMINAL_CANDIDATE_STATUSES = {"done", "declined"}


def section_body(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    match = re.search(r"^##\s+", text[start:], re.MULTILINE)
    return text[start : start + match.start()] if match else text[start:]


def control_value(body: str, field: str) -> str | None:
    match = re.search(rf"^- \*\*{re.escape(field)}\*\*:\s*(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else None


def table_rows(body: str, columns: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if len(cells) != columns:
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/code-cleanup/cleanup-plan.md")
    if not path.is_file():
        print(f"ERROR: cleanup plan not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    positions = [text.find(heading) for heading in REQUIRED_SECTIONS]
    for heading, position in zip(REQUIRED_SECTIONS, positions):
        if position < 0:
            errors.append(f"missing section: {heading}")
    if [position for position in positions if position >= 0] != sorted(
        position for position in positions if position >= 0
    ):
        errors.append("sections are not in the required order")

    control = section_body(text, "## 1. 运行控制")
    values: dict[str, str] = {}
    for field in REQUIRED_CONTROL:
        value = control_value(control, field)
        if value is None:
            errors.append(f"missing control field: {field}")
        else:
            values[field] = value

    plan_status = values.get("状态")
    if plan_status and plan_status not in {"inventory", "executing", "blocked", "complete"}:
        errors.append(f"invalid plan status: {plan_status}")
    baseline_status = values.get("范围基准状态")
    if baseline_status and baseline_status not in {"ready", "blocked"}:
        errors.append(f"invalid baseline scope status: {baseline_status}")

    inventory = table_rows(section_body(text, "## 3. 文件覆盖表"), 5)
    inventory_paths: set[str] = set()
    file_statuses: list[str] = []
    file_candidate_refs: set[str] = set()
    for row in inventory:
        file_path, _, status, candidate_ids, _ = row
        if not file_path:
            errors.append("file inventory contains an empty path")
        elif file_path in inventory_paths:
            errors.append(f"duplicate file inventory path: {file_path}")
        inventory_paths.add(file_path)
        if status not in FILE_STATUSES:
            errors.append(f"{file_path}: invalid file status '{status}'")
        file_statuses.append(status)
        refs = set(re.findall(r"\bC-\d{3,}\b", candidate_ids))
        file_candidate_refs.update(refs)
        if status == "candidate" and not refs:
            errors.append(f"{file_path}: candidate file has no candidate ID")

    candidates = table_rows(section_body(text, "## 4. 候选队列"), 9)
    candidate_statuses: dict[str, str] = {}
    for row in candidates:
        candidate_id, _, _, _, _, _, _, _, status = row
        if not re.fullmatch(r"C-\d{3,}", candidate_id):
            errors.append(f"invalid candidate ID: {candidate_id or '<empty>'}")
            continue
        if candidate_id in candidate_statuses:
            errors.append(f"duplicate candidate ID: {candidate_id}")
        if status not in CANDIDATE_STATUSES:
            errors.append(f"{candidate_id}: invalid candidate status '{status}'")
        candidate_statuses[candidate_id] = status

    for candidate_id in sorted(file_candidate_refs - set(candidate_statuses)):
        errors.append(f"file inventory references missing candidate: {candidate_id}")

    try:
        declared_total = int(values.get("总文件数", ""))
    except ValueError:
        declared_total = -1
        errors.append("总文件数 must be an integer")
    try:
        declared_reviewed = int(values.get("已审文件数", ""))
    except ValueError:
        declared_reviewed = -1
        errors.append("已审文件数 must be an integer")
    coverage_match = re.fullmatch(r"(\d+(?:\.\d+)?)%", values.get("覆盖率", ""))
    if not coverage_match:
        declared_coverage = -1.0
        errors.append("覆盖率 must be a percentage such as 100%")
    else:
        declared_coverage = float(coverage_match.group(1))

    actual_total = len(inventory_paths)
    actual_reviewed = sum(status != "unreviewed" for status in file_statuses)
    actual_coverage = 100.0 if actual_total == 0 else actual_reviewed / actual_total * 100
    if declared_total >= 0 and declared_total != actual_total:
        errors.append(f"总文件数 mismatch: declared {declared_total}, inventory {actual_total}")
    if declared_reviewed >= 0 and declared_reviewed != actual_reviewed:
        errors.append(f"已审文件数 mismatch: declared {declared_reviewed}, inventory {actual_reviewed}")
    if declared_coverage >= 0 and abs(declared_coverage - actual_coverage) > 0.01:
        errors.append(
            f"覆盖率 mismatch: declared {declared_coverage:g}%, calculated {actual_coverage:.2f}%"
        )

    if plan_status in {"executing", "complete"} and "unreviewed" in file_statuses:
        errors.append(f"{plan_status} plan still contains unreviewed files")

    if plan_status == "complete":
        if baseline_status != "ready":
            errors.append("complete plan requires a ready baseline for the cleanup scope")
        if actual_total == 0:
            errors.append("complete plan has no in-scope files")
        if actual_coverage != 100.0:
            errors.append("complete plan must have 100% file coverage")
        if any(status in {"unreviewed", "blocked", "candidate"} for status in file_statuses):
            errors.append("complete plan contains non-terminal file statuses")
        non_terminal = [
            candidate_id
            for candidate_id, status in candidate_statuses.items()
            if status not in TERMINAL_CANDIDATE_STATUSES
        ]
        if non_terminal:
            errors.append("complete plan contains non-terminal candidates: " + ", ".join(non_terminal))
        if not section_body(text, "## 5. 功能基准验证").strip():
            errors.append("complete plan is missing baseline verification")
        if not section_body(text, "## 6. 批次记录").strip():
            errors.append("complete plan is missing batch records")

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(
        f"OK: status={plan_status}, files={actual_reviewed}/{actual_total}, "
        f"coverage={actual_coverage:.2f}%, candidates={len(candidate_statuses)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
