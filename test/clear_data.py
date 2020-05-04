import sys , os
sys.path.append("..")
from fitterlog.sql_proxy.experi import SQL_Project , SQL_Experiment , SQL_ExperimentGroup
from fitterlog.sql_proxy.variable import SQL_Variable , SQL_SingleValue , SQL_VariableTrack
import pdb

def clear_class(clas):
	x =  list(clas.objects.all())
	for y in x:
		y.delete()

clear_class(SQL_Project)
clear_class(SQL_Experiment)
clear_class(SQL_ExperimentGroup)
clear_class(SQL_Variable)
clear_class(SQL_SingleValue)
clear_class(SQL_VariableTrack)

print ("done")