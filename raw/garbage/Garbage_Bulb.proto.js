{
"class" : "AssetPrototype",
"classname" : "Garbage_Bulb",
"title" : "Опрокинутая колба",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 27787,
"rand_reward" : {"all": [
                          {"p":55, "one_of": [
                                              {"asset":"Garbage_BulbCollection1", "p":100},
                                              {"asset":"Garbage_BulbCollection2", "p":90},
                                              {"asset":"Garbage_BulbCollection3", "p":70},
                                              {"asset":"Garbage_BulbCollection4", "p":100},
                                              {"asset":"Garbage_BulbCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                                {"asset":"Garbage_BulbCollection1", "p":100},
                                                {"asset":"Garbage_BulbCollection2", "p":90},
                                                {"asset":"Garbage_BulbCollection3", "p":70},
                                                {"asset":"Garbage_BulbCollection4", "p":100},
                                                {"asset":"Garbage_BulbCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}