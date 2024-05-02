from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='company-admin-dashboard'),

    path('job-posting/', views.job_posting, name='company-admin-job-posting'),
    path('company_interviewer/', views.company_interviewer, name='company_interviewer'),
    path('company_admins/', views.company_admins, name='company_admins'),
    path('company_user_detail/<str:id>/', views.company_user_detail, name='company_user_detail'),
    path('company_user_delete/<str:id>/', views.company_user_delete, name='company_user_delete'),
    path('change_status_user/<str:id>/', views.change_status_user, name='change_status_user'),
    path('company_admin_profile/', views.company_admin_profile, name='company_admin_profile'),
    path('company_admin_change_password/', views.company_admin_change_password, name='company_admin_change_password'),
    path('job-posting/<str:id>', views.job_detail, name='company-admin-job-posting-detail'),
    path('job-posting-delete/<str:id>', views.job_delete, name='company-admin-job-posting-delete'),

    path('applicant/', views.applicant, name='company-admin-applicant'),
    path('applicant/<str:id>/<str:job_id>', views.applicant_detail, name='company-admin-applicant-detail'),
]