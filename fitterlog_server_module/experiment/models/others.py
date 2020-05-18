from django.db import models
from ..utils.constants import short_name_len
from .experi import Experiment

class Figure(models.Model):
	name  = models.CharField(max_length = short_name_len)
	html = models.TextField(default = "")
	expe  = models.ForeignKey(Experiment , on_delete = models.CASCADE , related_name = "figures")

	def __str__(self):
		return "<img:" + self.name + ">"

__all__ = [
	"Figure" , 
]