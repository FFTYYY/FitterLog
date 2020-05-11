from ...models import Variable
from ...utils.str_opt import seped_s2list , seped_list2s , seped_s2list_allow_empty

def save_editables(editable_id , editable_val):
	'''更新那些可修改变量的值。注意这里不会创建新SingleValue'''
	
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
