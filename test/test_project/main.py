import os , sys
sys.path.append("../..")
from fitterlog.interface import new_or_load_experiment
from config import arg_proxy
from YTools.universe.timer import Timer
from YTools.universe.beautiful_str import beautiful_str
import random
from tqdm import tqdm

with Timer("new experiment"):
	E = new_or_load_experiment(project_name = "hahahaha")

with Timer("apply args"):
	E.use_argument_proxy( arg_proxy )

with Timer("new variable"):
	def avg_merge(*x):
		x = [d[0] for d in x]
		return sum(x) / len(x)
	E.new_variable("loss" , type = float , default = 0 , merge_func = avg_merge)
	E.new_variable("metric" , type = float , default = 0 , merge_func = avg_merge)

E.add_line("hahaha E!")
E.add_line("hello!")
E.add_line("???!")
E.add_line()
E.add_line("start  : {0}".format(E.core.start_time))
E.add_line("end    : {0}".format(E.core.end_time))
E.add_line("state  : {0}".format(E.core.sql_obj.state))

k = random.randint(0 , 23)
print (k)
E.new_variable("k" , type = int , default = k)
E.new_variable("23333" , type = int , default = 2333)


with Timer("updates"):
	for i in range(k):
		E["loss"]["test loss"].update(0.01 * i)

E["loss"]["train loss"].update(0)
E["loss"]["train loss"].update(0.1)
E["loss"]["train loss"].update(0.4)
E["loss"]["train loss"].update(0.5)


for i in range(3):
	E["loss"]["草"].update(3 * 0)
	E["loss"]["草"].update(3 * 0.1)
	E["loss"]["草"].update(3 * 0.4)
	E["loss"]["草"].update(3 * 0.5)

for i in tqdm(range(1000) , ncols = 100):
	E["metric"]["test acc"].update((i*random.random()) * 100 , 1 + i * 20)

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
E.add_line("state  : {0}".format(E.core.sql_obj.state))
