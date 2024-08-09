from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('create/', views.create_job, name='create_job'),
    path('<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:job_id>/update-status/', views.update_job_status, name='update_job_status'),
]