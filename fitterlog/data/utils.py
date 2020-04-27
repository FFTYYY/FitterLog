def find_or_new(sql_class , **kwargs):
	'''根据 kwargs 规定的属性查找 sql 对象，如果找不到就新建一个。
	'''
	kwargs = {x : kwargs[x] for x in kwargs if kwargs[x] is not None } #去除None（不查找项）
	obj = sql_class.objects.filter(**kwargs)
	if len(obj) >= 1:
		return obj[0]
	return sql_class(**kwargs)

def make_obj_list(clas , sql_objs):
	'''根据给定的 sql 对象生成 fitterlog 对象
	'''
	return [clas(from_obj = obj) for obj in sql_objs]

def none_or_id(obj):
	return obj.id if obj is not None else obj