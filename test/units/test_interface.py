import unittest
from fitterlog.interface import Sentence , Clause
import random
from YTools.universe.exceptions import ArgumentError

class TestInterface(unittest.TestCase):

	def setUp(self):
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
			Clause("note" , default = "")
		]))

		self.sb = Sentence(predicate_struct = Clause( sons = [
			Clause("loss" , haha = 2333 , default = 0 , sons = [
				Clause("test" , display = True , default = 0) ,
				Clause("dev"  , display = True , default = 4) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 12) , 
			]),
			Clause("note" , default = "")
		]))

	def tearDown(self):
		self.s = None
		self.sb = None

	def test_sentence(self):

		s = self.s
		sb = self.sb

		self.assertEqual(s["loss"].attrs["haha"] , 2333)
		self.assertEqual(s["test"].attrs["display"] , True)
		self.assertEqual(s["n"].attrs["default"] , 12)
		with self.assertRaises(ArgumentError):
				print (s["dev"])
		self.assertEqual(sb["dev"].attrs["default"] , 4)


		s["test"].update(3)
		
		self.assertEqual(s["test"].value , 3)		
		self.assertEqual(s["loss"]["dev"].value , 1)
		self.assertEqual(s["acc"]["dev"].value  , 3)
		self.assertIs(s["loss"]["dev"]._value.value  , None)
		self.assertEqual(s["note"].value , "")
		self.assertIs(s["m"].value , None)

		with self.assertRaises(ArgumentError):
			s["num_layers"]
		with self.assertRaises(ArgumentError):
			s["num_heads"]
		with self.assertRaises(ArgumentError):
			s["d"]
		with self.assertRaises(ArgumentError):
			s["is_torch"]

		cmd_hyper = {
			"num_layers" : 3 ,
			"num_heads" : 16 ,
			"d" : 128 ,  
			"is_torch": False , 
		}

		s.new_clauses_from_dict(cmd_hyper)

		self.assertEqual(s["num_layers"].value 	, 3 	)
		self.assertEqual(s["num_heads"].value  	, 16 	)
		self.assertEqual(s["d"].value 			, 128 	)
		self.assertEqual(s["is_torch"].value 	, False	)

		with self.assertRaises(ArgumentError):
			s["Acc"]

		self.assertEqual(s["test"].value , 3)		

		s.new_clause("Acc")
		s["Acc"].new_clause("train" , default = 0)
		s["Acc"].new_clause("test" )

		self.assertIs(s["Acc"]["test"].value , None)
		self.assertEqual(s["Acc"]["train"].value , 0)
		with self.assertRaises(ArgumentError):
				print (s["test"])

	def test_syntax(self):

		s = self.s
		sb = self.sb

		cc = "-fitterlog-concat-"

		self.assertEqual(s["loss"]._pred.name, "{0}_fitterlog_root{0}loss".format(cc))
		self.assertEqual(s["test"]._pred.name, "{0}_fitterlog_root{0}loss{0}test".format(cc))
		self.assertEqual(s["test"]._clause.name, "test")
		self.assertEqual(s["test"]._clause.real_name, "{0}_fitterlog_root{0}loss{0}test".format(cc))

		self.assertEqual(s["n"]._pred.id , sb["n"]._pred.id)


	def test_save_and_load(self):
		s = Sentence(predicate_struct = Clause( sons = [
			Clause("loss" , haha = 2333 , default = 0 , sons = [
				Clause("test" , display = True , default = 0 , fucke = "me") ,
				Clause("dev"  , display = True , default = 1) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 12) , 
				Clause("m") , 
			]),
			Clause("acc" , display = False , sons = [
				Clause("dev"  , display = True , default = 1) , 
			]),
			Clause("note" , default = "")
		]))

		s["test"].update(3)
		s["test"].update(2)
		s["test"].update(1)
		s["m"].update(2333)

		s.save()

		the_noun = s.noun

		sb = Sentence(noun = the_noun)
		self.assertEqual(sb["test"].value , s["test"].value)
		self.assertEqual(sb["test"].value , 1)
		self.assertEqual(sb["test"].attrs["display"] , True)
		self.assertEqual(sb["test"].attrs["fucke"] , "me")
		self.assertEqual(sb["loss"].attrs["haha"] , s["loss"].attrs["haha"])
		self.assertEqual(sb["loss"].attrs["haha"] , 2333)


if __name__ == "__main__":
	unittest.main()
	