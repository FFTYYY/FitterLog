from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack , SingleValue
from .base import get_path

def new_project(request):

	if request.POST:
		name = request.POST.get("name")
		path = request.POST.get("path")

		proj = Project(name = name , path = path)
		proj.save()
		grop = ExperimentGroup(name = "default", project_id = proj.id)
		grop.save()
	return HttpResponseRedirect("/")

def new_group(request , project_id):

	if request.POST:
		name = request.POST.get("name")

		grop = ExperimentGroup(name = name , project_id = project_id)
		grop.save()
	return HttpResponseRedirect("/project/%s" % str(project_id))

def new_experiment(request , group_id):

	if request.POST:

		expe = Experiment(group_id = group_id)
		expe.save()
	return HttpResponseRedirect("/group/%s" % (str(group_id)))

def new_variable(request , experiment_id):

	if request.POST:
		name = request.POST.get("name")
		vari = Variable(name = name , expe_id = experiment_id)
		vari.save()
	return HttpResponseRedirect("/experiment/%s" % (str(experiment_id)))

def new_track(request , variable_id):

	if request.POST:
		name = request.POST.get("name")
		track = VariableTrack(name = name , variable_id = variable_id)
		track.save()
	return HttpResponseRedirect("/variable/%s" % (str(variable_id)))

def new_value(request , track_id):

	if request.POST:
		time_stamp = request.POST.get("time_stamp")
		value = request.POST.get("value")
		value = SingleValue(time_stamp = time_stamp , value = value , track_id = track_id)
		value.save()
	return HttpResponseRedirect("/track/%s" % (str(track_id)))

def save_config(request , group_id):
	
	group = ExperimentGroup.objects.get(id = group_id)

	if request.POST:
		hide_columns = request.POST.get("hide_columns")
		hide_ids 	 = request.POST.get("hide_ids")
		intro 		 = request.POST.get("intro")

		group.add_hide_cols(hide_columns)
		group.add_hide_ids(hide_ids)
		group.intro = intro
		group.save()

	return HttpResponseRedirect("/group/%s" % (str(group_id)))
