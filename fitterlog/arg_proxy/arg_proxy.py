import argparse
from .types import *
from YTools.universe import beautiful_str

class Argument:
	def __init__(self , name , type , default , editable = False):
		self.name = name
		self.type = type 
		self.default = default
		self.editable = editable

class ArgProxy:
	def __init__(self , name = None):
		self.name 		= name
		self.args 		= []
		self.name2arg 	= {}

	def name_to_arg(self , name):
		'''给定name，查询对应的Argument'''

		first_ask = self.name2arg.get(name)
		if first_ask is not None: #存在精确匹配
			return first_ask

		ret = [x for x in self.name2arg if x.startswith(name)] #所有合法前缀匹配
		if len(ret) == 1: #只有一个前缀匹配
			return self.name2arg[ ret[0] ]

		return None

	def process_name(self , name):
		return name.strip().replace(" " , "_")

	def add_splitter(self , _ = ""):
		'''添加一个分割符号，没有实际意义'''
		self.args.append( Argument("" , FITTER_SPLITTER , None) )

	def add_argument(self , name , type = String , default = None , editable = False):
		'''添加一个命令行参数'''
		name = self.process_name(name)
		arg = Argument(name , type , default , editable = editable)
		self.args.append(arg)
		self.name2arg[name] = arg

	def add_store_true(self , name , editable = False):
		'''添加一个Bool类型的命令行参数'''
		name = self.process_name(name)
		arg = Argument(name , Bool , "False" , editable = editable)
		self.args.append(arg)
		self.name2arg[name] = arg

	def assign_from_cmd(self , args = None):
		C = argparse.ArgumentParser()

		for arg in self.args:
			if arg.type == FITTER_SPLITTER:
				continue 

			if arg.type == Bool:
				C.add_argument("--%s" % arg.name , action = "store_true" , default = False)
			else:
				C.add_argument("--%s" % arg.name , type = arg.type , default = arg.default)

		C = C.parse_args(args)

		return C

	def __str__(self):
		return beautiful_str(["name" , "default" , "type"] , [
			[x.name , x.default , x.type] for x in self.args
		])

