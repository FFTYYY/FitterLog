from .base import Object
from .utils import make_obj_list , none_or_id
import time
from ..importer import SingleValue as SQL_SingleValue
from ..importer import VariableTrack as SQL_VariableTrack
from ..importer import Variable as SQL_Variable

class Variable(Object):

	def __init__(self , name = None , experiment = None , from_obj = None):
		super().__init__(SQL_Variable , from_obj , name = name , expe_id = none_or_id(experiment))
		
		self.set_name_map(
			name 		= "name" , 
			experiment 	= "experiment" ,
			sql_tracks 	= "tracks" ,
			id 			= "id" , 
		)


class VariableTrack(Object):
	'''某个变量的一条时间线
	'''

	def __init__(self , name = None , variable = None , from_obj = None):
		super().__init__(SQL_VariableTrack , from_obj , name = name , variable_id = none_or_id(variable))
		self.set_name_map(
			name 		= "name" , 
			variable 	= "variable" ,
			sql_values 	= "values" ,
			id 			= "id" , 
		)

class SingleValue(Object):
	'''某个变量的某条时间线上的一个值
	'''

	def __init__(self , value = None, timestamp = None , track = None , from_obj = None):

		super().__init__(SQL_SingleValue , from_obj , value = value, time_stamp = timestamp , track_id = none_or_id(track))
		self.set_name_map(
			value 		= "value" , 
			timestamp 	= "time_stamp" ,
			id 			= "id" , 
		)


__all__ = [
	"SingleValue" , 
	"VariableTrack" , 
	"Variable" , 
]
__all__ = [
]