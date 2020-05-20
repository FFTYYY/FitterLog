from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup
from ..base import get_path
from .utils import group_sort , get_num_exp
from .create import *
from ...utils.permission import check_permission
from ..displays import ask_login
from ...utils.str_opt import seped_s2list , seped_list2s

def project(request , project_id):
	if not check_permission(request):
		return ask_login(request)

	project = Project.objects.get(id = project_id)

	groups = group_sort(project.groups.all())
	inform = get_num_exp(groups) 

	context = {
		"project": project , 
		"groups" : groups, 
		"inform" : inform, 
		"config_files" : seped_s2list(project.config_files), 
	}
	return render(request , get_path("project/project") , context)


def new_project(request):
	if not check_permission(request):
		return ask_login(request)

	if request.POST:
		name = request.POST.get("name")
		path = request.POST.get("path")

		proj = Project(name = name , path = path)
		proj.save()
		grop = ExperimentGroup(name = "default", project_id = proj.id)
		grop.save()
	return HttpResponseRedirect("/")

def project_save_config(request , project_id):
	if not check_permission(request):
		return ask_login(request)


	project = Project.objects.get(id = project_id)

	if request.POST:
		for name in request.POST:
			content = request.POST[name]
			name = name.strip()

			if name == "project_intro":
				project.intro = content
			if name == "path_inp":
				project.path = content
			if name == "config_files":
				project.config_files = content
			if name.startswith("group_intro_"):
				grp_id = int(name.split("group_intro_")[1])
				grp = ExperimentGroup.objects.get(id = grp_id)
				grp.intro = content
				grp.save()
		project.save()

	return HttpResponseRedirect("/project/%d" % project_id)