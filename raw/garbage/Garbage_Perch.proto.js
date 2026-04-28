{
"class" : "AssetPrototype",
"classname" : "Garbage_Perch",
"title" : "Насест",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 30122,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"Garbage_PerchCollection1", "p":100},
                                              {"asset":"Garbage_PerchCollection2", "p":15},
                                              {"asset":"Garbage_PerchCollection3", "p":100},
                                              {"asset":"Garbage_PerchCollection4", "p":80},
                                              {"asset":"Garbage_PerchCollection5", "p":35}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                              {"asset":"Garbage_PerchCollection1", "p":100},
                                              {"asset":"Garbage_PerchCollection2", "p":15},
                                              {"asset":"Garbage_PerchCollection3", "p":100},
                                              {"asset":"Garbage_PerchCollection4", "p":80},
                                              {"asset":"Garbage_PerchCollection5", "p":35}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}