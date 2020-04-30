from django.shortcuts import render
from django.http import HttpResponse , Http404
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack
from .base import get_path
from .get_experiment import experiment_list_to_str_list
from YTools.universe.strlen import max_len

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

	head , lines , styles = experiment_list_to_str_list( group.experiments.all() )
	ids = [str(x.id) for x in group.experiments.all()]

	# append id column
	head = ["id"] + head
	lines = [ [ids[i]] + lines[i] for i in range(len(lines))]
	styles = ["fixed : 'left' , style : 'background-color: #303030; color: #AAAAAAFF;',"] + styles

	lens = [max_len(s) for s in head]
	lens = [max( lens[k] , max( [max_len(line[k]) for line in lines] )) for k in range(len((head)))]
	lens = [ min(50 + x*10 , 300) for x in lens]

	# add line_index
	index_and_lines = zip(list(range(len(lines))) , lines)

	context = {
		"group": group , 
		"head" : head , 
		"lines" : lines , 
		"index_and_lines" : index_and_lines , 
		"lens" : lens , 
		"head_and_width_and_style": zip(head , lens , styles) , 
	}
	return render(request , get_path("group/group") , context)

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
