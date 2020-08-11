def get_search_space():
	return {
		"command" 		: "python" , 
		"entry_file" 	: "main_tc.py" , 
		"config_file" 	: "config.py", 
		"gpus"			: [0 ,] , 
		"max_proc_num"	: 2 ,
		"wait_time"		: 3 ,
		"is_torch" 		: True, 
		"space" : {
			"n" : [10  , 20],
			"lr" : [0.3  , 2333 , 999],
			"group" : ["st_tc_tes_6"] ,  
		},
	}