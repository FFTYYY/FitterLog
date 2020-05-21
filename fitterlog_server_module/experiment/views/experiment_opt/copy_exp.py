from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Experiment , Project
from ..base import get_path
import os
from fitterlog_cmd.cmd_start import run_a_experiment
from ...utils.constants import special_postfix , config_file_key
from ...utils.permission import check_permission
from ..displays import ask_login

def type2str(type):
	base_types = {
		int : "int" , 
		str : "str" , 
		float : "float" , 
		list : "list" , 
		dict : "dict" , 
	}
	if type in base_types:
		return base_types[type]

	if "function" in str(type):
		return "function"
	if "class" in str(type):
		return "class"
	return "others"

def get_val(exp , name):
	var = exp.variables.filter(name = name)
	if len(var) <= 0:
		return None
	var = var[0]

	trk = var.tracks.filter(name = "default")
	if len(trk) < 0:
		return None
	trk = trk[0]

	return trk.values.latest("time_stamp").value

def copy_exp(request , experiment_id):
	'''新建实验的界面'''
	if not check_permission(request):
		return ask_login(request)

	experiment = Experiment.objects.get(id = experiment_id)
	project = experiment.group.project

	if request.POST:
		config_name = request.POST.get("config_name")
	else:
		raise Http404
	
	target_file = os.path.join(project.path , config_name)
	if not os.path.exists(target_file):
		raise Http404

	nspace = {}
	with open(target_file , "r") as fil:
		config_content = fil.read()

	exec(config_content , nspace)
	argprox = nspace["get_arg_proxy"]()

	args = [ [type2str(x.type) , x.name , get_val(experiment , x.name).strip()] for x in argprox.args]

	context = {
		"args" : args , 
		"project" : project , 
		"config_file": target_file , 
		"config_name": config_name , 
		"last_page_path": "/group/{0}".format(experiment.group.id)
	}

	return render(request , get_path("project/create/experiment_create") , context)
