from ..sql_proxy import Experiment 		as Core_Experiment
from ..sql_proxy import ExperimentGroup as Core_Group
from .others import Variable

this_experiment = None

def new_or_load_experiment(group_id = None, group_name = None, project_id = None, project_name = None , force_new = False):
	global this_experiment
	if this_experiment is not None:
		if not force_new:
			return this_experiment

	new_exp = Experiment(group_id, group_name, project_id, project_name)
	this_experiment = new_exp

	return new_exp


class Experiment:
	def __init__(self , group_id = None, group_name = None, project_id = None, project_name = None):
		
		self.get_core(group_id , group_name , project_id , project_name)
		self.variables = {}
		self.add_line = self.write_log

	def get_core(self , group_id = None, group_name = None, project_id = None, project_name = None):

		if (group_id is None) and (group_name is None):
			group_name = "default"
		if (project_id is None) and (project_name is None):
			project_name = "default"
		self.core = Core_Experiment(group = Core_Group.find(group_id , group_name , project_id , project_name))

	def finish(self):
		from django.utils import timezone
		self.core.finish = True
		self.core.end_time = timezone.now()

	def write_log(self , content = ""):
		content = str(content) + "\n"
		self.core.logs = self.core.logs + content

	def new_variable(self , name , type = str , default = "None" , merge_func = None):
		self.variables[name] = Variable(self , name , type , default , merge_func)

	def use_argument_proxy(self , arg_prox , args = None):
		C = arg_prox.assign_from_cmd(args)
		for arg in arg_prox.args:
			self.new_variable(arg.name , arg.type , C.__dict__[arg.name])

	def __getitem__(self , name):
		return self.variables[name]
