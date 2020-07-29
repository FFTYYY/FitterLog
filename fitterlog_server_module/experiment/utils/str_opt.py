from .constants import split_token


def seped_s2list_allow_empty(s , sep = split_token):
	if s == None:
		return []

	return s.strip().split(sep)


def seped_s2list(s , sep = split_token):
	if s == None:
		return []
	return list(filter(lambda x:x , s.strip().split(sep)))

def seped_list2s(l , sep = split_token):
	return sep.join(l)