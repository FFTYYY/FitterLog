from ..interface.others import Variable
import argparse

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
		self.args.append(Argument(name , type , str(default)))

	def assign_from_cmd(self , args = None):
		C = argparse.ArgumentParser()

		for arg in self.args:
			C.add_argument("--%s" % arg.name , type = str , default = arg.default)

		C = C.parse_args(args)

		return C

