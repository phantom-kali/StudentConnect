from django.urls import path
from . import views

app_name = 'confessions'

urlpatterns = [
    path('', views.confession_list, name='confession_list'),
    path('submit/', views.submit_confession, name='submit_confession'),
    path('moderate/', views.moderate_confessions, name='moderate_confessions'),
]