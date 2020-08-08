'''
	伪前端，因为js太麻烦了，所以我直接在python里处理好发过去。
'''
from .utils import generate_len

def cols_from_data(heads , lines , extras):

	lens = generate_len(heads , lines)
	cols = []

	for i , head in enumerate(heads):
		extra = extras[i]
		width = lens[i]

		col = {
			"field"		: "inner-{head}".format(head = head), 
			"title"		: head, 
			"width" 	: width , 
			"minWidth"	: width // 2 , 
			"sort" 		: True ,
			"align" 	:'center', 
		}
		if extra.get("hide" , False):
			col["hide"] = True
		if extra.get("fixed") is not None:
			col["fixed"] = extra["fixed"]

		cols.append(col)

	return cols
