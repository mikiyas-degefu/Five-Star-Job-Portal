from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='company-admin-dashboard'),

    
    path('job-posting/', views.job_posting, name='company-admin-job-posting'),
     path('job-posting/<str:id>', views.job_detail, name='company-admin-job-posting-detail'),
    path('job-posting-delete/', views.job_delete, name='company-admin-job-posting-delete'),
]