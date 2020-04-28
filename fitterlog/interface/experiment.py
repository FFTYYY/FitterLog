from ..sql_proxy import Experiment 		as Core_Experiment
from ..sql_proxy import ExperimentGroup as Core_Group
from .others import Variable

this_experiment = None

class Experiment:
	def __init__(self , project_name = None , project_id = None, group_name = None, group_id = None, force_new = False):
		
		global this_experiment
		if this_experiment is not None:
			if not force_new:
				self.core = this_experiment.core
				self.variables = this_experiment.variables
				return 
		this_experiment = self

		self.core = Core_Experiment(group = Core_Group.find(group_name , project_name))
		self.variables = {}

	def new_variable(self , name , type = str , default = "None"):
		self.variables[name] = Variable(self , name , type , default)

	def use_argument_proxy(self , arg_prox , args = None):
		C = arg_prox.assign_from_cmd(args)
		for arg in arg_prox.args:
			self.new_variable(arg.name , arg.type , C.__dict__[arg.name])
			self[arg.name].update(C.__dict__[arg.name])

	def __getitem__(self , name):
		return self.variables[name]

	def finish(self):
		pass