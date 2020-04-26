from YTools.universe.extra_type import Struct

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

		self.set_name_map(**kwargs)

	def set_name_map(self , **kwargs):
		self.name_map = kwargs
		for name in kwargs:
			self._set_property(
				name , 
				make_get(name) , 
				make_set(name) , 
			)

	def save(self):
		self.stl_obj.save()