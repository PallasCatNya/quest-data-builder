{
"class" : "AssetPrototype",
"classname" : "DrCap",
"title" : "Шапочка доктора",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 10963 ,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"DrCapCollection1", "p":50},
                                              {"asset":"DrCapCollection2", "p":50},
                                              {"asset":"DrCapCollection3", "p":100},
                                              {"asset":"DrCapCollection4", "p":100},
                                              {"asset":"DrCapCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":50, "one_of": [
                                                {"asset":"DrCapCollection1", "p":50},
                                                {"asset":"DrCapCollection2", "p":50},
                                                {"asset":"DrCapCollection3", "p":100},
                                                {"asset":"DrCapCollection4", "p":100},
                                                {"asset":"DrCapCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}