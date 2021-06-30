from YTools.network.server.server import start_server
from fitterlog.interface.restore import load_noun_number , load_syntax , load_last , load_all
from fitterlog.core import Noun , Predicate
from fitterlog.core.utils import merge , ClauseFilter
from base64 import b64encode , b64decode

def ask_titles(request):
	# noun_number = load_noun_number()

	def title_filter_enter(clause , context):
		if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
			return False
		return True

	def title_filter_exit(clause , context , agg):

		my_list = [clause.name]
		if len(agg) > 0:
			my_list.append( agg )
		
		return my_list

	clauses = list(filter(lambda x:x , [ load_syntax(Noun(noun_idx)) for noun_idx in range(19,40)]))
	clauses = merge(clauses , "root")

	# 相当于一个clauses.linear(rigor = True)，但是带判断
	ret = ClauseFilter().run(clauses , title_filter_enter , title_filter_exit)[0]

	return ret

def ask_datas(request):
	# noun_number = load_noun_number()
	def title_filter_enter(clause , context):
		if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
			return False
		return True

	def title_filter_exit(clause , context , agg):

		if len(agg) <= 0: #如果自己是叶子，就是记录
			context["ret"].append(clause.name)
		
		return None

	clauses = list(filter(lambda x:x , [ load_syntax(Noun(noun_idx)) for noun_idx in range(19,40)]))
	clauses = merge(clauses , "root")

	# 拿到所有要展示的谓词
	pred_names = ClauseFilter().run(clauses , title_filter_enter , title_filter_exit , {"ret": []})
	pred_names = pred_names[1]["ret"]
	preds = [Predicate(pred_name) for pred_name in pred_names]

	data = {}
	for noun_idx in range(19,40):
		noun = Noun(noun_idx)
		now_data = {}
		for pred in preds:
			now_data[pred.name] = load_last(noun , pred , with_timestamp = False)
		data[noun.id] = now_data
		
	return data
