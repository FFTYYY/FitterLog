from fitterdb.static_list import StaticList_FileManager as Restorer
from ..core.semasiology import Value

def load_last(noun , predicate , with_timestamp = True):
	with Restorer(Value.FILENAME) as restorer:
		position = noun.ask_position(predicate)
		ret_val = restorer.read_last(position)

	if with_timestamp:
		return ret_val
	return ret_val[1]

def load_all(noun , predicate , with_timestamp = True):
	with Restorer(Value.FILENAME) as restorer:
		position = noun.ask_position(predicate)
		ret_val = restorer.read_all(position)
	if with_timestamp:
		return ret_val

	return [x[1] for x in ret_val]