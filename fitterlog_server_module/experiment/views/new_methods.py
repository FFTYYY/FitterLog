from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from ..models import Project , ExperimentGroup , Experiment
from ..models import Variable , VariableTrack , SingleValue
from .base import get_path


def new_experiment(request , group_id):

	if request.POST:

		expe = Experiment(group_id = group_id)
		expe.save()
	return HttpResponseRedirect("/group/%s" % (str(group_id)))
