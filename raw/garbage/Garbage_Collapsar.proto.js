{
"class" : "AssetPrototype",
"classname" : "Garbage_Collapsar",
"title" : "Чёрная дыра",
"group" : "garbage",
"subgroup" : "on_the_wall",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"Garbage_Collapsar_Collection1", "p":80},
                                              {"asset":"Garbage_Collapsar_Collection2", "p":20},
                                              {"asset":"Garbage_Collapsar_Collection3", "p":60},
                                              {"asset":"Garbage_Collapsar_Collection4", "p":30},
                                              {"asset":"Garbage_Collapsar_Collection5", "p":100}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                              {"asset":"Garbage_Collapsar_Collection1", "p":80},
                                              {"asset":"Garbage_Collapsar_Collection2", "p":20},
                                              {"asset":"Garbage_Collapsar_Collection3", "p":60},
                                              {"asset":"Garbage_Collapsar_Collection4", "p":30},
                                              {"asset":"Garbage_Collapsar_Collection5", "p":100}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32435
}