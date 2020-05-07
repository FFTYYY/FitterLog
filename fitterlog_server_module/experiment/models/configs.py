from django.db import models
from ..utils.constants import short_name_len , path_len

class GroupConfig(models.Model):
	hidden_heads = models.TextField(default = "")
	hidden_ids 	 = models.TextField(default = "")
	show_order 	 = models.TextField(default = "")
	hide_bad_exp = models.BooleanField(default = False)

	def __str__(self):
		return self.name

__all__ = [
	"GroupConfig" , 
]