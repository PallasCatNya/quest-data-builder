{
"class" : "AssetPrototype",
"classname" : "GarbageJuicer",
"title" : "Соковыжималка",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 23705,
"rand_reward" : {"all": [
                          {"p":40, "one_of": [
                                              {"asset":"GarbageJuicerCollection1", "p":100},
                                              {"asset":"GarbageJuicerCollection2", "p":100},
                                              {"asset":"GarbageJuicerCollection3", "p":100},
                                              {"asset":"GarbageJuicerCollection4", "p":100},
                                              {"asset":"GarbageJuicerCollection5", "p":27}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":18, "one_of": [
                                                {"asset":"GarbageJuicerCollection1", "p":100},
                                                {"asset":"GarbageJuicerCollection2", "p":100},
                                                {"asset":"GarbageJuicerCollection3", "p":100},
                                                {"asset":"GarbageJuicerCollection4", "p":100},
                                                {"asset":"GarbageJuicerCollection5", "p":35}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}