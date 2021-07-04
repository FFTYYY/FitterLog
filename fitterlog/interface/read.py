'''这个文件是一些独立的询问操作。
所有写操作都必须在对象内进行，读操作就无所谓。
'''

from fitterdb.static_list import StaticList_FileManager as Restorer , check_lastpos
from ..core.semasiology import Value
from ..core.morphology import Noun
from ..core.syntax import Clause

def load_noun_number():
	'''读取名词数量'''
	return Noun.persister.get(Noun.COUTER)

def load_syntax(noun):
	'''给定名词，读取句子结构'''
	return Clause.load(noun)

def load_last(noun , predicate , with_timestamp = True):
	'''给定名词和谓词，读取最后一个值。不存在则返回None'''

	last_pos = noun.ask_position(predicate)

	if check_lastpos(last_pos): #如果不存在，返回None
		ret_val = [None , None]
	else:
		with Restorer(Value.FILENAME) as restorer:
			ret_val = restorer.read_last(last_pos)

	if with_timestamp:
		return ret_val
		
	return ret_val[1]

def load_all(noun , predicate , with_timestamp = True):
	'''给定名词和谓词，读取所有历史值'''
	
	last_pos = noun.ask_position(predicate)

	if check_lastpos(last_pos): #如果不存在，返回None
		ret_val = []
	else:
		with Restorer(Value.FILENAME) as restorer:
			ret_val = restorer.read_all(last_pos)

	if with_timestamp:
		return ret_val

	return [x[1] for x in ret_val]
