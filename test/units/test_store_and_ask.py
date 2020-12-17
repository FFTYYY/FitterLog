import unittest
from fitterlog.core.morphology import Predicate
from fitterlog.interface import Sentence , Clause
from fitterlog.interface.restore import load_last , load_all
import random

class TestSave(unittest.TestCase):

	def test_save_and_load(self):

		predicate_struce = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("dev loss"  , display = True , default = 0) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
			]),
			Clause("note" , default = "")
		]

		s = Sentence(predicate_struct = predicate_struce)
		n = 1000
		test_loss_vals = [random.random() for _ in range(n)]

		for x in test_loss_vals:
			s["loss"]["test loss"].update(x)

		s["loss"]["test loss"].flush()
		self.assertEqual(s["loss"]["test loss"].value , test_loss_vals[-1])


		the_noun = s.noun

		self.assertEqual( load_last(the_noun , Predicate("test loss") , False) , test_loss_vals[-1])
		self.assertEqual( load_all(the_noun , Predicate("test loss") , False) , test_loss_vals)

	def test_restore_experiment(self):

		# --- 新建实验 ---
		predicate_struce = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("dev loss"  , display = True , default = 0) , 
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
			]),
			Clause("note" , default = "")
		]

		s = Sentence(predicate_struct = predicate_struce)
		n = 1000
		test_loss_vals = [random.random() for _ in range(n)]

		# --- 更新值 ---
		for x in test_loss_vals:
			s["loss"]["test loss"].update(x)

		s["loss"]["test loss"].flush()
		self.assertEqual(s["loss"]["test loss"].value , test_loss_vals[-1])
		s.flush_all() #保存实验

		# --- 恢复实验 ---
		the_noun = s.noun

		c = Sentence(noun = the_noun , predicate_struct = predicate_struce)

if __name__ == "__main__":
	unittest.main()
	