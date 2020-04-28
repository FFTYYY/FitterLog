import os , sys
sys.path.append("../..")
from fitterlog.interface import Experiment
from config import arg_proxy

E = Experiment(project_name = "hello" , group_name = "sdyyyf")
E.use_argument_proxy( arg_proxy )

E.new_variable("loss" , type = int , default = 0)
#E.loss.new_track("valid_loss")

E["loss"].update(1)
E["loss"].update("23")

print (E["loss"].value + 22)
print (E["n"])

E.finish()