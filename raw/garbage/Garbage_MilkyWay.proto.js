{
"class" : "AssetPrototype",
"classname" : "Garbage_MilkyWay",
"title" : "Рисунок млечного пути",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":60, "one_of": [
                                              {"asset":"Garbage_MilkyWay_Collection1", "p":100},
                                              {"asset":"Garbage_MilkyWay_Collection2", "p":80},
                                              {"asset":"Garbage_MilkyWay_Collection3", "p":12},
                                              {"asset":"Garbage_MilkyWay_Collection4", "p":100},
                                              {"asset":"Garbage_MilkyWay_Collection5", "p":80}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":50, "one_of": [
                                              {"asset":"Garbage_MilkyWay_Collection1", "p":100},
                                              {"asset":"Garbage_MilkyWay_Collection2", "p":80},
                                              {"asset":"Garbage_MilkyWay_Collection3", "p":12},
                                              {"asset":"Garbage_MilkyWay_Collection4", "p":100},
                                              {"asset":"Garbage_MilkyWay_Collection5", "p":80}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32437
}