from django.shortcuts import render
from django.http import HttpResponse , Http404
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack
from .base import get_path
from ..utils.str_opt import seped_s2list , seped_list2s

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
	from .get_experiment import experiment_list_to_str_list , append_ids , generate_len

	group = ExperimentGroup.objects.get(id = group_id)

	# generate hiddens
	hide_heads = seped_s2list(group.config.hidden_heads)
	hide_ids = [int(x) for x in seped_s2list(group.config.hidden_ids)]

	# generate heads and rows
	heads , lines , styles = experiment_list_to_str_list( group.experiments.all() , hide_heads , hide_ids)
	lens = generate_len(heads , lines)

	# add line_index
	index_and_lines = zip(list(range(len(lines))) , lines)

	context = {
		"group": group , 
		"heads" : heads , 
		"lines" : lines , 
		"index_and_lines" : index_and_lines , 
		"lens" : lens , 
		"head_and_width_and_style": zip(heads , lens , styles) , 
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
