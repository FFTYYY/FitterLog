from YTools.system.locker import Locker
from YTools.universe.onexit import add_quit_methods
import threading
import time

class ClientMaintainer(threading.Thread):
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
			now_live_clients = locker.ask_prefix(self.LIVE_LOCKER_PATH)
			now_live_clients = [int(x[len(self.LIVE_LOCKER_PATH):-1]) for x in now_live_clients] 
			father.clients = now_live_clients

			# 获得资源占用列表
			clients_on_resources = father.empty_client_on_resources() #生成报告表
			for resource_name , resource_ids in father.resources:
				prefix = self.RESOURCES_LOCKER_PATH + resource_name + "/" #查询的前缀
				now_clients = locker.ask_prefix(prefix) 			#获得所有占用这个资源的句子对应的key
				for client_key in now_clients:
					now_noun = int( client_key[len(prefix):-1] ) 	#获得句子编号
					now_ids = locker.get(client_key) 				#再查询一次获得具体占用资源的id
					for _id in now_ids:	# 填报告表
						clients_on_resources[resource_name][_id].append(now_noun)
			father.clients_on_resources = clients_on_resources

			time.sleep(0.1)

	def __del__(self):
		self.close()

	def close(self):
		self.closed = True

class Master:
	LOCKER_PATH = "fitterlog/mastermain/"
	locker = Locker()

	def __init__(self , resources = []):
		'''

		resources: list of tuple
			resources[i] : [name , id_list]

		'''

		self.resources = resources

		self.clients = [] #目前活跃的句子列表（句子编号）
		self.clients_on_resources = self.empty_client_on_resources() #报告表

		self.clientmaintainer = ClientMaintainer(self)
		self.clientmaintainer.start()

	def __del__(self):
		self.clientmaintainer.close()

	def ask_clients(self):
		return self.clients

	def ask_resources(self , res_name = None , res_id = None):

		ret = self.clients_on_resources
		if res_name is not None:
			ret = ret[res_name]
			if res_id is not None:
				ret = ret[res_id]

		return ret

	def empty_client_on_resources(self):
		'''生成一个空的resource报告表，方便填信息
	
		示例：
		clients_on_resources = {
			"gpu" : {
				0 : [] , 
				1 : [001 , 002] , 
				2 : [001 , ] , 
			}
		}
		'''
		return {
			name : {
				_id : [] for _id in ids
			}
			for name , ids in self.resources
		}
