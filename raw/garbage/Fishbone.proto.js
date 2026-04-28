{
"class" : "AssetPrototype",
"classname" : "Fishbone",
"title" : "Рыбий скелет",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 9673 ,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"FishboneCollection1", "p":100},
                                              {"asset":"FishboneCollection2", "p":80},
                                              {"asset":"FishboneCollection3", "p":100},
                                              {"asset":"FishboneCollection4", "p":100},
                                              {"asset":"FishboneCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":50, "one_of": [
                                                {"asset":"FishboneCollection1", "p":100},
                                                {"asset":"FishboneCollection2", "p":80},
                                                {"asset":"FishboneCollection3", "p":100},
                                                {"asset":"FishboneCollection4", "p":100},
                                                {"asset":"FishboneCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}