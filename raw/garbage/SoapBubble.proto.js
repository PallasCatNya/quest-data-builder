{
"class" : "AssetPrototype",
"classname" : "SoapBubble",
"title" : "Мыльный пузырь",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 21357,
"rand_reward" : {"all": [
                          {"p":75, "one_of": [
                                              {"asset":"SoapBubbleCollection1", "p":100},
                                              {"asset":"SoapBubbleCollection2", "p":100},
                                              {"asset":"SoapBubbleCollection3", "p":30},
                                              {"asset":"SoapBubbleCollection4", "p":100},
                                              {"asset":"SoapBubbleCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":60, "one_of": [
                                                {"asset":"SoapBubbleCollection1", "p":100},
                                                {"asset":"SoapBubbleCollection2", "p":100},
                                                {"asset":"SoapBubbleCollection3", "p":10},
                                                {"asset":"SoapBubbleCollection4", "p":100},
                                                {"asset":"SoapBubbleCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}