from YTools.system.locker import Locker
import threading
import time
import os.path as P

class ClientMaintainer(threading.Thread):
	'''这个线程维护各种进程信息'''
	LIVE_LOCKER_PATH 		= "fitterlog/sentence/live/"
	RESOURCES_LOCKER_PATH 	= "fitterlog/sentence/resources/"

	def __init__(self , father):
		''''''
		super().__init__()
		self.setDaemon(True) #不负责结束

		self.father = father
		self.closed = False

	def run(self):
		father = self.father
		locker = father.locker

		while not self.closed:

			# 获得活动的句子列表
			now_live_clients = locker.ask_prefix(self.LIVE_LOCKER_PATH , only_suffix = True , not_none = True)
			now_live_clients = [int(x) for x in now_live_clients] 
			father.clients = now_live_clients

			# 获得资源占用列表
			clients_on_resources = father.empty_client_on_resources() # 生成报告表
			for resource_name , resource_ids in father.resource_ids.items():
				prefix = P.join(self.RESOURCES_LOCKER_PATH , resource_name)  # 查询的前缀
				now_clients = locker.ask_prefix(prefix , not_none = True) 	 # 获得所有占用这个资源的句子对应的key
				for client_key in now_clients:
					now_noun = int( P.relpath(client_key , prefix) ) # 获得句子编号
					now_ids = locker.get(client_key) 				 # 再查询一次获得具体占用资源的id
					if now_ids is None: #突然finish
						continue
					for _id in now_ids:								 # 填报告表
						clients_on_resources[resource_name][_id].append(now_noun)
			father.clients_on_resources = clients_on_resources

			time.sleep(father.SYNC_TIME)

	def __del__(self):
		self.close()

	def close(self):
		self.closed = True

class Master:
	LOCKER_PATH = "fitterlog/mastermain/"
	locker = Locker()

	SYNC_TIME = 0.05 #子进程行为同步时间

	def __init__(self , resources = []):
		'''

		resources: list of tuple
			resources[i] : [name , id_list , amount] 名称，实例列表，每个实例允许放几个进程
			amount 默认为1

		'''

		self.resource_names   = [x[0] for x in resources]
		self.resource_ids     = {x[0] : x[1] for x in resources}
		self.resource_amounts = {x[0] : 1 if len(x) <= 2 else x[2] for x in resources}

		self.clients = [] #目前活跃的句子列表（句子编号）
		self.clients_on_resources = self.empty_client_on_resources() #报告表，初始化为空

		# 获取活跃句子信息
		self.clientmaintainer = ClientMaintainer(self)
		self.clientmaintainer.start()

	def __del__(self):
		self.clientmaintainer.close()

	def ask_clients(self):
		'''获取当前所有活跃度句子列表'''
		return self.clients

	def ask_resources(self , res_name = None , res_id = None):
		'''获取所有的资源占用情况
		
		格式示例：
		{
			"gpu" : {
				0 : [] , 
				1 : [001 , 002] , 
				2 : [001 , ] , 
			}
		}
		'''
		ret = self.clients_on_resources
		if res_name is not None:
			ret = ret[res_name]
			if res_id is not None:
				ret = ret[res_id]

		return ret

	def empty_client_on_resources(self):
		'''生成一个空的resource报告表，方便填信息
			'''
		return {
			name : {
				_id : [] for _id in ids
			}
			for name , ids in self.resource_ids.items()
		}
