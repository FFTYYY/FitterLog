from .constants import split_token


def seped_s2list(s , sep = split_token):
	return list(filter(lambda x:x , s.strip().split(sep)))

def seped_list2s(l , sep = split_token):
	return sep.join(l)