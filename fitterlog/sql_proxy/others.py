from .base import Object 
from .utils import make_obj_list , none_or_id
import time
from ..importer import Figure as SQL_Figure

class Figure(Object):
	'''一个图片
	'''

	def __init__(self , name = None , experiment = None , from_obj = None):

		super().__init__(SQL_Figure , from_obj , name = name , expe_id = none_or_id(experiment))

		self.set_name_map(
			name 		= "name" , 
			html 		= "html" ,
			sql_expe 	= "expe" ,
			id 			= "id" , 
		)



__all__ = [
	"Figure" 			, "SQL_Figure" 		, 
]