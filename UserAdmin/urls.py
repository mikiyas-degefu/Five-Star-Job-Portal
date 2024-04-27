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


    path('blog_category/', views.blog_category, name='user-admin-blog-category'),
    path('update-blog/', views.update_blog_category, name='user-admin-update-blog-category'),
    path('delete-blog/<str:id>/', views.blog_category_delete, name='user-admin-delete-blog-category'),


    path('blog/', views.blog, name='user-admin-blog'),
    path('blog/<str:id>/', views.blog_detail, name='user-admin-blog-detail'),
    path('blog-delete/<str:id>/', views.blog_delete, name='user-admin-blog-delete'),


    path('profile/',views.admin_profile, name='admin-profile'),
    path('change-password/', views.admin_change_password, name="admin-change-password"),

    path('social-media', views.admin_social_media, name="admin-social-media"),
    path('social-media-detail/<str:id>', views.admin_social_media_detail, name="admin-social-media-detail"),
    path('social-media-delete/<str:id>/', views.delete_social_media, name='user-admin-delete-social-media'),

   ]
