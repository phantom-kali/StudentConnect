from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<str:username>/', views.start_conversation, name='start_conversation'),
]