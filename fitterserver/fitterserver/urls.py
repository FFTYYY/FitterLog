from django.urls import path
from .responsers import test_response

urlpatterns = [
    path("test", test_response),
]
