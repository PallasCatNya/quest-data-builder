{
"class" : "AssetPrototype",
"classname" : "BrokenBarrel",
"title" : "Разбитая бочка",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 17711,
"rand_reward" : {"all": [
                          {"p":65, "one_of": [
                                              {"asset":"BrokenBarrelCollection1", "p":100},
                                              {"asset":"BrokenBarrelCollection2", "p":100},
                                              {"asset":"BrokenBarrelCollection3", "p":100},
                                              {"asset":"BrokenBarrelCollection4", "p":70},
                                              {"asset":"BrokenBarrelCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":50, "one_of": [
                                                {"asset":"BrokenBarrelCollection1", "p":100},
                                                {"asset":"BrokenBarrelCollection2", "p":100},
                                                {"asset":"BrokenBarrelCollection3", "p":100},
                                                {"asset":"BrokenBarrelCollection4", "p":70},
                                                {"asset":"BrokenBarrelCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}