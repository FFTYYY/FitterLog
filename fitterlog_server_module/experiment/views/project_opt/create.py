from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Experiment , Project
from ..base import get_path
import os

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


def experiment_to_create(request , project_id):
	'''新建实验的界面'''
	project = Project.objects.get(id = project_id)

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

	args = [ [type2str(x.type) , x.name , x.default] for x in argprox.args]

	context = {
		"args" : args , 
		"project" : project , 
		"config_file": target_file , 
	}

	return render(request , get_path("project/create/experiment_create") , context)


def new_experiment(request , project_id):
	'''根据获得的各种信息来在命令行开始一个实验（运行代码）。'''

	if request.POST:
		for name in request.POST:
			if name == "csrfmiddlewaretoken":
				continue
			print (request.POST[name])

	return HttpResponseRedirect("/project/%d" % project_id)