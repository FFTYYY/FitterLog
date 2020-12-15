from YTools.system.static_hash import DoubleHash , HighDimHash

class Noun:
	persister = HighDimHash(name = "fitterlog-noun-predicate") #查询名词和谓词的值的位置

	def __init__(self , id):
		self.id = id

	def ask_position(self , predicate):
		return self.persister.get( [self.id , predicate.id] )

	def set_position(self , predicate , val):
		'''理论上来说，同一个名词只（应）存在于一个线程内，所以不存在同步性的问题'''
		self.persister.set( [self.id , predicate.id] , val )


class Predicate:

	persister = DoubleHash(name = "fitterlog-predicate") #查询谓词的名称和值
	LOCK   = "_fitterlog_lock" #设置这一项来锁定数据库
	COUTER = "_fitterlog_count"

	def __init__(self , name):
		self.name = name

		self.ensure_id()
		self.id = self.persister.get(key = self.name)

	def ensure_id(self):
		'''确保自身id存在'''

		self.persister.set(self.LOCK , -1 , commit = False) #修改但不提交，以此来锁定数据库

		#保证谓词计数存在
		pred_count = self.persister.get(key = self.COUTER)
		if pred_count is None:
			self.persister.set(self.COUTER , 0 , commit = False) 
			pred_count = 0
		#查看此谓词是否存在
		if self.persister.get(key = self.name) is None:

			self.persister.set(self.COUTER , pred_count + 1 , commit = False) #先增加谓词计数
			self.persister.set(self.name   , pred_count 	   , commit = False) #将当前谓词的值设为谓词计数器之前的值

		self.persister.commit()

	def get_name(id):
		return Predicate.persister.get(val = id)

	def from_id(id):
		return Predicate(name = Predicate.get_name(id))