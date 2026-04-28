import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.apply_overrides import apply_overrides, main


def quest_plan() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверочный квест",
                "quest_number": 1,
                "task_numbers": [1, 2],
                "task_template_ids": ["TT-020", "TT-011"],
                "task_template_names": [
                    "Уборка конкретного мусора в гостях",
                    "Получить элемент коллекции (зависит от редкости)",
                ],
                "task_types": ["garbage classname in_guest", "get_asset Collection"],
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-020",
                        "task_template_name": "Уборка конкретного мусора в гостях",
                        "task_type": "garbage classname in_guest",
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-011",
                        "task_template_name": "Получить элемент коллекции (зависит от редкости)",
                        "task_type": "get_asset Collection",
                    },
                ],
            }
        ],
        "issues": [],
        "summary": {"quests_found": 1, "tasks_found": 2, "issues": 0},
    }


class ApplyOverridesTests(unittest.TestCase):
    def test_replaces_stage3_template_and_syncs_arrays(self) -> None:
        result = apply_overrides(
            quest_plan(),
            [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "task_number": 2,
                    "replace_template": {
                        "task_template_id": "TT-026",
                        "task_template_name": "Загадка на коллекцию (зависит от редкости)",
                        "task_type": "get_asset Collection mystery",
                    },
                }
            ],
        )

        quest = result["quests"][0]
        task = quest["tasks"][1]
        self.assertEqual(task["task_template_id"], "TT-026")
        self.assertEqual(task["task_template_name"], "Загадка на коллекцию (зависит от редкости)")
        self.assertEqual(task["task_type"], "get_asset Collection mystery")
        self.assertEqual(quest["task_template_ids"], ["TT-020", "TT-026"])
        self.assertEqual(result["manual_overrides"]["summary"]["applied"], 1)
        self.assertEqual(result["manual_overrides"]["summary"]["issues"], 0)

    def test_attaches_stage4_candidate_instructions(self) -> None:
        result = apply_overrides(
            quest_plan(),
            [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "task_number": 1,
                    "avoid_candidates": ["garbage:Ashes"],
                    "prefer_candidates": ["garbage:BrokenPlate"],
                    "prefer_instruction": "Выбери вариант, связанный с посудой.",
                }
            ],
        )

        manual = result["quests"][0]["tasks"][0]["manual_override"]
        self.assertEqual(manual["avoid_candidates"], ["garbage:Ashes"])
        self.assertEqual(manual["prefer_candidates"], ["garbage:BrokenPlate"])
        self.assertEqual(manual["instruction"], "Выбери вариант, связанный с посудой.")

    def test_reports_missing_task(self) -> None:
        result = apply_overrides(
            quest_plan(),
            [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "task_number": 99,
                    "avoid_candidates": ["garbage:Ashes"],
                }
            ],
        )

        self.assertEqual(result["manual_overrides"]["summary"]["issues"], 1)
        self.assertEqual(result["manual_overrides"]["issues"][0]["code"], "task_not_found")

    def test_cli_writes_overridden_plan_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "quest_plan.json"
            overrides_path = root / "manual_overrides.json"
            output_path = root / "quest_plan.overridden.json"
            report_path = root / "manual_overrides_report.md"
            input_path.write_text(json.dumps(quest_plan(), ensure_ascii=False), encoding="utf-8")
            overrides_path.write_text(
                json.dumps(
                    {
                        "overrides": [
                            {
                                "classname_quests": "Event_2026_Story_1",
                                "task_number": 1,
                                "avoid_candidates": ["garbage:Ashes"],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    str(input_path),
                    str(overrides_path),
                    "--output-json",
                    str(output_path),
                    "--report",
                    str(report_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertTrue(report_path.exists())
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["manual_overrides"]["summary"]["applied"], 1)


if __name__ == "__main__":
    unittest.main()
