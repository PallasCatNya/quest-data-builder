{
"class" : "AssetPrototype",
"classname" : "Pill",
"title" : "Пилюля",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 10967 ,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"PillCollection1", "p":100},
                                              {"asset":"PillCollection2", "p":25},
                                              {"asset":"PillCollection3", "p":100},
                                              {"asset":"PillCollection4", "p":100},
                                              {"asset":"PillCollection5", "p":8}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"PillCollection1", "p":100},
                                                {"asset":"PillCollection2", "p":25},
                                                {"asset":"PillCollection3", "p":100},
                                                {"asset":"PillCollection4", "p":100},
                                                {"asset":"PillCollection5", "p":8}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}