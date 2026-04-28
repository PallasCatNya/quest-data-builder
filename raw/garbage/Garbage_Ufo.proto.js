{
"class" : "AssetPrototype",
"classname" : "Garbage_Ufo",
"title" : "НЛО",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":35, "one_of": [
                                              {"asset":"Garbage_Ufo_Collection1", "p":35},
                                              {"asset":"Garbage_Ufo_Collection2", "p":100},
                                              {"asset":"Garbage_Ufo_Collection3", "p":70},
                                              {"asset":"Garbage_Ufo_Collection4", "p":70},
                                              {"asset":"Garbage_Ufo_Collection5", "p":100}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":25, "one_of": [
                                              {"asset":"Garbage_Ufo_Collection1", "p":35},
                                              {"asset":"Garbage_Ufo_Collection2", "p":100},
                                              {"asset":"Garbage_Ufo_Collection3", "p":70},
                                              {"asset":"Garbage_Ufo_Collection4", "p":70},
                                              {"asset":"Garbage_Ufo_Collection5", "p":100}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32436
}