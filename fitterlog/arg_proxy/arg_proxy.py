from ..interface.others import Variable
import argparse
from .types import *

class Argument:
	def __init__(self , name , type , default):
		self.name = name
		self.type = type 
		self.default = default

class ArgProxy:
	def __init__(self , name = None):
		self.name = name
		self.args = []

	def add_argument(self , name , type = str , default = None):
		self.args.append(Argument(name , type , default))

	def add_store_true(self , name):
		self.args.append(Argument(name , Bool , "False"))

	def assign_from_cmd(self , args = None):
		C = argparse.ArgumentParser()

		for arg in self.args:
			if arg.type == Bool:
				C.add_argument("--%s" % arg.name , action = "store_true" , default = False)
			else:
				C.add_argument("--%s" % arg.name , type = str , default = arg.default)

		C = C.parse_args(args)

		return C

