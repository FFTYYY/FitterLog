from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ..models import Project , ExperimentGroup , Experiment
from .base import get_path


def new_project(request):

	if request.POST:
		name = request.POST.get('name')
		path = request.POST.get('path')

		proj = Project(name = name , path = path)
		proj.save()
	return HttpResponseRedirect("../")

def new_group(request , project_id):

	if request.POST:
		name = request.POST.get('name')

		proj = ExperimentGroup(name = name , project_id = project_id)
		proj.save()
	return HttpResponseRedirect("../project/%s" % str(project_id))

def new_experiment(request , group_id):

	if request.POST:

		expe = Experiment(group_id = group_id)
		expe.save()
	return HttpResponseRedirect("../group/%s" % (str(group_id)))
