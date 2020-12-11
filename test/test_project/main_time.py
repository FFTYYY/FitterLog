import os , sys
sys.path.append("../..")
from fitterlog.interface import new_or_load_experiment
from YTools.universe.timer import Timer
from YTools.universe.beautiful_str import beautiful_str
import random
import time
import threading
import pdb

E = new_or_load_experiment(project_name = "test")

print ("std")

E.new_variable("loss" , default = 0 , type = float)

class UpdateThread (threading.Thread):
	def __init__(self , name):
		threading.Thread.__init__(self)

		self.name = name
		self.cnt = 0
	def run(self):
		for i in range(update_step):
			with Timer("update"):
				E["loss"][self.name].update(random.random())
			with Timer("add line"):
				E.write_log(self.name + " " + str(self.cnt))


time_1 = time.time()
update_step = 100
num_update  = 24

update_threads = []

for i in range(num_update):
	upd = UpdateThread(str(i))
	upd.start()
	update_threads.append(upd)

for x in update_threads:
	x.join()
	
print (Timer.output_all())
print ("Time for return " , time.time() - time_1)

E.finish()

print ("Time for quit" , time.time() - time_1)