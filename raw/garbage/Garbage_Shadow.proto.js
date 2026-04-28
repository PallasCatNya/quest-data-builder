{
"class" : "AssetPrototype",
"classname" : "Garbage_Shadow",
"title" : "Тень",
"group" : "garbage",
"subgroup" : "on_the_wall",
"g_pest_probability_percent" : "16",
"id" : 25506,
"rand_reward" : {"all": [
                          {"p":60, "one_of": [
                                              {"asset":"Garbage_ShadowCollection1", "p":100},
                                              {"asset":"Garbage_ShadowCollection2", "p":10},
                                              {"asset":"Garbage_ShadowCollection3", "p":100},
                                              {"asset":"Garbage_ShadowCollection4", "p":80},
                                              {"asset":"Garbage_ShadowCollection5", "p":30}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                                {"asset":"Garbage_ShadowCollection1", "p":100},
                                                {"asset":"Garbage_ShadowCollection2", "p":10},
                                                {"asset":"Garbage_ShadowCollection3", "p":100},
                                                {"asset":"Garbage_ShadowCollection4", "p":80},
                                                {"asset":"Garbage_ShadowCollection5", "p":30}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}