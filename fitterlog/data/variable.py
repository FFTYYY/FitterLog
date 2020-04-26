from .base import Object
import time
from ..importer import SingleValue as stl_singlevalue
from ..importer import VariableTrack as stl_variableTrack
from ..importer import Variable as stl_variable

class SingleValue(Object):
	'''某个变量的某条时间线上的一个值
	'''

	def __init__(self, value , timestamp = None , track = "default"):

		if timestamp is None:
			timestamp = timestamp or int(time.time() * 1000)

		super().__init__( 
			stl_singlevalue(value = value , 
				time_stamp = timestamp , 
				track = stl_variableTrack.objects.filter) 
		)


__all__ = [
]