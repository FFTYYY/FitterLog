import sys , os
sys.path.append("..")
from fitterlog.data.experi import Project
from fitterlog.importer import Project as P
import pdb

a = Project(name = "fuck")
#a.path = "blabla"
print (P.objects.all())
print (a.path)
