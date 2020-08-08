from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from ...utils.str_opt import seped_s2list , seped_list2s
from .editable import save_editables
from .get_data import *

def group(request , group_id):

	group = ExperimentGroup.objects.get(id = group_id)
	
	context = {
		"group": group , 
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
