from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('choose_register' , views.choose_register , name='choose_register'),
    path('signup/', views.registration_view, name="signup"),
    path('register_company_front/', views.register_company_front, name='register_company_front'),
    path('job-list/', views.job_list, name='job-list'),
    path('job_search/<str:job_title>/<str:city>', views.job_search, name='job_search'),
    path('job-sector/<slug:slug>', views.job_sector_categories, name='job_sector_categories'),
    path('job-detail/<slug:slug>', views.job_detail, name='Job-detail'),

    #User
    path('user-add-bookmark/<slug:slug>', views.user_add_bookmark, name="user-add-bookmark"),
    path('user-remove-bookmark/<slug:slug>', views.user_delete_bookmark, name='user-delete-bookmark'),
    path('user-apply-job/<slug:slug>', views.user_apply_job, name='user-apply-job'),
    path('user-cancel-job/<slug:slug>', views.user_cancel_job, name='user-cancel-job'),
    path('resetpassword/', views.reset_password, name='reset-password'),
    path('login/', views.login, name='login'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('user-add-resume/', views.user_resume, name='user-resume'),
    path('user-add-education/', views.user_add_education, name='user-add-education'),
    path('user-education/<slug:slug>/',views.detail_user_education, name='detail-user-education'),
    path('user-delete-education/<slug:slug>',views.user_delete_education, name='user-delete-education'),
    path('user-add-experience/', views.user_add_experience, name='user-add-experience'),
    path('user-experience/<slug:slug>/',views.detail_user_experience, name='detail-user-experience'),
    path('user-delete-experience/<slug:slug>',views.user_delete_experience, name='user-delete-experience'),
    path('user-add-project/', views.user_add_project, name='user-add-project'),
    path('user-project/<int:id>/',views.detail_user_project, name='detail-user-project'),
    path('user-delete-project/<int:id>',views.user_delete_project, name='user-delete-project'),
    path('user-add-language/', views.user_add_language, name='user-add-language'),
    path('user-language/<int:id>/',views.detail_user_language, name='detail-user-language'),
    path('user-delete-language/<int:id>',views.user_delete_language, name='user-delete-language'),
    path('user-applied-job/', views.user_applied_jobs, name='user-applied-job'),
    path('user-bookmark/', views.user_bookmark, name='user-bookmark'),
    path('user-change-password/', views.user_change_password, name='user-change-password'),

    #Interviewer
    path('interviewer-dashboard/', views.interviewer_dashboard, name='interviewer-dashboard'),
    path('interviewer-info/', views.interviewer_personal_info, name='interviewer-personal-info'),
    path('interviewer-job-list/', views.interviewer_job_list, name='interviewer-job-list'),
    path('interviewer-job-detail/<slug:slug>', views.interviewer_job_detail, name='interviewer-job-detail'),
    path('interviewer-interviews-list/', views.interviewer_interviews_lists, name='interviewer-interviews-list'),
    path('interview-detail/<slug:slug>', views.interview_detail, name='interview_detail'),
    path('cancel-interview/<slug:slug>', views.interview_cancel, name='cancel-interview'),
    path('interview-scheduled/', views.interview_scheduled, name='interview-scheduled'),
    path('today-interviews/', views.interview_today_interview_list, name='today-interviews'),
    path('interview-now/<slug:slug>', views.interview_individual_now, name="interviews-now"),
    path('interview-job-status/', views.interview_candidate_job_status, name="interview-job-status"),
    path('interview-applicant-category/<slug:slug>', views.interview_applicant_category, name='interview_applicant_category'),
    path('company_interviewer_change_password/', views.company_interviewer_change_password, name='company_interviewer_change_password'),




    path('validate_skill_list/', views.validate_skill_list, name="validate_skill_list"),
    path('instruction/<str:id>/', views.instruction, name="instruction"),
    path('validate_skill/<str:id>/', views.validate_skill, name="validate_skill"),


]
