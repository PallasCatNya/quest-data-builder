{
"class" : "AssetPrototype",
"classname" : "Garbage_Crescent",
"title" : "Полумесяц",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":35, "one_of": [
                                              {"asset":"Garbage_Crescent_Collection1", "p":80},
                                              {"asset":"Garbage_Crescent_Collection2", "p":100},
                                              {"asset":"Garbage_Crescent_Collection3", "p":30},
                                              {"asset":"Garbage_Crescent_Collection4", "p":80},
                                              {"asset":"Garbage_Crescent_Collection5", "p":100}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":25, "one_of": [
                                              {"asset":"Garbage_Crescent_Collection1", "p":80},
                                              {"asset":"Garbage_Crescent_Collection2", "p":100},
                                              {"asset":"Garbage_Crescent_Collection3", "p":30},
                                              {"asset":"Garbage_Crescent_Collection4", "p":80},
                                              {"asset":"Garbage_Crescent_Collection5", "p":100}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32438
}