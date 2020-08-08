from ...models import Variable , VariableTrack , SingleValue
from ...utils.str_opt import seped_s2list , seped_list2s , seped_s2list_allow_empty
from .utils import rand_num

def append_ids(the_ids , heads , lines , extras , hidden_heads = []):
	'''为输出的表格添加id列'''
	assert len(the_ids) == len(lines)

	heads = ["id"] + heads
	lines = [ 

		[ ( rand_num() , the_ids[i]) ] # (第一个元素是随便加的)
		+ lines[i]  
		for i in range(len(lines))
	] 
	extras = [{"fixed": "left"}] + extras

	if "id" in hidden_heads:
		extras["hide"] =  True

	return heads , lines , extras

def get_head_reorder(heads , show_order):
	'''将head重排序为config中保存的顺序'''

	show_order = [x for x in show_order if x in heads] #按顺序挑出那些记录了的head

	child_pos = [] #哪些head位置是需要重排序的
	for i in range(len(heads)):	
		if heads[i] in show_order:
			child_pos.append(i)
	for i in range(len(child_pos)): #将这些位置替换成show_order
		heads[child_pos[i]] = show_order[i]

	return heads

def get_expe_reorder(expe_lis , hidden_ids):
	'''重排序实验
	1）去掉删除的行
	2）异常退出的实验一定排在后面
	3）按开始时间降序排列
	'''
	expe_lis = expe_lis.order_by("-start_time") # 按开始时间降序排序
	expe_lis = [exp for exp in expe_lis if not (int(exp.id) in hidden_ids)] # 不显示删除的行

	expe_good = [exp for exp in expe_lis if exp.state != 3]
	expe_bad  = [exp for exp in expe_lis if exp.state == 3]

	return expe_good + expe_bad

def experiment_list_to_str_list(
		expe_lis , 
		hidden_heads 	= [] , 
		hidden_ids 		= [] , 
		show_order 		= [] , 
		fixed_left 		= [] , 
		fixed_right 	= [] , 
	):
	'''输出前端需要的表格的各种信息
	'''
	heads 	= {}
	values 	= []
	lines 	= []
	extras 	= []
	editable = set()

	# 获得要显示的实验列表
	expe_lis = get_expe_reorder(expe_lis , hidden_ids)

	# 获得表格的全部基本信息，包括表格头和表格值
	for exp in expe_lis:
		
		value_map = {}
		for varia in exp.variables.all():

			track = varia.tracks.filter(name = "default")
			if len(track) <= 0: #没有default track，则随机找一个track
				track = varia.tracks.all()
			if len(track) <= 0: #没有任何一个track，则跳过此变量
				continue
			track = track[0]

			if len( track.values.all() ) <= 0: #如果track没有变量，也跳过
				continue
				
			value_map[varia.name] = [ # value的每个元素是 (变量id，变量的值，变量的名)
				varia.id ,  
				track.values.latest("time_stamp").value , #找到这个track最新的一个变量
			]

			# 只要有一个元素可编辑，就整列可编辑
			if varia.editable:
				editable.add(varia.name)

		heads.update(value_map)
		values.append(value_map)

	# 获得 head 的排列顺序
	heads = get_head_reorder(list(heads) , show_order)

	# 获得每一行
	for i , exp in enumerate(expe_lis):
		this_line = []
		for h in heads:
			this_line.append( values[i].get(h , (rand_num() , "-")))
		lines.append(this_line)

	# 决定head的其余选项
	extras = [{} for _ in range(len(heads))]
	for i in range(len(heads)):
		if heads[i] in hidden_heads: # 前端点击隐藏的
			extras[i]["hide"] = True
		if heads[i] in fixed_left: # 固定左侧的
			extras[i]["fixed"] = "left"
		if heads[i] in fixed_right: # 固定右侧的
			extras[i]["fixed"] = "right"
		if heads[i] in editable:
		 	extras[i]["editable"] = True

	# 把id列添加进去
	ids = [exp.id for exp in expe_lis]
	heads , lines , extras = append_ids(ids , heads , lines , extras , hidden_heads)

	return ids , heads , lines , extras
		


