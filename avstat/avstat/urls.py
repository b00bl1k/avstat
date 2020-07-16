from django.urls import path
from rest_framework import routers
from main import views


urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetails.as_view(), name='user-details'),
    path('users/<int:pk>/stat/', views.UserStat.as_view(), name='user-stat'),
]
