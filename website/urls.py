from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apps/', views.apps, name='apps'),
    path('blacklist/', views.blacklist, name='blacklist'),
    path('resources/', views.resources, name='resources'),
    path('trends/',views.trends, name='trends')
]
