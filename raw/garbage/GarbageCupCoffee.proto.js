{
"class" : "AssetPrototype",
"classname" : "GarbageCupCoffee",
"title" : "Смятый стаканчик из-под кофе",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 23703,
"rand_reward" : {"all": [
                          {"p":50, "one_of": [
                                              {"asset":"GarbageCupCoffeeCollection1", "p":50},
                                              {"asset":"GarbageCupCoffeeCollection2", "p":5},
                                              {"asset":"GarbageCupCoffeeCollection3", "p":100},
                                              {"asset":"GarbageCupCoffeeCollection4", "p":50},
                                              {"asset":"GarbageCupCoffeeCollection5", "p":35}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":25, "one_of": [
                                                {"asset":"GarbageCupCoffeeCollection1", "p":25},
                                                {"asset":"GarbageCupCoffeeCollection2", "p":5},
                                                {"asset":"GarbageCupCoffeeCollection3", "p":100},
                                                {"asset":"GarbageCupCoffeeCollection4", "p":50},
                                                {"asset":"GarbageCupCoffeeCollection5", "p":35}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}