from .base import Object 
from .utils import find_or_new , make_obj_list
import time
from ..importer import Project as STL_Project
from ..importer import Experiment as STL_Experiment
from ..importer import ExperimentGroup as STL_ExperimentGroup

class Project(Object):
	'''一个项目
	'''

	def __init__(self , name = None , path = None , from_obj = None):

		if from_obj is None:
			from_obj = find_or_new(STL_Project , name = name , path = path , )

		super().__init__(from_obj)

		self.set_name_map(
			name 		= "name" , 
			path 		= "path" ,
			stl_groups 	= "groups" ,
			id 			= "id" , 
		)

		self.groups = make_obj_list(ExperimentGroup , self.stl_groups.all())

class ExperimentGroup(Object):
	'''一组实验
	'''

	def __init__(self , name = None , project = None , from_obj = None):

		if from_obj is None:
			from_obj = find_or_new(STL_ExperimentGroup , name = name , project_id = project.id)
		super().__init__(from_obj)

		self.set_name_map(
			name 		= "name" , 
			id 			= "id" , 
			stl_experiments = "experiments" , 
		)
		self.project = project
		self.experiments = make_obj_list(Experiment , self.stl_experiments.all())


class Experiment(Object):
	'''一次实验
	'''

	def __init__(self , group = None , from_obj = None):

		if from_obj is None:
			from_obj = find_or_new(STL_Experiment , group_id = group)
		super().__init__(from_obj)

		self.set_name_map(
			logs 			= "logs" , 
			stl_variables 	= "variables"
		)
		self.group = group
		#self.variables = make_obj_list(Variables , self.stl_variables)


__all__ = [
	"Project" , "STL_Project" , 
	"ExperimentGroup" , "STL_ExperimentGroup" , 
]