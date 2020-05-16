import os

def read_config(config_path):
	if not os.path.exists(config_path):
		raise "file does not exists."

	nspace = {}
	with open(config_path , "r") as fil:
		config_content = fil.read()

	exec(config_content , nspace)
	argprox = nspace["get_arg_proxy"]()

	return argprox
