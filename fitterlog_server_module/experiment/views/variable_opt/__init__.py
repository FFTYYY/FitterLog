from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ...models import Project , ExperimentGroup , Experiment
from ...models import Variable , VariableTrack , SingleValue
from ..base import get_path
from .utils import *

def variable(request , variable_id):

	variable = Variable.objects.get(id = variable_id)

	tracks_and_values = get_tracks(variable.tracks.all())

	context = {
		"variable": variable ,
		"tracks_and_values": tracks_and_values ,  
	}
	return render(request , get_path("variable/variable") , context)



def new_variable(request , experiment_id):

	if request.POST:
		name = request.POST.get("name")
		vari = Variable(name = name , expe_id = experiment_id)
		vari.save()
	return HttpResponseRedirect("/experiment/%s" % (str(experiment_id)))


def track(request , track_id):

	track = VariableTrack.objects.get(id = track_id)

	context = {
		"track": track , 
		"values": track.values.all() , 
	}
	return render(request , get_path("track") , context)
