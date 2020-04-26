'''这个模块用于管理程序的退出时行为。

全局变量:
	on_quit_list: 退出时要调用的方法列表，在退出时会依次调用（当然，不能有参数）。

方法:
	add_quit_process: 向on_quit_list中添加一个方法。
'''
import atexit

on_quit_list = []

def add_quit_process(f):
	'''向on_quit_list中添加一个方法。
	'''
	on_quit_list.append(f)

def on_quit():
	for x in on_quit_list:
		x()

atexit.register(on_quit)