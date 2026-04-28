{
"class" : "AssetPrototype",
"classname" : "Valve",
"title" : "Вентиль",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 14621,
"rand_reward" : {"all": [
                          {"p":75, "one_of": [
                                              {"asset":"ValveCollection1", "p":25},
                                              {"asset":"ValveCollection2", "p":50},
                                              {"asset":"ValveCollection3", "p":75},
                                              {"asset":"ValveCollection4", "p":100},
                                              {"asset":"ValveCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":55, "one_of": [
                                                {"asset":"ValveCollection1", "p":25},
                                                {"asset":"ValveCollection2", "p":50},
                                                {"asset":"ValveCollection3", "p":75},
                                                {"asset":"ValveCollection4", "p":100},
                                                {"asset":"ValveCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}