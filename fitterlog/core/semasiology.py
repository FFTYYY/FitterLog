from fitterdb.static_list import StaticList , StaticList_FileManager
from .syntax import Clause

class Value:

	FILENAME = "fitterlog-value"

	def __init__(self , noun , predicate):
		self.persister = StaticList(filename = self.FILENAME)
		
		self.noun 		= noun
		self.predicate 	= predicate

		self.now_time = 0
		self.save_point = 0

	def value(self):
		get_val = self.persister.last()
		if get_val is None:
			return None
		return get_val[1]

	def update(self , value , time_stamp = None):
		if time_stamp is None: #自动设置时间戳
			time_stamp = self.now_time
		self.now_time = max(self.now_time , time_stamp + 1)

		self.persister.append( (time_stamp , value) )

	def set_default(self , value):
		self.update( value )

	def dump(self):
		save_point = self.persister.save()
		if save_point >= 0:
			self.noun.set_position(self.predicate , save_point) #保存储存点

	def load_last(self):
		
		last_position = self.noun.ask_position(self.predicate)

		if last_position is None or last_position < 0: # no value saved
			return 

		with StaticList_FileManager(self.FILENAME) as restorer:
			last_val = restorer.read_last(last_position)

		self.persister.set_last(last_pos = last_position , last_val = last_val)

