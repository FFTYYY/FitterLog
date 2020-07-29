from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from ...utils.str_opt import seped_s2list , seped_list2s
from .get_experiment import *
from .editable import save_editables
from .utils import *

def group(request , group_id):

	group = ExperimentGroup.objects.get(id = group_id)
	group.checkconfig()
	
	# generate hiddens
	hide_heads = seped_s2list(group.config.hidden_heads)
	hide_ids = [int(x) for x in seped_s2list(group.config.hidden_ids)]
	show_order = seped_s2list(group.config.show_order)
	fixed_left = seped_s2list(group.config.fixed_left)
	fixed_right= seped_s2list(group.config.fixed_right)

	# generate heads and rows
	ids , heads , lines , styles = experiment_list_to_str_list( 
					group.experiments.all() , hide_heads , hide_ids , show_order , fixed_left , fixed_right)
	
	lens = generate_len(heads , lines)
	min_lens = [x//2 for x in lens]

	# add line_index
	line_information = zip(ids , list(range(len(lines))) , lines)

	# add state
	line_information = [ [Experiment.objects.get(id = x[0]).state] + list(x) for x in line_information]

	context = {
		"hide_bad_exp" : "true" if group.config.hide_bad_exp else "false", 
		"group": group , 
		"line_information" : line_information , 
		"head_information": zip(heads , lens , min_lens , styles) , 
		"config_files": seped_s2list(group.project.config_files) , 
	}
	return render(request , get_path("group/group") , context)

def new_group(request , project_id):

	if request.POST:
		name = request.POST.get("name")

		grop = ExperimentGroup(name = name , project_id = project_id)
		grop.save()
	return HttpResponseRedirect("/project/%s" % str(project_id))


def group_save_config(request , group_id):
	group = ExperimentGroup.objects.get(id = group_id)

	if request.POST:
		hide_columns = request.POST.get("hide_columns")
		hide_ids 	 = request.POST.get("hide_ids")
		intro 		 = request.POST.get("intro")
		show_order 	 = request.POST.get("show_order")
		hide_bad_exp = request.POST.get("hide_bad_exp")
		editable_id  = request.POST.get("editable_id") 
		editable_val = request.POST.get("editable_val") 
		fixed_left	 = request.POST.get("fixed_left") 
		fixed_right	 = request.POST.get("fixed_right") 

		save_editables(editable_id , editable_val)


		hide_bad_exp = True if hide_bad_exp == "true" else False

		group.checkconfig()

		group.config.hide_bad_exp = hide_bad_exp
		group.add_hide_cols(hide_columns)
		group.add_hide_ids(hide_ids)
		group.intro = intro
		group.config.show_order = show_order
		group.config.fixed_left = fixed_left
		group.config.fixed_right = fixed_right
		group.save()

	return HttpResponseRedirect("/group/%s" % (str(group_id)))
