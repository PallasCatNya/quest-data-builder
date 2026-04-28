{
"class" : "AssetPrototype",
"classname" : "Garbage_Armor",
"title" : "Доспех с гербом",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 30114,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"Garbage_ArmorCollection1", "p":30},
                                              {"asset":"Garbage_ArmorCollection2", "p":90},
                                              {"asset":"Garbage_ArmorCollection3", "p":70},
                                              {"asset":"Garbage_ArmorCollection4", "p":100},
                                              {"asset":"Garbage_ArmorCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                              {"asset":"Garbage_ArmorCollection1", "p":30},
                                              {"asset":"Garbage_ArmorCollection2", "p":90},
                                              {"asset":"Garbage_ArmorCollection3", "p":70},
                                              {"asset":"Garbage_ArmorCollection4", "p":100},
                                              {"asset":"Garbage_ArmorCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}