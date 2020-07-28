from django.db import models
from ..utils.constants import short_name_len , path_len
from ..utils.str_opt import seped_list2s , seped_s2list
from .configs import GroupConfig , ProjectConfig

class Project(models.Model):
	'''一个项目
	'''	
	name = models.CharField(max_length = short_name_len , unique = True)
	path = models.CharField(max_length = path_len)
	intro = models.TextField(default = "")
	config = models.OneToOneField(ProjectConfig , on_delete = models.SET_NULL , null = True)

	def __str__(self):
		return self.name

	def checkconfig(self):
		if self.config is None:
			self.config = ProjectConfig()
			self.config.save()
			self.save()

	def save(self):
		self.checkconfig()
		self.config.save()
		return super().save()

	@property
	def config_files(self):
		self.checkconfig()
		return self.config.config_files

	@config_files.setter
	def config_files(self , v):
		self.checkconfig()
		self.config.config_files = v
	

class Experiment(models.Model):
	'''一次实验
	'''
	logs = models.TextField(default = "")
	intro = models.TextField(default = "")
	group = models.ForeignKey("ExperimentGroup" , on_delete = models.CASCADE , related_name = "experiments")

	# 0: running , 1: finished , 2: almost finished , 3: unexpected quit
	state = models.IntegerField(default = 0)

	start_time = models.DateTimeField(auto_now_add = True) # 创建时间
	end_time   = models.DateTimeField(null = True)

	def __str__(self):
		return self.name

class ExperimentGroup(models.Model):
	name = models.CharField(max_length = short_name_len)
	intro = models.TextField(default = "")
	project = models.ForeignKey(Project , on_delete = models.CASCADE , related_name = "groups")
	config = models.OneToOneField(GroupConfig , on_delete = models.SET_NULL , null = True)

	start_time = models.DateTimeField(auto_now_add = True) # 创建时间

	def __str__(self):
		return self.name

	def checkconfig(self):
		if self.config is None:
			self.config = GroupConfig()
			self.config.save()

	def save(self):
		self.checkconfig()
		self.config.save()
		return super().save()

	def add_hide_cols(self , s):
		self.checkconfig()

		hide_cols = seped_s2list(s)
		hide_cols = list(set(hide_cols))
		self.config.hidden_heads = seped_list2s(hide_cols)

	def add_hide_ids(self , s):
		self.checkconfig()

		hide_ids = seped_s2list(self.config.hidden_ids)
		hide_ids += seped_s2list(s)
		hide_ids = list(set(hide_ids))
		self.config.hidden_ids = seped_list2s(hide_ids)

	def add_show_order(self , s):
		self.checkconfig()

		self.config.show_order = s


__all__ = [
	"Project" , 
	"Experiment" , 
	"ExperimentGroup" , 
]