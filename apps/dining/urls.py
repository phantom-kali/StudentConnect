from django.urls import path
from . import views

app_name = 'dining'

urlpatterns = [
    path('', views.dining_hall_list, name='dining_hall_list'),
    path('<int:dining_hall_id>/', views.dining_hall_detail, name='dining_hall_detail'),
    path('menu-item/<int:item_id>/update/', views.update_menu_item, name='update_menu_item'),
]