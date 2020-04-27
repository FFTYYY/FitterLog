import sys , os
sys.path.append("..")
from fitterlog.data.experi import Project , SQL_Project
from fitterlog.data.experi import ExperimentGroup , SQL_ExperimentGroup
import pdb

a = Project(name = "fuck")
#a.path = "blabla"
print ("a:" , SQL_Project.objects.all())
print ("a.path", a.path)

print ()

g = ExperimentGroup("test" , a)
print ("g:" , SQL_ExperimentGroup.objects.all())
print ("g.project.path", g.project.path)
print ()

print ("a.stl_sons[0]:" , a.sql_groups.all())
print ("a.sons[0]:" , a.groups[0])
