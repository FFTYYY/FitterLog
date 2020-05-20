from django.shortcuts import render
from django.http import HttpResponse , Http404
from ...models import Experiment
from ..base import get_path
from .copy_exp import *

def experiment(request , experiment_id):

	experiment = Experiment.objects.get(id = experiment_id)

	context = {
		"experiment": experiment , 
		"variables": experiment.variables.all() , 
	}
	return render(request , get_path("experiment/experiment") , context)



def experiment_log(request , experiment_id):

	experiment = Experiment.objects.get(id = experiment_id)

	context = {
		"experiment": experiment , 
		"logs": experiment.logs , 
	}
	return render(request , get_path("experiment/logs") , context)

def experiment_figure(request , experiment_id):
	experiment = Experiment.objects.get(id = experiment_id)

	figs = [ [fig.name , fig.html] for fig in experiment.figures.all()]
	context = {
		"experiment": experiment , 
		"figs": figs ,
		"first_name" : figs[0][0] if len(figs) > 0 else "" ,  
	}
	return render(request , get_path("experiment/figures") , context)
