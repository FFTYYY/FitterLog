'''out of date'''

import unittest
from fitterlog.interface import Sentence , Clause
from fitterlog.interface.restore import load_syntax
import random

class TestSyntax(unittest.TestCase):

	def test_syntax_save_load(self):

		s = Sentence(predicate_struct = Clause(sons = [
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

		s_lin = s._clause.linearize()

		self.assertEqual (
			s._clause.linearize() , 
			['_fitterlog_root', [['loss', ['test loss', 'dev loss']], ['hyper parameter', ['n', 'm']], 'note']]
		)

		s.save_syntax()
		thd_noun = s.noun
		del s
		
		e = load_syntax(thd_noun)
		self.assertEqual(e.linearize() , s_lin)

	def test_syntax_save_load_2(self):

		s = Sentence(predicate_struct = Clause(sons = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("train loss" , display = True , default = 0) ,
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") , 
				Clause("fuck!")
			]),
			Clause("note" , default = "")
		]))

		s_lin = s._clause.linearize()

		s.save_syntax()
		thd_noun = s.noun
		del s
		
		e = load_syntax(thd_noun)
		self.assertEqual(e.linearize() , s_lin)

		print (thd_noun)

	def test_syntax_save_load_3(self):

		s = Sentence(predicate_struct = Clause(sons = [
			Clause("loss" , default = 0 , sons = [
				Clause("test loss" , display = True , default = 0) ,
				Clause("train loss" , display = True , default = 0) ,
			]) , 
			Clause("hyper parameter" , display = False , sons = [
				Clause("n" , default = 0) , 
				Clause("m") ,
			]),
			Clause("note" , default = "") , 
			Clause("no disp" , display = False , sons = [
				Clause("yes disp" , display = True , sons = [
					Clause("should not see" , display = True) , 
					Clause("should not see2" , display = True) , 
				]),
				Clause("no disp 2" , display = False , sons = [])
			]) , 
			Clause("no disp3" , display = False , sons = [
				Clause("yes disp2" , display = False , sons = [
					Clause("now should see" , display = True) , 
					Clause("now should see2" , display = True) , 
				]),
				Clause("no disp 4" , display = False , sons = [])
			])

		]))

		s_lin = s._clause.linearize()

		s.save_syntax()
		thd_noun = s.noun
		del s
		
		e = load_syntax(thd_noun)
		self.assertEqual(e.linearize() , s_lin)

		print (thd_noun)






if __name__ == "__main__":
	unittest.main()
	