{
"class" : "AssetPrototype",
"classname" : "Bulletin",
"title" : "Бюллетень",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 10964 ,
"rand_reward" : {"all": [
                          {"p":75, "one_of": [
                                              {"asset":"BulletinCollection1", "p":50},
                                              {"asset":"BulletinCollection2", "p":50},
                                              {"asset":"BulletinCollection3", "p":75},
                                              {"asset":"BulletinCollection4", "p":100},
                                              {"asset":"BulletinCollection5", "p":100}
                                            ]
                          },
                          {"p":5, "energy":1}
                        ],
                  "money_alt":1,
                  "xp":1
                },
"rand_reward_in_guest" : {"all": [
                                    {"p":55, "one_of": [
                                                {"asset":"BulletinCollection1", "p":50},
                                                {"asset":"BulletinCollection2", "p":50},
                                                {"asset":"BulletinCollection3", "p":75},
                                                {"asset":"BulletinCollection4", "p":100},
                                                {"asset":"BulletinCollection5", "p":100}
                                              ]
                                    },
                                    {"p":5, "energy":1}
                                ],
                        "money_alt":1,
                        "reputation_progress":1,
                        "xp":1}
}