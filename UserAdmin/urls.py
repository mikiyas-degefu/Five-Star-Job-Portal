from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin-dashboard'),
    path('company/', views.company, name='user-admin-company'),
    path('company/<str:id>/', views.company_detail, name='user-admin-company-detail'),
    path('company-delete/<str:id>/', views.company_delete, name='user-admin-company-delete'),

    path('sector/', views.job_sector, name='user-admin-sector'),
    path('update-sector/', views.update_sector, name='user-admin-update-sector'),
    path('sector-delete/<str:id>/', views.sector_delete, name='user-admin-sector-delete'),


    path('skills/', views.skills, name='user-admin-skills'),
    path('update-skill/', views.update_skill, name='user-admin-update-skills'),
    path('skill-delete/<str:id>/', views.skill_delete, name='user-admin-skill-delete'),

    path('job_posting/', views.job_posting, name='user-admin-job-posting'),
    path('update-job_posting/<str:id>', views.job_detail, name='user-admin-job-detail'),
    path('delete-job_posting/<str:id>/', views.job_delete, name='user-admin-delete-job-posting'),


   ]
