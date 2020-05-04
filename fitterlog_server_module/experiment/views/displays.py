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
	from .group_opt.group_sort import group_sort

	project = Project.objects.get(id = project_id)

	context = {
		"project": project , 
		"groups": group_sort(project.groups.all()) , 
	}
	return render(request , get_path("project") , context)

def group(request , group_id):
	from .group_opt.get_experiment import experiment_list_to_str_list , append_ids , generate_len

	group = ExperimentGroup.objects.get(id = group_id)
	group.checkconfig()
	
	# generate hiddens
	hide_heads = seped_s2list(group.config.hidden_heads)
	hide_ids = [int(x) for x in seped_s2list(group.config.hidden_ids)]

	# generate heads and rows
	ids , heads , lines , styles = experiment_list_to_str_list( group.experiments.all() , hide_heads , hide_ids)
	
	lens = generate_len(heads , lines)
	min_lens = [x//2 for x in lens]

	# add line_index
	id_and_index_and_lines = zip(ids , list(range(len(lines))) , lines)

	context = {
		"group": group , 
		"heads" : heads , 
		"lines" : lines , 
		"id_and_index_and_lines" : id_and_index_and_lines , 
		"lens" : lens , 
		"head_and_width_and_style": zip(heads , lens , min_lens , styles) , 
	}
	return render(request , get_path("group/group") , context)

def experiment(request , experiment_id):

	experiment = Experiment.objects.get(id = experiment_id)

	context = {
		"experiment": experiment , 
		"variables": experiment.variables.all() , 
	}
	return render(request , get_path("experiment/experiment") , context)


def experiment_log(request , experiment_id):

	experiment = Experiment.objects.get(id = experiment_id)

	context = {
		"experiment": experiment , 
		"logs": experiment.logs , 
	}
	return render(request , get_path("experiment/logs") , context)


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