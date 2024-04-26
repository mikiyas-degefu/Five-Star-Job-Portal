from django.urls import path
from . import views

urlpatterns = [
    path('admin-user/', views.admin_user, name='admin_user'),
    path('admin-user/<str:id>/', views.admin_user_detail, name='admin_user-detail'),
    path('admin-user-delete/<str:id>/', views.admin_user_delete, name='admin_user-delete'),

    path('company-user/', views.company_user, name='company_user'),
    path('company-user/<str:id>/', views.company_user_detail, name='company_user-detail'),
    path('company-user-delete/<str:id>/', views.company_user_delete, name='company_user-delete'),


    path('candidate-user/', views.candidate_user, name='candidate_user'),
    path('candidate-user/<str:id>/', views.candidate_user_detail, name='candidate_user-detail'),
    path('candidate-user-delete/<str:id>/', views.candidate_user_delete, name='candidate_user-delete')
   ]
