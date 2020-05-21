from .utils import *
import os
from subprocess import Popen , DEVNULL
from contextlib import redirect_stdout

def run_a_experiment(path , config_name , values , 
		command = "python" , entry_file = "main.py" , prefix = "", suffix = ""):
	from fitterlog.arg_proxy.types import Bool
	'''
		config_name: str。 对应的config文件的名。用于获得各个参数的类型。
		values: dict。 名-值字典。
	'''

	print (os.path.join(path , config_name))
	argprox = read_config(os.path.join(path , config_name))

	cmds = []
	for name , value in values.items():
		name = argprox.process_name(name)

		the_arg = argprox.name2arg.get(name)
		if the_arg is None:
			continue
		if the_arg.type is Bool:
			if not Bool(value):
				cmd = ""
			else:
				cmd = "--{name}".format(name = name)
		else:
			# "" is always acceptable while '' is only for linux.
			cmd = "--{name}=\"{value}\"".format(name = name , value = value) 

		cmds.append(cmd)

	cmd = "{prefix} {command} {entry_file} {cmds} {suffix}".format(
		prefix = prefix , command = command , entry_file = entry_file , cmds = " ".join(cmds) , suffix = suffix , 
	)

	# && is always acceptable while & is only for windows
	full_cmd = "cd {path} && {cmd}".format(path = path , cmd = cmd) 

	return Popen(full_cmd , shell = True , stdout = DEVNULL)
