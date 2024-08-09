from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/attend/', views.attend_event, name='attend_event'),
    path('<int:event_id>/unattend/', views.unattend_event, name='unattend_event'),
]