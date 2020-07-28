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
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.tasks = []

	def add_task(self , path , config_name , values , 
			command = "python" , entry_file = "main.py" , prefix = "", suffix = ""):
		self.tasks.append( [path , config_name , values , command , entry_file , prefix, suffix] )

	def run(self):
		while True:
			time.sleep(1) # 等待一秒，防止并发错误

			if len(self.tasks) <= 0:
				continue
			task = self.tasks.pop(0)

			run_a_experiment(*task)

class ExperimentProxer_Torch(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)

		self.tasks = []
		self.picked = {}

	def get_mem_used_kth_gpu(self , k):
		handle = pynvml.nvmlDeviceGetHandleByIndex(k)
		meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
		return meminfo.used

	def get_gpu_num(self):
		return pynvml.nvmlDeviceGetCount()

	def good_gpu(self , k):
		mem_s = self.get_mem_used_kth_gpu(k)
		# if mem_s > 500 * 1024 * 1024: # 已用的内存大于500M，视为不可用
		if mem_s > 15 * 1024 * 1024: # 已用的内存大于15M，视为不可用
			return False
		return True

	def add_task(self , path , config_name , values , 
			command = "python" , entry_file = "main.py" , prefix = "", suffix = ""):
		if pynvml_failed:
			raise "PYNVML not useable"
		self.tasks.append( [path , config_name , values , command , entry_file , prefix, suffix] )

	def start_task_on_device(self , task , device):
		task[-2] = "CUDA_VISIBLE_DEVICES={0}".format(device) #前缀
		run_a_experiment(*task)

	def run(self):
		while True:
			time.sleep(10) # 等待10秒，防止并发错误，让显存加载
			if len(self.tasks) <= 0:
				continue
			task = self.tasks[0]

			flag = False # 是否成功运行了这个任务
			for k in range(self.get_gpu_num()):
				if self.good_gpu(k): 
					self.start_task_on_device(task , k)
					flag = True
					break
			if flag:
				self.tasks.pop(0) #成功运行任务，删除此任务

expe_prox_cpu = ExperimentProxer_CPU()
expe_prox_torch = ExperimentProxer_Torch()

expe_prox_cpu.start()
expe_prox_torch.start()