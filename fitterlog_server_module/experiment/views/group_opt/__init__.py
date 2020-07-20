from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from ...utils.str_opt import seped_s2list , seped_list2s
from .get_experiment import *
from .editable import save_editables

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
	
	#把head添加进每个单元格的信息
	lines = [ [ [x[0] , x[1] , heads[i]] for i , x in enumerate(line) ] for line in lines ] 

	# add line_index
	line_information = zip(ids , list(range(len(lines))) , lines)

	# add state
	line_information = [ [Experiment.objects.get(id = x[0]).state] + list(x) for x in line_information]

	context = {
		"hide_bad_exp" : "true" if group.config.hide_bad_exp else "false", 
		"group": group , 
		"heads" : heads , 
		"lines" : lines , 
		#"line_information" : line_information , 
		#"head_and_style": zip(heads , styles) , 
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
