class Clause:
	'''这个类方便用户描述句子结构'''
	def __init__(self , name , sons = [] , **kwargs):
		self.name = name
		self.sons = sons

		self.kwargs = kwargs
