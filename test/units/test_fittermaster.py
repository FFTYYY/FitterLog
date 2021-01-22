import unittest
import random
from fittermaster.mastermain import Master
from fitterlog.interface import Sentence , Clause
import time
from YTools.system.locker import Locker

def new_sentence():
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

	for i in range(1000):
		s["loss"].update(random.random())

	return s

class TestFittermaster(unittest.TestCase):

	def test_master(self):
		# self.assertEqual = print
		locker = Locker()
		locker.clear()

		master = Master(resources = [ ["gpu" , list(range(8))] ] )

		s1 = new_sentence()
		s2 = new_sentence()

		s1.require_resource("gpu" , [1])
		s2.require_resource("gpu" , [1 , 2])

		time.sleep(1)

		self.assertEqual (master.ask_clients() , [s1.noun.id , s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 1) , [s1.noun.id , s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 2) , [s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 3) , [])
		self.assertEqual (master.ask_resources("gpu" , 0) , [])

		s1.finish()
		time.sleep(1)
		print (locker.ask_prefix(""))
		xs = locker.ask_prefix("fitterlog/sentence/live")
		for x in xs:
			print (x + " = " + str(locker.get(x)))
		self.assertEqual (master.ask_clients() , [s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 1) , [s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 2) , [s2.noun.id])
		self.assertEqual (master.ask_resources("gpu" , 3) , [])
		self.assertEqual (master.ask_resources("gpu" , 0) , [])

		s2.finish()
		time.sleep(1)

		self.assertEqual (len(locker.ask_prefix("")) , 0)




if __name__ == "__main__":
	unittest.main()
