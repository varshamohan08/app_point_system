from django.urls import path
from .views import *

urlpatterns = [
    path('appdetails/', AppAPI.as_view(), name='appdetails'),
    # path('appdetails/', AppAPI.as_view(), name='appdetails'),
    path('category', AppCategoriesAPI.as_view(), name='category'),
    # path('sub_category', AppSubCategoriesAPI.as_view(), name='sub_category'),
]