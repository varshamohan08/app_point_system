from django.urls import path
from .views import *

urlpatterns = [
    path('taskdetails/', TaskAPI.as_view(), name='taskdetails'),
]