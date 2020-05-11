def smooth_lis(lis):
	lim = 500
	if len(lis) < lim:
		return lis
	p = len(lis) / lim #每p个采样一次

	lis = [lis[int(p*i+0.5)] for i in range(lim) if int(p*i+0.5) < len(lis)]

	return lis

def get_tracks(track_lis):

	t_vs = []

	for t in track_lis:
		vlis = []
		for v in t.values.all():
			if v.time_stamp < 0:
				continue
			val = v.value
			try:
				float(val)
			except ValueError: #not a float
				continue
			vlis.append( (v.time_stamp , val) )
		vlis = smooth_lis(vlis)
		t_vs.append( (t , vlis))

	return t_vs
