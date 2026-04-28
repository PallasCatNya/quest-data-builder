{
"class" : "AssetPrototype",
"classname" : "Garbage_Chandelier",
"title" : "Канделябр",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 25504,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"Garbage_ChandelierCollection1", "p":100},
                                              {"asset":"Garbage_ChandelierCollection2", "p":40},
                                              {"asset":"Garbage_ChandelierCollection3", "p":100},
                                              {"asset":"Garbage_ChandelierCollection4", "p":75},
                                              {"asset":"Garbage_ChandelierCollection5", "p":25}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"Garbage_ChandelierCollection1", "p":100},
                                                {"asset":"Garbage_ChandelierCollection2", "p":40},
                                                {"asset":"Garbage_ChandelierCollection3", "p":100},
                                                {"asset":"Garbage_ChandelierCollection4", "p":75},
                                                {"asset":"Garbage_ChandelierCollection5", "p":25}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}