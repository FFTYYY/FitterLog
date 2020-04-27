from django.urls import path
from . import views

urlpatterns = [
	path("" , views.index),
	path("new_project" , views.new_project),

	path("project/<int:project_id>" , views.project),
	path("<int:project_id>/new_group" , views.new_group),

	path("group/<str:group_id>" , views.group),
	path("<int:group_id>/new_experiment" , views.new_experiment),

	path("experiment/<str:experiment_id>" , views.experiment),
]