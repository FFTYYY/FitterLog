import os , sys
sys.path.append("../..")
from fitterlog.interface import new_or_load_experiment
from config import arg_proxy
from YTools.universe.timer import Timer
from YTools.universe.beautiful_str import beautiful_str
import random

with Timer("new experiment"):
	E = new_or_load_experiment(project_name = "hahahaha" , group_name = "latest 2")

with Timer("apply args"):
	E.use_argument_proxy( arg_proxy )

with Timer("new variable"):
	E.new_variable("loss" , type = float , default = 0)

E.add_line("hahaha E!")
E.add_line("hello!")
E.add_line("???!")
E.add_line()
E.add_line("start  : {0}".format(E.core.start_time))
E.add_line("end    : {0}".format(E.core.end_time))
E.add_line("running: {0}".format(E.core.running))

k = random.randint(0 , 233)
print (k)
E.new_variable("k" , type = int , default = k)
with Timer("updates"):
	for i in range(k):
		E["loss"].update(0.01 * i)

x = 0
with Timer("gets"):	
	x += E["loss"].value

print (Timer.output_all())
print (E["n"])

E.finish()
E.add_line()
E.add_line("----after finish----")
E.add_line("start  : {0}".format(E.core.start_time))
E.add_line("end    : {0}".format(E.core.end_time))
E.add_line("running: {0}".format(E.core.running))
