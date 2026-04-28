{
"class" : "AssetPrototype",
"classname" : "GarbageSpoon",
"title" : "Половник",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 23702,
"rand_reward" : {"all": [
                          {"p":60, "one_of": [
                                              {"asset":"GarbageSpoonCollection1", "p":100},
                                              {"asset":"GarbageSpoonCollection2", "p":48},
                                              {"asset":"GarbageSpoonCollection3", "p":100},
                                              {"asset":"GarbageSpoonCollection4", "p":86},
                                              {"asset":"GarbageSpoonCollection5", "p":30}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"GarbageSpoonCollection1", "p":100},
                                                {"asset":"GarbageSpoonCollection2", "p":48},
                                                {"asset":"GarbageSpoonCollection3", "p":100},
                                                {"asset":"GarbageSpoonCollection4", "p":86},
                                                {"asset":"GarbageSpoonCollection5", "p":30}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}