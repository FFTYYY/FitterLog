from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last , load_all
from fitterlog.core import Noun , Predicate
from fitterlog.core.utils import merge , ClauseFilter
from base64 import b64encode , b64decode
import warnings
import json
from clause_filters import title_cf_enter , title_cf_exit , data_cf_enter , data_cf_exit
import re
# TODO：对于title也分块

def my_float(val):
	# 是不是浮点数
	try:
		val = float(str(val))
	except ValueError:
		return None
	return  float(val)

# TODO: 考虑default
def check_noun(noun_idx , filter_info):
	noun = Noun(noun_idx)
	for pred_name , cond_info in filter_info.items():
		pred = Predicate(pred_name)
		val = load_last(noun , pred , with_timestamp = False)
		if cond_info["type"] == "exists":
			if val is None:
				return False
		if cond_info["type"] == "regular":
			if re.search( cond_info["cond"] , str(val) ) is None:
				return False
		if cond_info["type"] == "interval":
			val = my_float(val)
			if val is None: # 不是浮点数，条件作废
				continue
			l , r = cond_info["cond"]
			l = float(l)
			r = float(r)
			if val < l or val > r:
				return False
	return True


def ask_datas(request):

	# ----- 获得POST的数据 -----
	if len(request.body) == 0:		
		warnings.warn("ask_datas: 没传POST数据啊？ / 无body")
		return []

	req_data 	= json.loads(request.body)
	filter_info = req_data.get("filter") # 过滤器描述
	start 		= req_data.get("start") # 从第几个名词开始搜索
	trans_size 	= req_data.get("trans_size") # 最多获得几个结果
	searc_size 	= req_data.get("searc_size") # 最多搜索多少个名词

	if None in [filter_info , start , trans_size , searc_size]: # warn
		warnings.warn("ask_datas: 没传POST数据啊？")
		return []

	start 		= int( start  	  )
	trans_size 	= int( trans_size )
	searc_size 	= int( searc_size )

	# ----- 筛选名词 -----
	noun_num = load_noun_number()
	search_r = min( start+searc_size , noun_num) # 搜索范围上界
	end_flag = search_r == noun_num # 这次是不是搜到头了

	valid_nouns = []
	for noun_idx in range(start , search_r):
		if check_noun(noun_idx , filter_info):
			valid_nouns.append(noun_idx)
			if len(valid_nouns) > trans_size:
				break

	# 如果没有找到名词，就直接返回
	blank_response = {
		"title_list": [] , 
		"data_dict" : [] , 
		"num_loaded": 0 , 
		"pos" : -1 if end_flag else search_r , 
	}
	if len(valid_nouns) == 0:
		return blank_response

	# ----- 获得合法名词的clause -----
	clauses = list(filter(lambda x:x , [ load_syntax(Noun(noun_idx)) for noun_idx in valid_nouns]))
	if len(clauses) == 0: #虽然有合法名词，但是没有记录句子结构
		return blank_response

	merged_clause = merge(clauses , "root")

	# ----- 生成 title_list -----
	title_list = ClauseFilter().run(merged_clause , title_cf_enter , title_cf_exit)[0]

	# ----- 生成 data_dict -----

	# 拿到所有要展示的谓词的信息 	
	pred_infos = ClauseFilter().run(merged_clause , data_cf_enter , data_cf_exit , {"ret": []})
	pred_infos = pred_infos[1]["ret"]
	defaults   = [info[1]            for info in pred_infos] # 默认值
	preds      = [Predicate(info[0]) for info in pred_infos] # 谓词列表
	# note：之所以把pred_infos拆开再合并是为了提前把谓词id询问出来，不用在循环中每次询问
	# 生成 data_dict
	data_dict = {}
	for noun_idx in valid_nouns:
		noun = Noun(noun_idx)  # 获得当前名词
		now_data = {} 			# 当前名词的数据
		for pred , default_val in zip(preds , defaults):
			val = load_last(noun , pred , with_timestamp = False) 	# 获取记录的最后一个值
			# if val is None: 										# 使用默认值
			# 	val = default_val
			now_data[pred.name] = val 
		data_dict[noun.id] = now_data

	return {
		"title_list": title_list , 
		"data_dict" : data_dict , 
		"num_loaded": len(valid_nouns) , 
		"pos" : -1 if end_flag else search_r , 
	}
