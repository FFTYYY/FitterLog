from fitterdb.static_list import StaticList_FileManager as Restorer
from ..core.semasiology import Value
from ..core.morphology import Noun
from ..core.syntax import Clause

def load_noun_number():
	'''读取名词数量'''
	return Noun.persister.get(Noun.COUTER)


def load_syntax(noun):
	'''给定名词，读取句子结构'''
	return Clause.load_clauses(noun)

def load_last(noun , predicate , with_timestamp = True):
	'''给定名词和谓词，读取最后一个值。不存在则返回None'''

	position = noun.ask_position(predicate)
	if position is None or position < 0: #如果不存在，返回None
		ret_val = [None , None]
	else:
		with Restorer(Value.FILENAME) as restorer:
			ret_val = restorer.read_last(position)

	if with_timestamp:
		return ret_val
	return ret_val[1]

def load_all(noun , predicate , with_timestamp = True):
	'''给定名词和谓词，读取所有历史值'''
	
	position = noun.ask_position(predicate)
	with Restorer(Value.FILENAME) as restorer:
		ret_val = restorer.read_all(position)
	if with_timestamp:
		return ret_val

	return [x[1] for x in ret_val]
