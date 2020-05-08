from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from ...utils.str_opt import seped_s2list , seped_list2s
from .get_experiment import *


def group(request , group_id):

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

def new_group(request , project_id):

	if request.POST:
		name = request.POST.get("name")

		grop = ExperimentGroup(name = name , project_id = project_id)
		grop.save()
	return HttpResponseRedirect("/project/%s" % str(project_id))


def save_config(request , group_id):
	
	group = ExperimentGroup.objects.get(id = group_id)

	if request.POST:
		hide_columns = request.POST.get("hide_columns")
		hide_ids 	 = request.POST.get("hide_ids")
		intro 		 = request.POST.get("intro")
		show_order 	 = request.POST.get("show_order")
		hide_bad_exp = request.POST.get("hide_bad_exp")
		editable_id  = request.POST.get("editable_id") 
		editable_val = request.POST.get("editable_val") 

		save_editables(editable_id , editable_val)


		hide_bad_exp = True if hide_bad_exp == "true" else False

		group.checkconfig()

		group.config.hide_bad_exp = hide_bad_exp
		group.add_hide_cols(hide_columns)
		group.add_hide_ids(hide_ids)
		group.add_show_order(show_order)
		group.intro = intro
		group.save()

	return HttpResponseRedirect("/group/%s" % (str(group_id)))
