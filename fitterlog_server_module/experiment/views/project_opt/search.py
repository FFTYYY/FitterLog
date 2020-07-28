from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project
from ..base import get_path
import os
from fitterlog_cmd.cmd_start import run_a_experiment
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

def hyper_search(request , project_id):

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
	comm ,  main_file , cfg_file , search_space = nspace["get_search_space"]()

	#遍历搜索空间
	namelist = list(search_space)
	args = dfs(search_space , namelist , 0 , {})

	for arg in args:
		run_a_experiment(
			path 		= project.path , 
			config_name = cfg_file , 
			values 		= arg, 
			command 	= comm , 
			entry_file 	= main_file , 
			prefix 		= "" , 
			suffix 		= "" , 
		)

	return HttpResponseRedirect("/project/%s" % (str(project_id)))



