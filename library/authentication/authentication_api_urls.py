from django.urls import path
from rest_framework import routers
from . import views


urlpatterns = [
    path('', views.CustomUserListView.as_view()),
    path('/<int:pk>', views.CustomUserDetailView.as_view()),
    path('/<user_id>/order', views.UserOrderListView.as_view()),
    path('/<user_id>/order/<int:pk>', views.UserOrderDetailView.as_view())
]
