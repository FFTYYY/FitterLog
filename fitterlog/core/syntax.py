from YTools.system.static_hash import DoubleHash , HighDimHash
from .morphology import Predicate

class Clause:
	'''这个类方便用户描述句子结构'''
	
	persister = HighDimHash(name = "fitterlog-syntax") # (noun , spred) -> (fpred) 表示在noun中，spred是fpred的儿子
	ROOT_NAME = "_fitterlog_root"

	def __init__(self , name = None, sons = [] , from_id = None , **kwargs):
		'''
			如果name非空，就根据name创建谓词，如果from_id非空，就根据id创建谓词，如果均为空，就自动生成一个匿名谓词

			kwargs：把一些信息传递给CoreSentence，这些信息由后者负责保存，Clause不负责保存
		'''
		if from_id is not None:
			self.predicate = Predicate.from_id(from_id)
		elif name is not None:
			self.predicate = Predicate(name)
		else:
			self.predicate = Predicate(self.ROOT_NAME)

		self.name = self.predicate.name

		self.sons = {}
		self.sons.update( {x.name : x for x in sons} )

		self.kwargs = kwargs

	def add_son(self , clause):
		self.sons[clause.name] = clause

	def son_list(self):
		return [self.sons[x] for x in self.sons]

	def save(self , noun , is_root = False):
		'''保存整个clause结构'''
		for x in self.son_list():
			self.persister.set( (noun.id , x.predicate.id) , self.predicate.id) #将自己的所有儿子持久化
			x.save(noun , is_root = False) #递归处理子树

		if is_root: #如果自己是根
			self.persister.set( (noun.id , self.predicate.id) , -1)

	def load_clause_struct(noun):
		'''给定noun，读取这个noun保存的clause结构，返回根clause'''
		all_preds = Clause.persister.get_partial( (noun.id , None) )
		clauses = {}
		root = None
		for (_ , spred_id) , (fpred_id,) in all_preds: #第一次遍历找到clause列表
			if fpred_id == -1:
				root = spred_id #找到根pred
			clauses[spred_id] = Clause(from_id = spred_id)

		for (_ , spred_id) , (fpred_id,) in all_preds: #第二次遍历重建树形关系
			if fpred_id != -1:
				clauses[fpred_id].add_son(clauses[spred_id])

		return clauses[root] #返回根节点

	def linearize(self):
		'''返回一个列表，描述树结构'''
		if len(self.sons) > 0: 
			return [self.predicate.name , [ x.linearize() for x in self.son_list() ]]
		return self.predicate.name