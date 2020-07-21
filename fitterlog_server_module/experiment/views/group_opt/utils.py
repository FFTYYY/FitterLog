from YTools.universe.strlen import max_len
import random

def rand_num():
	return random.randint(-1e8 , 0)

def generate_len(heads , lines):
	'''为heads生成长度（根据字符串长度）用于前端'''
	if len(lines) == 0:
		return []
	lens = [max_len(s) for s in heads]
	lens = [max( lens[k] , max( [max_len(line[k][1]) for line in lines] )) for k in range(len((heads)))]
	lens = [ min(50 + x*10 , 300) for x in lens]

	return lens
