from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "quest_plan.json"
DEFAULT_OVERRIDES_PATH = PROJECT_ROOT / "input" / "manual_overrides.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "output" / "quest_plan.overridden.json"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "output" / "manual_overrides_report.md"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_tasks_from_arrays(quest: dict[str, Any]) -> list[dict[str, Any]]:
    if quest.get("tasks"):
        return [dict(task) for task in quest["tasks"]]

    task_numbers = quest.get("task_numbers", [])
    task_template_ids = quest.get("task_template_ids", [])
    task_template_names = quest.get("task_template_names", [])
    task_types = quest.get("task_types", [])
    count = max(len(task_numbers), len(task_template_ids), len(task_template_names), len(task_types), 0)
    tasks: list[dict[str, Any]] = []
    for index in range(count):
        tasks.append(
            {
                "task_number": task_numbers[index] if index < len(task_numbers) else None,
                "task_template_id": task_template_ids[index] if index < len(task_template_ids) else None,
                "task_template_name": task_template_names[index] if index < len(task_template_names) else None,
                "task_type": task_types[index] if index < len(task_types) else None,
            }
        )
    return tasks


def sync_quest_task_arrays(quest: dict[str, Any]) -> None:
    tasks = split_tasks_from_arrays(quest)
    quest["tasks"] = tasks
    quest["task_numbers"] = [task.get("task_number") for task in tasks]
    quest["task_template_ids"] = [task.get("task_template_id") for task in tasks]
    quest["task_template_names"] = [task.get("task_template_name") for task in tasks]
    quest["task_types"] = [task.get("task_type") for task in tasks]


def load_overrides(path: Path) -> list[dict[str, Any]]:
    data = read_json(path)
    if isinstance(data, list):
        return data
    overrides = data.get("overrides", [])
    if not isinstance(overrides, list):
        raise ValueError("manual_overrides.json must contain an overrides list.")
    return overrides


def find_quest(quests: list[dict[str, Any]], override: dict[str, Any]) -> tuple[int | None, dict[str, Any] | None]:
    classname = override.get("classname_quests")
    quest_number = override.get("quest_number")
    for index, quest in enumerate(quests, start=1):
        if classname and quest.get("classname_quests") == classname:
            return index, quest
        if quest_number is not None and quest.get("quest_number") == quest_number:
            return index, quest
    return None, None


def find_task(quest: dict[str, Any], task_number: Any) -> tuple[int | None, dict[str, Any] | None]:
    sync_quest_task_arrays(quest)
    for index, task in enumerate(quest.get("tasks", []), start=1):
        if task.get("task_number") == task_number:
            return index, task
    return None, None


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def apply_replace_template(task: dict[str, Any], replace_template: dict[str, Any]) -> list[str]:
    changed: list[str] = []
    mapping = {
        "task_template_id": "task_template_id",
        "task_template_name": "task_template_name",
        "task_type": "task_type",
    }
    for source_key, target_key in mapping.items():
        if source_key in replace_template:
            task[target_key] = replace_template[source_key]
            changed.append(target_key)
    return changed


def apply_stage4_override(task: dict[str, Any], override: dict[str, Any], override_index: int) -> list[str]:
    manual = dict(task.get("manual_override") or {})
    changed: list[str] = []

    if "avoid_candidates" in override:
        manual["avoid_candidates"] = normalize_list(override.get("avoid_candidates"))
        changed.append("avoid_candidates")
    if "prefer_candidates" in override:
        manual["prefer_candidates"] = normalize_list(override.get("prefer_candidates"))
        changed.append("prefer_candidates")

    force_candidate = override.get("force_candidate_id", override.get("force_candidate"))
    if force_candidate:
        manual["force_candidate_id"] = str(force_candidate)
        changed.append("force_candidate_id")

    instruction = override.get("instruction", override.get("prefer_instruction"))
    if instruction:
        manual["instruction"] = str(instruction)
        changed.append("instruction")

    reason = override.get("reason")
    if reason:
        manual["reason"] = str(reason)

    if changed:
        manual["source_override_index"] = override_index
        task["manual_override"] = manual
    return changed


def apply_overrides(quest_plan: dict[str, Any], overrides: list[dict[str, Any]]) -> dict[str, Any]:
    output = json.loads(json.dumps(quest_plan, ensure_ascii=False))
    quests = output.get("quests", [])
    issues: list[dict[str, Any]] = []
    applied: list[dict[str, Any]] = []

    for override_index, override in enumerate(overrides, start=1):
        quest_index, quest = find_quest(quests, override)
        if quest is None:
            issues.append(
                {
                    "code": "quest_not_found",
                    "override_index": override_index,
                    "classname_quests": override.get("classname_quests"),
                    "quest_number": override.get("quest_number"),
                    "message": "Override target quest was not found.",
                }
            )
            continue

        task_number = override.get("task_number")
        task_index, task = find_task(quest, task_number)
        if task is None:
            issues.append(
                {
                    "code": "task_not_found",
                    "override_index": override_index,
                    "classname_quests": quest.get("classname_quests"),
                    "task_number": task_number,
                    "message": "Override target task was not found.",
                }
            )
            continue

        changed: list[str] = []
        if "replace_template" in override:
            replace_template = override.get("replace_template")
            if not isinstance(replace_template, dict):
                issues.append(
                    {
                        "code": "invalid_replace_template",
                        "override_index": override_index,
                        "classname_quests": quest.get("classname_quests"),
                        "task_number": task_number,
                        "message": "replace_template must be an object.",
                    }
                )
            else:
                changed.extend(apply_replace_template(task, replace_template))

        changed.extend(apply_stage4_override(task, override, override_index))
        sync_quest_task_arrays(quest)

        if changed:
            applied.append(
                {
                    "override_index": override_index,
                    "quest_index": quest_index,
                    "classname_quests": quest.get("classname_quests"),
                    "task_index": task_index,
                    "task_number": task_number,
                    "changed": changed,
                }
            )
        else:
            issues.append(
                {
                    "code": "empty_override",
                    "override_index": override_index,
                    "classname_quests": quest.get("classname_quests"),
                    "task_number": task_number,
                    "message": "Override did not contain any supported changes.",
                }
            )

    output["manual_overrides"] = {
        "applied": applied,
        "issues": issues,
        "summary": {
            "overrides_found": len(overrides),
            "applied": len(applied),
            "issues": len(issues),
        },
    }
    output.setdefault("summary", {})
    output["summary"]["manual_overrides_applied"] = len(applied)
    output["summary"]["manual_override_issues"] = len(issues)
    return output


def render_report(overridden_plan: dict[str, Any]) -> str:
    manual = overridden_plan.get("manual_overrides", {})
    summary = manual.get("summary", {})
    lines = [
        "# Manual Overrides Report",
        "",
        f"Overrides found: {summary.get('overrides_found', 0)}",
        f"Applied: {summary.get('applied', 0)}",
        f"Issues: {summary.get('issues', 0)}",
        "",
        "## Applied",
        "",
    ]

    applied = manual.get("applied", [])
    if not applied:
        lines.append("Нет примененных правок.")
    for item in applied:
        lines.append(
            "- "
            f"override {item.get('override_index')}: "
            f"{item.get('classname_quests')} task {item.get('task_number')} "
            f"changed {', '.join(item.get('changed', []))}"
        )

    lines.extend(["", "## Issues", ""])
    issues = manual.get("issues", [])
    if not issues:
        lines.append("Ошибок применения overrides нет.")
    for issue in issues:
        lines.append(
            "- "
            f"`{issue.get('code')}` override {issue.get('override_index')}: "
            f"{issue.get('message')}"
        )
    lines.append("")
    return "\n".join(lines)


def apply_overrides_file(
    input_path: Path,
    overrides_path: Path,
    output_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    overrides = load_overrides(overrides_path)
    overridden_plan = apply_overrides(read_json(input_path), overrides)
    write_json(output_path, overridden_plan)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(overridden_plan), encoding="utf-8")
    return overridden_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply manual quest/task overrides to parsed stage 3 quest plan.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Input quest_plan.json from src/parse_stage3.py.",
    )
    parser.add_argument(
        "overrides",
        nargs="?",
        type=Path,
        default=DEFAULT_OVERRIDES_PATH,
        help="Manual overrides JSON. Default: input/manual_overrides.json",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output overridden quest plan JSON.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Output Markdown report.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Сначала запусти: python src/parse_stage3.py input/stage3_quests.txt")
        return 1
    if not args.overrides.exists():
        print(f"overrides file not found: {args.overrides}")
        print("Создай input/manual_overrides.json или используй input/manual_overrides.example.json как основу.")
        return 1

    overridden_plan = apply_overrides_file(args.input, args.overrides, args.output_json, args.report)
    summary = overridden_plan["manual_overrides"]["summary"]
    print(f"overrides found: {summary['overrides_found']}")
    print(f"applied: {summary['applied']}")
    print(f"issues: {summary['issues']}")
    print(f"json written: {args.output_json}")
    print(f"report written: {args.report}")
    return 0 if summary["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
