import unittest
from fitterlog.interface import Sentence , Clause
import random

class TestInterface(unittest.TestCase):

	def test_rough(self):

		s = Sentence(predicate_struct = Clause( sons = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("dev loss"  , display = True , default = 0) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
			]),
			Clause("note" , default = "")
		]))

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
		self.assertEqual(s["is_torch"].value 	, False	)

		with self.assertRaises(KeyError):
			s["Acc"]

		s.new_clause("Acc")
		s["Acc"].new_clause("Train Acc" , default = 0)
		s["Acc"].new_clause("Test Acc" )

		self.assertIs(s["Acc"]["Test Acc"].value , None)
		self.assertEqual(s["Acc"]["Train Acc"].value , 0)

	def test_attrs(self):

		s = Sentence(Clause( sons = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0 , fuck = 12) ,
				Clause("dev loss"  , display = True , default = 0) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
			]),
			Clause("note" , default = "")
		]))

		n = 1000
		test_loss_vals = [random.random() for _ in range(n)]

		# --- 更新值 ---
		for x in test_loss_vals:
			s["loss"]["test loss"].update(x)

		s["loss"]["test loss"].save_values()
		self.assertEqual(s["loss"]["test loss"].value , test_loss_vals[-1])
		s.save() #保存实验

		self.assertEqual(s["loss"]["test loss"].attrs["fuck"] , 12)


		# --- 恢复实验 ---
		s_struct = s._clause.linearize()
		the_noun = s.noun
		del s

		c = Sentence(noun = the_noun)

		self.assertEqual(c["loss"]["test loss"].value , test_loss_vals[-1])
		self.assertEqual(c._clause.linearize() , s_struct)
		self.assertEqual(c["loss"]["test loss"].attrs["fuck"] , 12)


if __name__ == "__main__":
	unittest.main()
	