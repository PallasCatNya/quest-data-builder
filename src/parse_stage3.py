from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "input" / "stage3_quests.txt"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "quest_plan.json"
DEFAULT_OUTPUT_PREVIEW_PATH = PROJECT_ROOT / "output" / "quest_plan.preview.md"


@dataclass
class QuestPlan:
    classname_quests: str | None = None
    title_quest: str | None = None
    quest_number: int | None = None
    task_numbers: list[int] | None = None
    task_template_ids: list[str] | None = None
    task_template_names: list[str] | None = None
    task_types: list[str] | None = None
    description: str | None = None
    congratulation: str | None = None
    character: str | None = None
    raw_text: str = ""

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["task_numbers"] = data["task_numbers"] or []
        data["task_template_ids"] = data["task_template_ids"] or []
        data["task_template_names"] = data["task_template_names"] or []
        data["task_types"] = data["task_types"] or []
        data["tasks"] = build_task_rows(
            data["task_numbers"],
            data["task_template_ids"],
            data["task_template_names"],
            data["task_types"],
        )
        return data


FIELD_ALIASES = {
    "Classname quests": "classname_quests",
    "title_quest": "title_quest",
    "№ quest": "quest_number",
    "в„– quest": "quest_number",
    "# quest": "quest_number",
    "No quest": "quest_number",
    "№ task": "task_numbers",
    "в„– task": "task_numbers",
    "# task": "task_numbers",
    "No task": "task_numbers",
    "Task template ID": "task_template_ids",
    "Task template IDs": "task_template_ids",
    "Task template id": "task_template_ids",
    "Task template ids": "task_template_ids",
    "Task template name": "task_template_names",
    "Task template names": "task_template_names",
    "Task type": "task_types",
    "description": "description",
    "congratulation": "congratulation",
    "Character": "character",
}


REQUIRED_FIELDS = [
    "classname_quests",
    "title_quest",
    "quest_number",
    "task_numbers",
    "task_template_ids",
    "task_template_names",
    "task_types",
    "description",
    "congratulation",
    "character",
]


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="latin-1")


def clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def parse_int_list(value: str) -> list[int]:
    return [int(number) for number in re.findall(r"\d+", value)]


def parse_first_int(value: str) -> int | None:
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def split_slash_list(value: str) -> list[str]:
    return [part.strip() for part in value.split("/") if part.strip()]


def build_task_rows(
    task_numbers: list[int],
    task_template_ids: list[str],
    task_template_names: list[str],
    task_types: list[str],
) -> list[dict[str, Any]]:
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


def split_quest_blocks(text: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in text.splitlines():
        if line.strip().startswith("Classname quests:"):
            if current:
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)

    if current:
        blocks.append(current)

    return ["\n".join(block).strip() for block in blocks if "\n".join(block).strip()]


def parse_quest_block(block: str) -> QuestPlan:
    quest = QuestPlan(raw_text=block)

    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        raw_key, raw_value = line.split(":", 1)
        key = raw_key.strip()
        value = clean_value(raw_value)
        field_name = FIELD_ALIASES.get(key)
        if field_name is None:
            continue

        if field_name == "quest_number":
            setattr(quest, field_name, parse_first_int(value))
        elif field_name == "task_numbers":
            setattr(quest, field_name, parse_int_list(value))
        elif field_name in ("task_template_ids", "task_template_names", "task_types"):
            setattr(quest, field_name, split_slash_list(value))
        else:
            setattr(quest, field_name, value)

    task_count = max(
        len(quest.task_template_ids or []),
        len(quest.task_template_names or []),
        len(quest.task_types or []),
        0,
    )
    if task_count and not quest.task_numbers:
        quest.task_numbers = list(range(1, task_count + 1))

    return quest


def parse_stage3_text(text: str) -> list[QuestPlan]:
    return [parse_quest_block(block) for block in split_quest_blocks(text)]


def find_quest_issues(quests: list[QuestPlan]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, quest in enumerate(quests, start=1):
        data = quest.to_json()
        for field_name in REQUIRED_FIELDS:
            value = data.get(field_name)
            if value in (None, "", []):
                issues.append(
                    {
                        "code": "missing_field",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "field": field_name,
                        "message": f"Quest is missing required field: {field_name}",
                    }
                )

        task_counts = {
            "task_numbers": len(quest.task_numbers or []),
            "task_template_ids": len(quest.task_template_ids or []),
            "task_template_names": len(quest.task_template_names or []),
            "task_types": len(quest.task_types or []),
        }
        present_task_counts = {field: count for field, count in task_counts.items() if count > 0}
        if len(set(present_task_counts.values())) > 1:
            issues.append(
                {
                    "code": "task_count_mismatch",
                    "quest_index": index,
                    "classname_quests": quest.classname_quests,
                    "task_counts": present_task_counts,
                    "message": "Number of task numbers, template IDs, template names and task types must match.",
                }
            )

        for task_template_id in quest.task_template_ids or []:
            if not re.fullmatch(r"TT-\d{3}", task_template_id):
                issues.append(
                    {
                        "code": "invalid_task_template_id",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "task_template_id": task_template_id,
                        "message": "Task template ID must match TT-001 format.",
                    }
                )
            if task_template_id == "TT-035":
                issues.append(
                    {
                        "code": "not_ready_task_template",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "task_template_id": task_template_id,
                        "message": "TT-035 is marked as not_ready and must not be used.",
                    }
                )

    return issues


def build_quest_plan(text: str) -> dict[str, Any]:
    quests = parse_stage3_text(text)
    quest_json = [quest.to_json() for quest in quests]
    issues = find_quest_issues(quests)
    return {
        "quests": quest_json,
        "issues": issues,
        "summary": {
            "quests_found": len(quests),
            "tasks_found": sum(len(quest["tasks"]) for quest in quest_json),
            "issues": len(issues),
        },
    }


def render_preview(quest_plan: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Quest Plan Preview",
        "",
        f"Quests found: {quest_plan['summary']['quests_found']}",
        f"Tasks found: {quest_plan['summary'].get('tasks_found', 0)}",
        f"Issues: {quest_plan['summary']['issues']}",
        "",
    ]

    for index, quest in enumerate(quest_plan["quests"], start=1):
        title = quest.get("title_quest") or "Без названия"
        lines.extend(
            [
                f"## Quest {quest.get('quest_number') or index} — {title}",
                "",
                f"- classname_quests: `{quest.get('classname_quests')}`",
                f"- character: {quest.get('character') or ''}",
                f"- task_numbers: {', '.join(str(number) for number in quest.get('task_numbers', []))}",
                "",
                "| № | Template ID | Template name | Task type |",
                "|---|-------------|---------------|-----------|",
            ]
        )
        for task in quest.get("tasks", []):
            lines.append(
                "| "
                f"{task.get('task_number') or ''} | "
                f"`{task.get('task_template_id') or ''}` | "
                f"{task.get('task_template_name') or ''} | "
                f"`{task.get('task_type') or ''}` |"
            )
        lines.extend(
            [
                "",
                f"Description: {quest.get('description') or ''}",
                "",
                f"Congratulation: {quest.get('congratulation') or ''}",
                "",
            ]
        )

    if quest_plan["issues"]:
        lines.extend(["## Issues", ""])
        for issue in quest_plan["issues"]:
            lines.append(
                f"- `{issue['code']}` quest={issue.get('classname_quests')} field={issue.get('field', '')}: {issue['message']}"
            )
        lines.append("")

    return "\n".join(lines)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_file(input_path: Path, output_json_path: Path, output_preview_path: Path) -> dict[str, Any]:
    quest_plan = build_quest_plan(read_text(input_path))
    write_json(output_json_path, quest_plan)
    output_preview_path.parent.mkdir(parents=True, exist_ok=True)
    output_preview_path.write_text(render_preview(quest_plan), encoding="utf-8")
    return quest_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse stage 3 quest text into QuestPlan JSON.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Stage 3 text input file. Default: input/stage3_quests.txt",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON_PATH,
        help="Output quest plan JSON path.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=DEFAULT_OUTPUT_PREVIEW_PATH,
        help="Output human-readable preview path.",
    )
    args = parser.parse_args(argv)

    (PROJECT_ROOT / "input").mkdir(exist_ok=True)
    (PROJECT_ROOT / "output").mkdir(exist_ok=True)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Создай input/stage3_quests.txt или передай путь к файлу этапа 3 первым аргументом.")
        return 1

    quest_plan = parse_file(args.input, args.output_json, args.preview)
    print(f"quests found: {quest_plan['summary']['quests_found']}")
    print(f"tasks found: {quest_plan['summary']['tasks_found']}")
    print(f"issues: {quest_plan['summary']['issues']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    return 0 if quest_plan["summary"]["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
