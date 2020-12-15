from YTools.network.protocol import Protocol
from YTools.network.protocol import int2bytes , bytes2int , str2bytes , bytes2str
from YTools.system.fakepath import new_fakefolder
from YTools.system.locker import Locker
from YTools.system.onexit import add_quit_methods
from YTools.system.filewrite import write_file , read_file , get_filesize
from functools import partial
import pickle
import os

class StaticList_FileManager:
	'''这个类管理静态链表的文件'''

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
	LOCKER_FOLDER = "fitterlog/static_list/"

	def __init__(self , name):

		# 获取文件名
		self.save_file_name = os.path.abspath(new_fakefolder(self.FOLDER_NAME))
		self.save_file_name = os.path.join(self.save_file_name , name)

		open(self.save_file_name , "ab+").close() 		#确保文件存在
		self.file = open(self.save_file_name , "rb+") 	#以读写模式打开，这个模式下可以随意写，无视文件大小
		add_quit_methods(self.close) 					#保证文件关闭

		self.locker = Locker()
		self.locker_name = self.LOCKER_FOLDER + name + "/" #在lokcer中使用的键的前缀
		self.key_filesize = self.locker_name + "filesize/"

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
		dy = self.proto.body["dy"][3](dy_data) # dy的解码函数

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

class StaticList(list , StaticList_FileManager):
	'''这个类结合list的特性'''

	def __init__(self , name , init_list = [] , last_pos = None):
		StaticList_FileManager.__init__(self , name)
		list.__init__(self , init_list)

		self.remember_last = None #清空后，依然记得之前的最后一个元素
		self.saved_last = -1 #上一块保存的位置
		self.saved_size = 0  #已经保存了前多少个

		if last_pos is not None:
			self.saved_last = last_pos

	def clear(self):
		self.remember_last = self.last() #记住之前的最后一个元素
		list.clear(self)
		self.saved_size = 0

	@property
	def size(self):
		return len(self)

	@property
	def active_size(self):
		return self.size - self.saved_size
	
	def active_empty(self):
		return self.active_size == 0

	def last(self):
		if len(self) > 0:
			return self[-1]
		return self.remember_last #已经clear过，返回clear之前的最后一个元素

	def active_nonlast(self): 
		'''尚未保存的，且不是最后的'''
		return self[self.saved_size : -1]

	def encode(self , last_pos = None):
		'''把目前尚未保存的所有部分编码为二进制向量。如果为空则返回None'''
		if self.active_size == 0:
			return None
		if last_pos is None:
			last_pos = self.saved_last
		return self.proto.encode(last_pos = last_pos , bo = self.active_nonlast() , dy = self.last())

	def save(self , last_pos = None):
		'''
			把目前尚未保存的所有部分编码为二进制向量保存到文件。
			如果为空则返回-1，如果不为空返回此次save的位置
		'''

		 # 将内存中保存的文件长度更新成自己看到的文件长度，具体是不是这个长度并不重要，locker会保证一致性
		self.locker.set_if(self.key_filesize , None , get_filesize(self.file))

		# 编码数据
		data = self.encode(last_pos)
		if data is None:
			return -1

		# 向locker请求长度
		end_point = self.locker.plus(self.key_filesize , len(data)) #仅在这一步执行同步
		start_point = end_point - len(data) 						#算出开头位置
		write_file(self.file , start_point , data)

		self.saved_last = start_point
		self.saved_size = len(self)

		return start_point

if __name__ == "__main__":
	static = StaticList("test.dat" , init_list = [1,2,3])
	print (static)
	static.clear()
	print (static)
	static.append(3)
	print (static.last())
	# static += [1,2,3]
	# print (static.save())
	# static += [233,4,"34"]
	# print (static.save())
	# print (static)
	#print (static.save())
	print (static.read_block(246))
	print (static.read_block(287))
	print (static.read_all(246))
	print (static.read_all(287))
