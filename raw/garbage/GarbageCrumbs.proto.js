{
"class" : "AssetPrototype",
"classname" : "GarbageCrumbs",
"title" : "Крошки",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 23701,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"GarbageCrumbsCollection1", "p":100},
                                              {"asset":"GarbageCrumbsCollection2", "p":38},
                                              {"asset":"GarbageCrumbsCollection3", "p":100},
                                              {"asset":"GarbageCrumbsCollection4", "p":75},
                                              {"asset":"GarbageCrumbsCollection5", "p":20}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":30, "one_of": [
                                                {"asset":"GarbageCrumbsCollection1", "p":100},
                                                {"asset":"GarbageCrumbsCollection2", "p":37},
                                                {"asset":"GarbageCrumbsCollection3", "p":100},
                                                {"asset":"GarbageCrumbsCollection4", "p":75},
                                                {"asset":"GarbageCrumbsCollection5", "p":20}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}