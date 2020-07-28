import os , sys
sys.path.append("../..")
from fitterlog.interface import new_or_load_experiment
from config import get_arg_proxy
from YTools.universe.timer import Timer
from YTools.universe.beautiful_str import beautiful_str
import random
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

C = get_arg_proxy().assign_from_cmd()

with Timer("new experiment"):
	E = new_or_load_experiment(project_name = "hahahaha" , group_name = C.group)

with Timer("apply args"):
	E.use_argument_proxy( get_arg_proxy() )

with Timer("new variable"):
	def avg_merge(*x):
		x = [d[0] for d in x]
		return sum(x) / len(x)
	E.new_variable("loss" , type = float , default = 0 , merge_func = avg_merge)
	E.new_variable("metric" , type = float , default = 0 , merge_func = avg_merge)

with Timer("paint"):
	with E.new_figure("test figure"):
		x = [1, 2, 3, 4]
		y = [1.2, 2.5, 4.5, 7.3]
		plt.plot(x, y) 
	with E.new_figure("test figure 2"):
		x = [1, 2, 3, 4]
		y = [5.2, 2.5, 4.5, 7.3]
		plt.plot(x, y) 
	with E.new_figure("test figure 3"):
		import numpy as np
		plt.figure(figsize = (10 , 6) , dpi = 100)

		t1 = np.arange(0, 5, 0.1)
		t2 = np.arange(0, 5, 0.02)

		plt.subplot(221)
		plt.plot(t1, (t1 * 0.25), 'bo', t2, (t2 + 0.1), 'r--')

		plt.subplot(333)
		plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')

		plt.subplot(212)
		plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
		plt.plot(x, y) 

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


for i in range(k):
	with Timer("updates"):
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

for i in tqdm(range(10) , ncols = 100):
	E["metric"]["test acc"].update((i*random.random()) * 100 , 1 + i * 20)


# time.sleep(20)
# sys.stderr.write("I'm awake!!!")

E["loss"].update("23.4 ( 2.0 )")

print (Timer.output_all())
print (E["n"])

E.finish()
E.add_line()
E.add_line("----after finish----")
E.add_line("start  : {0}".format(E.core.start_time))
E.add_line("end    : {0}".format(E.core.end_time))
E.add_line("state  : {0}".format(E.core.sql_obj.state))

sys.stderr.write("Im done.\n")