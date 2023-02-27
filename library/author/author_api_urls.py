from django.urls import path
from rest_framework import routers
from . import views


urlpatterns = [
    path('', views.author_list),
    path('/<int:pk>', views.author_detail)
]