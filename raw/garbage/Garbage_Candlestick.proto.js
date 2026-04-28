{
"class" : "AssetPrototype",
"classname" : "Garbage_Candlestick",
"title" : "Подсвечник",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"energy_cost" : "dexterity=1",
"rand_reward" : {"all": [
                          {"p":55, "one_of": [
                                              {"asset":"Garbage_Candlestick_Collection1", "p":100},
                                              {"asset":"Garbage_Candlestick_Collection2", "p":100},
                                              {"asset":"Garbage_Candlestick_Collection3", "p":20},
                                              {"asset":"Garbage_Candlestick_Collection4", "p":60},
                                              {"asset":"Garbage_Candlestick_Collection5", "p":20}
                                            ]
                          },
                          {"p":5, "dexterity":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":40, "one_of": [
                                              {"asset":"Garbage_Candlestick_Collection1", "p":100},
                                              {"asset":"Garbage_Candlestick_Collection2", "p":100},
                                              {"asset":"Garbage_Candlestick_Collection3", "p":20},
                                              {"asset":"Garbage_Candlestick_Collection4", "p":60},
                                              {"asset":"Garbage_Candlestick_Collection5", "p":20}
                                              ]
                                    }
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1},
"id" : 32431
}