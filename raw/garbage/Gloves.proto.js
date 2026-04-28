{
"class" : "AssetPrototype",
"classname" : "Gloves",
"title" : "Грязные рукавицы",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 14622,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"GlovesCollection1", "p":50},
                                              {"asset":"GlovesCollection2", "p":50},
                                              {"asset":"GlovesCollection3", "p":100},
                                              {"asset":"GlovesCollection4", "p":15},
                                              {"asset":"GlovesCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":50, "one_of": [
                                                {"asset":"GlovesCollection1", "p":50},
                                                {"asset":"GlovesCollection2", "p":50},
                                                {"asset":"GlovesCollection3", "p":100},
                                                {"asset":"GlovesCollection4", "p":15},
                                                {"asset":"GlovesCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}