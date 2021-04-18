import os
from fitterlog.arg_proxy.types import Bool
from YTools.universe.temp_cwd import TempCWD
from subprocess import Popen , DEVNULL
from queue import Queue
import threading
from collections import namedtuple

def read_config_carg(config_path):
	'''读取一个标准格式的config文件中的命令行参数定义'''
	if not os.path.exists(config_path):
		raise "file does not exists."

	nspace = {}
	with open(config_path , "r") as fil:
		config_content = fil.read()

	exec(config_content , nspace)
	argprox = nspace["get_arg_proxy"]()

	return argprox

def read_config_rsc(config_path):
	'''读取一个标准格式的config文件中的资源需求定义'''
	if not os.path.exists(config_path):
		raise "file does not exists."

	nspace = {}
	with open(config_path , "r") as fil:
		config_content = fil.read()

	exec(config_content , nspace)
	rsc_aq = nspace["get_resource_acuire"]()

	return rsc_aq

def run_a_experiment(path , config_name , values , 
		command = "python" , entry_file = "main.py" , prefix = [], suffix = []):
	'''
		config_name: str。 对应的config文件的名。用于获得各个参数的类型。
		values: dict。 名-值字典，表示对应config项的赋值，如果没有赋值则使用默认值。
	'''

	argprox = read_config_carg(os.path.join(path , config_name))

	cmds = []
	for name , value in values.items():
		name = argprox.process_name(name)
		the_arg = argprox.name_to_arg(name) #允许前缀匹配

		if the_arg is None:
			continue
		if the_arg.type is Bool:
			if Bool(value):
				cmds.append("--{name}".format(name = the_arg.name))
		else:
			# "" is always acceptable while '' is only for linux.
			cmds.append("--{name}".format(name = the_arg.name))
			cmds.append(str(value))

	#组装完整命令
	full_cmd = prefix + [command , entry_file] + cmds + suffix

	with TempCWD(path): #切换当前工作目录到目标目录
		popen_ret = Popen(full_cmd)

	return popen_ret

class BatchRunner(threading.Thread):
	'''这个线程管理实验的运行'''

	Task = namedtuple("Task" , ["config_name" , "values" , "command" , "entry_file" , "prefix" , "suffix"])

	def __init__(self , father):
		'''
		task格式：[Task]
		'''
		super().__init__()
		self.setDaemon(True) #不负责结束

		self.father = father
		self.tasks = Queue() #等待运行的任务列表

		self.closed = False

	def run(self):
		while not self.closed:
			if self.tasks.empty():
				continue
			one_task = self.tasks.get()
			# run_a_experiment()

	def __del__(self):
		self.close()

	def close(self):
		self.closed = True
