{
"class" : "AssetPrototype",
"classname" : "BrokenTyre",
"title" : "Рваная шина",
"group" : "garbage",
"subgroup" : "on_the_floor",
"g_pest_probability_percent" : "16",
"id" : 6401,
"rand_reward" : {"all":
		[{"p":60,
			"one_of":
  		[
  		    {"asset":"TireServiceCollection1",
  					"p":25},
  				{"asset":"TireServiceCollection2",
  					"p":100},
  				{"asset":"TireServiceCollection3",
  					"p":100},
  				{"asset":"TireServiceCollection4",
  					"p":50 },
  				{"asset":"TireServiceCollection5",
  					"p":75}
  		]
  	 }
		],
		"money_alt":2,
  	"xp":3},
"rand_reward_in_guest" : {"all":
		[{"p":40,
			"one_of":
		[{"asset":"TireServiceCollection1",
					"p":25},
				{"asset":"TireServiceCollection2",
					"p":100},
				{"asset":"TireServiceCollection3",
					"p":100},
				{"asset":"TireServiceCollection4",
					"p":50},
				{"asset":"TireServiceCollection5",
					"p":75}]}],
	"money_alt":2,
	"reputation_progress":1,
	"xp":3}
}