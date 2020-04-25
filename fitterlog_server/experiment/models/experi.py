from django.db import models
from ..utils.constants import short_name_len , path_len

class Project(models.Model):
	'''一个课题
	'''
	name = models.CharField(max_length = short_name_len)
	path = models.CharField(max_length = path_len)

class Experiment(models.Model):
	'''一次实验
	'''
	logs = models.TextField(default = "")
	group = models.ForeignKey("ExperimentGroup" , on_delete = models.CASCADE , related_name = "experiments")

	#start_date

	def __str__(self):
		return self.name

class ExperimentGroup(models.Model):
	name = models.CharField(max_length = short_name_len)

	def __str__(self):
		return self.name

__all__ = [
	"Project" , 
	"Experiment" , 
	"ExperimentGroup" , 
]