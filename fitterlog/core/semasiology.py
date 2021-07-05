'''Value是fitterlog中唯一可以调用persister.save()和noun.set_position()的对象。
如果在其他地方也可以调用，值就有可能不一致。

'''

from fitterdb.static_list import StaticList , StaticList_FileManager
from .syntax import Clause
from ..base.constants import FILE_NAME_VALUE

class Value:
	'''Value是StaticList的一个面向用户的封装。
	给定一个noun和一个predicate，就可以确定他们的历史值，这就是一个Value对象。

	Value添加这个约定：每个列表元素都是一个二元组，第一个元素是时间戳，第二个元素是值。

	方法：
		value：最近一次的值。只要给定了noun和predicate就可以保证这个value是真实的上一次的值。
	'''

	FILENAME = FILE_NAME_VALUE

	def __init__(self , noun , predicate):
		self.noun 		= noun
		self.predicate 	= predicate

		self.last_pos   = self.noun.ask_position(self.predicate) # 从数据库读取上一次的位置
		self.persister  = StaticList(filename = self.FILENAME , last_pos = self.last_pos)
		

		self.now_time   = self.get_timestamp() # 询问保存了的最近的时间戳
		if self.now_time is None:
			self.now_time = 0

	@property	
	def value(self):
		get_val = self.persister.recent()
		if get_val is None: # persister中没有上次保存的值。
			return None
		return get_val[1] # 返回值部分

	def get_timestamp(self):
		get_val = self.persister.recent()
		if get_val is None: # persister中没有上次保存的值。
			return None
		return get_val[0] # 返回时间戳部分

	def update(self , value , time_stamp = None):
		if time_stamp is None: #自动设置时间戳
			time_stamp = self.now_time

		# 这个函数不会做时间戳合法性检查，给予一定的灵活性
		self.now_time = max(self.now_time , time_stamp + 1) 

		self.persister.append( (time_stamp , value) )

	# def set_default(self , value):
	# 	'''设置默认值'''
	# 	self.update( value , time_stamp = -1) # 用-1时间的值表示默认值

	def save(self , last_pos = -1):
		'''把所有保存的值都持久化到硬盘上'''
		if not self.persister.check_lastpos(last_pos): # 没有输入上一次的位置
			last_pos = self.last_pos

		save_point = self.persister.save(last_pos = last_pos)

		# 立刻保存储存点。始终保证数据库中的约束是成立的。
		if save_point >= 0:
			self.noun.set_position(self.predicate , save_point)
			self.last_pos = save_point # 也更新自己的值

	def close(self):
		self.persister.close()
	def __del__(self):
		self.close()
