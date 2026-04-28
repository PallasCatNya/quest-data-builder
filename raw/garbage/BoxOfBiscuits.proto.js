{
"class" : "AssetPrototype",
"classname" : "BoxOfBiscuits",
"title" : "Коробка печенья",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 21358,
"rand_reward" : {"all": [
                          {"p":80, "one_of": [
                                              {"asset":"BoxOfBiscuitsCollection1", "p":60},
                                              {"asset":"BoxOfBiscuitsCollection2", "p":100},
                                              {"asset":"BoxOfBiscuitsCollection3", "p":100},
                                              {"asset":"BoxOfBiscuitsCollection4", "p":25},
                                              {"asset":"BoxOfBiscuitsCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":2
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":70, "one_of": [
                                                {"asset":"BoxOfBiscuitsCollection1", "p":60},
                                                {"asset":"BoxOfBiscuitsCollection2", "p":100},
                                                {"asset":"BoxOfBiscuitsCollection3", "p":100},
                                                {"asset":"BoxOfBiscuitsCollection4", "p":12},
                                                {"asset":"BoxOfBiscuitsCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}