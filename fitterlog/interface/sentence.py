from ..core.morphology import Predicate , Noun
from ..core.semasiology import Value
from ..core.syntax import Clause
from YTools.system.locker import Locker
from YTools.universe.exceptions import ArgumentError
from ..base.constants import SENT_LOCK_PATH , SENT_KEY_AMBI , SENT_ATTR_DEFAULT

class _CoreSentence_Syntax:
	'''定义各种句法操作的模块
	只有_syntax_newson这个方法可以新建子句，保证_sons、_allson_dire、_allson_real的一致性
	'''

	def _syntax_newson(self , son_clause):
		'''根据给定的子句，给自身的树结构添加一个新节点
		只有这个函数可以更改_sons、_allson_dire、_allson_real
		'''

		if son_clause.name in self._sons:
			raise ArgumentError( "_syntax_newson" , "son_clause.name" , son_clause.name , 
				class_name = "_CoreSentence_Syntax" , note_str = "Duplicated clause name"
			)

		son_core_sentence = CoreSentence(
			root 		= self._root , # 继承自己的根节点
			noun 		= self._noun , # 继承自己的名词
			clause 		= son_clause , 
		)

		self._sons[son_clause.name]                    = son_core_sentence
		self._root._allson_real [son_clause.real_name] = son_core_sentence

		if son_clause.name in self._root._allson_dire: # 根节点有重复的
			self._root._allson_dire[son_clause.name]   = SENT_KEY_AMBI
		else:
			self._root._allson_dire[son_clause.name]   = son_core_sentence

	def _init_syntax(self):
		'''根据给定的子句，初始化自身的树结构
		'''

		for son_clause in self._clause.sons.values():
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
		if key in self._sons: # 从直接儿子中可以找到
			return self._sons[key]

		if key in self._allson_dire:

			# 如果有歧义，抛出异常
			if self._allson_dire[key] == SENT_KEY_AMBI:
				raise ArgumentError("__getitem__" , "key" , key , 
					class_name = "_CoreSentence_Value" , note_str = "Has multiple shortcut keys"
				)
			# 返回正常的值
			return self._allson_dire[key]

		if key in self._allson_real:
			return self._allson_real[key]

		raise ArgumentError("__getitem__" , "key" , key , 
			class_name = "_CoreSentence_Value" , note_str = "No predicate name"
		)

class _CoreSentence_Persist:
	'''保存，恢复模块'''

	# 保存
	def save_values(self):
		self._value.save()

	def save_all_values(self):
		'''保存自己和所有子节点的值，key是noun和predicate'''
		self.save_values()
		for x in self._sons.values():
			x.save_all_values()

	def save_syntax(self):
		'''保存自己的句法。key是noun'''
		self._clause.save(self.noun)

	def save(self):
		self.save_all_values()
		self.save_syntax()

class CoreSentence(_CoreSentence_Syntax , _CoreSentence_Value , _CoreSentence_Persist):
	'''概念上说，这个类私有继承 Predicate , Noun ，公有继承 Value , Clause
		但是写成多重继承很不方便，所以就手动写了一些接口，又把这些接口封装在其他基类里面，再多重继承
	'''
	def __init__(self , noun , clause = None, root = None):
		'''root is None表示自己是根'''

		self._is_root    = root is None
		self._root 		 = root if root is not None else self

		self._noun 		 = noun

		if clause is None:
			self._clause = Clause.load(noun)
		else:
			self._clause = clause

		self._pred  	 = Predicate(self._clause.real_name)
		self._value 	 = Value(self._noun , self._pred)

		self._allson_dire = {} # 无视结构的所有子孙（以直接名索引。在_init_syntax()中初始化。
		self._allson_real = {} # 无视结构的所有子孙（以真名索引）。在_init_syntax()中初始化。

		self._sons 		 = {}

		self._init_syntax()


	@property
	def noun(self):
		return self._noun

	# value的接口
	@property
	def value(self):
		val = self._value.value
		if val is None: # 如果没有任何值，就返回默认值
			val = self.attrs.get(SENT_ATTR_DEFAULT)
		return val

	# attrs的接口
	@property	
	def attrs(self):
		return self._clause.attrs

class Sentence(CoreSentence):

	LOCKER_PATH = SENT_LOCK_PATH

	def __init__(self , predicate_struct = None , noun = None):
		if noun is None:
			noun = Noun.new()
			super().__init__(noun , clause = predicate_struct)
		else:
			super().__init__(noun)

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
			self.locker.remove(x)
