from .utils import *
import os

def run_a_experiment(path , config_file , values , command = "python" , entry_file = "main.py"):
	'''
		config_file: str。 对应的config文件的名。用于获得各个参数的类型。
		values: dict。 名-值字典。
	'''

	print (os.path.join(path , config_file))
	argprox = read_config(os.path.join(path , config_file))

	cmds = []
	for name , value in values.items():
		name = argprox.process_name(name)

		# "" is always acceptable while '' is only for linux.
		cmd = "--{name}=\"{value}\"".format(name = name , value = value) 
		cmds.append(cmd)

	cmd = "{command} {entry_file} {cmds}".format(
		command = command , entry_file = entry_file , cmds = " ".join(cmds)
	)

	# && is always acceptable while & is only for windows
	full_cmd = "cd {path} && {cmd}".format(path = path , cmd = cmd) 

	print (full_cmd)

	return os.system(full_cmd)
