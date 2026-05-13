from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blacklist/', views.blacklist, name='blacklist'),
    path('resources/', views.resources, name='resources'),
    path('trends/', views.trends, name='trends'),

    path('login/', auth_views.LoginView.as_view(template_name='website/login.html') , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('register/', views.register, name='register'),

    path('forum/', views.forum, name='forum'),
    path('forum/create/', views.create_post, name='create_post'),
    path('forum/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('forum/vote/<int:post_id>/<int:vote_value>/', views.vote_post, name='vote_post'),
    path('forum/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('forum/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('forum/comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),

    path('profile/edit-bio/', views.edit_bio, name='edit_bio'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/edit-bio/', views.edit_bio, name='edit_bio'),

    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/important/', views.toggle_important_notification, name='toggle_important_notification'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/clear/', views.clear_notifications, name='clear_notifications'),
]