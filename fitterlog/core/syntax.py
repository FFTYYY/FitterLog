'''	

一个Clause类对象和一个三元组一一对应，这个列表的第一个元素是谓词名，第二个元素是属性dict，第三个元素是儿子列表。
儿子列表是Clause三元组的列表。
例如：

clause = (
	"root" , 
	{} , 
	[
		(
			"loss" , 
			{"default" : 0,} , 
			[
				(
					"test" , 
					{"default": 0,} , 
					[]
				) , 
				(
					"train" , 
					{"show": False,},
					[]
				)
			]
		) , 
		(
			"n" , 
			{"default" : 30 , } , 
			[]
		) ,
	] , 
)

给定一个Clause对象，可以构造这样一个三元组，也可以从这样一个三元组还原一个Clause对象。
'''

from YTools.system.static_hash import DoubleHash , HighDimHash , StaticBlob
from .morphology import Predicate
import json
from ..base.constants import DB_NAME , CLAUSE_ROOT_NAME , TB_NAME_CLAUSE , CLAUSE_CONCAT
from YTools.universe.exceptions import ArgumentError

class Clause:
	'''这个类是用于储存的Clause类。

	这个类需要用两个阶段来完善。第一个阶段由用户创建，描述clause的结构，但是此时结构还没有解析，也没有分配
		名词，因此语义是不完善的，只能进行结构上的修改，也不能保存。
	第二阶段是用户将其传给fitterlog之后由fitterlog创建，会解析树结构，并

	每个从句的「名」有两个部分。直接名(name)是显示给用户的名称。真实名（real name）是谓词在数据库中的
		名称。
	'''
	ROOT_NAME = CLAUSE_ROOT_NAME


	# 储存子句结构和属性
	persister = StaticBlob(db_name = DB_NAME , tb_name = TB_NAME_CLAUSE) # 从(noun,pred)到2进制的映射

	def __init__(self , name = None , sons = [] , **attrs):

		if name is None:
			self.name = self.ROOT_NAME
		else:
			self.name = name

		self.father = None

		self.sons = {}
		self.sons.update( {x.name : x for x in sons} )

		self.attrs = attrs

		for x in sons:
			x._set_father(self)

		self._real_name = None

	@property
	def real_name(self):
		if self._real_name is None:
			fname = "" #没有father的人的默认name
			if self.father is not None:
				fname = self.father.real_name
			self._real_name = "{0}{1}{2}".format(fname , CLAUSE_CONCAT , self.name)

		return self._real_name

	def _set_father(self , father):
		self.father = father
		self._real_name = None # 如果是重新设置的，就要重设real_name

	def add_son(self , clause):
		self.sons[clause.name] = clause
		clause._set_father(self)

	# 把自己转成list描述
	def listize(self , no_attr = False):
		sonlist = [x.listize(no_attr = no_attr) for _,x in self.sons.items()]
		if no_attr:
			return [self.name , sonlist]
		return [self.name , self.attrs , sonlist]

	def from_list(l):
		if len(l) != 3:
			raise ArgumentError("from_list" , "l" , l , class_name = "Clause")

		name , attrs , sons_list = l
		sons = [Clause.from_list(x) for x in sons_list]
		return Clause(name , sons , **attrs)

	def save(self , noun):
		key = "{noun_id}".format(noun_id = noun.id) 
		Clause.persister.set(key , self.listize())

	def load(noun):
		key = "{noun_id}".format(noun_id = noun.id) 
		l = Clause.persister.get(key)

		if l is None:
			return None
		return Clause.from_list(l)

