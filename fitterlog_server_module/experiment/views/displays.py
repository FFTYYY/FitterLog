from django.shortcuts import render
from django.http import HttpResponse , Http404
from ..models import Project
from .base import get_path

def index(request):
	context = {
		"projects": Project.objects.all() , 
	}
	return render(request , get_path("index") , context)