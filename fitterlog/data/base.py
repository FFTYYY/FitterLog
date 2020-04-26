from YTools.universe.extra_type import Struct

def find_or_new(clas , **kwargs):
	kwargs = {x : kwargs[x] for x in kwargs if kwargs[x] is not None } #去除None（不查找项）
	obj = clas.objects.filter(**kwargs)
	if len(obj) >= 1:
		return obj[0]
	return clas(**kwargs)

def make_get(name):
	def gets(self):
		return getattr(self.stl_obj , self.name_map[name] )
	return gets

def make_set(name):
	def sets(self , val):
		setattr( self.stl_obj , self.name_map[name] , val )
		self.stl_obj.save()
	return sets

class Object(Struct):
	def __init__(self , stl_obj , **kwargs):

		super().__init__()

		self.stl_obj = stl_obj
		self.stl_obj.save()

		self.name_map = kwargs
		for name in kwargs:
			self._set_property(
				name , 
				make_get(name) , 
				make_set(name) , 
			)

	def save(self):
		self.stl_obj.save()