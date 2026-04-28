{
"class" : "AssetPrototype",
"classname" : "Garbage_FoldingChair",
"title" : "Складной стул",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":60, "one_of": [
                                              {"asset":"Garbage_FoldingChair_Collection1", "p":25},
                                              {"asset":"Garbage_FoldingChair_Collection2", "p":100},
                                              {"asset":"Garbage_FoldingChair_Collection3", "p":25},
                                              {"asset":"Garbage_FoldingChair_Collection4", "p":100},
                                              {"asset":"Garbage_FoldingChair_Collection5", "p":80}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":55, "one_of": [
                                              {"asset":"Garbage_FoldingChair_Collection1", "p":25},
                                              {"asset":"Garbage_FoldingChair_Collection2", "p":100},
                                              {"asset":"Garbage_FoldingChair_Collection3", "p":25},
                                              {"asset":"Garbage_FoldingChair_Collection4", "p":100},
                                              {"asset":"Garbage_FoldingChair_Collection5", "p":80}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32429
}