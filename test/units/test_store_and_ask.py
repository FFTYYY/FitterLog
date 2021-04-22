import unittest
from fitterlog.core.morphology import Predicate
from fitterlog.interface import Sentence , Clause
from fitterlog.interface.restore import load_last , load_all
import random
import pdb

class TestSave(unittest.TestCase):

	def test_save_and_load_value(self):
		predicate_struce = Clause(sons = [
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

		s = Sentence(predicate_struct = predicate_struce)
		n = 1000
		test_loss_vals = [random.random() for _ in range(n)]

		for x in test_loss_vals:
			s["loss"]["test loss"].update(x)

		s["loss"]["test loss"].save_values()
		self.assertEqual(s["loss"]["test loss"].value , test_loss_vals[-1])

		the_noun = s.noun

		self.assertEqual( load_last(the_noun , Predicate("test loss") , False) , test_loss_vals[-1])
		self.assertEqual( load_all(the_noun , Predicate("test loss") , False)[-1000:] , test_loss_vals)

	def test_restore_experiment(self):

		# --- 新建实验 ---

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
		
		n = 1000
		test_loss_vals = [random.random() for _ in range(n)]

		# --- 更新值 ---
		for x in test_loss_vals:
			s["loss"]["test loss"].update(x)

		s["loss"]["test loss"].save_values()
		self.assertEqual(s["loss"]["test loss"].value , test_loss_vals[-1])
		s.save() #保存实验

		# --- 恢复实验 ---
		s_struct = s._clause.linearize()
		the_noun = s.noun
		print (s.noun)
		del s

		c = Sentence(noun = the_noun)

		self.assertEqual(c["loss"]["test loss"].value , test_loss_vals[-1])
		self.assertEqual(c._clause.linearize() , s_struct)

if __name__ == "__main__":
	unittest.main()
	