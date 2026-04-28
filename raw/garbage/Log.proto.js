{
"class" : "AssetPrototype",
"classname" : "Log",
"title" : "Обгорелое бревно",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 14623,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"LogCollection1", "p":100},
                                              {"asset":"LogCollection2", "p":25},
                                              {"asset":"LogCollection3", "p":100},
                                              {"asset":"LogCollection4", "p":100},
                                              {"asset":"LogCollection5", "p":30}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":35, "one_of": [
                                                {"asset":"LogCollection1", "p":100},
                                                {"asset":"LogCollection2", "p":25},
                                                {"asset":"LogCollection3", "p":100},
                                                {"asset":"LogCollection4", "p":100},
                                                {"asset":"LogCollection5", "p":30}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}