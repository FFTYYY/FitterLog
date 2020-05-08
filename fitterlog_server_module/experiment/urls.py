from django.urls import path
from . import views

urlpatterns = [
	path("" , views.index),
	path("new_project" , views.new_project),

	path("project/<int:project_id>" , views.project),
	path("project/<int:project_id>/new_group" , views.new_group),

	path("group/<int:group_id>" , views.group),
	path("group/<int:group_id>/new_experiment" , views.new_experiment),
	path("group/<int:group_id>/save_config" , views.save_config),

	path("experiment/<int:experiment_id>" , views.experiment),
	path("experiment/<int:experiment_id>/new_variable" , views.new_variable),
	path("experiment/<int:experiment_id>/logs" , views.experiment_log),

	path("variable/<str:variable_id>" , views.variable),

	path("track/<str:track_id>" , views.track),

]