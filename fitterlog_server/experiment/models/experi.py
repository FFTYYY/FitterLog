from django.db import models
from ..utils.constants import short_name_len , path_len

class Project(models.Model):
	'''一个项目
	'''
	name = models.CharField(max_length = short_name_len , unique = True)
	path = models.CharField(max_length = path_len)

	def __str__(self):
		return self.name

class Experiment(models.Model):
	'''一次实验
	'''
	logs = models.TextField(default = "")
	group = models.ForeignKey("ExperimentGroup" , on_delete = models.CASCADE , related_name = "experiments")

	start_time = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.name

class ExperimentGroup(models.Model):
	name = models.CharField(max_length = short_name_len)
	project = models.ForeignKey(Project , on_delete = models.CASCADE , related_name = "groups")

	def __str__(self):
		return self.name

__all__ = [
	"Project" , 
	"Experiment" , 
	"ExperimentGroup" , 
]