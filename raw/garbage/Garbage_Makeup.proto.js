{
"class" : "AssetPrototype",
"classname" : "Garbage_Makeup",
"title" : "Косметика",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 26135,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"Garbage_MakeupCollection1", "p":100},
                                              {"asset":"Garbage_MakeupCollection2", "p":10},
                                              {"asset":"Garbage_MakeupCollection3", "p":100},
                                              {"asset":"Garbage_MakeupCollection4", "p":100},
                                              {"asset":"Garbage_MakeupCollection5", "p":40}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"Garbage_MakeupCollection1", "p":100},
                                                {"asset":"Garbage_MakeupCollection2", "p":10},
                                                {"asset":"Garbage_MakeupCollection3", "p":100},
                                                {"asset":"Garbage_MakeupCollection4", "p":100},
                                                {"asset":"Garbage_MakeupCollection5", "p":40}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}