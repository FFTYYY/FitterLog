from YTools.network.server.server import start_server
from fitterlog.interface.read import load_noun_number , load_syntax , load_last , load_all
from fitterlog.interface import Sentence
from fitterlog.core import Noun , Predicate
from fitterlog.core.utils import merge , ClauseFilter
from base64 import b64encode , b64decode
import warnings
import json
import re
from YTools.universe.exceptions import ArgumentError , YAttributeError

def my_float(val):
	# 是不是浮点数
	try:
		val = float(str(val))
	except ValueError:
		return None
	return  float(val)

def close_all(lis):
	'''关闭所有文件'''
	[s.close() for s in lis]

def check_noun(noun , filter_info):
	try:
		s = Sentence(noun = noun)
	except YAttributeError: # 读取失败
		return None


	for pred_name , cond_info in filter_info.items():
		val = s.get_son(pred_name)
		if val is not None:
			val = val.value

		if cond_info["type"] == "exists":
			if val is None:
				s.close() # 返回None的时候一定要关闭s
				return None

		if cond_info["type"] == "regular":
			if re.search( cond_info["cond"] , str(val) ) is None:
				s.close()
				return None

		if cond_info["type"] == "interval":
			val = my_float(val) # 不是浮点数，条件不成立
			if val is None:
				s.close()
				return None

			l , r = cond_info["cond"]
			l = my_float(l)
			r = my_float(r)
			if None in [l,r]: # 不是浮点数，条件作废
				continue
			if val < l or val > r:
				s.close()
				return None
				
	return s # 返回一个sentence表示成功


def ask_datas(request):
	'''给定过滤器参数和大小限制，返回符合条件的noun（datas）和clause（title）。

	request.POST：
		filter_info： 一个dict，描述过滤条件
		start： 从第几个名词开始搜索
		trans_size： 最多传输几个名词。
		searc_size： 最多搜索几个名词。
	'''

	# ----- 获得POST的数据 -----
	if len(request.body) == 0:		
		warnings.warn("ask_datas: 没传POST数据啊？ / 无body")
		return []

	req_data 	= json.loads(request.body)
	filter_info = req_data.get("filter"    ) # 过滤器描述
	start 		= req_data.get("start"     ) # 从第几个名词开始搜索
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

	valid_sents = [] # 每一条记录： (noun , clause)
	for noun_idx in range(start , search_r):
		noun = Noun(noun_idx)
		sent = check_noun(noun , filter_info)

		if sent is not None:
			valid_sents.append( sent )

			if len(valid_sents) > trans_size: # 记录够多了，就返回
				search_r = noun_idx + 1 # 实际上搜到的上界
				break

	end_flag = search_r == noun_num # 这次是不是搜到头了

	# 没有找到合法的数据的返回值
	blank_response = {
		"title_list": [] , 
		"data_dict" : [] , 
		"num_loaded": 0 , 
		"pos" : -1 if end_flag else search_r , 
	}
	if len(valid_sents) == 0: # 如果没有找到名词，就直接返回
		return blank_response

	# ----- 获得合法名词的clause的并 -----
	merged_clause = merge(valid_sents , "root")

	title_list = merged_clause.listize(no_attr = True)

	# ----- 生成 data_dict -----

	# 生成 data_dict
	data_dict = {
		s.noun.id : {son_sent.real_name : son_sent.value for son_sent in s.all_sons()}
		for s in valid_sents
	}

	close_all(valid_sents) # return之前先关闭文件
	return {
		"title_list": title_list , 
		"data_dict" : data_dict , 
		"num_loaded": len(valid_sents) , 
		"pos" : -1 if end_flag else search_r , 
	}
