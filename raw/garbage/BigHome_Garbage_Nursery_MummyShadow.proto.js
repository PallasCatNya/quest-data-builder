{
"class" : "AssetPrototype",
"classname" : "BigHome_Garbage_Nursery_MummyShadow",
"stuff_icon" : "BigHome_Garbage_Nursery_MummyShadowIcon",
"title" : "Муми-тень",
"group" : "garbage",
"subgroup" : "on_the_wall",
"g_pest_probability_percent" : "16",
"behaviour" : [{"type":"fly", "distance":200}],
"rand_reward" : 
	{"all": 
		[
			{"p":40, "one_of": 
				[
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection1", "p":36},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection2", "p":100},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection3", "p":50},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection4", "p":50},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection5", "p":25}
				]
			},
			{"p":5, "energy":1}
		],
		"money_alt":1,
		"xp":1
	},
"rand_reward_in_guest" : 
	{"all": 
		[
			{"p":30, "one_of": 
				[
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection1", "p":36},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection2", "p":100},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection3", "p":50},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection4", "p":50},
					{"asset":"BigHome_Garbage_Nursery_MummyShadow_Collection5", "p":25}
				]
			},
			{"p":5, "energy":1}
		],
		"money_alt":1,
		"reputation_progress":1,
		"xp":1
	},
"id" : 70152
}