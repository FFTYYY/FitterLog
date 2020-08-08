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


def find_range_explist(group , page , limit , hide_ids):
	'''获取某一个特定范围的实验列表，而不是全部'''

	l = (page-1) * limit # 注意page是从1开始的
	r = page * limit

	# 先排除删除的id，再排序，再取区间
	return group.experiments.order_by("-start_time").exclude(id__in = hide_ids)[l : r]


def get_data(request , group_id):

	''' 把表格数据传过去
	'''
	group = ExperimentGroup.objects.get(id = group_id)
	group.checkconfig()

	get_parameter 	= json.loads( list(request.GET)[0] ) # layui的傻逼实现
	page 			= get_parameter["page"] #页号，从1开始
	limit 			= get_parameter["limit"] #每页数量
	
	# 获得保存的各种设置
	hide_heads 	= seped_s2list(group.config.hidden_heads) 	# 隐藏的列
	hide_ids 	= [int(x) for x in seped_s2list(group.config.hidden_ids) if x.isdigit()] # 隐藏的行
	show_order 	= seped_s2list(group.config.show_order)  	# 列顺序
	fixed_left 	= seped_s2list(group.config.fixed_left)  	# 左侧固定的列
	fixed_right = seped_s2list(group.config.fixed_right) 	# 右侧固定的列

	# 生成行和列信息
	expe_list = find_range_explist(group , page , limit , hide_ids) #这一步已经去除了所有隐藏的行

	ids , heads , lines , extras = experiment_list_to_str_list( 
		expe_list , hide_heads , show_order , fixed_left , fixed_right
	)

	# 生成要传回的data
	datas = []
	for i , line in enumerate(lines):
		exp_id 	= ids[i]
		state 	= Experiment.objects.get(id = exp_id).state

		val_map = {}
		vid_map = {}

		for i , (v_id , val) in enumerate( line ):

			val_map [heads[i]] = val
			vid_map [heads[i]] = v_id

		datas.append({
			"exp_id" 	: exp_id , 
			"state"  	: state , 
			"val" 		: val_map , 
			"vid" 		: vid_map , 
		})
	
	# 生成要返回的列名
	cols = cols_from_data(heads , lines , extras)

	# 生成额外信息
	extra_elements = {
		"editable": { heads[i]: (extras[i].get("editable") is not None) for i in range(len(heads))}, 
		"page" 	  : page ,
		"limit"	  : limit ,
		"tot_num" : group.experiments.exclude(id__in = hide_ids).count() , 
	}

	# 生成返回的json字符串
	resp = json.dumps({
		"data": datas , 
		"cols": cols , 
		"extr": extra_elements , 
	})

	return HttpResponse(resp)

