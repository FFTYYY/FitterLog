from fitterdb.static_list import StaticList

class Value:
	persister = StaticList(name = "fitterlog-value")

	def __init__(self , noun , predicate):
		self.noun 		= noun
		self.predicate 	= predicate

		self.now_time = 0
		self.save_point = 0

	def value(self):
		return self.persister.last()

	def update(self , value , time_stamp = None):
		if time_stamp is None: #自动设置时间戳
			time_stamp = self.now_time
		self.now_time = max(self.now_time , time_stamp + 1)

		self.persister.append( (time_stamp , value) )

	def dump(self):
		save_point = self.persister.save()
		self.noun.set_position(self.predicate , save_point) #保存储存点



