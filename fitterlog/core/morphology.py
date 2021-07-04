from YTools.system.static_hash import DoubleHash , HighDimHash
from ..base.constants import DB_NAME
from ..base.constants import TB_NAME_NOUN_PRED_POS , KEY_NOUN_CNT 
from ..base.constants import TB_NAME_PRED_ID , KEY_PRED_CNT



class Noun:
	'''名词类，描述一个名词。注意名词和名词的编号一一对应，本质上这个类只是给编号赋予更多含义。
	这个类负责维护一个从名词、谓词对到值的映射。
	
	常量：
		persister：用来持久化全体名词数据的对象
		COUTER：persister中计数器的key

	属性：
		id: int，这个名词的全局唯一的编号


	方法：
		ask_position
		set_position
		get_new_id
		new
	'''
	persister = HighDimHash(db_name = DB_NAME , tb_name = TB_NAME_NOUN_PRED_POS) #查询名词和谓词对应的值的位置
	COUTER = KEY_NOUN_CNT #计数器key，统计目前有多少名词，用来生成名词编号。（注意这里key必须是二维向量所以用了-1,-1）

	def __init__(self , id):
		'''
		参数：
			id：int，这个名词的编号。
		'''
		self.id = id

		self.persister.ensure(self.COUTER , 0) #保证counter位置存在

	def ask_position(self , predicate):
		'''给定谓词，查询本名词以及给定的谓词的保存位置
		不存在则返回None
		'''
		return self.persister.get( [self.id , predicate.id] )

	def set_position(self , predicate , val):
		'''给定谓词和值，将本名词和给定谓词的保存位置设置为给定值
		'''

		#理论上来说，同一个名词只（应）存在于一个线程内，所以不存在同步性的问题
		self.persister.set( [self.id , predicate.id] , val )

	def get_new_id():
		'''生成一个新的名词编号'''
		return Noun.persister.plus(Noun.COUTER , 1)

	def new():
		return Noun(Noun.get_new_id())

	def __str__(self):
		return "<Noun: {0}>".format(self.id)
	def __int__(self):
		return self.id

class Predicate:
	'''这个类用来建立谓词名（字符串）和谓词编号（整数）的双向持久化映射。
	'''

	persister = DoubleHash(db_name = DB_NAME , tb_name = TB_NAME_PRED_ID) # 查询谓词的名称和值
	COUTER = KEY_PRED_CNT # 计数器key，统计目前有多少谓词，用来生成谓词编号

	def __init__(self , name):
		'''给定谓词名的初始化'''
		self.name = name

		self.ensure_id()
		self.id = self.persister.ask_val(key = self.name)

	def ensure_id(self):
		'''确保自身name和id的映射在数据库中存在
		'''

		self.persister.ensure(self.COUTER , 0) #如果counter不存在，就设为0

		if self.persister.ask_val(self.name) is None:
			counter = self.persister.plus(self.COUTER , 1)
			self.persister.ensure(self.name , counter - 1)

		# 注意，多个同时发生的ensure操作只会把值设置一次，因此即使多个线程plus了多次，生成的id会不连续，
		# 但是可以保证所有线程得到的id是一致的

	def get_name(id):
		'''给定id，询问谓词名
		'''
		return Predicate.persister.ask_key(val = id)

	def from_id(id):
		'''给定id，生成一个谓词
		'''
		return Predicate(name = Predicate.get_name(id))	

	def __str__(self):
		return "<Predicate: id = {0} , name = {1}>".format(self.id , self.name)
