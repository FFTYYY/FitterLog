def group_sort(group_list):
	group_list = list(group_list)
	group_list.sort(key = lambda x: x.start_time , reverse = True)

	didx = None
	for i in range(len(group_list)):
		if group_list[i].name == "default":
			didx = i
	if didx is not None:
		group_list = group_list[didx:didx+1] + group_list[:didx] + group_list[didx+1:]

	return group_list