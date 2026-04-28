{
"class" : "AssetPrototype",
"classname" : "WebGhost",
"title" : "Паутина на монстрике под кроватью",
"group" : "garbage",
"subgroup" : "on_asset",
"tags":["exclude_for_generation"],
"id" : 45743,
"rand_reward" : {"all": [
                          {"p":45, "one_of": [
                                              {"asset":"Garbage_SpiderCollection1", "p":100},
                                              {"asset":"Garbage_SpiderCollection2", "p":100},
                                              {"asset":"Garbage_SpiderCollection3", "p":100},
                                              {"asset":"Garbage_SpiderCollection4", "p":100},
                                              {"asset":"Garbage_SpiderCollection5", "p":28}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":25, "one_of": [
                                                {"asset":"Garbage_SpiderCollection1", "p":100},
                                                {"asset":"Garbage_SpiderCollection2", "p":100},
                                                {"asset":"Garbage_SpiderCollection3", "p":100},
                                                {"asset":"Garbage_SpiderCollection4", "p":100},
                                                {"asset":"Garbage_SpiderCollection5", "p":28}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}