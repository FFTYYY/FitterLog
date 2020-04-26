from .base import Object , find_or_new
import time
from ..importer import Project as STL_Project
from ..importer import Experiment as STL_Experiment
from ..importer import ExperimentGroup as STL_ExperimentGroup

class Project(Object):
	'''一个项目
	'''

	def __init__(self , name , path = None):

		super().__init__(
			find_or_new(STL_Project , 
				name = name , 
				path = path , 
			),
			name = "name" , 
			path = "path" ,
			groups = "groups" ,
		)

class ExperimentGroup(Object):
	'''一组实验
	'''

	def __init__(self , name , project):

		super().__init__(
			STL_ExperimentGroup(
				name = name , 
				project = project , 
			),
			name = "name" , 
			project = "project" , 
		)




__all__ = [
	"Project" , 
]