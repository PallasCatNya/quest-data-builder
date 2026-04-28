{
"class" : "AssetPrototype",
"classname" : "Goldfish",
"title" : "Золотая рыбка",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 9674 ,
"rand_reward" : {"all": [
                          {"p":60, "one_of": [
                                              {"asset":"GoldfishCollection1", "p":100},
                                              {"asset":"GoldfishCollection2", "p":100},
                                              {"asset":"GoldfishCollection3", "p":100},
                                              {"asset":"GoldfishCollection4", "p":50},
                                              {"asset":"GoldfishCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":60, "one_of": [
                                                {"asset":"GoldfishCollection1", "p":100},
                                                {"asset":"GoldfishCollection2", "p":100},
                                                {"asset":"GoldfishCollection3", "p":100},
                                                {"asset":"GoldfishCollection4", "p":50},
                                                {"asset":"GoldfishCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}