from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apps/', views.apps, name='apps'),
    path('blacklist/', views.blacklist, name='blacklist'),
    path('resources/', views.resources, name='resources'),
    path('trends/', views.trends, name='trends'),

    path('login/', auth_views.LoginView.as_view(template_name='website/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('register/', views.register, name='register'),

    path('forum/', views.forum, name='forum'),
    path('forum/create/', views.create_post, name='create_post'),
    path('forum/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]

