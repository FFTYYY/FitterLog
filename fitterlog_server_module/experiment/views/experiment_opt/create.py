from django.shortcuts import render
from django.http import HttpResponse , Http404
from ...models import Experiment
from ..base import get_path

def experiment_create(request):
	return render(request , get_path("experiment/experiment_create") , {})