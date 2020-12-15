from ..core.morphology import Predicate , Noun
from ..core.semasiology import Value
from .syntax import Clause

class CoreSentence:
	'''大体来说，这个类私有继承 Predicate , Noun ，公有继承 Value , Clause
		但是写成多重继承很不方便，所以就手动写了一些接口
	'''
	def __init__(self , noun , predicate , clause , default = None , **kwargs):

		self._noun 		= noun
		self._predicate = predicate
		self._value 	= Value(noun , predicate)
		self._sons 		= {}

		self._create_tree(clause)

		# other params 
		self._default_val = default

	def _create_tree(self , name_struct = None):
		'''
			name_struct: list of clause
			把clause树转成CoreSentence树
			注意这里name_struct描述的是本节点的子树，不包括本节点
		'''
		if name_struct is None:
			return 

		for clause in name_struct:
			self._sons[clause.name] = CoreSentence(
				noun 		= self._noun , 
				predicate 	= Predicate(clause.name) , 
				clause 		= clause.sons , 
				**clause.kwargs
			)

	# value的接口
	@property	
	def value(self):
		val = self._value.value()
		if val is None:
			val = self._default_val
		return val

	def update(self , value , time_stamp = None):
		self._value.update(value , time_stamp)

	def __getitem__(self , key):
		return self._sons[key]

	def new_clause(self , name , sons = [] , **kwargs):
		self._sons[name] = CoreSentence(
			noun 		= self._noun , 
			predicate 	= Predicate(name) , 
			clause 		= sons , 
			**kwargs
		)

	def new_clauses_from_dict(self , dic):

		for name , value in dic.items():
			self._sons[name] = CoreSentence(
				noun 		= self._noun , 
				predicate 	= Predicate(name) , 
				clause 		= None ,
				default 	= value ,  
			)
	def append_clauses(self , clauses):
		self._create_tree(name_struct = clauses)

class Sentence(CoreSentence):

	ROOT_PRED = "_fitterlog_root"

	def __init__(self , noun = None , predicate_struct = None):
		if noun is None:
			noun = Noun.new()

		super().__init__(noun , Predicate(self.ROOT_PRED) , predicate_struct)
