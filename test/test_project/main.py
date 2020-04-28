import os , sys
sys.path.append("../..")
from fitterlog.interface.experiment import Experiment

E = Experiment(project_name = "hello" , group_name = "sdf")

E.new_variable("loss" , default = "0")
#E.loss.new_track("valid_loss")

E["loss"]["default"].add_value(1)
E["loss"]["default"].add_value(2)

print (E["loss"])

E.finish()