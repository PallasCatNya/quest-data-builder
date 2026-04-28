{
"class" : "AssetPrototype",
"classname" : "Ashes",
"title" : "Пепел",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 14624,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"AshesCollection1", "p":80},
                                              {"asset":"AshesCollection2", "p":80},
                                              {"asset":"AshesCollection3", "p":80},
                                              {"asset":"AshesCollection4", "p":50},
                                              {"asset":"AshesCollection5", "p":25}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":25, "one_of": [
                                                {"asset":"AshesCollection1", "p":80},
                                                {"asset":"AshesCollection2", "p":80},
                                                {"asset":"AshesCollection3", "p":80},
                                                {"asset":"AshesCollection4", "p":50},
                                                {"asset":"AshesCollection5", "p":25}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}