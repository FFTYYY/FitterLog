from ..data.experi import Experiment as Core_Experiment , SQL_Experiment
from ..data.experi import ExperimentGroup as Core_Group
from ..data.variable import Variable as Core_Variable
from ..data.variable import VariableTrack as Core_Track
from ..data.variable import SingleValue as Core_SingleValue

class SingleValue:
	def __init__(self , track , timestamp , value):
		self.timestamp = timestamp
		self.value = value
		self.track = track

		self.core = Core_SingleValue(value , timestamp , track = track.core)

	def __str__(self):
		return str(self.value)

class Track:
	def __init__(self , variable , name , default_value):
		self.variable = variable
		self.name = name
		self.default_value = default_value

		self.core = Core_Track(name , variable = variable.core)
		
		self.max_time_stamp = 0
		self.single_values = {}
		self.now_value = None

	def add_value(self , value , time_stamp = None):
		if time_stamp is None:
			time_stamp = self.max_time_stamp + 1

		if time_stamp <= self.max_time_stamp:
			raise "Bad time stamp."

		self.max_time_stamp = time_stamp

		self.now_value = value
		self.single_values[time_stamp] = SingleValue(self , time_stamp , value)

	def __getitem__(self , time_stamp):
		return self.single_values[time_stamp]

	def __str__(self):
		return str(self.now_value)

class Variable:
	def __init__(self , experiment , name , default_value):
		self.experiment = experiment
		self.name = name
		self.default_value = default_value

		self.core = Core_Variable(name , experiment = experiment.core)
		self.tracks = {}

		self.new_track("default")

	def new_track(self , name , default_value = None):
		if default_value is None:
			default_value = self.default_value
		self.tracks[name] = Track(self , name , default_value)

	def __getitem__(self , name):
		return self.tracks[name]

	def __str__(self):
		return str(self["default"])

class Experiment:
	def __init__(self , project_name = None , project_id = None, group_name = None, group_id = None):

		self.core = Core_Experiment(group = Core_Group.find(group_name , project_name))
		self.variables = {}

	def new_variable(self , name , default = "None"):
		self.variables[name] = Variable(self , name , default)

	def __getitem__(self , name):
		return self.variables[name]

	def finish(self):
		pass