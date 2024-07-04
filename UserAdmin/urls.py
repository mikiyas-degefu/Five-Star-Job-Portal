from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin-dashboard'),
    path('company/', views.company, name='user-admin-company'),
    path('company/<str:id>/', views.company_detail, name='user-admin-company-detail'),
    path('company-delete/<str:id>/', views.company_delete, name='user-admin-company-delete'),
    path('company_status/<int:company_id>/', views.company_status, name='company_status'),

    path('sector/', views.job_sector, name='user-admin-sector'),
    path('update-sector/', views.update_sector, name='user-admin-update-sector'),
    path('sector-delete/<str:id>/', views.sector_delete, name='user-admin-sector-delete'),


    path('skills/', views.skills, name='user-admin-skills'),
    path('update-skill/', views.update_skill, name='user-admin-update-skills'),
    path('question_delete/<str:id>/', views.question_delete, name='question_delete'),


    path('skill-questions/', views.skill_questions, name='skill-questions'),
    path('update_question/', views.update_question, name='update_question'),
    path('skill-questions-delete/<str:id>/', views.skill_delete, name='user-admin-questions-delete'),



    path('faq/', views.faq, name='faq'),
    path('update_faq/', views.update_faq, name='update_faq'),
    path('faq_delete/<str:id>/', views.faq_delete, name='faq_delete'),

    path('account_delete/', views.account_delete, name='account_delete'),

    path('job_posting/', views.job_posting, name='user-admin-job-posting'),
    path('update-job_posting/<str:id>', views.job_detail, name='user-admin-job-detail'),
    path('delete-job_posting/<str:id>/', views.job_delete, name='user-admin-delete-job-posting'),


    path('blog_category/', views.blog_category, name='user-admin-blog-category'),
    path('update-blog/', views.update_blog_category, name='user-admin-update-blog-category'),
    path('delete-blog/<str:id>/', views.blog_category_delete, name='user-admin-delete-blog-category'),


    path('blog/', views.blog, name='user-admin-blog'),
    path('blog/<str:id>/', views.blog_detail, name='user-admin-blog-detail'),
    path('blog-delete/<str:id>/', views.blog_delete, name='user-admin-blog-delete'),


    path('profile/',views.admin_profile, name='admin-profile'),
    path('change-password/', views.admin_change_password, name="admin-change-password"),

    path('social-media/', views.admin_social_media, name="admin-social-media"),
    path('social-media-detail/<str:id>/', views.admin_social_media_detail, name="admin-social-media-detail"),
    path('social-media-delete/<str:id>/', views.delete_social_media, name='user-admin-delete-social-media'),


    path('contact-messages/', views.contact_messages, name="admin-contact-message"),
    path('contact-messages/<str:id>/', views.contact_messages_detail, name="admin-contact-message-detail"),

    path('log/', views.audit, name="admin-audit"),

    path('companies-download/', views.export_companies, name="download-companies"),
    path('sectors-download/', views.export_job_sector, name="download-sector"),
    path('job-download/', views.export_job, name="download-job"),
    path('skill-download/', views.export_skill, name="download-skill"),
    path('superuser-download/', views.export_superusers, name="download-superuser"),
    path('company-admin-download/', views.export_company_admin, name="download-company-admin"),
    path('candidate-download/', views.export_company_admin, name="download-candidate"),

   ]
