{
"class" : "AssetPrototype",
"classname" : "BrokenStick",
"title" : "Сломанный посох",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 21350,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"BrokenStickCollection1", "p":100},
                                              {"asset":"BrokenStickCollection2", "p":100},
                                              {"asset":"BrokenStickCollection3", "p":100},
                                              {"asset":"BrokenStickCollection4", "p":100},
                                              {"asset":"BrokenStickCollection5", "p":87}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":60, "one_of": [
                                                {"asset":"BrokenStickCollection1", "p":100},
                                                {"asset":"BrokenStickCollection2", "p":100},
                                                {"asset":"BrokenStickCollection3", "p":100},
                                                {"asset":"BrokenStickCollection4", "p":100},
                                                {"asset":"BrokenStickCollection5", "p":20}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}