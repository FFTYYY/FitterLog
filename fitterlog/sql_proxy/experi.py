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

	def find(id = None , name = None):
		assert (id is not None) or (name is not None)
		if id is None:

			objs = SQL_Project.objects.filter(name = name)
			if len(objs) <= 0:
				proj = SQL_Project(name = name)
				proj.save()
			else:
				proj = objs[0]
			return proj

		return SQL_Project.objects.get(id = id)

class ExperimentGroup(Object):
	'''一组实验
	'''

	def __init__(self , name = None , project = None , from_obj = None):
		super().__init__(SQL_ExperimentGroup , from_obj , name = name , project_id = none_or_id(project))

		self.set_name_map(
			name 			= "name" , 
			id 				= "id" , 
			sql_experiments = "experiments" , 
			sql_project 	= "project" , 
		)

	def find(id = None , name = None , project_id = None , project_name = None):
		proj = Project.find(id = project_id , name = project_name)
		assert (id is not None) or (name is not None)

		if id is None:
			objs = SQL_ExperimentGroup.objects.filter(name = name , project = proj)
			if len(objs) <= 0:
				grop = SQL_ExperimentGroup(name = name , project = proj)
				grop.save()
			else:
				grop = objs[0]
			return grop
		return SQL_ExperimentGroup.objects.get(id = id , project = proj)

class Experiment(Object):
	'''一次实验
	'''

	def __init__(self , group = None , from_obj = None):

		super().__init__(SQL_Experiment , from_obj , force_new = True , group_id = none_or_id(group))

		self.set_name_map(
			logs 			= "logs" , 
			sql_variables 	= "variables" ,
			id 				= "id" , 
			state 			= "state" , 
			end_time 		= "end_time" , 
			start_time 		= "start_time" , 
		)



__all__ = [
	"Project" 			, "SQL_Project" 		, 
	"ExperimentGroup" 	, "SQL_ExperimentGroup" , 
	"Experiment" 		, "SQL_Experiment" 		, 
]