from YTools.universe.extra_type import Struct
from .utils import find_or_new , make_obj_list

def make_get(name):	
	'''Object类对象的定制属性的get函数，在访问对应属性的时候查找数据库对象
	'''

	def gets(self):
		return getattr(self.sql_obj , self.name_map[name] )
	return gets

def make_set(name):
	'''Object类对象的定制属性的set函数，在访问对应属性的时候查找数据库对象
	'''
	def sets(self , val):
		setattr( self.sql_obj , self.name_map[name] , val )
		self.sql_obj.save()
	return sets

class Object(Struct):

	def __init__(self , sql_class , from_obj , force_new = False , **kwargs):
		'''
		
		参数：
			sql_class：对应的 sql 类
			from_obj：用于初始化的 sql 对象。如果为 None 则根据 kwargs 新建或者查找
		'''

		super().__init__()

		self.sql_obj = from_obj
		if force_new:
			self.sql_obj = sql_class(from_obj , **kwargs)
		else:
			if from_obj is None:
				self.sql_obj = find_or_new(sql_class , **kwargs)

		self.sql_obj.save()

	def set_name_map(self , **kwargs):
		self.name_map = kwargs
		for name in kwargs:
			self._set_property(
				name , 
				make_get(name) , 
				make_set(name) , 
			)

	def save(self):
		self.sql_obj.save()