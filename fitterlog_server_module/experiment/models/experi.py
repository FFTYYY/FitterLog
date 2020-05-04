from django.db import models
from ..utils.constants import short_name_len , path_len
from ..utils.str_opt import seped_list2s , seped_s2list
from .configs import GroupConfig

class Project(models.Model):
	'''一个项目
	'''	
	name = models.CharField(max_length = short_name_len , unique = True)
	path = models.CharField(max_length = path_len)
	intro = models.TextField(default = "")

	def __str__(self):
		return self.name

class Experiment(models.Model):
	'''一次实验
	'''
	logs = models.TextField(default = "")
	intro = models.TextField(default = "")
	group = models.ForeignKey("ExperimentGroup" , on_delete = models.CASCADE , related_name = "experiments")

	running = models.BooleanField(default = True)

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