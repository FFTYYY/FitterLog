from django.shortcuts import render
from django.http import HttpResponse , Http404
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack
from .base import get_path
from .get_experiment import experiment_list_to_str_list

def index(request):
	context = {
		"projects": Project.objects.all() , 
	}
	return render(request , get_path("index") , context)

def project(request , project_id):

	project = Project.objects.get(id = project_id)

	context = {
		"project": project , 
		"groups": project.groups.all() , 
	}
	return render(request , get_path("project") , context)

def group(request , group_id):

	group = ExperimentGroup.objects.get(id = group_id)

	head , lines = experiment_list_to_str_list( group.experiments.all() )
	ids = [str(x.id) for x in group.experiments.all()]
	lines = [ [ids[i]] + lines[i] for i in range(len(lines))] 

	context = {
		"group": group , 
		"head" : head , 
		"lines" : lines , 
	}
	return render(request , get_path("group") , context)

def experiment(request , experiment_id):

	experiment = Experiment.objects.get(id = experiment_id)

	context = {
		"experiment": experiment , 
		"variables": experiment.variables.all() , 
	}
	return render(request , get_path("experiment") , context)

def variable(request , variable_id):

	variable = Variable.objects.get(id = variable_id)

	context = {
		"variable": variable ,
		"tracks" : variable.tracks.all() ,  
	}
	return render(request , get_path("variable") , context)

def track(request , track_id):

	track = VariableTrack.objects.get(id = track_id)

	context = {
		"track": track , 
		"values": track.values.all() , 
	}
	return render(request , get_path("track") , context)
