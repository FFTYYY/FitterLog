from ..sql_proxy import Variable 		as Core_Variable
from ..sql_proxy import VariableTrack 	as Core_Track
from ..sql_proxy import SingleValue 	as Core_SingleValue

class SingleValue:
	def __init__(self , track , timestamp , value):
		self.timestamp = timestamp
		self.value = str(value)
		self.track = track

		self.core = Core_SingleValue(value , timestamp , track = track.core)

	def __str__(self):
		return self.value

class Track:
	def __init__(self , variable , name , type , default_value):
		self.variable = variable
		self.name = name
		self.type = type
		self.default_value = default_value

		self.core = Core_Track(name , variable = variable.core)
		
		self.max_time_stamp = 0
		self.time_stamps = []
		self.single_values = {}
		self.now_value = None

		self.update = self.add_value

	def kth_value(self , k):
		'''离散化后的时间戳。
		'''
		return self.single_values[self.time_stamps[k]]

	def add_value(self , value , time_stamp = None):
		if time_stamp is None:
			time_stamp = self.max_time_stamp + 1

		if time_stamp <= self.max_time_stamp:
			raise "Bad time stamp."

		self.max_time_stamp = time_stamp

		self.time_stamps.append(time_stamp)
		self.single_values[time_stamp] = SingleValue(self , time_stamp , value)
		self.now_value = self.single_values[time_stamp]


	def __getitem__(self , time_stamp):
		return self.single_values[time_stamp]

	@property
	def recent_value(self):
		'''返回最近的value
		返回值类型：str
		'''
		if len(self.time_stamps) > 0:
			return self.kth_value(-1).value #返回最近的值
		return self.default_value

	@property
	def value(self):
		'''返回最近的value的值
		返回值类型：self.type
		'''
		return self.type(self.recent_value)
	
	def __str__(self):
		return str(self.value)

class Variable:
	def __init__(self , experiment , name , type , default_value):
		self.experiment = experiment
		self.name = name
		self.type = type
		self.default_value = default_value

		self.core = Core_Variable(name , experiment = experiment.core)
		self.tracks = {}

		self.new_track("default")

	def update(self , value , time_stamp = None , track = "default"):
		self[track].update(value , time_stamp)

	def new_track(self , name , default_value = None):
		if default_value is None:
			default_value = self.default_value
		self.tracks[name] = Track(self , name , self.type , default_value)

	def __getitem__(self , name):
		if name not in self.tracks:
			return self.tracks["default"][name]
		return self.tracks[name]

	def __str__(self):
		return str(self["default"])
