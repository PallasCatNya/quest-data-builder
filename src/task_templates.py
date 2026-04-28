from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SUPPORTED_TEMPLATE_IDS = {
    "garbage_classname_in_guest",
    "garbage_classname",
    "get_asset_collection",
    "get_asset_gr_in_guest_garbage",
    "action_take_crop_in_guest",
}


def load_task_templates(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {item["id"]: item for item in data.get("templates", [])}


def normalize_task_type(task_type: str) -> str:
    normalized = task_type.strip().lower()
    normalized = normalized.replace(",", " ")
    normalized = normalized.replace("_", "_")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def task_type_tokens(task_type: str) -> set[str]:
    return set(normalize_task_type(task_type).split())


def detect_template_id(task_type: str) -> str | None:
    normalized = normalize_task_type(task_type)
    tokens = task_type_tokens(task_type)

    if {"action", "take_crop_in_guest"}.issubset(tokens):
        if "mystery" not in tokens and "is_silhouette" not in tokens:
            return "action_take_crop_in_guest"

    if {"get_asset", "gr", "in_guest", "garbage"}.issubset(tokens):
        return "get_asset_gr_in_guest_garbage"

    if "get_asset" in tokens and "collection" in tokens:
        if "mystery" not in tokens and "is_silhouette" not in tokens:
            return "get_asset_collection"

    if "garbage" in tokens and "classname" in tokens and "get_asset" not in tokens:
        if "in_guest" in tokens:
            return "garbage_classname_in_guest"
        return "garbage_classname"

    if normalized == "garbage classname in_guest":
        return "garbage_classname_in_guest"
    if normalized == "garbage classname":
        return "garbage_classname"

    return None


def is_supported_task_type(task_type: str) -> bool:
    template_id = detect_template_id(task_type)
    return template_id in SUPPORTED_TEMPLATE_IDS
