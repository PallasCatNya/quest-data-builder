import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.task_type_resolver import (
    load_template_catalog,
    main,
    resolve_quest_plan,
    resolve_task,
)


def quest_plan_with_task(task: dict[str, object]) -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверочный квест",
                "quest_number": 1,
                "task_numbers": [task.get("task_number", 1)],
                "tasks": [task],
            }
        ],
        "issues": [],
        "summary": {"quests_found": 1, "tasks_found": 1, "issues": 0},
    }


class TaskTypeResolverTests(unittest.TestCase):
    def test_loads_actual_template_catalog(self) -> None:
        catalog = load_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")

        self.assertEqual(len(catalog["templates"]), 35)
        self.assertEqual(catalog["by_id"]["TT-020"]["name_ru"], "Уборка конкретного мусора в гостях")
        self.assertEqual(catalog["by_id"]["TT-035"]["status"], "not_ready")

    def test_resolves_valid_task(self) -> None:
        catalog = load_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")
        resolved = resolve_task(
            {
                "task_number": 1,
                "task_template_id": "TT-020",
                "task_template_name": "Уборка конкретного мусора в гостях",
                "task_type": "garbage classname in_guest",
            },
            catalog,
        )

        self.assertEqual(resolved["status"], "ok")
        self.assertEqual(resolved["resolved_template_id"], "TT-020")
        self.assertEqual(resolved["canonical_task_type"], "garbage classname in_guest")
        self.assertEqual(resolved["issues"], [])

    def test_reports_name_and_type_mismatch(self) -> None:
        catalog = load_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")
        resolved = resolve_task(
            {
                "task_number": 1,
                "task_template_id": "TT-020",
                "task_template_name": "Уборка конкретного мусора дома",
                "task_type": "garbage classname",
            },
            catalog,
        )

        self.assertEqual(resolved["status"], "issue")
        self.assertEqual(
            [issue["code"] for issue in resolved["issues"]],
            ["task_template_name_mismatch", "task_type_mismatch"],
        )

    def test_reports_not_ready_template(self) -> None:
        catalog = load_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")
        result = resolve_quest_plan(
            quest_plan_with_task(
                {
                    "task_number": 1,
                    "task_template_id": "TT-035",
                    "task_template_name": "Следы с ресурсами",
                    "task_type": "not_ready",
                }
            ),
            catalog,
        )

        self.assertEqual(result["summary"]["issues"], 1)
        self.assertEqual(result["issues"][0]["code"], "not_ready_task_template")
        self.assertEqual(result["summary"]["resolved_tasks"], 0)

    def test_cli_writes_resolved_json_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "quest_plan.json"
            output_json = root / "quest_plan.resolved.json"
            preview = root / "quest_plan.resolved.preview.md"
            input_path.write_text(
                json.dumps(
                    quest_plan_with_task(
                        {
                            "task_number": 1,
                            "task_template_id": "TT-011",
                            "task_template_name": "Получить элемент коллекции (зависит от редкости)",
                            "task_type": "get_asset Collection",
                        }
                    ),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    str(input_path),
                    "--templates",
                    str(PROJECT_ROOT / "data" / "task_templates.json"),
                    "--output-json",
                    str(output_json),
                    "--preview",
                    str(preview),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_json.exists())
            self.assertTrue(preview.exists())
            data = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["resolved_tasks"], 1)
            self.assertIn("TT-011", preview.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
