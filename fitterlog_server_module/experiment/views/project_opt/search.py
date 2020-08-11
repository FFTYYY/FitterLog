from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project
from ..base import get_path
import os
from fitterlog_cmd.cmd_start import run_a_experiment
from fitterlog_cmd.experiment_prox import ExperimentProxer_CPU , ExperimentProxer_Torch
from ...utils.permission import check_permission
from ..displays import ask_login
import copy

def dfs(dic , namelist , k , now_arg):
	if k >= len(namelist):
		return [ now_arg ]

	now_name = namelist[k]

	args = []
	for y in dic[now_name]:
		new_arg = copy.copy(now_arg)
		new_arg[now_name] = y
		args += dfs(dic , namelist , k + 1 , new_arg)
	return args

exp_proxs = []

def check_proxs(): #弹出那些已经没有任务的prox
	to_rem = []
	for i in range(len(exp_proxs)):
		if len(exp_proxs[i].tasks) == 0 and not exp_proxs[i].protect:
			exp_proxs[i].close() #关闭线程
			to_rem.append(i) 	 #移除对象
	to_rem.reverse()
	for x in to_rem:
		exp_proxs.pop(x)

def hyper_search(request , project_id):

	global exp_proxs

	# 进行一次检查，弹出那些以前创建的，已经跑完了的子线程，防止内存无限增长
	check_proxs()

	# 要求权限
	if not check_permission(request):
		return ask_login(request)

	# 获取对象
	project = Project.objects.get(id = project_id)

	# 获取搜索空间文件名
	if request.POST:
		search_name = request.POST.get("search-space")
	else:
		raise Http404
	
	# 获取空间文件
	search_file = os.path.join(project.path , search_name)
	if not os.path.exists(search_file):
		raise Http404

	# 运行空间文件，获取搜索空间
	nspace = {}
	with open(search_file , "r") as fil:
		search_content = fil.read()

	exec(search_content , nspace)

	d = nspace["get_search_space"]()
	comm 		= d["command"]
	main_file	= d["entry_file"]
	cfg_file 	= d["config_file"]
	space 		= d["space"]
	is_torch 	= d["is_torch"]
	wait_time 	= d["wait_time"]
	if is_torch:
		gpus 			= d["gpus"]
		max_proc_num 	= d["max_proc_num"]

	#遍历搜索空间，获取所有参数列表
	args = dfs(space , list(space) , 0 , {})

	if is_torch:
		prox = ExperimentProxer_Torch(gpus , max_proc_num , wait_time = wait_time)
	else:
		prox = ExperimentProxer_CPU(wait_time = wait_time)

	for arg in args:
		prox.add_task(
			path 		= project.path , 
			config_name = cfg_file , 
			values 		= arg, 
			command 	= comm , 
			entry_file 	= main_file , 
			prefix 		= "" , 
			suffix 		= "" , 
		)
	prox.protect = False
	prox.start()
	exp_proxs.append(prox)

	return HttpResponseRedirect("/project/%s" % (str(project_id)))



