from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DATA_DIR_NAME = "data"
RAW_DIR_NAME = "raw"
SUPPORTED_SUFFIXES = {".json", ".js"}
IGNORED_MISSING_COLLECTION_FRAGMENTS = ("Cocoon", "Web", "Common", "Mold")


@dataclass
class ValidationReport:
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)

    def error(self, issue_code: str, message: str, **context: Any) -> None:
        entry = dict(context)
        entry["code"] = issue_code
        entry["message"] = message
        self.errors.append(entry)

    def warning(self, issue_code: str, message: str, **context: Any) -> None:
        entry = dict(context)
        entry["code"] = issue_code
        entry["message"] = message
        self.warnings.append(entry)

    def to_json(self) -> dict[str, Any]:
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
        }


def iter_data_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []

    return (
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and (path.suffix.lower() in SUPPORTED_SUFFIXES or path.name.endswith(".proto.js"))
    )


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="latin-1")


def strip_js_comments(text: str) -> str:
    result: list[str] = []
    i = 0
    in_string: str | None = None
    escaped = False

    while i < len(text):
        ch = text[i]
        next_ch = text[i + 1] if i + 1 < len(text) else ""

        if in_string:
            result.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch in {"'", '"'}:
            in_string = ch
            result.append(ch)
            i += 1
            continue

        if ch == "/" and next_ch == "/":
            i += 2
            while i < len(text) and text[i] not in {"\n", "\r"}:
                i += 1
            continue

        if ch == "/" and next_ch == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                result.append("\n" if text[i] in {"\n", "\r"} else " ")
                i += 1
            i += 2
            continue

        result.append(ch)
        i += 1

    return "".join(result)


def remove_trailing_commas(text: str) -> str:
    result: list[str] = []
    i = 0
    in_string: str | None = None
    escaped = False

    while i < len(text):
        ch = text[i]

        if in_string:
            result.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue

        if ch in {"'", '"'}:
            in_string = ch
            result.append(ch)
            i += 1
            continue

        if ch == ",":
            j = i + 1
            while j < len(text) and text[j].isspace():
                j += 1
            if j < len(text) and text[j] in {"]", "}"}:
                i += 1
                continue

        result.append(ch)
        i += 1

    return "".join(result)


def load_json_values(path: Path) -> list[Any]:
    text = remove_trailing_commas(strip_js_comments(read_text(path))).strip()
    if not text:
        return []

    try:
        return [json.loads(text)]
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    values: list[Any] = []
    i = 0
    while i < len(text):
        if text[i] not in {"{", "["}:
            i += 1
            continue
        try:
            value, end = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            i += 1
            continue
        values.append(value)
        i = end

    if values:
        return values
    raise ValueError("No JSON object or array found")


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for item in value:
            yield from iter_dicts(item)


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def title_or_none(value: Any) -> Any:
    if value is None or value == "":
        return None
    return value


def normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    if isinstance(value, str) and value:
        return [value]
    return []


def location_summary(location: dict[str, Any]) -> dict[str, Any]:
    return {
        "code": location.get("code"),
        "title": location.get("title"),
        "tags": location.get("tags"),
    }


def collect_locations(raw_dir: Path, project_root: Path, report: ValidationReport) -> dict[str, Any]:
    locations_by_code: dict[str, Any] = {}

    for path in iter_data_files(raw_dir / "locations"):
        source_file = relative_path(path, project_root)
        try:
            values = load_json_values(path)
        except Exception as exc:
            report.error(
                "parse_error",
                "Could not parse location file",
                file=source_file,
                detail=str(exc),
            )
            continue

        for value in values:
            for obj in iter_dicts(value):
                if "code" not in obj:
                    continue

                code = str(obj["code"])
                if code in locations_by_code:
                    report.error(
                        "duplicate_location_code",
                        "Duplicate location code",
                        location_code=code,
                        first_file=locations_by_code[code].get("source_file"),
                        duplicate_file=source_file,
                    )
                    continue

                title = title_or_none(obj.get("title"))
                tags = obj.get("tags")
                garbage_assets = normalize_string_list(obj.get("garbage_assets"))

                if title is None:
                    report.warning(
                        "location_missing_title",
                        "Location has no title",
                        location_code=code,
                        file=source_file,
                    )
                if not tags:
                    report.warning(
                        "location_missing_tags",
                        "Location has no tags",
                        location_code=code,
                        title=title,
                        file=source_file,
                    )
                if not garbage_assets:
                    report.warning(
                        "location_empty_garbage_assets",
                        "Location has empty or null garbage_assets",
                        location_code=code,
                        title=title,
                        file=source_file,
                    )

                locations_by_code[code] = {
                    "code": code,
                    "title": title,
                    "tags": tags,
                    "garbage_assets": garbage_assets,
                    "source_file": source_file,
                }

    return locations_by_code


def collect_assets(
    raw_dir: Path,
    folder_name: str,
    project_root: Path,
    report: ValidationReport,
    asset_type: str,
    predicate: Any,
    fields: list[str],
) -> dict[str, Any]:
    by_classname: dict[str, Any] = {}

    for path in iter_data_files(raw_dir / folder_name):
        source_file = relative_path(path, project_root)
        try:
            values = load_json_values(path)
        except Exception as exc:
            report.error(
                "parse_error",
                f"Could not parse {asset_type} file",
                file=source_file,
                detail=str(exc),
            )
            continue

        for value in values:
            for obj in iter_dicts(value):
                if not predicate(obj):
                    continue

                classname = obj.get("classname")
                if not classname:
                    report.warning(
                        f"{asset_type}_missing_classname",
                        f"{asset_type} object has no classname",
                        file=source_file,
                    )
                    continue

                classname = str(classname)
                if classname in by_classname:
                    report.error(
                        f"duplicate_{asset_type}_classname",
                        f"Duplicate {asset_type} classname",
                        classname=classname,
                        first_file=by_classname[classname].get("source_file"),
                        duplicate_file=source_file,
                    )
                    continue

                record = {field_name: obj.get(field_name) for field_name in fields}
                record["classname"] = classname
                record["title"] = title_or_none(obj.get("title"))
                record["source_file"] = source_file

                if record["title"] is None:
                    report.warning(
                        f"{asset_type}_missing_title",
                        f"{asset_type} object has no title",
                        classname=classname,
                        file=source_file,
                    )

                by_classname[classname] = record

    return by_classname


def build_locations_by_garbage(
    locations_by_code: dict[str, Any],
    garbage_by_classname: dict[str, Any],
    report: ValidationReport,
) -> dict[str, list[dict[str, Any]]]:
    locations_by_garbage: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for location in locations_by_code.values():
        for garbage_classname in location.get("garbage_assets", []):
            locations_by_garbage[garbage_classname].append(location_summary(location))
            if garbage_classname not in garbage_by_classname:
                report.warning(
                    "location_unknown_garbage",
                    "Location has garbage_assets entry missing from garbage_by_classname",
                    location_code=location.get("code"),
                    location_title=location.get("title"),
                    garbage_classname=garbage_classname,
                )

    used_garbage = set(locations_by_garbage)
    for garbage_classname, garbage in garbage_by_classname.items():
        if garbage_classname not in used_garbage:
            report.warning(
                "garbage_unused_in_locations",
                "Garbage exists but is not used in any location",
                garbage_classname=garbage_classname,
                garbage_title=garbage.get("title"),
                file=garbage.get("source_file"),
            )

    return dict(sorted(locations_by_garbage.items()))


def iter_reward_assets(value: Any, reward_group_p: Any = None) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if "asset" in value:
            yield {
                "asset": value.get("asset"),
                "reward_group_p": reward_group_p,
                "asset_p": value.get("p"),
            }
            for key, child in value.items():
                if key != "asset":
                    yield from iter_reward_assets(child, reward_group_p)
            return

        next_group_p = value.get("p", reward_group_p)
        for child in value.values():
            yield from iter_reward_assets(child, next_group_p)
    elif isinstance(value, list):
        for item in value:
            yield from iter_reward_assets(item, reward_group_p)


COLLECTION_ASSET_RE = re.compile(r"(Collection|Col\d+$)")


def looks_like_collection_asset(asset: Any) -> bool:
    return isinstance(asset, str) and bool(COLLECTION_ASSET_RE.search(asset))


def build_drops(
    garbage_by_classname: dict[str, Any],
    flowers_by_classname: dict[str, Any],
    collections_by_classname: dict[str, Any],
    locations_by_garbage: dict[str, list[dict[str, Any]]],
    report: ValidationReport,
) -> tuple[list[dict[str, Any]], int, int, list[dict[str, Any]]]:
    drops: list[dict[str, Any]] = []
    missing_collection_issues: list[dict[str, Any]] = []
    garbage_drop_count = 0
    flower_drop_count = 0

    for garbage in garbage_by_classname.values():
        for mode, reward_field in (("home", "rand_reward"), ("guest", "rand_reward_in_guest")):
            for reward_asset in iter_reward_assets(garbage.get(reward_field)):
                asset = reward_asset["asset"]
                if asset in collections_by_classname:
                    collection = collections_by_classname[asset]
                    drops.append(
                        {
                            "source_type": "garbage",
                            "source_classname": garbage.get("classname"),
                            "source_title": garbage.get("title"),
                            "source_id": garbage.get("id"),
                            "garbage_classname": garbage.get("classname"),
                            "garbage_title": garbage.get("title"),
                            "garbage_id": garbage.get("id"),
                            "collection_classname": collection.get("classname"),
                            "collection_title": collection.get("title"),
                            "collection_id": collection.get("id"),
                            "mode": mode,
                            "reward_group_p": reward_asset.get("reward_group_p"),
                            "asset_p": reward_asset.get("asset_p"),
                            "locations": locations_by_garbage.get(garbage.get("classname"), []),
                        }
                    )
                    garbage_drop_count += 1
                elif looks_like_collection_asset(asset):
                    missing_collection_issues.append(
                        {
                            "code": "missing_collection_asset",
                            "message": "Reward references an asset that looks like a collection but is missing from collections_by_classname",
                            "source_type": "garbage",
                            "source_classname": garbage.get("classname"),
                            "reward_field": reward_field,
                            "mode": mode,
                            "asset": asset,
                        }
                    )

    for flower in flowers_by_classname.values():
        for mode, reward_field in (("home", "rand_reward"), ("guest", "rand_reward_in_guest")):
            for reward_asset in iter_reward_assets(flower.get(reward_field)):
                asset = reward_asset["asset"]
                if asset in collections_by_classname:
                    collection = collections_by_classname[asset]
                    drops.append(
                        {
                            "source_type": "flower",
                            "source_classname": flower.get("classname"),
                            "source_title": flower.get("title"),
                            "source_id": flower.get("id"),
                            "flower_classname": flower.get("classname"),
                            "flower_title": flower.get("title"),
                            "flower_id": flower.get("id"),
                            "flower_tags": flower.get("tags"),
                            "req_user_level": flower.get("req_user_level"),
                            "collection_classname": collection.get("classname"),
                            "collection_title": collection.get("title"),
                            "collection_id": collection.get("id"),
                            "mode": mode,
                            "reward_group_p": reward_asset.get("reward_group_p"),
                            "asset_p": reward_asset.get("asset_p"),
                            "locations": [],
                        }
                    )
                    flower_drop_count += 1
                elif looks_like_collection_asset(asset):
                    missing_collection_issues.append(
                        {
                            "code": "missing_collection_asset",
                            "message": "Reward references an asset that looks like a collection but is missing from collections_by_classname",
                            "source_type": "flower",
                            "source_classname": flower.get("classname"),
                            "reward_field": reward_field,
                            "mode": mode,
                            "asset": asset,
                        }
                    )

    return drops, garbage_drop_count, flower_drop_count, missing_collection_issues


def is_ignored_missing_collection_asset(asset: Any) -> bool:
    return isinstance(asset, str) and any(
        fragment in asset for fragment in IGNORED_MISSING_COLLECTION_FRAGMENTS
    )


def with_reason(issue: dict[str, Any], reason: str) -> dict[str, Any]:
    result = dict(issue)
    result["reason"] = reason
    return result


def critical_issue(
    issue: dict[str, Any],
    reason: str,
    suggested_fix: str,
) -> dict[str, Any]:
    result = {
        "code": issue.get("code"),
        "reason": reason,
        "suggested_fix": suggested_fix,
    }
    for key, value in issue.items():
        if key not in result:
            result[key] = value
    return result


def issue_key(issue: dict[str, Any]) -> tuple[Any, ...]:
    return (
        issue.get("code"),
        issue.get("source_type"),
        issue.get("source_classname"),
        issue.get("asset"),
        issue.get("location_code"),
        issue.get("garbage_classname"),
        issue.get("classname"),
        issue.get("file"),
        issue.get("mode"),
        issue.get("reward_field"),
    )


def add_unique_issue(
    items: list[dict[str, Any]],
    seen: set[tuple[Any, ...]],
    issue: dict[str, Any],
) -> None:
    key = issue_key(issue)
    if key not in seen:
        seen.add(key)
        items.append(issue)


def make_location_exclusion(
    location: dict[str, Any],
    reason: str,
    known_garbage_assets: list[str] | None = None,
    unknown_garbage_assets: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "code": location.get("code"),
        "title": location.get("title"),
        "tags": location.get("tags"),
        "garbage_assets": location.get("garbage_assets", []),
        "known_garbage_assets": known_garbage_assets or [],
        "unknown_garbage_assets": unknown_garbage_assets or [],
        "reason": reason,
    }


def make_garbage_exclusion(garbage: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "classname": garbage.get("classname"),
        "title": garbage.get("title"),
        "id": garbage.get("id"),
        "source_file": garbage.get("source_file"),
        "reason": reason,
    }


def build_quest_ready_data(
    locations_by_code: dict[str, Any],
    garbage_by_classname: dict[str, Any],
    flowers_by_classname: dict[str, Any],
    collections_by_classname: dict[str, Any],
    drops: list[dict[str, Any]],
    report: ValidationReport,
    missing_collection_issues: list[dict[str, Any]],
    generated_at: str,
) -> dict[str, Any]:
    non_critical_issues: list[dict[str, Any]] = []
    critical_issues: list[dict[str, Any]] = []
    seen_non_critical: set[tuple[Any, ...]] = set()
    seen_critical: set[tuple[Any, ...]] = set()
    excluded_locations: list[dict[str, Any]] = []
    excluded_garbage: list[dict[str, Any]] = []
    quest_ready_locations: dict[str, Any] = {}

    for location in locations_by_code.values():
        garbage_assets = location.get("garbage_assets", [])
        known_assets = [
            classname for classname in garbage_assets if classname in garbage_by_classname
        ]
        unknown_assets = [
            classname for classname in garbage_assets if classname not in garbage_by_classname
        ]

        if not garbage_assets:
            reason = "Location has no garbage and is not needed for quest generation"
            excluded_locations.append(make_location_exclusion(location, reason))
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(
                    {
                        "code": "location_empty_garbage_assets",
                        "location_code": location.get("code"),
                        "title": location.get("title"),
                    },
                    reason,
                ),
            )
            if not location.get("tags"):
                add_unique_issue(
                    non_critical_issues,
                    seen_non_critical,
                    with_reason(
                        {
                            "code": "location_missing_tags",
                            "location_code": location.get("code"),
                            "title": location.get("title"),
                        },
                        "Location is already excluded because it has no garbage",
                    ),
                )
            continue

        for unknown_asset in unknown_assets:
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(
                    {
                        "code": "location_unknown_garbage",
                        "location_code": location.get("code"),
                        "location_title": location.get("title"),
                        "garbage_classname": unknown_asset,
                    },
                    "Unknown garbage is ignored because raw/garbage is the source of needed garbage",
                ),
            )

        if not known_assets:
            reason = "Location has no known garbage after filtering and is not needed for quest generation"
            excluded_locations.append(
                make_location_exclusion(
                    location,
                    reason,
                    known_garbage_assets=known_assets,
                    unknown_garbage_assets=unknown_assets,
                )
            )
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(
                    {
                        "code": "location_no_known_garbage_after_filter",
                        "location_code": location.get("code"),
                        "title": location.get("title"),
                    },
                    reason,
                ),
            )
            if not location.get("tags"):
                add_unique_issue(
                    non_critical_issues,
                    seen_non_critical,
                    with_reason(
                        {
                            "code": "location_missing_tags",
                            "location_code": location.get("code"),
                            "title": location.get("title"),
                        },
                        "Location is already excluded because it has no known garbage",
                    ),
                )
            continue

        ready_location = dict(location)
        ready_location["garbage_assets"] = known_assets
        if unknown_assets:
            ready_location["ignored_garbage_assets"] = unknown_assets
        quest_ready_locations[str(location.get("code"))] = ready_location

        if not location.get("tags"):
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(
                    {
                        "code": "location_missing_tags",
                        "location_code": location.get("code"),
                        "title": location.get("title"),
                    },
                    "Location has known garbage; missing tags remain a warning but do not block quest-ready indexes",
                ),
            )

    quest_ready_locations_by_garbage: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for location in quest_ready_locations.values():
        for garbage_classname in location.get("garbage_assets", []):
            quest_ready_locations_by_garbage[garbage_classname].append(location_summary(location))

    used_garbage = set(quest_ready_locations_by_garbage)
    quest_ready_garbage = {
        classname: garbage_by_classname[classname]
        for classname in sorted(used_garbage)
        if classname in garbage_by_classname
    }

    for classname, garbage in sorted(garbage_by_classname.items()):
        if classname in used_garbage:
            continue
        reason = "Garbage is not used by any quest-ready location"
        excluded_garbage.append(make_garbage_exclusion(garbage, reason))
        add_unique_issue(
            non_critical_issues,
            seen_non_critical,
            with_reason(
                {
                    "code": "garbage_unused_in_locations",
                    "garbage_classname": classname,
                    "garbage_title": garbage.get("title"),
                    "file": garbage.get("source_file"),
                },
                reason,
            ),
        )

    quest_ready_flowers = {
        classname: flower
        for classname, flower in sorted(flowers_by_classname.items())
        if flower.get("title") is not None
    }

    for issue in report.warnings:
        code = issue.get("code")
        if code == "garbage_missing_title":
            classname = issue.get("classname")
            if classname in quest_ready_garbage:
                add_unique_issue(
                    critical_issues,
                    seen_critical,
                    critical_issue(
                        issue,
                        "Active garbage used by quest-ready locations has no title",
                        "Add title to the garbage AssetPrototype in raw/garbage.",
                    ),
                )
            else:
                add_unique_issue(
                    non_critical_issues,
                    seen_non_critical,
                    with_reason(issue, "Garbage is not used by any quest-ready location"),
                )
        elif code == "flower_missing_title":
            add_unique_issue(
                critical_issues,
                seen_critical,
                critical_issue(
                    issue,
                    "Active flower has no title",
                    "Add title to the flower AssetPrototype in raw/flowers.",
                ),
            )
        elif code == "collection_missing_title":
            continue
        elif code == "location_missing_title":
            location_code = str(issue.get("location_code"))
            reason = (
                "Location is excluded from quest-ready data"
                if location_code not in quest_ready_locations
                else "Location title is not required for quest-ready drop links yet"
            )
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(issue, reason),
            )

    for issue in report.errors:
        code = issue.get("code")
        if code in {
            "duplicate_garbage_classname",
            "duplicate_flower_classname",
            "duplicate_collection_classname",
            "duplicate_location_code",
        }:
            add_unique_issue(
                critical_issues,
                seen_critical,
                critical_issue(
                    issue,
                    "Duplicate identifiers make the quest-ready index ambiguous",
                    "Keep one canonical object or rename duplicate classnames/codes in raw data.",
                ),
            )

    critical_missing_collection_issues: list[dict[str, Any]] = []
    for issue in missing_collection_issues:
        asset = issue.get("asset")
        source_type = issue.get("source_type")
        source_classname = issue.get("source_classname")

        if is_ignored_missing_collection_asset(asset):
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(
                    issue,
                    "Collection asset belongs to ignored non-quest patterns: Cocoon/Web/Common/Mold",
                ),
            )
            continue

        if source_type == "garbage" and source_classname not in quest_ready_garbage:
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(issue, "Missing collection asset belongs to excluded garbage"),
            )
            continue

        if source_type == "flower" and source_classname not in quest_ready_flowers:
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(issue, "Missing collection asset belongs to non-quest-ready flower"),
            )
            continue

        critical_missing_collection_issues.append(issue)
        add_unique_issue(
            critical_issues,
            seen_critical,
            critical_issue(
                issue,
                "Quest-ready drop references a collection asset missing from collections_by_classname",
                "Add the missing collection AssetPrototype to raw/collections or remove the reward reference.",
            ),
        )

    for issue in critical_missing_collection_issues:
        report.error(
            "missing_collection_asset",
            issue.get(
                "message",
                "Reward references an asset that looks like a collection but is missing from collections_by_classname",
            ),
            source_type=issue.get("source_type"),
            source_classname=issue.get("source_classname"),
            reward_field=issue.get("reward_field"),
            mode=issue.get("mode"),
            asset=issue.get("asset"),
        )

    quest_ready_drops: list[dict[str, Any]] = []
    used_collection_classnames: set[str] = set()
    critical_collection_missing_titles: set[str] = set()

    for drop in drops:
        source_type = drop.get("source_type")
        collection_classname = drop.get("collection_classname")
        collection = collections_by_classname.get(collection_classname)

        if collection is None:
            continue

        if source_type == "garbage":
            source_classname = drop.get("source_classname")
            locations = quest_ready_locations_by_garbage.get(source_classname, [])
            if source_classname not in quest_ready_garbage:
                continue
            if not drop.get("garbage_title"):
                continue
            if not collection.get("title"):
                critical_collection_missing_titles.add(str(collection_classname))
                add_unique_issue(
                    critical_issues,
                    seen_critical,
                    critical_issue(
                        {
                            "code": "collection_missing_title",
                            "classname": collection_classname,
                            "source_type": "garbage",
                            "source_classname": source_classname,
                        },
                        "Collection used by quest-ready garbage drop has no title",
                        "Add title to the collection AssetPrototype in raw/collections.",
                    ),
                )
                continue
            if not locations:
                continue
            ready_drop = dict(drop)
            ready_drop["locations"] = locations
            quest_ready_drops.append(ready_drop)
            used_collection_classnames.add(str(collection_classname))
        elif source_type == "flower":
            source_classname = drop.get("source_classname")
            if source_classname not in quest_ready_flowers:
                continue
            if not drop.get("flower_title"):
                continue
            if not collection.get("title"):
                critical_collection_missing_titles.add(str(collection_classname))
                add_unique_issue(
                    critical_issues,
                    seen_critical,
                    critical_issue(
                        {
                            "code": "collection_missing_title",
                            "classname": collection_classname,
                            "source_type": "flower",
                            "source_classname": source_classname,
                        },
                        "Collection used by quest-ready flower drop has no title",
                        "Add title to the collection AssetPrototype in raw/collections.",
                    ),
                )
                continue
            quest_ready_drops.append(dict(drop))
            used_collection_classnames.add(str(collection_classname))

    for issue in report.warnings:
        if issue.get("code") != "collection_missing_title":
            continue
        classname = issue.get("classname")
        if (
            classname not in used_collection_classnames
            and classname not in critical_collection_missing_titles
        ):
            add_unique_issue(
                non_critical_issues,
                seen_non_critical,
                with_reason(issue, "Collection is not used by quest-ready drops"),
            )

    quest_ready_collections = {
        classname: collections_by_classname[classname]
        for classname in sorted(used_collection_classnames)
        if classname in collections_by_classname and collections_by_classname[classname].get("title")
    }

    garbage_drop_count = sum(1 for drop in quest_ready_drops if drop.get("source_type") == "garbage")
    flower_drop_count = sum(1 for drop in quest_ready_drops if drop.get("source_type") == "flower")
    summary = {
        "generated_at": generated_at,
        "quest_ready_locations": len(quest_ready_locations),
        "quest_ready_garbage": len(quest_ready_garbage),
        "quest_ready_flowers": len(quest_ready_flowers),
        "quest_ready_collections": len(quest_ready_collections),
        "quest_ready_drops": len(quest_ready_drops),
        "quest_ready_garbage_drops": garbage_drop_count,
        "quest_ready_flower_drops": flower_drop_count,
        "critical_issues": len(critical_issues),
        "non_critical_issues": len(non_critical_issues),
        "excluded_locations": len(excluded_locations),
        "excluded_garbage": len(excluded_garbage),
    }

    return {
        "quest_ready_index": {
            "quest_ready_locations": dict(sorted(quest_ready_locations.items())),
            "quest_ready_garbage": dict(sorted(quest_ready_garbage.items())),
            "quest_ready_flowers": dict(sorted(quest_ready_flowers.items())),
            "quest_ready_collections": quest_ready_collections,
            "summary": summary,
        },
        "quest_ready_drops": quest_ready_drops,
        "non_critical_issues": non_critical_issues,
        "critical_issues": critical_issues,
        "excluded_entities": {
            "locations": excluded_locations,
            "garbage": excluded_garbage,
            "summary": {
                "locations": len(excluded_locations),
                "garbage": len(excluded_garbage),
            },
        },
        "summary": summary,
    }


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(value) for value in row) + " |")
    return lines


def group_issue_counts(issues: list[dict[str, Any]], keys: list[str]) -> list[list[Any]]:
    counter: Counter[tuple[Any, ...]] = Counter(
        tuple(issue.get(key, "") for key in keys) for issue in issues
    )
    return [list(key) + [count] for key, count in counter.most_common()]


def build_validation_summary_markdown(
    validation_report: dict[str, Any],
    quest_ready: dict[str, Any],
) -> str:
    non_critical_issues = quest_ready["non_critical_issues"]
    critical_issues = quest_ready["critical_issues"]
    excluded_entities = quest_ready["excluded_entities"]
    quest_summary = quest_ready["summary"]
    raw_summary = validation_report["summary"]

    lines: list[str] = [
        "# Validation Summary",
        "",
        "## Raw validation counts",
        "",
    ]
    lines.extend(
        markdown_table(
            ["Metric", "Count"],
            [
                ["locations found", raw_summary.get("locations_found", 0)],
                ["garbage found", raw_summary.get("garbage_found", 0)],
                ["flowers found", raw_summary.get("flowers_found", 0)],
                ["collections found", raw_summary.get("collections_found", 0)],
                ["errors", raw_summary.get("errors", 0)],
                ["warnings", raw_summary.get("warnings", 0)],
            ],
        )
    )
    lines.extend(["", "## Non-critical issues", ""])
    if non_critical_issues:
        lines.extend(
            markdown_table(
                ["code", "reason", "count"],
                group_issue_counts(non_critical_issues, ["code", "reason"]),
            )
        )
    else:
        lines.append("Non-critical issues не найдены.")

    lines.extend(["", "## Critical issues to fix manually", ""])
    if critical_issues:
        lines.extend(
            markdown_table(
                ["code", "count"],
                group_issue_counts(critical_issues, ["code"]),
            )
        )
    else:
        lines.append("Критичных ошибок для quest-ready генерации не найдено.")

    lines.extend(["", "## Excluded locations", ""])
    excluded_locations = excluded_entities.get("locations", [])
    lines.append(f"Количество исключённых локаций: {len(excluded_locations)}.")
    if excluded_locations:
        lines.extend(
            markdown_table(
                ["code", "title", "reason"],
                [
                    [
                        item.get("code"),
                        item.get("title"),
                        item.get("reason"),
                    ]
                    for item in excluded_locations[:20]
                ],
            )
        )

    lines.extend(["", "## Excluded garbage", ""])
    excluded_garbage = excluded_entities.get("garbage", [])
    lines.append(f"Количество исключённого мусора: {len(excluded_garbage)}.")
    if excluded_garbage:
        lines.extend(
            markdown_table(
                ["classname", "title", "reason"],
                [
                    [
                        item.get("classname"),
                        item.get("title"),
                        item.get("reason"),
                    ]
                    for item in excluded_garbage[:20]
                ],
            )
        )

    lines.extend(["", "## Quest-ready summary", ""])
    lines.extend(
        markdown_table(
            ["Metric", "Count"],
            [
                ["quest-ready locations", quest_summary["quest_ready_locations"]],
                ["quest-ready garbage", quest_summary["quest_ready_garbage"]],
                ["quest-ready flowers", quest_summary["quest_ready_flowers"]],
                ["quest-ready collections", quest_summary["quest_ready_collections"]],
                ["quest-ready garbage drops", quest_summary["quest_ready_garbage_drops"]],
                ["quest-ready flower drops", quest_summary["quest_ready_flower_drops"]],
            ],
        )
    )
    lines.append("")
    return "\n".join(lines)


def build_indexes(project_root: Path | str, write_files: bool = True) -> dict[str, Any]:
    project_root = Path(project_root)
    raw_dir = project_root / RAW_DIR_NAME
    data_dir = project_root / DATA_DIR_NAME
    report = ValidationReport()
    generated_at = datetime.now(timezone.utc).isoformat()

    locations_by_code = collect_locations(raw_dir, project_root, report)
    garbage_by_classname = collect_assets(
        raw_dir=raw_dir,
        folder_name="garbage",
        project_root=project_root,
        report=report,
        asset_type="garbage",
        predicate=lambda obj: obj.get("group") == "garbage",
        fields=[
            "id",
            "group",
            "subgroup",
            "rand_reward",
            "rand_reward_in_guest",
        ],
    )
    flowers_by_classname = collect_assets(
        raw_dir=raw_dir,
        folder_name="flowers",
        project_root=project_root,
        report=report,
        asset_type="flower",
        predicate=lambda obj: obj.get("group") == "seeds" and obj.get("subgroup") == "flower",
        fields=[
            "id",
            "group",
            "subgroup",
            "tags",
            "price",
            "req_user_level",
            "meta_info",
            "rand_reward",
            "rand_reward_in_guest",
        ],
    )
    collections_by_classname = collect_assets(
        raw_dir=raw_dir,
        folder_name="collections",
        project_root=project_root,
        report=report,
        asset_type="collection",
        predicate=lambda obj: obj.get("group") == "collection",
        fields=[
            "id",
            "group",
            "subgroup",
        ],
    )

    locations_by_garbage = build_locations_by_garbage(
        locations_by_code=locations_by_code,
        garbage_by_classname=garbage_by_classname,
        report=report,
    )
    drops, garbage_drop_count, flower_drop_count, missing_collection_issues = build_drops(
        garbage_by_classname=garbage_by_classname,
        flowers_by_classname=flowers_by_classname,
        collections_by_classname=collections_by_classname,
        locations_by_garbage=locations_by_garbage,
        report=report,
    )
    quest_ready = build_quest_ready_data(
        locations_by_code=locations_by_code,
        garbage_by_classname=garbage_by_classname,
        flowers_by_classname=flowers_by_classname,
        collections_by_classname=collections_by_classname,
        drops=drops,
        report=report,
        missing_collection_issues=missing_collection_issues,
        generated_at=generated_at,
    )

    summary = {
        "generated_at": generated_at,
        "locations_found": len(locations_by_code),
        "garbage_found": len(garbage_by_classname),
        "flowers_found": len(flowers_by_classname),
        "collections_found": len(collections_by_classname),
        "garbage_drop_links_created": garbage_drop_count,
        "flower_drop_links_created": flower_drop_count,
        "errors": len(report.errors),
        "warnings": len(report.warnings),
    }

    master_index = {
        "locations_by_code": dict(sorted(locations_by_code.items())),
        "locations_by_garbage": locations_by_garbage,
        "garbage_by_classname": dict(sorted(garbage_by_classname.items())),
        "flowers_by_classname": dict(sorted(flowers_by_classname.items())),
        "collections_by_classname": dict(sorted(collections_by_classname.items())),
        "summary": summary,
    }

    validation_report = report.to_json()
    validation_report["summary"].update(
        {
            "generated_at": summary["generated_at"],
            "locations_found": summary["locations_found"],
            "garbage_found": summary["garbage_found"],
            "flowers_found": summary["flowers_found"],
            "collections_found": summary["collections_found"],
            "garbage_drop_links_created": summary["garbage_drop_links_created"],
            "flower_drop_links_created": summary["flower_drop_links_created"],
        }
    )
    validation_summary_markdown = build_validation_summary_markdown(
        validation_report=validation_report,
        quest_ready=quest_ready,
    )

    result = {
        "master_index": master_index,
        "garbage_index": {
            "garbage_by_classname": dict(sorted(garbage_by_classname.items())),
            "summary": {
                "garbage_found": len(garbage_by_classname),
            },
        },
        "flowers_index": {
            "flowers_by_classname": dict(sorted(flowers_by_classname.items())),
            "summary": {
                "flowers_found": len(flowers_by_classname),
            },
        },
        "collections_index": {
            "collections_by_classname": dict(sorted(collections_by_classname.items())),
            "summary": {
                "collections_found": len(collections_by_classname),
            },
        },
        "drops": drops,
        "validation_report": validation_report,
        "quest_ready_index": quest_ready["quest_ready_index"],
        "quest_ready_drops": quest_ready["quest_ready_drops"],
        "non_critical_issues": quest_ready["non_critical_issues"],
        "critical_issues": quest_ready["critical_issues"],
        "excluded_entities": quest_ready["excluded_entities"],
        "validation_summary_markdown": validation_summary_markdown,
        "quest_ready_summary": quest_ready["summary"],
        "summary": summary,
    }

    if write_files:
        write_indexes(data_dir, result)

    return result


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_indexes(data_dir: Path, result: dict[str, Any]) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    write_json(data_dir / "master_index.json", result["master_index"])
    write_json(data_dir / "garbage.index.json", result["garbage_index"])
    write_json(data_dir / "flowers.index.json", result["flowers_index"])
    write_json(data_dir / "collections.index.json", result["collections_index"])
    write_json(data_dir / "drops.index.json", result["drops"])
    write_json(data_dir / "validation_report.json", result["validation_report"])
    write_json(data_dir / "quest_ready_index.json", result["quest_ready_index"])
    write_json(data_dir / "quest_ready_drops.index.json", result["quest_ready_drops"])
    write_json(data_dir / "non_critical_issues.json", result["non_critical_issues"])
    write_json(data_dir / "critical_issues.json", result["critical_issues"])
    write_json(data_dir / "excluded_entities.json", result["excluded_entities"])
    (data_dir / "validation_summary.md").write_text(
        result["validation_summary_markdown"],
        encoding="utf-8",
    )


def print_summary(summary: dict[str, Any], quest_ready_summary: dict[str, Any]) -> None:
    print("Raw:")
    print(f"locations found: {summary['locations_found']}")
    print(f"garbage found: {summary['garbage_found']}")
    print(f"flowers found: {summary['flowers_found']}")
    print(f"collections found: {summary['collections_found']}")
    print(f"raw errors: {summary['errors']}")
    print(f"raw warnings: {summary['warnings']}")
    print("")
    print("Quest-ready:")
    print(f"quest-ready locations: {quest_ready_summary['quest_ready_locations']}")
    print(f"quest-ready garbage: {quest_ready_summary['quest_ready_garbage']}")
    print(f"quest-ready flowers: {quest_ready_summary['quest_ready_flowers']}")
    print(f"quest-ready drops: {quest_ready_summary['quest_ready_drops']}")
    print(f"critical issues: {quest_ready_summary['critical_issues']}")
    print(f"non-critical issues: {quest_ready_summary['non_critical_issues']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build game data indexes from raw files.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Project root containing raw/ and data/ directories.",
    )
    args = parser.parse_args(argv)

    result = build_indexes(args.project_root)
    print_summary(result["summary"], result["quest_ready_summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
