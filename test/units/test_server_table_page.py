import unittest
from fitterserver.table_page import ask_datas
from fitterlog.interface import Sentence , Clause
import random
from YTools.universe.exceptions import ArgumentError
import random
import json

CLAUSE_ROOT_NAME = "_fitterlog_root"   # 从句的默认名
CLAUSE_CONCAT = "-fitterlog-concat-"   # 在clause的真实名中连接父名和子名的字符串
def make_pred_name(*names):
	return CLAUSE_CONCAT + CLAUSE_ROOT_NAME + CLAUSE_CONCAT + CLAUSE_CONCAT.join(names)

class FakeRequest:
	def __init__(self , data):
		self.body = json.dumps(data)

class TestInterface(unittest.TestCase):
	def setUp(self):
		self.special_val_1 = random.random()
		self.special_val_2 = random.random()
		self.s = Sentence(predicate_struct = Clause( sons = [
			Clause("loss" , haha = 2333 , default = 0 , sons = [
				Clause("test" , display = True , default = 0) ,
				Clause("dev"  , display = True , default = 1) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 12) , 
				Clause("m") , 
			]),
			Clause("acc" , display = False , sons = [
				Clause("dev"  , display = True , default = 3) , 
			]),
			Clause("note" , default = "") , 
			Clause("special" , default = 0.0) , 
		]))
		self.sb = Sentence(predicate_struct = Clause( sons = [
			Clause("loss" , haha = 2333 , default = 0 , sons = [
				Clause("test" , display = True , default = 0) ,
				Clause("dev"  , display = True , default = 1) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 12) , 
				Clause("m") , 
			]),
			Clause("acc" , display = False , sons = [
				Clause("test"  , display = True , default = 3) , 
			]),
			Clause("note" , default = "") , 
			Clause("special" , default = 0.0) , 
		]))

		self.s["special"].update(self.special_val_1)
		self.sb["special"].update(self.special_val_2)
		self.s.save()
		self.sb.save()

	def tearDown(self):
		self.s = None
		self.sb = None
		self.special_val_1 = None
		self.special_val_2 = None

	def test_merged_title(self):

		filter_info = {
			make_pred_name("loss" , "test") : {
				"type" : "exists" , 
			},
		}
		
		start 		= 0 # 从第几个名词开始搜索
		trans_size 	= 1000 # 最多获得几个结果
		searc_size 	= 1000 # 最多搜索多少个名词


		ret = ask_datas(FakeRequest({
			"filter": filter_info , 
			"start": start , 
			"trans_size": trans_size , 
			"searc_size": searc_size , 
		}))

		expect_title = ["root" , [
			 ["loss" , [ ["test" , []] , ["dev" , []] ] ] , 
			 ["hyper parameter" , [ ["n" , []] , ["m" , []] ] ] , 
			 ["acc" , [ ["dev" , []] , ["test" , []] ] ] , 
			 ["note" , []] , 
			 ["special" , []]
		 ]]

		self.assertEqual(ret["title_list"] , expect_title)
	def test_single_title(self):

		filter_info = {
			make_pred_name("special") : {
				"type" : "interval" , 
				"cond" : [self.special_val_1 , self.special_val_1]
			},
		}
		
		start 		= 0 # 从第几个名词开始搜索
		trans_size 	= 1000 # 最多获得几个结果
		searc_size 	= 1000 # 最多搜索多少个名词


		ret = ask_datas(FakeRequest({
			"filter": filter_info , 
			"start": start , 
			"trans_size": trans_size , 
			"searc_size": searc_size , 
		}))

		expect_title = ["root" , [
			 ["loss" , [ ["test" , []] , ["dev" , []] ] ] , 
			 ["hyper parameter" , [ ["n" , []] , ["m" , []] ] ] , 
			 ["acc" , [ ["dev" , []] ] ] , 
			 ["note" , []] , 
			 ["special" , []]
		 ]]
		self.assertEqual(ret["title_list"] , expect_title)

		expect_data = {
			make_pred_name("loss" , "test") : 0 , 
			make_pred_name("loss" , "dev") : 1 , 
			make_pred_name("loss") : 0 , 
			make_pred_name("hyper parameter" , "n") : 12 , 
			make_pred_name("hyper parameter" , "m") : None , 
			make_pred_name("hyper parameter") : None , 
			make_pred_name("acc" , "dev") : 3 , 
			make_pred_name("acc") : None , 
			make_pred_name("note") : "" , 
			make_pred_name("special") : self.special_val_1, 
		}
		self.assertEqual(len(ret["data_dict"]) , 1)

		self.assertEqual(ret["data_dict"][self.s.noun.id] , expect_data)



if __name__ == "__main__":
	unittest.main()
	