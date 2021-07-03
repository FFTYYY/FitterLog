from YTools.network.protocol import Protocol
from YTools.network.protocol import int2bytes , bytes2int , str2bytes , bytes2str
from YTools.system.fakepath import new_fakefolder
from YTools.system.locker import Locker
from YTools.universe.onexit import add_quit_methods
from YTools.system.filewrite import write_file , read_file , get_filesize
from functools import partial
import pickle
import os

class StaticList_FileManager:
	'''这个类管理静态链表的文件。

	每个静态链表会储存一个链表头（head）记录一些元信息，和链表身（body）来保存主要数据。
	body由bo和dy两个部分组成，原则上bo是链表的历史元素，dy是链表的最后一个元素。这样要读取链表的最后一个元素
		时就可以更快速的读取。
	head记录三个信息：上次保存的位置，bo的长度、dy的长度。

	'''

	proto = Protocol(
		head = [
			["last_pos" , 8 , partial(int2bytes , length = 8) , bytes2int] , 
			["bo_size"  , 8 , partial(int2bytes , length = 8) , bytes2int] , 
			["dy_size"  , 8 , partial(int2bytes , length = 8) , bytes2int] , 
		] , 
		body = [
			["bo"  , "bo_size" , pickle.dumps , pickle.loads] , 
			["dy"  , "dy_size" , pickle.dumps , pickle.loads] , 
		] , 
	)

	FOLDER_NAME = "Fitterlog_Static_List"
	LOCKER_PATH = "fitterlog/static_list/"

	def __init__(self , filename):

		# 获取文件名
		self.save_file_name = os.path.abspath(new_fakefolder(self.FOLDER_NAME))
		self.save_file_name = os.path.join(self.save_file_name , filename)

		open(self.save_file_name , "ab+").close() 		#确保文件存在
		self.file = open(self.save_file_name , "rb+") 	#以读写模式打开，这个模式下可以随意写，无视文件大小
		add_quit_methods(self.close) 					#保证文件关闭

		self.locker = Locker()
		self.locker_name  = self.LOCKER_PATH + filename + "/" #在lokcer中使用的键的前缀
		self.key_filesize = self.locker_name + "filesize/"

	def __enter__(self):
		return self
	def __exit__(self , *args , **kwargs):
		self.close()

	def close(self):
		self.file.close()

	def read_head(self , save_pos):
		'''从save_pos开始读，读取一个head'''
		head_data = read_file(self.file , save_pos , self.proto.headsize)
		head = self.proto.decode_head(head_data)
		return head

	def read_last(self, save_pos, head = None):
		'''从save_pos开始读，读取一个dy'''

		if head is None:
			head = self.read_head(save_pos)

		#跳过bo，直接读dy
		dy_data = read_file(self.file , save_pos + self.proto.headsize + head["bo_size"] , head["dy_size"]) 
		dy = self.proto.body[-1][3](dy_data) # dy的解码函数

		return dy

	def read_block(self , save_pos):
		'''读一整个block'''

		head = self.read_head(save_pos)

		#读取完整的body
		body_data = read_file(self.file , save_pos + self.proto.headsize , head["bo_size"] + head["dy_size"])
		body = self.proto.decode_body(body_data , head)

		return head , body

	def read_all(self , save_pos):
		'''从某个位置开始往前读'''

		got_content = []

		while save_pos >= 0:
			head , body = self.read_block(save_pos)

			#重建这一块的数据
			now_list = body["bo"]
			now_list.append(body["dy"])

			#存入这一块
			got_content.append(now_list)

			save_pos = head["last_pos"]

		res_list = []
		for x in got_content[::-1]: #逆序
			res_list.extend(x)
		return res_list

	def dump_data(self , last_pos , bo , dy):

		# 将内存中保存的文件长度更新成自己看到的文件长度，具体是不是这个长度并不重要，locker会保证一致性
		self.locker.set_if(self.key_filesize , None , get_filesize(self.file))

		# 编码数据
		data = self.proto.encode(last_pos = last_pos , bo = bo , dy = dy)

		# 向locker请求长度
		end_point   = self.locker.plus(self.key_filesize , len(data)) # 仅在这一步执行同步
		start_point = end_point - len(data) 						  # 算出开头位置
		write_file(self.file , start_point , data)

		return start_point

class StaticList(list , StaticList_FileManager):
	'''这个类是一个可以持久化的list。正常使用就像普通的list一样。当调用save()后，会把所有数据保存下来，并返回
		保存位置。只要记得保存的位置，下次可以从这个保存位置还原元素。
	对于已经保存的部分，内存中的值可以看成一种缓存，可以任意清空。但是清空后要保证最后一个元素仍然是可读取的。

	注意，StaticList是「一次性的」，即一个进程中使用StaticList来给list加上保存的功能，而并没有设计在另一个进
		程中恢复一个StaticList的功能，因为那会添加额外的设计，没有必要。在另一个进程中只有读取所有值的功能。
	而在另一个进程中只要可以读取这个StaticList上一次保存的位置，依然可以在他后面续上值。

	属性：
		last_pos： int。上一次保存的位置。
		saved_size： int。所有内存中的元素中，前多少个已经保存了。
		remember_last： 最近保存的元素。保证清空后这个值也依然存在。
	'''

	def __init__(self , filename , init_list = [] , last_pos = -1):
		'''创建一个新的StaticList。需要初始化两个部分，一个是已经保存的数据的信息（last_pos)，二个是新
			加入的数据，可以用一个list来初始化。
		在初始化时传入last_pos只是为了读取remember_last。如果不需要则不用传入last_pos。

		'''
		StaticList_FileManager.__init__(self , filename)
		list.__init__(self , init_list)

		self._remember_last = None # 清空后，依然记得之前的最后一个元素。采用懒惰维护，只在需要读取时读取。
		self.last_pos   = -1       # 上一块保存的位置

		if self.check_lastpos(last_pos):
			self.last_pos = last_pos

	def check_lastpos(self , last_pos):
		'''检查一个给定的last_pos输入是否合法'''
		return last_pos is not None and int(last_pos) >= 0

	@property
	def size(self):
		return len(self)

	def recent(self):
		'''总之是最后一个元素'''
		
		if len(self) > 0:
			return self[-1]

		# 如果自己没有_remember_last的值，但是有last_pos，就去文件中读取
		if self._remember_last is None and self.check_lastpos(self.last_pos):
			self._remember_last = self.read_last(self.last_pos)
		return self._remember_last


	def active_last(self): 
		'''尚未保存的，且是最后的'''
		if len(self) > 0:
			return self[-1]
		return None

	def active_nonlast(self): 
		'''尚未保存的，且不是最后的'''
		return self[ : -1]

	def save(self , last_pos = -1):
		'''把目前尚未保存的所有部分编码为二进制向量保存到文件。如果为空则返回-1，如果不为空返回此次save的位置。
	
		可以选择把自己接到一个给定的位置，或者接到初始化的时候传入的位置。

		'''
		if self.size == 0:
			return -1 # 没有值
		if not self.check_lastpos(last_pos): #没有给定last_pos，就用自己保存的
			last_pos = self.last_pos

		assert self.recent() is not None # dy不可能是None

		# 保存数据，获取保存位置
		start_point = self.dump_data(last_pos , bo = self.active_nonlast() , dy = self.active_last()) 

		self.last_pos   = start_point # 更新自己的last_pos
		list.clear(self) # 清空内存

		return start_point
