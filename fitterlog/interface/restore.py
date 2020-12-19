from fitterdb.static_list import StaticList_FileManager as Restorer
from ..core.semasiology import Value
from ..core.syntax import Clause

def load_syntax(noun):
	return Clause.load_clause_struct(noun)

def load_last(noun , predicate , with_timestamp = True):

	position = noun.ask_position(predicate)
	with Restorer(Value.FILENAME) as restorer:
		ret_val = restorer.read_last(position)

	if with_timestamp:
		return ret_val
	return ret_val[1]

def load_all(noun , predicate , with_timestamp = True):
	
	position = noun.ask_position(predicate)
	with Restorer(Value.FILENAME) as restorer:
		ret_val = restorer.read_all(position)
	if with_timestamp:
		return ret_val

	return [x[1] for x in ret_val]