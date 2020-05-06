def get_tracks(track_lis):

	t_vs = []

	for t in track_lis:
		vlis = []
		for v in t.values.all():
			if v.time_stamp < 0:
				continue
			vlis.append( (v.time_stamp , v.value) )
		t_vs.append( (t , vlis))

	return t_vs
