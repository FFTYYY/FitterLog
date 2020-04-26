def find_or_new(clas , **kwargs):
	kwargs = {x : kwargs[x] for x in kwargs if kwargs[x] is not None } #去除None（不查找项）
	obj = clas.objects.filter(**kwargs)
	if len(obj) >= 1:
		return obj[0]
	return clas(**kwargs)

def make_obj_list(clas , objs):
	return [clas(from_obj = obj) for obj in objs]
