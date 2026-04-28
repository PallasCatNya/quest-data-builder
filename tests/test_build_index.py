import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.build_index import build_indexes


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class BuildIndexTests(unittest.TestCase):
    def test_builds_indexes_and_drops_for_example_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            write_json(
                root / "raw" / "locations" / "locations.json",
                [
                    {
                        "code": "boiler_room",
                        "title": "Котельная",
                        "tags": ["home", "boiler"],
                        "garbage_assets": ["Ashes"],
                    }
                ],
            )
            write_json(
                root / "raw" / "garbage" / "Ashes.proto.js",
                {
                    "class": "AssetPrototype",
                    "classname": "Ashes",
                    "title": "Пепел",
                    "group": "garbage",
                    "subgroup": "on_the_floor",
                    "id": 14624,
                    "rand_reward": {
                        "all": [
                            {
                                "p": 50,
                                "one_of": [
                                    {
                                        "asset": "AshesCollection1",
                                        "p": 80,
                                    }
                                ],
                            }
                        ]
                    },
                    "rand_reward_in_guest": {
                        "all": [
                            {
                                "p": 25,
                                "one_of": [
                                    {
                                        "asset": "AshesCollection1",
                                        "p": 80,
                                    }
                                ],
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "raw" / "flowers" / "FlowerSix.proto.js",
                {
                    "class": "AssetPrototype",
                    "classname": "FlowerSix",
                    "title": "Василек",
                    "group": "seeds",
                    "subgroup": "flower",
                    "tags": ["seed_simple", "seed_flower", "category_1"],
                    "price": 25,
                    "req_user_level": 10,
                    "meta_info": "life=900;states=3;spoil_period=3600",
                    "id": 34878595,
                    "rand_reward": {
                        "all": [
                            {
                                "p": 33,
                                "one_of": [
                                    {
                                        "asset": "Fl6Col1",
                                        "p": 20,
                                    }
                                ],
                            }
                        ]
                    },
                    "rand_reward_in_guest": {
                        "all": [
                            {
                                "p": 33,
                                "one_of": [
                                    {
                                        "asset": "Fl6Col1",
                                        "p": 20,
                                    }
                                ],
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "raw" / "collections" / "AshesCollection1.proto.js",
                {
                    "class": "AssetPrototype",
                    "classname": "AshesCollection1",
                    "title": "Огненная саламандра",
                    "group": "collection",
                    "subgroup": "collection_common",
                    "id": 14634,
                },
            )
            write_json(
                root / "raw" / "collections" / "Fl6Col1.proto.js",
                {
                    "class": "AssetPrototype",
                    "classname": "Fl6Col1",
                    "title": "Сухой василек",
                    "group": "collection",
                    "subgroup": "collection_common",
                    "id": "2989534",
                },
            )

            result = build_indexes(root)

            self.assertTrue((root / "data" / "master_index.json").exists())
            self.assertTrue((root / "data" / "drops.index.json").exists())
            self.assertEqual(result["validation_report"]["summary"]["errors"], 0)
            self.assertEqual(result["validation_report"]["summary"]["warnings"], 0)

            master = result["master_index"]
            self.assertEqual(
                master["locations_by_garbage"]["Ashes"][0]["title"],
                "Котельная",
            )
            self.assertIn("Ashes", master["garbage_by_classname"])
            self.assertIn("FlowerSix", master["flowers_by_classname"])
            self.assertIn("AshesCollection1", master["collections_by_classname"])
            self.assertIn("Fl6Col1", master["collections_by_classname"])

            drops = result["drops"]
            self.assertEqual(len(drops), 4)

            garbage_home_drop = next(
                drop
                for drop in drops
                if drop["source_type"] == "garbage" and drop["mode"] == "home"
            )
            self.assertEqual(garbage_home_drop["source_classname"], "Ashes")
            self.assertEqual(garbage_home_drop["collection_classname"], "AshesCollection1")
            self.assertEqual(garbage_home_drop["reward_group_p"], 50)
            self.assertEqual(garbage_home_drop["asset_p"], 80)
            self.assertEqual(garbage_home_drop["locations"][0]["code"], "boiler_room")

            flower_home_drop = next(
                drop
                for drop in drops
                if drop["source_type"] == "flower" and drop["mode"] == "home"
            )
            self.assertEqual(flower_home_drop["source_classname"], "FlowerSix")
            self.assertEqual(flower_home_drop["collection_classname"], "Fl6Col1")
            self.assertEqual(flower_home_drop["reward_group_p"], 33)
            self.assertEqual(flower_home_drop["asset_p"], 20)
            self.assertEqual(flower_home_drop["flower_tags"], ["seed_simple", "seed_flower", "category_1"])
            self.assertEqual(flower_home_drop["req_user_level"], 10)
            self.assertEqual(flower_home_drop["locations"], [])

            self.assertTrue((root / "data" / "quest_ready_index.json").exists())
            self.assertTrue((root / "data" / "quest_ready_drops.index.json").exists())
            self.assertTrue((root / "data" / "critical_issues.json").exists())
            self.assertTrue((root / "data" / "non_critical_issues.json").exists())
            self.assertTrue((root / "data" / "excluded_entities.json").exists())
            self.assertTrue((root / "data" / "validation_summary.md").exists())

    def test_classifies_quest_ready_issues_and_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            write_json(
                root / "raw" / "locations" / "locations.json",
                [
                    {
                        "code": "active",
                        "title": "Active location",
                        "tags": ["home"],
                        "garbage_assets": ["ActiveGarbage", "UnknownGarbage"],
                    },
                    {
                        "code": "empty",
                        "title": "Empty location",
                        "tags": [],
                        "garbage_assets": [],
                    },
                    {
                        "code": "unknown_only",
                        "title": "Unknown only",
                        "tags": ["event"],
                        "garbage_assets": ["UnknownOnly"],
                    },
                ],
            )
            write_json(
                root / "raw" / "garbage" / "ActiveGarbage.proto.js",
                {
                    "classname": "ActiveGarbage",
                    "title": "Active garbage",
                    "group": "garbage",
                    "id": 1,
                    "rand_reward": {
                        "all": [
                            {
                                "p": 50,
                                "one_of": [
                                    {"asset": "ExistingCollection1", "p": 100},
                                    {"asset": "CocoonActiveCollection1", "p": 100},
                                    {"asset": "WebActiveCollection1", "p": 100},
                                    {"asset": "CriticalMissingCollection1", "p": 100},
                                ],
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "raw" / "garbage" / "UnusedGarbage.proto.js",
                {
                    "classname": "UnusedGarbage",
                    "title": "Unused garbage",
                    "group": "garbage",
                    "id": 2,
                    "rand_reward": {
                        "all": [
                            {
                                "p": 50,
                                "one_of": [
                                    {"asset": "ExistingCollection1", "p": 100},
                                    {"asset": "ExcludedMissingCollection1", "p": 100},
                                ],
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "raw" / "flowers" / "FlowerSix.proto.js",
                {
                    "classname": "FlowerSix",
                    "title": "Flower six",
                    "group": "seeds",
                    "subgroup": "flower",
                    "id": 3,
                    "tags": ["seed_flower"],
                    "req_user_level": 10,
                    "rand_reward": {
                        "all": [
                            {
                                "p": 33,
                                "one_of": [
                                    {"asset": "FlowerCollection1", "p": 20},
                                ],
                            }
                        ]
                    },
                },
            )
            write_json(
                root / "raw" / "collections" / "ExistingCollection1.proto.js",
                {
                    "classname": "ExistingCollection1",
                    "title": "Existing collection",
                    "group": "collection",
                    "id": 10,
                },
            )
            write_json(
                root / "raw" / "collections" / "FlowerCollection1.proto.js",
                {
                    "classname": "FlowerCollection1",
                    "title": "Flower collection",
                    "group": "collection",
                    "id": 11,
                },
            )

            result = build_indexes(root)

            non_critical = result["non_critical_issues"]
            non_critical_codes = {issue["code"] for issue in non_critical}
            self.assertIn("location_empty_garbage_assets", non_critical_codes)
            self.assertIn("garbage_unused_in_locations", non_critical_codes)
            self.assertIn("location_unknown_garbage", non_critical_codes)

            non_critical_assets = {
                issue.get("asset")
                for issue in non_critical
                if issue.get("code") == "missing_collection_asset"
            }
            self.assertIn("CocoonActiveCollection1", non_critical_assets)
            self.assertIn("WebActiveCollection1", non_critical_assets)
            self.assertIn("ExcludedMissingCollection1", non_critical_assets)

            quest_ready_locations = result["quest_ready_index"]["quest_ready_locations"]
            self.assertIn("active", quest_ready_locations)
            self.assertNotIn("empty", quest_ready_locations)
            self.assertNotIn("unknown_only", quest_ready_locations)
            self.assertEqual(
                quest_ready_locations["active"]["garbage_assets"],
                ["ActiveGarbage"],
            )

            quest_ready_garbage = result["quest_ready_index"]["quest_ready_garbage"]
            self.assertIn("ActiveGarbage", quest_ready_garbage)
            self.assertNotIn("UnusedGarbage", quest_ready_garbage)

            excluded_garbage = {
                item["classname"]
                for item in result["excluded_entities"]["garbage"]
            }
            self.assertIn("UnusedGarbage", excluded_garbage)

            quest_ready_drops = result["quest_ready_drops"]
            self.assertTrue(
                all(drop["source_classname"] != "UnusedGarbage" for drop in quest_ready_drops)
            )
            self.assertIn(
                ("ActiveGarbage", "ExistingCollection1"),
                {
                    (drop["source_classname"], drop["collection_classname"])
                    for drop in quest_ready_drops
                },
            )

            critical = result["critical_issues"]
            self.assertEqual(len(critical), 1)
            self.assertEqual(critical[0]["code"], "missing_collection_asset")
            self.assertEqual(critical[0]["asset"], "CriticalMissingCollection1")


if __name__ == "__main__":
    unittest.main()
