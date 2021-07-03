import unittest
from fitterdb import StaticList
import random

class TestStaticList(unittest.TestCase):

	def test_save_and_load(self):
		n = 100
		m = 33
		init_list = [random.random() for i in range(n)]
		secd_list = [random.random() for i in range(m)]
		my_list = StaticList("test" , init_list = init_list)

		self.assertEqual(my_list.recent() , init_list[-1])
		self.assertEqual(len(my_list) , n)

		save_point = my_list.save()
		self.assertEqual(my_list.recent() , init_list[-1])
		self.assertEqual(len(my_list) , 0)

		for x in secd_list:
			my_list.append(x)
		self.assertEqual(my_list.recent() , secd_list[-1])
		self.assertEqual(len(my_list) , m)


		anothor_list = StaticList("test" , init_list = [] , last_pos = save_point)
		self.assertEqual(anothor_list.recent() , init_list[-1])
		self.assertEqual(len(anothor_list) , 0)



if __name__ == "__main__":
	unittest.main()

