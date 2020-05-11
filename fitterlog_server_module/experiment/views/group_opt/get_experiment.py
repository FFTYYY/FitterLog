from YTools.universe.strlen import max_len
from ...models import Variable , VariableTrack , SingleValue
from ...utils.str_opt import seped_s2list , seped_list2s , seped_s2list_allow_empty

def save_editables(editable_id , editable_val):

	editable_id = [int(x) for x in seped_s2list(editable_id)]
	editable_val = seped_s2list_allow_empty(editable_val) #允许空白字符
	for k , v_id in enumerate(editable_id):
		if v_id < 0:
			continue
		varia = Variable.objects.get(id = v_id)

		track = varia.tracks.filter(name = "default")
		if len(track) <= 0: #没有default track，则跳过此变量
			continue
		track = track[0]

		val = track.values.latest("time_stamp")
		val.value = editable_val[k]
		val.save()

def generate_len(heads , lines):
	if len(lines) == 0:
		return []
	lens = [max_len(s) for s in heads]
	lens = [max( lens[k] , max( [max_len(line[k][1]) for line in lines] )) for k in range(len((heads)))]
	lens = [ min(50 + x*10 , 300) for x in lens]

	return lens

def append_ids(the_ids , heads , lines , styles , hidden_heads = [] , hidden_ids = []):
	assert len(the_ids) == len(lines)

	heads = ["id"] + heads
	lines = [ [(-1 , the_ids[i])] + lines[i] for i in range(len(lines))]
	styles = ["fixed: 'left', style: 'background-color: #363636; color: #AAAAAAFF;',"] + styles

	if "id" in hidden_heads:
		styles[0] += "hide: true,"

	return heads , lines , styles

def get_head_reorder(heads , show_order):

	show_order = [x for x in show_order if x in heads]

	child_pos = []
	for i in range(len(heads)):
		if heads[i] in show_order:
			child_pos.append(i)
	for i in range(len(child_pos)):
		heads[child_pos[i]] = show_order[i]

	return heads

def experiment_list_to_str_list(expe_lis , hidden_heads = [] , hidden_ids = [] , show_order = []):
	heads = {}
	values = []
	lines = []
	styles = []
	editable = {}

	
	expe_lis = expe_lis.order_by("-start_time") # 按开始时间降序排序
	expe_lis = [exp for exp in expe_lis if not (int(exp.id) in hidden_ids)] # 不显示删除的行

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
				
			value_map[varia.name] = (
				varia.id ,  # value的每个元素是 (变量id，变量的值)
				track.values.latest("time_stamp").value , #找到这个track最新的一个变量
			)

			# 只要有一个元素可编辑，就整列可编辑
			if varia.editable:
				editable[varia.name] = True
		heads.update(value_map)
		values.append(value_map)

	# 获得 head 的排列顺序
	heads = get_head_reorder(list(heads) , show_order)

	# 获得每一行
	for i , exp in enumerate(expe_lis):
		this_line = []
		for h in heads:
			this_line.append(values[i].get(h , (-1 , "-") ))
		lines.append(this_line)


	# 决定head的style
	styles = ["" for _ in range(len(heads))]
	for i in range(len(heads)):
		if heads[i] in hidden_heads: # 前端点击隐藏的
			styles[i] += "hide: true,"
		if editable.get(heads[i] , False):
			styles[i] += "edit: 'text',"

	ids = [exp.id for exp in expe_lis]
	heads , lines , styles = append_ids(ids , heads , lines , styles , hidden_heads , hidden_ids)

	return ids , heads , lines , styles
		


