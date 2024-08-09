from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.create_story, name='create_story'),
    path('', views.view_stories, name='view_stories'),
    path('<int:story_id>/', views.story_detail, name='story_detail'),
    path('user_stories/<str:username>/', views.user_stories, name='user_stories'),
    path('auto-load/', views.auto_load_stories, name='auto_load_stories'),
    path('get-all-stories/', views.get_all_stories, name='get_all_stories'),

]