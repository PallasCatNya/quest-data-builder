{
"class" : "AssetPrototype",
"classname" : "FlowerEith",
"title" : "Лютик",
"group" : "seeds",
"subgroup" : "flower",
"tags" : ["seed_simple","seed_flower","category_1"],
"can_be_gifted" : 1,
"price" : 10,
"currency" : "money_alt",
"req_user_level" : 1,
"meta_info" : "life=180;states=3",
"extra" : {"hide_in_shop":1, "can_spoil_be_extended":0, "lock_use_with_booster":1},
"shop_conditions" : "active_quest!=guest6_plant_lutiks+active_quest!=guest7_accelerate_lutiks+active_quest!=guest8_take_crop_lutiks",
"energy_cost" : "energy=1",
"accelerate_cost" : "asset=AccelerationPlantBooster:1",
"recover_cost" : "asset=RecoverPlantBooster:1",
"id" : 223810178,
"rand_reward" : {
                 "money_alt":16,
                 "pie":2,
                 "xp":2,
                 "all":[{"p":20,
                        "one_of":
                                 [{"asset":"Fl8Col1",	"p":100},
                                  {"asset":"Fl8Col2",	"p":100},
                                  {"asset":"Fl8Col3",	"p":5},
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
                                   {"asset":"Fl8Col3",	"p":5},
                                   {"asset":"Fl8Col4",	"p":30},
                                   {"asset":"Fl8Col5",	"p":100}]}]}
}