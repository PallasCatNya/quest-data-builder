{
"class" : "AssetPrototype",
"classname" : "Garbage_TornStrap",
"title" : "Порванный ремешок часов",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 26425,
"rand_reward" : {"all": [
                          {"p":40, "one_of": [
                                              {"asset":"Garbage_TornStrapCollection1", "p":100},
                                              {"asset":"Garbage_TornStrapCollection2", "p":30},
                                              {"asset":"Garbage_TornStrapCollection3", "p":50},
                                              {"asset":"Garbage_TornStrapCollection4", "p":100},
                                              {"asset":"Garbage_TornStrapCollection5", "p":40}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":20, "one_of": [
                                                {"asset":"Garbage_TornStrapCollection1", "p":100},
                                                {"asset":"Garbage_TornStrapCollection2", "p":30},
                                                {"asset":"Garbage_TornStrapCollection3", "p":50},
                                                {"asset":"Garbage_TornStrapCollection4", "p":100},
                                                {"asset":"Garbage_TornStrapCollection5", "p":40}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}