import threading
from .cmd_start import run_a_experiment
import pynvml
import time

pynvml_failed = False
try:
	pynvml.nvmlInit()
except pynvml.nvml.NVMLError_LibraryNotFound:
	pynvml_failed = True

class ExperimentProxer_CPU(threading.Thread):
	def __init__(self , wait_time = 0):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.tasks = []
		self.protect = True #设置这个变量来防止代理器还没添加任务就被意外删除。在添加任务完毕后关闭保护。
		self.wait_time = wait_time
		self.closed = False
	def add_task(self , path , config_name , values , 
			command = "python" , entry_file = "main.py" , prefix = "", suffix = ""):
		self.tasks.append( [path , config_name , values , command , entry_file , prefix, suffix] )

	def run(self):
		while not self.closed:
			time.sleep(self.wait_time + 1) # 等待多一秒，防止并发错误

			if len(self.tasks) <= 0:
				continue
			task = self.tasks.pop(0)

			run_a_experiment(*task)

	def close(self): #结束任务
		self.closed = True

class ExperimentProxer_Torch(threading.Thread):

	def __init__(self , gpus = [0] , max_process = 1 , wait_time = 0):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.tasks = []
		self.gpus = gpus
		self.max_process = max_process
		self.protect = True
		self.wait_time = wait_time

		self.closed = False


	def good_gpu(self , k):
		if pynvml_failed:
			raise "PYNVML not useable"
		handle = pynvml.nvmlDeviceGetHandleByIndex(k)
		process = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)

		return len(process) < self.max_process

	def add_task(self , path , config_name , values , 
			command = "python" , entry_file = "main.py" , prefix = "", suffix = ""):
		self.tasks.append( [path , config_name , values , command , entry_file , prefix, suffix] )

	def start_task_on_device(self , task , device):
		task[-2] = "CUDA_VISIBLE_DEVICES={0}".format(device) #前缀
		run_a_experiment(*task)

	def run(self):
		while not self.closed:
			time.sleep(self.wait_time + 1) # 防止并发错误

			if len(self.tasks) <= 0:
				continue

			task = self.tasks[0]

			flag = False # 是否成功运行了这个任务
			for k in self.gpus:
				if self.good_gpu(k): 
					self.start_task_on_device(task , k)
					flag = True
					break
			if flag:
				self.tasks.pop(0) #成功运行任务，删除此任务
	def close(self):
		self.closed = True

# expe_prox_cpu = ExperimentProxer_CPU()
# expe_prox_torch = ExperimentProxer_Torch()
# 
# expe_prox_cpu.start()
# expe_prox_torch.start()