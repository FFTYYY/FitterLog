from .syntax import Clause

def merge(clauses , name):
	'''
		给定一系列clause，合并他们并返回树结构。
		name是这棵树的根的谓词的名。理论上这棵树的根的谓词应该是一样的，但是额外传一个参数可以提供一些灵活性。

		返回一个list，描述树结构
	'''

	if len(clauses) <= 0:
		return None

	attrs = {}

	complex_clauses = [] # 有子节点的从句
	sons_list = {}       # sons_list[x] = [全体有x这个子节点的父节点]
	for clause in clauses:
		attrs.update(clause.attrs) # 更新attrs
		if len( clause.sons ) > 0:
			complex_clauses.append(clause)
			for x in clause.sons:
				sons_list[x] = sons_list.get(x , [])
				sons_list[x].append(clause)

	if len(complex_clauses) > 0:
		return Clause(name , sons = [ 
				merge([f.sons[s_name] for f in f_list] , s_name) 
				for s_name , f_list in sons_list.items() 
			]
			, ** attrs
		)

	return Clause(name , ** attrs)

def do_nothing_filter(clause , context , agg = None):
	return True

class ClauseFilter:
	def __init__(self):
		pass


	def unfold(self , clause):
		agg = []
		if self.filter_enter(clause , self.context): #如果filter返回false，停止递归 
			for _,c in clause.sons.items():
				agg.append( self.unfold(c) )
		return self.filter_exit(clause , self.context , agg)

	def run(self , clause , 
			filter_enter = do_nothing_filter, filter_exit = do_nothing_filter , 
			init_context = {}
		):		
		'''
			filter：function(clause , context)
		'''
		self.filter_enter = filter_enter
		self.filter_exit  = filter_exit
		self.context = init_context
		ret = self.unfold(clause)
		return ret , self.context
