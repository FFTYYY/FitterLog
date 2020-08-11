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
E = new_or_load_experiment(project_name = "hahahaha" , group_name = C.group)
E.use_argument_proxy( get_arg_proxy() )

import torch

a = torch.rand(5 , 5).cuda()
b = torch.rand(5 , 5).cuda()
time.sleep(3) #等待60s
c = a.matmul(b)
E.new_variable("C sum")
E["C sum"].update(float(c.sum()))


E.finish()
E.add_line()
E.add_line("----after finish----")
E.add_line("start  : {0}".format(E.core.start_time))
E.add_line("end    : {0}".format(E.core.end_time))
E.add_line("state  : {0}".format(E.core.sql_obj.state))

sys.stderr.write("Im done.\n")