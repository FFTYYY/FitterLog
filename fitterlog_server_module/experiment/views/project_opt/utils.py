def group_sort(group_list):
	'''按创建时间降序排列，将default放在最前面'''
	group_list = list(group_list)
	group_list.sort(key = lambda x: x.start_time , reverse = True)

	didx = None
	for i in range(len(group_list)):
		if group_list[i].name == "default":
			didx = i
	if didx is not None:
		group_list = group_list[didx:didx+1] + group_list[:didx] + group_list[didx+1:]

	return group_list

def get_num_exp(group_list):

	ret = []
	for g in group_list:
		tot_num = 0
		state_num = [0] * 4

		for e in g.experiments.all():
			tot_num += 1
			state_num[e.state] += 1
		ret.append( [tot_num , state_num , g] )

	return ret