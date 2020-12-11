from ..sql_proxy import Experiment 		as Core_Experiment
from ..sql_proxy import ExperimentGroup as Core_Group
from .others import Variable
from .paint import Painter
from ..quit import add_quit_process
import time

this_experiment = None

def new_or_load_experiment(group_id = None, group_name = None, project_id = None, project_name = None , force_new = False):
	'''创建实验。如果已经创建过，就直接返回刚刚创建的那个实验
	
	参数：
		group_id：实验组的id
		group_name：实验组的名。和group_id只需给定其中一个
		project_id：项目id
		project_name：项目名。和project_id只需给出其中一个
		force_new：如果为True，则强制创建新实验。默认为False。
	'''
	global this_experiment
	if this_experiment is not None:
		if not force_new:
			return this_experiment

	new_exp = Experiment(group_id, group_name, project_id, project_name)
	this_experiment = new_exp

	return new_exp

def new_or_load_expr_from_cmd(arg_prx , args = None , force_new = False):
	'''从命令行参数直接创建实验。如果已经创建过，就直接返回刚刚创建的那个实验
	
	参数：
		arg_prx：超参数代理
		args：命令行参数列表。默认使用sys.args
		force_new：如果为True，则强制创建新实验。默认为False。
	'''
	global this_experiment
	if this_experiment is not None:
		if not force_new:
			return this_experiment

	C = arg_prx.assign_from_cmd(args)

	new_exp = Experiment(group_name = C.fitter_group, project_name = C.fitter_project)
	new_exp.use_argument_proxy(arg_prx , args)
	this_experiment = new_exp

	return new_exp


class Experiment:
	def __init__(self , group_id = None, group_name = None, project_id = None, project_name = None):
		'''创建实验。
		'''
		
		self._get_core(group_id , group_name , project_id , project_name)
		self.variables = {}
		self.figures = {}
		self.add_line = self.write_log
		self.id = int(self.core.id)

		self.log_cache = self.core.log or ""
		self.last_save_log = time.time()

	def _get_core(self , group_id = None, group_name = None, project_id = None, project_name = None):

		if (group_id is None) and (group_name is None):
			group_name = "default"
		if (project_id is None) and (project_name is None):
			project_name = "default"
		self.core = Core_Experiment(group = Core_Group.find(group_id , group_name , project_id , project_name))

	def finish(self):
		'''结束实验。在实验正常结束时调用'''

		from ..sql_proxy.base import on_quit_kill_thread
		on_quit_kill_thread()

		self._save_log()

		from django.utils import timezone
		self.core.state = 1
		self.core.end_time = timezone.now()

	def _save_log(self):
		self.core.logs = self.log_cache
		self.core.save()

	def write_log(self , content = ""):
		'''写一行文字log'''
		content = str(content) + "\n"
		self.log_cache = self.log_cache + content

		# 每秒保存一次log
		if time.time() - self.last_save_log > 1:
			self._save_log()
			self.last_save_log = time.time()

	def new_variable(self , name , type = str , default = "None" , merge_func = None , editable = False):
		'''新建一个变量
		参数：
			name：变量的名。请保证不重复。
			type：如何解释变量（所有变量都以字符串储存，这个函数将字符串解释成值）。
			default：变量的默认值。可以给字符串。
			merge_func：function。如何合并所有track。如果给定这个参数，则每次更新其他track时时会自动更新default。
			editable：是否可以在前端修改。
		'''
		self.variables[name] = Variable(self , name , type , default , merge_func , editable)

	def use_argument_proxy(self , arg_prox , args = None):
		'''使用一个参数代理
		'''
		C = arg_prox.assign_from_cmd(args)
		for arg in arg_prox.args:
			if arg.type.name == "_FITTER_SPLITTER":
				continue
			self.new_variable(arg.name , arg.type , str(C.__dict__[arg.name]) , editable = arg.editable)

	def new_figure(self , name):
		fig = Painter(name , self)
		self.figures[name] = Painter(name , self)
		return fig

	def __getitem__(self , name):
		return self.variables[name]



def make_exp_state_on_quit():
	if this_experiment is not None:
		if this_experiment.core.state == 0:
			print ("unexpected quit!!!")
			this_experiment.core.state = 3 #unexpected quit

add_quit_process(make_exp_state_on_quit)
