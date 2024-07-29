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

    #Applicant
    path('applicant/', views.applicant, name='company-admin-applicant'),
    path('applicant/<str:app_id>/', views.applicant_detail, name='company-admin-applicant-detail'),

    #Interview Status
    path('interview-status/', views.interview_status, name='company-admin-interview-status'),
    path('interview-status/<str:id>/', views.interview_status_detail, name='company-admin-interview-detail'),

    path('company_info/', views.company_info, name='company_info'),
    path('edit_company_info/<str:id>', views.edit_company_info, name='edit_company_info'),


    #Export Excel
    path('job-download/', views.export_job, name='company-export-job'),
    path('application-download/', views.export_application, name='company-export-application'),
    path('admin-download/', views.export_admins, name='company-export-admin'),
    path('interviewer-download/', views.export_interviewers, name='company-export-interviewers'),


    #Filter Candidates
     path('filter_candidates/<int:id>', views.filter_candidates, name='filter_candidates'), 
     path('find_candidate_detail/<int:id>', views.find_candidate_detail, name='find_candidate_detail'), 
       
]