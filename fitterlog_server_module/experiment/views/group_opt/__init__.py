from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from ...utils.str_opt import seped_s2list , seped_list2s
from .editable import save_editables
from .ask_database import experiment_list_to_str_list
from .fake_frontface import cols_from_data
import json


def group(request , group_id):

	group = ExperimentGroup.objects.get(id = group_id)
	
	context = {
		"group": group , 
		"config_files": seped_s2list(group.project.config_files) , 
	}
	return render(request , get_path("group/group") , context)

def get_data(request , group_id):
	''' 把表格数据传过去
	'''
	group = ExperimentGroup.objects.get(id = group_id)
	group.checkconfig()
	
	# 获得保存的各种设置
	hide_heads 	= seped_s2list(group.config.hidden_heads) 	# 隐藏的列
	hide_ids 	= [int(x) for x in seped_s2list(group.config.hidden_ids) if x.isdigit()] # 隐藏的行
	show_order 	= seped_s2list(group.config.show_order)  	# 列顺序
	fixed_left 	= seped_s2list(group.config.fixed_left)  	# 左侧固定的列
	fixed_right = seped_s2list(group.config.fixed_right) 	# 右侧固定的列

	# 生成行和列信息
	ids , heads , lines , extras = experiment_list_to_str_list( 
		group.experiments.all() , 
		hide_heads , hide_ids , show_order , fixed_left , fixed_right
	)

	# 生成要传回的data
	datas = []
	for i , line in enumerate(lines):
		exp_id = ids[i]
		state = Experiment.objects.get(id = exp_id).state

		val_map = {}
		vid_map = {}

		for i , (v_id , val) in enumerate( line ):

			val_map 	[heads[i]] = val
			vid_map 	[heads[i]] = v_id

		datas.append({
			"exp_id" 	: exp_id , 
			"state"  	: state , 
			"val" 		: val_map , 
			"vid" 		: vid_map , 
		})
	
	# 生成要返回的列名
	cols = cols_from_data(heads , lines , extras)

	# 生成列的额外要素
	extra_elements = {
		"editable": { heads[i]: (extras[i].get("editable") is not None) for i in range(len(heads))} , 
	}

	# 生成返回的json字符串
	resp = json.dumps({
		"data": datas , 
		"cols": cols , 
		"extr": extra_elements , 
	})

	return HttpResponse(resp)

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
