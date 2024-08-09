from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('create/', views.create_item, name='create_item'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('', views.item_list, name='item_list'),
]