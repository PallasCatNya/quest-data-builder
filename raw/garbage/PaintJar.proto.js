{
"class" : "AssetPrototype",
"classname" : "PaintJar",
"title" : "Баночка с рассыпавшейся краской",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : 16,
"rand_reward" : {"all":
                        [{"p":75,
                          "one_of":
                                    [{"asset":"PaintJar1", "p":100},
                                     {"asset":"PaintJar2", "p":100},
                                     {"asset":"PaintJar3", "p":100},
                                     {"asset":"PaintJar4", "p":100},
                                     {"asset":"PaintJar5", "p":100}]},
                        {"p":5,"energy":1}],
                "money_alt":1,
                "xp":1},
"rand_reward_in_guest" : {"all":
                                [{"p":10,
                                 "one_of":
                                          [{"asset":"PaintJar1", "p":100},
                                           {"asset":"PaintJar2", "p":100},
                                           {"asset":"PaintJar3", "p":100},
                                           {"asset":"PaintJar4", "p":100},
                                           {"asset":"PaintJar5", "p":100}]},
                                  {"p":5, "energy":1}],
                          "money_alt":1,
                          "reputation_progress":1,
                          "xp":1},
"id" : 6164
}