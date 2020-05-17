import random
from .constants import cookie_key , debugging

passwords = []
my_seed = str(random.randint(2333 , 23333333))

if debugging:
	my_seed = str(233333)

def check_passwords():
	if len(passwords) == 0:
		if debugging:
			passwords.append("2333")
		else:
			passwords.append(input("input a possword:"))
	return passwords

def check_permission(request):
	check_passwords()
	return ask_cookie_value(request , cookie_key) == my_seed

def give_permission(request , response):
	'''给request的源发许可'''
	check_passwords()
	return set_cookie_value(response , key = cookie_key , value = my_seed)

def ask_cookie_value(request , key):
	'''输入一个request，返回这个request对应的cookie值

	:param request: 一个用户请求
	:param str key: cookie名 
	:return str: 这个请求的名为key的cookie的值，不存在则返回None
	'''
	return request.COOKIES.get(key)

def set_cookie_value(response , key , value = None):
	'''给用户设置cookie值

	:param response: 一个网站响应
	:param str key: cookie名 
	:param str value: cookie值
	:return response: 返回输入的response
	'''
	response.set_cookie(
		key = key ,
		value = value ,
		max_age = 60 * 60 * 24 * 365 * 100 , #每过一百年就得重新获取一次
		#domain =  domain,
		#path = "/" , 
	)
	return response

def del_cookie(response , key):
	response.delete_cookie(key)
