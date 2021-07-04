# 生成 table_list 的 clause_filter 的入口
def title_cf_enter(clause , context):
	if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
		return False
	return True
	
# 生成 table_list 的 clause_filter 的出口
def title_cf_exit(clause , context , sons):

	my_list = [clause.name]
	my_list.append( sons )
	return my_list
	
# 生成 data_dict 的 clause_filter 的入口
def data_cf_enter(clause , context):
	if clause.attrs.get("display" , False): #如果遇到一个display，就停止递归
		return False
	return True
# 生成 data_dict 的 clause_filter 的出口
def data_cf_exit(clause , context , sons):

	if len(sons) <= 0: #如果自己是叶子，就是记录
		context["ret"].append( [ clause.name , clause.attrs.get("default")] ) # [名，默认值]
	
	return None
