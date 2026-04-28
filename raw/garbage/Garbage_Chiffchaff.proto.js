{
"class" : "AssetPrototype",
"classname" : "Garbage_Chiffchaff",
"title" : "Пеночка",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":40, "one_of": [
                                              {"asset":"Garbage_Chiffchaff_Collection1", "p":100},
                                              {"asset":"Garbage_Chiffchaff_Collection2", "p":80},
                                              {"asset":"Garbage_Chiffchaff_Collection3", "p":35},
                                              {"asset":"Garbage_Chiffchaff_Collection4", "p":20},
                                              {"asset":"Garbage_Chiffchaff_Collection5", "p":80}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                              {"asset":"Garbage_Chiffchaff_Collection1", "p":100},
                                              {"asset":"Garbage_Chiffchaff_Collection2", "p":80},
                                              {"asset":"Garbage_Chiffchaff_Collection3", "p":35},
                                              {"asset":"Garbage_Chiffchaff_Collection4", "p":20},
                                              {"asset":"Garbage_Chiffchaff_Collection5", "p":80}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32433
}