{
"class" : "AssetPrototype",
"classname" : "Garbage_Bread",
"title" : "Кусочек хлеба",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 30120,
"rand_reward" : {"all": [
                          {"p":55, "one_of": [
                                              {"asset":"Garbage_BreadCollection1", "p":100},
                                              {"asset":"Garbage_BreadCollection2", "p":90},
                                              {"asset":"Garbage_BreadCollection3", "p":25},
                                              {"asset":"Garbage_BreadCollection4", "p":100},
                                              {"asset":"Garbage_BreadCollection5", "p":90}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                              {"asset":"Garbage_BreadCollection1", "p":100},
                                              {"asset":"Garbage_BreadCollection2", "p":90},
                                              {"asset":"Garbage_BreadCollection3", "p":25},
                                              {"asset":"Garbage_BreadCollection4", "p":100},
                                              {"asset":"Garbage_BreadCollection5", "p":90}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}