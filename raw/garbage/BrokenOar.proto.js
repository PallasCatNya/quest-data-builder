{
"class" : "AssetPrototype",
"classname" : "BrokenOar",
"title" : "Сломанное весло",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 9672 ,
"rand_reward" : {"all": [
                          {"p":35, "one_of": [
                                              {"asset":"BrokenOarCollection1", "p":100},
                                              {"asset":"BrokenOarCollection2", "p":100},
                                              {"asset":"BrokenOarCollection3", "p":10},
                                              {"asset":"BrokenOarCollection4", "p":100},
                                              {"asset":"BrokenOarCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":35, "one_of": [
                                                {"asset":"BrokenOarCollection1", "p":100},
                                                {"asset":"BrokenOarCollection2", "p":100},
                                                {"asset":"BrokenOarCollection3", "p":10},
                                                {"asset":"BrokenOarCollection4", "p":100},
                                                {"asset":"BrokenOarCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}