import os , sys
import os.path as P
import django


target_path = P.join( P.dirname(__file__) , "../fitterlog_server_module/")
flag = target_path in sys.path

if not flag:
	sys.path.append( target_path )

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitterlog_server.settings')
django.setup()

from experiment.models import *

if not flag:
	sys.path.remove( target_path )

