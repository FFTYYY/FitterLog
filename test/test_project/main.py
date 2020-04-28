import os , sys
sys.path.append("../..")
from fitterlog.interface import Experiment
from config import arg_proxy

E = Experiment(project_name = "hello" , group_name = "sdf")
E.use_argument_proxy( arg_proxy )

E.new_variable("loss" , default = "0")
#E.loss.new_track("valid_loss")

E["loss"].update(1)
E["loss"].update(2)

print (E["loss"])
print (E["n"])

E.finish()