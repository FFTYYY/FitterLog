from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last , load_all
from fitterlog.core import Noun , Predicate
from fitterlog.core.utils import merge , ClauseFilter
from base64 import b64encode , b64decode
import warnings
import json

def ask_titles(request):

	# ----- 定义filter函数 -----
	def title_filter_enter(clause , context):
		if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
			return False
		return True

	def title_filter_exit(clause , context , agg):

		my_list = [clause.name]
		if len(agg) > 0:
			my_list.append( agg )
		
		return my_list

	# ----- 获得POST的数据 -----
	if len(request.body) == 0:		
		warnings.warn("ask_titles: 没传POST数据啊？")
		return []

	req_data = json.loads(request.body)
	f = req_data.get("from")
	t = req_data.get("to")

	if f is None or t is None: # warn
		warnings.warn("ask_titles: 没传POST数据啊？")
		return []
	
	# ----- 初步获得范围内的clause -----
	clauses = list(filter(lambda x:x , [ load_syntax(Noun(noun_idx)) for noun_idx in range(f,t)]))
	clauses = merge(clauses , "root")

	# ----- 合并选出的clause -----
	# 相当于一个clauses.linear(rigor = True)，但是带判断
	ret = ClauseFilter().run(clauses , title_filter_enter , title_filter_exit)[0]

	return ret

def ask_datas(request):

	# ----- 定义filter函数 -----
	def title_filter_enter(clause , context):
		if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
			return False
		return True

	def title_filter_exit(clause , context , agg):

		if len(agg) <= 0: #如果自己是叶子，就是记录
			context["ret"].append( [ clause.name , clause.attrs.get("default")] ) # [名，默认值]
		
		return None

	# ----- 获得POST的数据 -----
	if len(request.body) == 0:		
		warnings.warn("ask_datas: 没传POST数据啊？")
		return []

	req_data = json.loads(request.body)
	f = req_data.get("from")
	t = req_data.get("to")

	if f is None or t is None: # warn
		warnings.warn("ask_datas: 没传GET数据啊？")
		return []

	# ----- 初步获得范围内的clause -----
	clauses = list(filter(lambda x:x , [ load_syntax(Noun(noun_idx)) for noun_idx in range(f,t)]))
	clauses = merge(clauses , "root")

	# ----- 拿到所有要展示的谓词的信息 -----
	pred_infos = ClauseFilter().run(clauses , title_filter_enter , title_filter_exit , {"ret": []})
	pred_infos = pred_infos[1]["ret"]
	defaults   = [info[1]            for info in pred_infos] # 默认值
	preds      = [Predicate(info[0]) for info in pred_infos] # 谓词列表
	# note：之所以把pred_infos拆开再合并是为了提前把谓词id询问出来，不用在循环中每次询问

	# ----- 生成返回的data -----
	data = {}
	for noun_idx in range(f,t):
		noun = Noun(noun_idx)  # 获得当前名词
		now_data = {} 			# 当前名词的数据
		for pred , default_val in zip(preds , defaults):
			val = load_last(noun , pred , with_timestamp = False) 	# 获取记录的最后一个值
			if val is None: 										# 使用默认值
				val = default_val
			now_data[pred.name] = val 
		data[noun.id] = now_data

	return data
