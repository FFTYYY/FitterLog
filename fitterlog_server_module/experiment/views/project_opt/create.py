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
	if hasattr(type , "name"):
		return type.name
	return "unknown"

def get_val(exp , name , default = ""):
	var = exp.variables.filter(name = name)
	if len(var) <= 0:
		return str(default)
	var = var[0]

	trk = var.tracks.filter(name = "default")
	if len(trk) < 0:
		return str(default)
	trk = trk[0]

	return trk.values.latest("time_stamp").value

def experiment_to_create(request , project_id = None, experiment_id = None):
	'''新建实验的界面'''

	# 要求权限
	if not check_permission(request):
		return ask_login(request)

	# 至少要有一个参数
	if project_id is None and experiment_id is None:
		raise Http404

	# 获取对象
	if experiment_id is not None:
		experiment = Experiment.objects.get(id = experiment_id)
		project = experiment.group.project
	else:
		project = Project.objects.get(id = project_id)

	# 获取config文件名
	if request.POST:
		config_name = request.POST.get("chosen-config")
	else:
		raise Http404
	
	# 获取config文件
	target_file = os.path.join(project.path , config_name)
	if not os.path.exists(target_file):
		raise Http404

	# 运行config文件，获取argprox对象
	nspace = {}
	with open(target_file , "r") as fil:
		config_content = fil.read()

	exec(config_content , nspace)
	argprox = nspace["get_arg_proxy"]()

	# 决定各种参数
	if experiment_id is not None: # 复制实验
		args = [ [type2str(x.type) , x.name , get_val(experiment , x.name , x.default).strip()] 
					for x in argprox.args]
		last_page_path = "/group/{0}".format(experiment.group.id)
	else: #使用默认值
		args = [ [type2str(x.type) , x.name , x.default] for x in argprox.args]
		last_page_path = "/project/{0}".format(project.id)

	# 返回的上下文
	context = {
		"args" : args , 
		"project" : project , 
		"config_file": target_file , 
		"config_name": config_name , 
		"last_page_path": last_page_path,
	}

	return render(request , get_path("project/create/experiment_create") , context)


def new_experiment(request , project_id):
	'''根据获得的各种信息来在命令行开始一个实验（运行代码）。'''	

	if not check_permission(request):
		return ask_login(request)

	project = Project.objects.get(id = project_id)


	values = {}
	if request.POST:
		for name in request.POST:
			if name == "csrfmiddlewaretoken":
				continue
			if name.startswith(special_postfix):
				continue
			values[name] = str(request.POST[name])
		config_name = request.POST[config_file_key]
		last_page_path = request.POST["__last_page_path"]

		prefix 	= request.POST["__prefix"]
		command = request.POST["__command"]
		file 	= request.POST["__file"]
		suffix 	= request.POST["__suffix"]

	run_a_experiment(
		path 		= project.path , 
		config_name = config_name , 
		values 		= values, 
		command 	= command , 
		entry_file 	= file , 
		prefix 		= prefix , 
		suffix 		= suffix , 
	)
	
	return HttpResponseRedirect(last_page_path)