from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack , SingleValue
from .base import get_path


def new_project(request):

	if request.POST:
		name = request.POST.get('name')
		path = request.POST.get('path')

		proj = Project(name = name , path = path)
		proj.save()
	return HttpResponseRedirect("/")

def new_group(request , project_id):

	if request.POST:
		name = request.POST.get('name')

		proj = ExperimentGroup(name = name , project_id = project_id)
		proj.save()
	return HttpResponseRedirect("/project/%s" % str(project_id))

def new_experiment(request , group_id):

	if request.POST:

		expe = Experiment(group_id = group_id)
		expe.save()
	return HttpResponseRedirect("/group/%s" % (str(group_id)))

def new_variable(request , experiment_id):

	if request.POST:
		name = request.POST.get('name')
		vari = Variable(name = name , expe_id = experiment_id)
		vari.save()
	return HttpResponseRedirect("/experiment/%s" % (str(experiment_id)))

def new_track(request , variable_id):

	if request.POST:
		name = request.POST.get('name')
		track = VariableTrack(name = name , variable_id = variable_id)
		track.save()
	return HttpResponseRedirect("/variable/%s" % (str(variable_id)))

def new_value(request , track_id):

	if request.POST:
		time_stamp = request.POST.get('time_stamp')
		value = request.POST.get('value')
		value = SingleValue(time_stamp = time_stamp , value = value , track_id = track_id)
		value.save()
	return HttpResponseRedirect("/track/%s" % (str(track_id)))
