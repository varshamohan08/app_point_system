from django.urls import path
from .views import *

urlpatterns = [
    path('login/', userLogin.as_view(), name='login'),
    path('logout/', userLogout.as_view(), name='logout'),
    path('signup/', userSignUp.as_view(), name='signup'),
    path('user_api/', userApi.as_view(), name='user_api'),
]