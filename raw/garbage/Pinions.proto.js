{
"class" : "AssetPrototype",
"classname" : "Pinions",
"title" : "Горстка перьев",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : "214",
"rand_reward" : {"all": [
                          {"p":75, "one_of": [
                                              {"asset":"PinionsCollection1", "p":100},
                                              {"asset":"PinionsCollection2", "p":100},
                                              {"asset":"PinionsCollection3", "p":100},
                                              {"asset":"PinionsCollection4", "p":100},
                                              {"asset":"PinionsCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                                {"asset":"PinionsCollection1", "p":100},
                                                {"asset":"PinionsCollection2", "p":100},
                                                {"asset":"PinionsCollection3", "p":15},
                                                {"asset":"PinionsCollection4", "p":100},
                                                {"asset":"PinionsCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}