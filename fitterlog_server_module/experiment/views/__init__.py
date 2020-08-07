from .displays import *
from .group_opt import *
from .variable_opt import *
from .project_opt import *
from .experiment_opt import *

def test_data(request):
	from django.http import HttpResponse , Http404 , HttpResponseRedirect

	return HttpResponse("""{
		"code":0,
		"msg":"",
		"count":100,
		"data":[
			{"asd" : "233" , "SS" : "tr"} , 
			{"asd" : "23" , "SS" : "4"} 
		]
	}""")