from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
]