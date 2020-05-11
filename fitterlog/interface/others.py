from ..sql_proxy import Variable 		as Core_Variable
from ..sql_proxy import VariableTrack 	as Core_Track
from ..sql_proxy import SingleValue 	as Core_SingleValue

class SingleValue:
	def __init__(self , track , timestamp , value):
		self.timestamp = timestamp
		self.value = str(value)
		self.track = track

		self.core = Core_SingleValue(str(value) , timestamp , track = track.core)

	def __str__(self):
		return self.value

class Track:

	#public
	def __init__(self , variable , name , type , default_value):
		self.variable = variable
		self.name = name
		self.type = type
		self.default_value = default_value

		self.core = Core_Track(name , variable = variable.core)
		
		self.max_time_stamp = -1
		self.time_stamps = []
		self.single_values = {}

		self.single_values[-1] = SingleValue(self , -1 , default_value)
		self.now_value = self.single_values[-1]

	def __getitem__(self , time_stamp):
		return self.single_values[time_stamp]

	def update(self , value , time_stamp = None):
		'''更新track。
		time_stamp如果留空，则默认为上一次的值加一。初始默认为0。
		'''
		if time_stamp is None:
			time_stamp = self.max_time_stamp + 1

		if time_stamp <= self.max_time_stamp: # bad timestamp
			return 

		self.max_time_stamp = time_stamp

		self.time_stamps.append(time_stamp)
		self.single_values[time_stamp] = SingleValue(self , time_stamp , str(value))
		self.now_value = self.single_values[time_stamp]

		# 更新变量的值
		if self.name != "default":
			self.variable.merge()

	@property
	def value(self):
		'''返回最近的value的值（解释）
		返回值类型：self.type
		'''
		return self.type(self.recent_value)

	@property
	def recent_value(self):
		'''返回最近的value（不解释）
		返回值类型：str
		'''
		if len(self.time_stamps) > 0:
			return self.kth_value(-1).value #返回最近的值
		return self.default_value

	def kth_value(self , k):
		'''离散化后的时间戳。返回第k个value解释前的值。
		'''
		return self.single_values[self.time_stamps[k]]
	
	def __str__(self):
		return str(self.value)


# variable 实际上是 track 的公有继承。
class Variable:
	def __init__(self , experiment , name , type , default_value , merge_func , editable):
		self.experiment = experiment
		self.name = name
		self.type = type
		self.default_value = str(default_value)
		self.merge_func = merge_func
		self.editable = editable

		self.core = Core_Variable(name , experiment = experiment.core)
		self.core.editable = editable
		self.tracks = {}

		self.new_track("default")

		self.id = int(self.core.id)

	def new_track(self , name , default_value = None):
		if default_value is None:
			default_value = self.default_value
		self.tracks[name] = Track(self , name , self.type , str(default_value))

	def merge(self): #合并所有track的值，生成default的值
		if self.merge_func is None:
			return
		v_list = []
		for t in self.tracks:
			v_list.append([self.tracks[t].max_time_stamp , self.tracks[t].value])

		new_val = self.merge_func(*v_list)
		if new_val is not None:
			self.update(new_val)

	def update(self , value , time_stamp = None , track = "default"):
		self[track].update(value , time_stamp)

	@property
	def value(self):
		'''返回最近的value的值
		返回值类型：self.type
		'''
		return self["default"].value

	def __getitem__(self , name):
		if name not in self.tracks:
			if isinstance(name , int): #time stamp
				return self.tracks["default"][name]
			else: #new track name
				self.new_track(name)
		return self.tracks[name]

	def __str__(self):
		return str(self["default"])
