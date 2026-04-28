{
"class" : "AssetPrototype",
"classname" : "Barometer",
"title" : "Разбитый барометр",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 17710,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"BarometerCollection1", "p":15},
                                              {"asset":"BarometerCollection2", "p":60},
                                              {"asset":"BarometerCollection3", "p":100},
                                              {"asset":"BarometerCollection4", "p":50},
                                              {"asset":"BarometerCollection5", "p":27}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":60, "one_of": [
                                                {"asset":"BarometerCollection1", "p":60},
                                                {"asset":"BarometerCollection2", "p":15},
                                                {"asset":"BarometerCollection3", "p":100},
                                                {"asset":"BarometerCollection4", "p":100},
                                                {"asset":"BarometerCollection5", "p":84}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}