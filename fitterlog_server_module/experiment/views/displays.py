from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ..models import Project
from .base import get_path
from ..utils.permission import check_permission as check_per , give_permission as give_per
from ..utils.permission import check_passwords
from urllib.parse import urlencode

def index(request):
	context = {
		"projects": Project.objects.all() , 
	}
	return render(request , get_path("index") , context)

def ask_login(request , path = None , info = ""):

	if path is None:
		path = request.get_full_path()
	return render(request , get_path("ask_login") , {
		"path": path , 
		"info": info , 
	})

def login(request):
	if request.POST:
		password = request.POST.get("password")
		path = request.POST.get("path")

		if password in check_passwords():
			return give_per(request , HttpResponseRedirect(path))
		return ask_login(request , path = path ,  info = "不对啊啊啊啊啊啊")

	raise Http404