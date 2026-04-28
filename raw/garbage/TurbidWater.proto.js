{
"class" : "AssetPrototype",
"classname" : "TurbidWater",
"title" : "Мутная вода",
"group" : "garbage",
"subgroup" : "on_the_wall",
"g_pest_probability_percent" : "16",
"id" : 19505,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"TurbidWaterCollection1", "p":100},
                                              {"asset":"TurbidWaterCollection2", "p":80},
                                              {"asset":"TurbidWaterCollection3", "p":80},
                                              {"asset":"TurbidWaterCollection4", "p":44},
                                              {"asset":"TurbidWaterCollection5", "p":26}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":60, "one_of": [
                                                {"asset":"TurbidWaterCollection1", "p":100},
                                                {"asset":"TurbidWaterCollection2", "p":85},
                                                {"asset":"TurbidWaterCollection3", "p":85},
                                                {"asset":"TurbidWaterCollection4", "p":59},
                                                {"asset":"TurbidWaterCollection5", "p":30}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}