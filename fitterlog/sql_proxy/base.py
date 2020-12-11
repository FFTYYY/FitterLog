from YTools.universe.extra_type import Struct
from .utils import find_or_new , make_obj_list
import time
import queue
import threading
from ..quit import add_quit_process

class SaveThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.queue = queue.Queue(maxsize = 5000)

		self.wait = False
		self.closed = False

	def run(self):
		while not self.closed:
			if (not self.wait) and not self.queue.empty():
				obj = self.queue.get()
				obj.save()
			time.sleep(0.01)

	def close(self):
		self.closed = True
				

nohurry_save_server = SaveThread()
nohurry_save_server.start()
def on_quit_kill_thread():
	while not nohurry_save_server.queue.empty():
		pass
	nohurry_save_server.close()

# add_quit_process(on_quit_kill_thread)


def save_sql_obj(obj , hurry = False):
	if hurry:
		nohurry_save_server.wait = True #hurry的人优先
		obj.save()
		nohurry_save_server.wait = False
		return

	nohurry_save_server.queue.put(obj)


def make_get(name):	
	'''Object类对象的定制属性的get函数，在访问对应属性的时候查找数据库对象
	'''

	def gets(self):
		return getattr(self.sql_obj , self.name_map[name] )
	return gets

def make_set(name):
	'''Object类对象的定制属性的set函数，在访问对应属性的时候查找数据库对象
	'''
	def sets(self , val):
		setattr( self.sql_obj , self.name_map[name] , val )
		save_sql_obj(self.sql_obj , hurry = self.hurry)
	return sets

class Object(Struct):

	def __init__(self , sql_class , from_obj , force_new = False , no_hurry = False , **kwargs):
		'''
		
		参数：
			sql_class：对应的 sql 类
			from_obj：用于初始化的 sql 对象。如果为 None 则根据 kwargs 新建或者查找
		'''

		super().__init__()

		self.sql_obj = from_obj
		if force_new:
			self.sql_obj = sql_class(from_obj , **kwargs)
		else:
			if from_obj is None:
				self.sql_obj = find_or_new(sql_class , **kwargs)

		self.hurry = not no_hurry
		save_sql_obj(self.sql_obj , hurry = self.hurry)

	def set_name_map(self , **kwargs):
		self.name_map = kwargs
		for name in kwargs:
			self._set_property(
				name , 
				make_get(name) , 
				make_set(name) , 
			)

	def save(self):
		save_sql_obj(self.sql_obj , hurry = self.hurry)
