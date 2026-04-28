{
"class" : "AssetPrototype",
"classname" : "FlowerEith_ForTutorial",
"title" : "Лютик",
"group" : "seeds",
"subgroup" : "flower",
"tags" : ["seed_simple","category_1"],
"can_be_gifted" : 1,
"price" : 10,
"currency" : "money_alt",
"req_user_level" : 1,
"meta_info" : "life=600;states=3;spoil_period=3600",
"extra" : {"hide_in_shop":1, "hide_in_hint":1, "can_spoil_be_extended":0, "lock_use_with_booster":1},
"shop_conditions" : "active_quest=guest6_plant_lutiks||guest7_accelerate_lutiks||guest8_take_crop_lutiks",
"energy_cost" : "energy=1",
"accelerate_cost" : "asset=AccelerationPlantBooster:1",
"recover_cost" : "asset=RecoverPlantBooster:1",
"id" : 10655,
"rand_reward" : {
                 "money_alt":16,
                 "pie":2,
                 "xp":2,
                 "all":[{"p":20,
                        "one_of":
                                 [{"asset":"Fl8Col1",	"p":100},
                                  {"asset":"Fl8Col2",	"p":100},
                                  {"asset":"Fl8Col3",	"p":7},
                                  {"asset":"Fl8Col4",	"p":30},
                                  {"asset":"Fl8Col5",	"p":100}]}]},
"rand_reward_in_guest" : {
                  "money_alt":1,
                  "pie":1,
                  "reputation_progress":1,
                  "xp":1,
                  "all":
                        [{"p":20,
                         "one_of":
                                  [{"asset":"Fl8Col1",	"p":100},
                                   {"asset":"Fl8Col2",  "p":100},
                                   {"asset":"Fl8Col3",	"p":7},
                                   {"asset":"Fl8Col4",	"p":30},
                                   {"asset":"Fl8Col5",	"p":100}]}]}
}