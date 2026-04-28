{
"class" : "AssetPrototype",
"classname" : "BigHome_Garbage_Server_BrokenCable",
"title" : "Обрывок кабеля",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "10",
"rand_reward" : 
	{"all": 
		[
			{"p":40, "one_of": 
				[
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection1", "p":100},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection2", "p":50},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection3", "p":40},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection4", "p":20},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection5", "p":80}
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
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection1", "p":90},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection2", "p":50},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection3", "p":40},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection4", "p":15},
					{"asset":"BigHome_Garbage_Server_BrokenCable_Collection5", "p":80}
				]
			},
			{"p":5, "energy":1}
		],
		"money_alt":1,
		"reputation_progress":2,
		"xp":2
	},
"id" : 44999
}