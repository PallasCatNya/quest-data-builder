from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATES_PATH = PROJECT_ROOT / "data" / "task_templates.json"
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "quest_plan.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "quest_plan.resolved.json"
DEFAULT_OUTPUT_PREVIEW_PATH = PROJECT_ROOT / "output" / "quest_plan.resolved.preview.md"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_spaces(value: str | None) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", value.strip())


def normalize_task_type(value: str | None) -> str:
    normalized = normalize_spaces(value).replace(",", " ").lower()
    return normalize_spaces(normalized)


def normalize_name(value: str | None) -> str:
    return normalize_spaces(value).lower()


def load_template_catalog(path: Path = DEFAULT_TEMPLATES_PATH) -> dict[str, Any]:
    data = read_json(path)
    templates = data.get("templates", [])
    by_id = {template["id"]: template for template in templates}
    by_task_type: dict[str, list[dict[str, Any]]] = {}
    by_name: dict[str, list[dict[str, Any]]] = {}

    for template in templates:
        by_task_type.setdefault(normalize_task_type(template.get("task_type")), []).append(template)
        by_name.setdefault(normalize_name(template.get("name_ru")), []).append(template)

    return {
        "version": data.get("version"),
        "source": data.get("source"),
        "templates": templates,
        "by_id": by_id,
        "by_task_type": by_task_type,
        "by_name": by_name,
    }


def make_issue(code: str, message: str, **extra: Any) -> dict[str, Any]:
    issue = {
        "code": code,
        "severity": "error",
        "message": message,
    }
    issue.update(extra)
    return issue


def find_template_by_task_type(
    task_type: str | None,
    catalog: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not task_type:
        return None, []
    matches = catalog["by_task_type"].get(normalize_task_type(task_type), [])
    if len(matches) == 1:
        return matches[0], matches
    return None, matches


def resolve_task(task: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    task_template_id = normalize_spaces(task.get("task_template_id"))
    task_template_name = normalize_spaces(task.get("task_template_name"))
    task_type = normalize_spaces(task.get("task_type"))
    issues: list[dict[str, Any]] = []

    template = None
    if task_template_id:
        template = catalog["by_id"].get(task_template_id)
        if template is None:
            issues.append(
                make_issue(
                    "unknown_task_template_id",
                    "Task template ID is not present in data/task_templates.json.",
                    task_template_id=task_template_id,
                )
            )
    else:
        issues.append(
            make_issue(
                "missing_task_template_id",
                "Task is missing Task template ID.",
            )
        )
        template, matches = find_template_by_task_type(task_type, catalog)
        if len(matches) > 1:
            issues.append(
                make_issue(
                    "ambiguous_task_type",
                    "Task type matches multiple templates.",
                    task_type=task_type,
                    matching_template_ids=[item["id"] for item in matches],
                )
            )

    if template is None and task_type:
        inferred_template, matches = find_template_by_task_type(task_type, catalog)
        if inferred_template is not None:
            template = inferred_template
        elif not matches:
            issues.append(
                make_issue(
                    "unknown_task_type",
                    "Task type is not present in data/task_templates.json.",
                    task_type=task_type,
                )
            )

    if task_template_id and not re.fullmatch(r"TT-\d{3}", task_template_id):
        issues.append(
            make_issue(
                "invalid_task_template_id",
                "Task template ID must match TT-001 format.",
                task_template_id=task_template_id,
            )
        )

    if template is not None:
        expected_name = template.get("name_ru")
        expected_task_type = template.get("task_type")

        if template.get("status") == "not_ready":
            issues.append(
                make_issue(
                    "not_ready_task_template",
                    "Template is marked as not_ready and must not be used.",
                    task_template_id=template.get("id"),
                )
            )

        if not task_template_name:
            issues.append(
                make_issue(
                    "missing_task_template_name",
                    "Task is missing human-readable Task template name.",
                    task_template_id=template.get("id"),
                    expected=expected_name,
                )
            )
        elif normalize_name(task_template_name) != normalize_name(expected_name):
            issues.append(
                make_issue(
                    "task_template_name_mismatch",
                    "Task template name does not match catalog.",
                    task_template_id=template.get("id"),
                    expected=expected_name,
                    actual=task_template_name,
                )
            )

        if not task_type:
            issues.append(
                make_issue(
                    "missing_task_type",
                    "Task is missing machine Task type.",
                    task_template_id=template.get("id"),
                    expected=expected_task_type,
                )
            )
        elif normalize_task_type(task_type) != normalize_task_type(expected_task_type):
            issues.append(
                make_issue(
                    "task_type_mismatch",
                    "Task type does not match template ID in catalog.",
                    task_template_id=template.get("id"),
                    expected=expected_task_type,
                    actual=task_type,
                )
            )

    resolved = dict(task)
    resolved["task_template_id"] = task_template_id or None
    resolved["task_template_name"] = task_template_name or None
    resolved["task_type"] = task_type or None
    resolved["resolved_template_id"] = template.get("id") if template else None
    resolved["canonical_task_template_name"] = template.get("name_ru") if template else None
    resolved["canonical_task_type"] = template.get("task_type") if template else None
    resolved["category"] = template.get("category") if template else None
    resolved["data_needs"] = template.get("data_needs", []) if template else []
    resolved["status"] = "ok" if not issues else "issue"
    resolved["issues"] = issues
    return resolved


def task_rows_from_quest(quest: dict[str, Any]) -> list[dict[str, Any]]:
    if quest.get("tasks"):
        return list(quest["tasks"])

    task_numbers = quest.get("task_numbers", [])
    task_template_ids = quest.get("task_template_ids", [])
    task_template_names = quest.get("task_template_names", [])
    task_types = quest.get("task_types", [])
    task_count = max(
        len(task_numbers),
        len(task_template_ids),
        len(task_template_names),
        len(task_types),
        0,
    )

    tasks: list[dict[str, Any]] = []
    for index in range(task_count):
        tasks.append(
            {
                "task_number": task_numbers[index] if index < len(task_numbers) else None,
                "task_template_id": task_template_ids[index] if index < len(task_template_ids) else None,
                "task_template_name": task_template_names[index] if index < len(task_template_names) else None,
                "task_type": task_types[index] if index < len(task_types) else None,
            }
        )
    return tasks


def resolve_quest_plan(quest_plan: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    resolved_quests: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for quest_index, quest in enumerate(quest_plan.get("quests", []), start=1):
        resolved_quest = dict(quest)
        resolved_tasks = []
        for task_index, task in enumerate(task_rows_from_quest(quest), start=1):
            resolved_task = resolve_task(task, catalog)
            resolved_tasks.append(resolved_task)
            for issue in resolved_task["issues"]:
                issues.append(
                    {
                        **issue,
                        "quest_index": quest_index,
                        "classname_quests": quest.get("classname_quests"),
                        "task_index": task_index,
                        "task_number": task.get("task_number"),
                    }
                )
        resolved_quest["tasks"] = resolved_tasks
        resolved_quests.append(resolved_quest)

    tasks_found = sum(len(quest.get("tasks", [])) for quest in resolved_quests)
    resolved_tasks = sum(
        1
        for quest in resolved_quests
        for task in quest.get("tasks", [])
        if task.get("resolved_template_id") and task.get("status") == "ok"
    )

    return {
        "quests": resolved_quests,
        "issues": issues,
        "summary": {
            "quests_found": len(resolved_quests),
            "tasks_found": tasks_found,
            "resolved_tasks": resolved_tasks,
            "issues": len(issues),
        },
        "templates_summary": {
            "templates_found": len(catalog["templates"]),
            "not_ready_templates": [
                template["id"]
                for template in catalog["templates"]
                if template.get("status") == "not_ready"
            ],
        },
    }


def render_preview(resolved_plan: dict[str, Any]) -> str:
    lines = [
        "# Quest Plan Template Resolution",
        "",
        f"Quests found: {resolved_plan['summary']['quests_found']}",
        f"Tasks found: {resolved_plan['summary']['tasks_found']}",
        f"Resolved tasks: {resolved_plan['summary']['resolved_tasks']}",
        f"Issues: {resolved_plan['summary']['issues']}",
        "",
    ]

    for quest in resolved_plan["quests"]:
        lines.extend(
            [
                f"## {quest.get('classname_quests') or 'Quest'}",
                "",
                "| № | Status | Template ID | Template name | Task type |",
                "|---|--------|-------------|---------------|-----------|",
            ]
        )
        for task in quest.get("tasks", []):
            lines.append(
                "| "
                f"{task.get('task_number') or ''} | "
                f"{task.get('status') or ''} | "
                f"`{task.get('task_template_id') or ''}` | "
                f"{task.get('task_template_name') or ''} | "
                f"`{task.get('task_type') or ''}` |"
            )
        lines.append("")

    if resolved_plan["issues"]:
        lines.extend(["## Issues", ""])
        for issue in resolved_plan["issues"]:
            lines.append(
                f"- `{issue['code']}` quest={issue.get('classname_quests')} "
                f"task={issue.get('task_number')}: {issue['message']}"
            )
        lines.append("")

    return "\n".join(lines)


def resolve_file(
    input_path: Path,
    templates_path: Path,
    output_json_path: Path,
    output_preview_path: Path,
) -> dict[str, Any]:
    catalog = load_template_catalog(templates_path)
    resolved_plan = resolve_quest_plan(read_json(input_path), catalog)
    write_json(output_json_path, resolved_plan)
    output_preview_path.parent.mkdir(parents=True, exist_ok=True)
    output_preview_path.write_text(render_preview(resolved_plan), encoding="utf-8")
    return resolved_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve and validate stage 3 task template choices.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Quest plan JSON from src/parse_stage3.py. Default: output/quest_plan.json",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        default=DEFAULT_TEMPLATES_PATH,
        help="Task template catalog JSON. Default: data/task_templates.json",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON_PATH,
        help="Output resolved quest plan JSON path.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=DEFAULT_OUTPUT_PREVIEW_PATH,
        help="Output human-readable preview path.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Сначала запусти: python src/parse_stage3.py input/stage3_quests.txt")
        return 1

    resolved_plan = resolve_file(args.input, args.templates, args.output_json, args.preview)
    print(f"quests found: {resolved_plan['summary']['quests_found']}")
    print(f"tasks found: {resolved_plan['summary']['tasks_found']}")
    print(f"resolved tasks: {resolved_plan['summary']['resolved_tasks']}")
    print(f"issues: {resolved_plan['summary']['issues']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    return 0 if resolved_plan["summary"]["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
