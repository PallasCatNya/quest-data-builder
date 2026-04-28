{
"class" : "AssetPrototype",
"classname" : "GarbageSphere",
"title" : "Сфера",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 23934,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"GarbageSphereCollection1", "p":100},
                                              {"asset":"GarbageSphereCollection2", "p":100},
                                              {"asset":"GarbageSphereCollection3", "p":100},
                                              {"asset":"GarbageSphereCollection4", "p":70},
                                              {"asset":"GarbageSphereCollection5", "p":40}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"GarbageSphereCollection1", "p":100},
                                                {"asset":"GarbageSphereCollection2", "p":100},
                                                {"asset":"GarbageSphereCollection3", "p":100},
                                                {"asset":"GarbageSphereCollection4", "p":70},
                                                {"asset":"GarbageSphereCollection5", "p":40}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}