from django.db import models
from ..utils.constants import short_name_len , path_len

class GroupConfig(models.Model):
	hidden_heads = models.TextField(default = "")
	hidden_ids 	 = models.TextField(default = "")
	show_order 	 = models.TextField(default = "")
	hide_bad_exp = models.BooleanField(default = False)

class ProjectConfig(models.Model):
	config_files = models.TextField(default = "")
	cmd_pref = models.CharField(default = "" , max_length = short_name_len)
	cmd_comm = models.CharField(default = "" , max_length = short_name_len)
	cmd_entr = models.CharField(default = "" , max_length = short_name_len)
	cmd_suff = models.CharField(default = "" , max_length = short_name_len)

__all__ = [
	"GroupConfig" , 
	"ProjectConfig" , 
]