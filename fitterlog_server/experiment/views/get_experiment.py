
def experiment_list_to_str_list(expe_lis):
	head = {}
	values = []
	lines = []
	styles = []

	for exp in expe_lis:
		value_map = {}
		for varia in exp.variables.all():

			track = varia.tracks.filter(name = "default")
			if len(track) <= 0:
				track = varia.tracks.all()
			if len(track) <= 0:
				continue
			track = track[0]

			if len( track.values.all() ) <= 0:
				continue
				
			value_map[varia.name] = track.values.latest("time_stamp").value
		head.update(value_map)
		values.append(value_map)

	head = list(head)
	styles = ["" for _ in range(len(head))]

	for i , exp in enumerate(expe_lis):
		this_line = []
		for h in head:
			this_line.append(values[i].get(h , "-"))
		lines.append(this_line)

	return head , lines , styles
		


