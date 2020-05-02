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

	start_time = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.name

class ExperimentGroup(models.Model):
	name = models.CharField(max_length = short_name_len)
	intro = models.TextField(default = "")
	project = models.ForeignKey(Project , on_delete = models.CASCADE , related_name = "groups")
	config = models.OneToOneField(GroupConfig , on_delete = models.SET_NULL , null = True)

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

		hide_cols = seped_s2list(self.config.hidden_heads)
		hide_cols = seped_s2list(s)
		hide_cols = list(set(hide_cols))
		self.config.hidden_heads = seped_list2s(hide_cols)

	def add_hide_ids(self , s):
		self.checkconfig()

		hide_cols = seped_s2list(self.config.hidden_ids)
		hide_cols += seped_s2list(s)
		hide_cols = list(set(hide_cols))
		self.config.hidden_ids = seped_list2s(hide_cols)


__all__ = [
	"Project" , 
	"Experiment" , 
	"ExperimentGroup" , 
]