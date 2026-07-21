#!/usr/bin/env python3
"""Validate the structural contract of docs/product-spec/feature-list.md."""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_SECTIONS = [
    "## 1. 文档控制",
    "## 2. 产品边界",
    "## 3. 参与者与权限",
    "## 4. 术语与业务对象",
    "## 5. 产品体验规范",
    "## 6. 全局规则",
    "## 7. 功能索引",
    "## 8. 功能详述",
    "## 9. 跨功能旅程",
    "## 10. 外部契约总表",
    "## 11. 数据生命周期",
    "## 12. 质量属性",
    "## 13. 排除项与未决事项",
    "## 14. 变更记录",
]

REQUIRED_METADATA = [
    "产品",
    "规格版本",
    "基线日期",
    "覆盖状态",
    "覆盖范围",
    "不包含范围",
]

REQUIRED_FEATURE_SECTIONS = [
    "参与者与权限",
    "触发与前置条件",
    "输入与校验",
    "主流程",
    "分支与异常",
    "状态与反馈",
    "界面与交互",
    "输出与副作用",
    "业务规则",
    "外部契约",
    "非功能约束",
    "依赖",
    "验收场景",
]

FEATURE_HEADING = re.compile(r"^### (F-\d{3,})\s+(.+?)\s*$", re.MULTILINE)
UNKNOWN_MARKERS = re.compile(r"\b(?:TODO|TBD)\b|未知|待确认|待补充", re.IGNORECASE)


def section_body(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    match = re.search(r"^##\s+", text[start:], re.MULTILINE)
    return text[start : start + match.start()] if match else text[start:]


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/product-spec/feature-list.md")
    if not path.is_file():
        print(f"ERROR: feature list not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    positions = [text.find(heading) for heading in REQUIRED_SECTIONS]
    for heading, position in zip(REQUIRED_SECTIONS, positions):
        if position < 0:
            errors.append(f"missing section: {heading}")
    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("top-level sections are not in the required order")

    control = section_body(text, "## 1. 文档控制")
    for field in REQUIRED_METADATA:
        if not re.search(rf"^- \*\*{re.escape(field)}\*\*:\s*\S", control, re.MULTILINE):
            errors.append(f"missing document-control field: {field}")

    coverage_match = re.search(r"^- \*\*覆盖状态\*\*:\s*(\S+)", control, re.MULTILINE)
    if coverage_match and coverage_match.group(1) not in {"draft", "partial", "ready"}:
        errors.append("覆盖状态 must be draft, partial, or ready")
    version_match = re.search(r"^- \*\*规格版本\*\*:\s*(\S+)", control, re.MULTILINE)
    if version_match and not re.fullmatch(r"\d+\.\d+\.\d+", version_match.group(1)):
        errors.append("规格版本 must use MAJOR.MINOR.PATCH")
    date_match = re.search(r"^- \*\*基线日期\*\*:\s*(\S+)", control, re.MULTILINE)
    if date_match:
        try:
            datetime.strptime(date_match.group(1), "%Y-%m-%d")
        except ValueError:
            errors.append("基线日期 must be a valid YYYY-MM-DD date")

    for heading in REQUIRED_SECTIONS:
        if heading in text and not section_body(text, heading).strip():
            errors.append(f"empty section: {heading}")

    details = section_body(text, "## 8. 功能详述")
    matches = list(FEATURE_HEADING.finditer(details))
    if not matches:
        errors.append("功能详述 must contain at least one heading such as '### F-001 功能名称'")

    seen: set[str] = set()
    statuses: dict[str, str | None] = {}
    for index, match in enumerate(matches):
        feature_id = match.group(1)
        if feature_id in seen:
            errors.append(f"duplicate feature ID: {feature_id}")
        seen.add(feature_id)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(details)
        body = details[match.end() : end]

        status_match = re.search(r"^- \*\*基准状态\*\*:\s*(\S+)", body, re.MULTILINE)
        if not status_match:
            errors.append(f"{feature_id}: missing 基准状态")
            status = None
        else:
            status = status_match.group(1)
            if status not in {"ready", "draft", "deprecated"}:
                errors.append(f"{feature_id}: invalid 基准状态 '{status}'")
        statuses[feature_id] = status

        if not re.search(r"^- \*\*目标\*\*:\s*\S", body, re.MULTILINE):
            errors.append(f"{feature_id}: missing 目标")
        for subsection in REQUIRED_FEATURE_SECTIONS:
            subsection_match = re.search(
                rf"^#### {re.escape(subsection)}\s*$\n(?P<content>.*?)(?=^#### |\Z)",
                body,
                re.MULTILINE | re.DOTALL,
            )
            if not subsection_match:
                errors.append(f"{feature_id}: missing subsection '{subsection}'")
            elif not subsection_match.group("content").strip():
                errors.append(f"{feature_id}: empty subsection '{subsection}'")
        if status == "ready" and UNKNOWN_MARKERS.search(body):
            errors.append(f"{feature_id}: ready feature contains an unresolved marker")

    index_body = section_body(text, "## 7. 功能索引")
    for feature_id in seen:
        if feature_id not in index_body:
            errors.append(f"{feature_id}: missing from 功能索引")
            continue
        index_line = re.search(
            rf"^\|[^\n]*\b{re.escape(feature_id)}\b[^\n]*\|\s*$",
            index_body,
            re.MULTILINE,
        )
        if not index_line:
            errors.append(f"{feature_id}: 功能索引 entry must be a Markdown table row")
            continue
        index_status = re.search(r"\b(ready|draft|deprecated)\b", index_line.group(0))
        if not index_status:
            errors.append(f"{feature_id}: 功能索引 row is missing 基准状态")
        elif statuses.get(feature_id) and index_status.group(1) != statuses[feature_id]:
            errors.append(f"{feature_id}: 功能索引 status does not match 功能详述")
    indexed_ids = set(re.findall(r"\bF-\d{3,}\b", index_body))
    for feature_id in sorted(indexed_ids - seen):
        errors.append(f"{feature_id}: listed in 功能索引 but missing from 功能详述")

    coverage = coverage_match.group(1) if coverage_match else None
    if coverage == "ready":
        non_ready = [feature_id for feature_id, status in statuses.items() if status == "draft"]
        if non_ready:
            errors.append("ready coverage contains draft features: " + ", ".join(sorted(non_ready)))
        if UNKNOWN_MARKERS.search(text):
            errors.append("ready coverage contains an unresolved marker")

    leakage_patterns = {
        "inline or fenced code formatting": r"`",
        "source-like statement": r"^\s*(?:import|from|export|const|let|var|def|class|function|interface|type|return)\s+",
        "code-style identifier": r"\b[a-z][a-z0-9]*_[a-z0-9_]+\b",
        "source-directory path": r"(?:^|[\s`(])(?:src|lib|app|apps|packages)/[\w./-]+",
        "implementation filename": r"\b[\w-]+\.(?:py|ts|tsx|js|jsx|java|go|rs|rb|php|vue|svelte|css|scss|sql)\b",
        "implementation evidence": r"实现证据|源码位置|代码位置|调用链|测试文件|文件路径|函数名|类名|方法名|模块名|组件名|数据库表名|数据库字段|框架名称|依赖包|环境变量",
    }
    for label, pattern in leakage_patterns.items():
        flags = re.MULTILINE | (re.IGNORECASE if label == "source-like statement" else 0)
        if re.search(pattern, text, flags):
            errors.append(f"possible {label}; keep implementation evidence out of the feature list")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: {len(seen)} feature(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
