from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('referral-program/', views.referral_program, name='referral_program'),

    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
    path('profile/<int:user_id>/following/', views.following_list, name='following_list'),
    path('profile/<int:user_id>/posts/', views.posts_list, name='posts_list'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
]