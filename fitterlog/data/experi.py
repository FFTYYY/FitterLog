from .base import Object 
from .utils import make_obj_list , none_or_id
import time
from ..importer import Project as SQL_Project
from ..importer import Experiment as SQL_Experiment
from ..importer import ExperimentGroup as SQL_ExperimentGroup
from .variable import Variable

class Project(Object):
	'''一个项目
	'''

	def __init__(self , name = None , path = None , from_obj = None):

		super().__init__(SQL_Project , from_obj , name = name , path = path)

		self.set_name_map(
			name 		= "name" , 
			path 		= "path" ,
			sql_groups 	= "groups" ,
			id 			= "id" , 
		)		
		self.groups = make_obj_list(ExperimentGroup , self.sql_groups.all())

class ExperimentGroup(Object):
	'''一组实验
	'''

	def __init__(self , name = None , project = None , from_obj = None):
		super().__init__(SQL_ExperimentGroup , from_obj , name = name , project_id = none_or_id(project))

		self.set_name_map(
			name 		= "name" , 
			id 			= "id" , 
			sql_experiments = "experiments" , 
		)
		self.project = project
		self.experiments = make_obj_list(Experiment , self.sql_experiments.all())


class Experiment(Object):
	'''一次实验
	'''

	def __init__(self , group = None , from_obj = None):

		super().__init__(SQL_Experiment , from_obj , group_id = none_or_id(group))

		self.set_name_map(
			logs 			= "logs" , 
			sql_variables 	= "variables"
		)
		self.group = group
		self.variables = make_obj_list(Variable , self.sql_variables)


__all__ = [
	"Project" 			, "SQL_Project" 		, 
	"ExperimentGroup" 	, "SQL_ExperimentGroup" , 
	"Experiment" 		, "SQL_Experiment" 		, 
]