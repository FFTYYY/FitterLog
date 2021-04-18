import unittest
from fitterdb import StaticList
import random

class TestStaticList(unittest.TestCase):

	def test_init(self):

		init_list = random.sample(range(1000) , 20)
		l = StaticList(filename = "test" , init_list = init_list)
		self.assertEqual(l , init_list)

	def test_clear(self):
		l = StaticList(filename = "test")
		self.assertEqual(l.remember_last , None)

	def test_size(self):
		pass

	def test_active_size(self):
		pass

	def test_active_empty(self):
		pass

	def test_last(self):
		pass

	def test_active_nonlast(self): 
		pass

	def test_encode(self):
		pass
if __name__ == "__main__":
	unittest.main()

