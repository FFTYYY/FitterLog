import sys , os
sys.path.append("..")
from fitterlog.data.experi import Project , STL_Project
from fitterlog.data.experi import ExperimentGroup , STL_ExperimentGroup
import pdb

a = Project(name = "fuck")
#a.path = "blabla"
print ("a:" , STL_Project.objects.all())
print (a.path)

print ()

g = ExperimentGroup("test" , a)
print ("g:" , STL_ExperimentGroup.objects.all())
print (g.project.path)
print ()

print ("a.stl_sons[0]:" , a.stl_groups.all())
print ("a.sons[0]:" , a.groups[0])
