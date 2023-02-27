from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.order_list),
    path('/<int:pk>', views.order_detail)
]