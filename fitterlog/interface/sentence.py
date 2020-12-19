from ..core.morphology import Predicate , Noun
from ..core.semasiology import Value
from ..core.syntax import Clause

class _CoreSentence_Syntax:
	'''定义各种句法操作的模块'''

	def _syntax_newson(self , son_clause):
		'''根据给定的子句，给自身的树结构添加一个新节点'''

		if self._sons.get(son_clause.name) is not None:
			raise ValueError("duplicated clause name")

		self._sons[son_clause.name] = CoreSentence(
			noun 		= self._noun , 
			clause 		= son_clause , 
			**son_clause.kwargs
		)


	def _init_syntax(self):
		'''根据给定的子句，初始化自身的树结构
		'''

		for son_clause in self._clause.son_list():
			self._syntax_newson(son_clause)

	def append_son(self , new_clause):
		'''添加一个子子句，自动新建子结构'''

		self._syntax.add_son(new_clause)
		self._syntax_newson(new_clause)

	def new_son(self , name , sons = [] , **kwargs):
		'''根据名和其他要素，新建一个子句，自动新建子结构
		'''
		new_clause = Clause(name , sons , **kwargs)
		self.append_son(new_clause)
	

	def new_clauses_from_dict(self , dic):

		for name , value in dic.items():
			self.new_son(name = name , default = value)

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
		self._clause 	= Clause.load_clause_struct(noun) #读取句法结构
		self._predicate = self._clause.predicate
		self._value 	= Value(self._noun , self._predicate)
		self._sons 		= {}

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
	def __init__(self , noun , clause , default = None , **kwargs):

		self._noun 		= noun
		self._clause 	= clause
		self._predicate = self._clause.predicate
		self._value 	= Value(self._noun , self._predicate)
		self._sons 		= {}

		self._init_syntax()

		# other params 
		if default is not None:
			self._value.set_default(default)

	@property
	def noun(self):
		return self._noun

	# value的接口
	@property	
	def value(self):
		val = self._value.value()
		if val is None:
			val = self._default_val
		return val


class Sentence(CoreSentence):

	ROOT_PRED = "_fitterlog_root"

	def __init__(self , noun = None , predicate_struct = None):
		if noun is None:
			noun = Noun.new()
			super().__init__(noun , predicate_struct)
		else:
			super()._init_from_noun(noun)