from django.urls import path
from . import views

urlpatterns = [
	path("" , views.index),
	path("new_project" , views.new_project),

	path("project/<int:project_id>" , views.project),
	path("project/<int:project_id>/new_group" , views.new_group),

	path("group/<int:group_id>" , views.group),
	path("group/<int:group_id>/new_experiment" , views.new_experiment),

	path("experiment/<int:experiment_id>" , views.experiment),
	path("experiment/<int:experiment_id>/new_variable" , views.new_variable),

	path("variable/<str:variable_id>" , views.variable),
	path("variable/<str:variable_id>/new_track" , views.new_track),

	path("track/<str:track_id>" , views.track),
	path("track/<str:track_id>/new_value" , views.new_value),

]