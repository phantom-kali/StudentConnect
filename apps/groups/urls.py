from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/join/', views.join_group, name='join_group'),
    path('<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('', views.group_list, name='group_list'),
]