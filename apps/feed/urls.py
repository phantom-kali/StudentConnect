from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.feed, name='index'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('recommended/', views.recommended_posts, name='recommended_posts'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/report/', views.report_post, name='report_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('create/', views.create_post, name='create_post'),
    path('following/', views.following_feed, name='following'),
    path('trending/', views.trending_feed, name='trending'),
]