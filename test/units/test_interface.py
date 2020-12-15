import unittest
from fitterlog.interface import Sentence , Clause
import random

class TestInterface(unittest.TestCase):

	def test_rough(self):

		s = Sentence(predicate_struct = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("dev loss"  , display = True , default = 0) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
			]),
			Clause("note" , default = "")
		])

		s["loss"]["test loss"].update(3)
		
		self.assertEqual(s["loss"]["test loss"].value , 3)		
		self.assertEqual(s["loss"]["dev loss"].value  , 0)
		self.assertEqual(s["note"].value , "")

		with self.assertRaises(KeyError):
			s["num_layers"]
		with self.assertRaises(KeyError):
			s["num_heads"]
		with self.assertRaises(KeyError):
			s["d"]
		with self.assertRaises(KeyError):
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
		self.assertEqual(s["is_torch"].value 		, False	)

		with self.assertRaises(KeyError):
			s["Acc"]

		s.new_clause("Acc")
		s["Acc"].new_clause("Train Acc" , default = 0)
		s["Acc"].new_clause("Test Acc" )

		self.assertIs(s["Acc"]["Test Acc"].value , None)
		self.assertEqual(s["Acc"]["Train Acc"].value , 0)


if __name__ == "__main__":
	unittest.main()
	