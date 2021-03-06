from ..interface.others import Variable
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
		self.name = name
		self.args = []
		self.name2arg = {}

		self.add_argument("fitter_project" , String , default = "default")
		self.add_argument("fitter_group" , String , default = "default")
		self.add_splitter()

	def process_name(self , name):
		return name.strip().replace(" " , "_")

	def add_splitter(self , _ = ""):
		self.args.append( Argument("" , FITTER_SPLITTER , None) )

	def add_argument(self , name , type = String , default = None , editable = False):
		name = self.process_name(name)
		arg = Argument(name , type , default , editable = editable)
		self.args.append(arg)
		self.name2arg[name] = arg

	def add_store_true(self , name , editable = False):
		name = self.process_name(name)
		arg = Argument(name , Bool , "False" , editable = editable)
		self.args.append(arg)
		self.name2arg[name] = arg

	def assign_from_cmd(self , args = None):
		C = argparse.ArgumentParser()

		for arg in self.args:
			if arg.type.name == "_FITTER_SPLITTER":
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

