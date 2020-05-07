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
	show_order = seped_s2list(group.config.show_order)

	# generate heads and rows
	ids , heads , lines , styles = experiment_list_to_str_list( 
					group.experiments.all() , hide_heads , hide_ids , show_order)
	
	lens = generate_len(heads , lines)
	min_lens = [x//2 for x in lens]

	# add line_index
	line_information = zip(ids , list(range(len(lines))) , lines)

	# add state
	line_information = [ [Experiment.objects.get(id = x[0]).state] + list(x) for x in line_information]

	print (group.config.hide_bad_exp)

	context = {
		"hide_bad_exp" : "true" if group.config.hide_bad_exp else "false", 
		"group": group , 
		"heads" : heads , 
		"lines" : lines , 
		"line_information" : line_information , 
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

	from .varaible_opt import get_tracks

	variable = Variable.objects.get(id = variable_id)

	tracks_and_values = get_tracks(variable.tracks.all())

	context = {
		"variable": variable ,
		"tracks_and_values": tracks_and_values ,  
	}
	return render(request , get_path("variable/variable") , context)


def track(request , track_id):

	track = VariableTrack.objects.get(id = track_id)

	context = {
		"track": track , 
		"values": track.values.all() , 
	}
	return render(request , get_path("track") , context)
