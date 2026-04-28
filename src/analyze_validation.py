from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_index import build_validation_summary_markdown


DATA_DIR_NAME = "data"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def analyze(project_root: Path) -> Path:
    data_dir = project_root / DATA_DIR_NAME
    validation_report = load_json(data_dir / "validation_report.json")
    quest_ready_index = load_json(data_dir / "quest_ready_index.json")
    quest_ready = {
        "non_critical_issues": load_json(data_dir / "non_critical_issues.json"),
        "critical_issues": load_json(data_dir / "critical_issues.json"),
        "excluded_entities": load_json(data_dir / "excluded_entities.json"),
        "summary": quest_ready_index["summary"],
    }

    output_path = data_dir / "validation_summary.md"
    output_path.write_text(
        build_validation_summary_markdown(validation_report, quest_ready),
        encoding="utf-8",
    )
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze quest-ready validation outputs.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing generated data/*.json files.",
    )
    args = parser.parse_args(argv)

    output_path = analyze(args.project_root)
    print(f"validation summary written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
