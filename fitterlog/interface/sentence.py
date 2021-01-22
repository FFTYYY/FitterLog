from ..core.morphology import Predicate , Noun
from ..core.semasiology import Value
from ..core.syntax import Clause
from YTools.system.locker import Locker

class _CoreSentence_Syntax:
	'''定义各种句法操作的模块'''

	def _syntax_newson(self , son_clause):
		'''根据给定的子句，给自身的树结构添加一个新节点'''

		if self._sons.get(son_clause.name) is not None:
			raise ValueError("duplicated clause name")

		self._sons[son_clause.name] = CoreSentence(
			noun 		= self._noun , 
			clause 		= son_clause , 
			attrs 		= son_clause.attrs , 
		)

	def _init_syntax(self):
		'''根据给定的子句，初始化自身的树结构
		'''

		for son_clause in self._clause.son_list():
			self._syntax_newson(son_clause)

	def append_son(self , new_clause):
		'''添加一个子子句，自动新建子结构'''

		self._clause.add_son(new_clause)
		self._syntax_newson(new_clause)

	def new_clause(self , name , sons = [] , **kwargs):
		'''根据名和其他要素，新建一个子句，自动新建子结构
		'''
		new_clause = Clause(name , sons , **kwargs)
		self.append_son(new_clause)
	
	def new_clauses_from_dict(self , dic):

		for name , value in dic.items():
			self.new_clause(name = name , default = value)

	def append_clauses(self , clauses):
		for clause in clauses:
			self.append_son(clauses)

class _CoreSentence_Value:
	'''定义对值的操作的模块'''
	def update(self , value , time_stamp = None):
		self._value.update(value , time_stamp)

	def __getitem__(self , key):
		return self._sons[key]

class _CoreSentence_Persist:
	'''保存，恢复模块'''

	def _init_from_noun(self , noun):
		'''给定一个历史名词，读取这个名词保存的信息来初始化'''
		self._noun 		= noun
		self._clause 	= Clause.load_clauses(noun) #读取句法结构
		self._predicate = self._clause.predicate
		self._value 	= Value(self._noun , self._predicate)
		self._sons 		= {}
		self._attrs 	= self._clause.attrs

		self._init_syntax()
		self._recursive_load_value() #读取所有子节点的值

	# 读取
	def _recursive_load_value(self):
		'''递归读取所有谓词保存的最后一个值'''
		self._value.load_last()
		for x in self._son_list:
			x._recursive_load_value()

	# 保存
	def save_values(self):
		self._value.dump()

	def save_all_values(self):
		self.save_values()
		for x in self._son_list:
			x.save_values()

	def save_syntax(self):
		self._clause.save(self.noun , is_root = True)

	def save(self):
		self.save_all_values()
		self.save_syntax()

	@property
	def _son_list(self):
		return [self._sons[x] for x in self._sons]

class CoreSentence(_CoreSentence_Syntax , _CoreSentence_Value , _CoreSentence_Persist):
	'''概念上说，这个类私有继承 Predicate , Noun ，公有继承 Value , Clause
		但是写成多重继承很不方便，所以就手动写了一些接口，又把这些接口封装在其他基类里面，再多重继承
	'''
	def __init__(self , noun , clause , attrs = {}):

		self._noun 		= noun
		self._clause 	= clause
		self._predicate = self._clause.predicate
		self._value 	= Value(self._noun , self._predicate)
		self._sons 		= {}
		self._attrs 	= attrs

		self._init_syntax()

		# other params 
		if self._attrs.get("default") is not None:
			self._value.set_default(self._attrs.get("default"))

	@property
	def noun(self):
		return self._noun

	# value的接口
	@property
	def value(self):
		val = self._value.value()
		return val

	# attrs的接口
	@property	
	def attrs(self):
		return self._attrs

class Sentence(CoreSentence):

	LOCKER_PATH = "fitterlog/sentence/"

	def __init__(self , predicate_struct = None , noun = None):
		if noun is None:
			noun = Noun.new()
			super().__init__(noun , predicate_struct)
		else:
			super()._init_from_noun(noun)

		self.locker = Locker()
		self._setted_key = [] #所有设置过的key，在离开时要清空

		self.set("live" , True)

	def set(self , key , val):
		key = self.LOCKER_PATH + key + "/"  + str(self.noun.id) + "/" 
		self.locker.set(key , val) #设置自己的位置的值
		self._setted_key.append(key) #记录下设置的key，方便最后删除

	def get(self , key):
		return self.locker.get(self.LOCKER_PATH + key + "/" + str(self.noun.id) + "/")

	def require_resource(self , resource_name , ids):
		'''对resource_name这个名称的ids资源声称占有。
			注意虽然名字叫require，这个函数实际上不是请求，是声称。
		'''
		self.set("resources/" + resource_name , ids)


	def finish(self):
		for x in self._setted_key:
			self.locker.set(x , None)
