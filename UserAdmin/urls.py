from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin-dashboard'),
    path('company/', views.company, name='user-admin-company'),
    path('company/<str:id>/', views.company_detail, name='user-admin-company-detail'),
    path('company-delete/<str:id>/', views.company_delete, name='user-admin-company-delete'),

    path('sector/', views.job_sector, name='user-admin-sector'),
    path('update-sector/', views.update_sector, name='user-admin-update-sector'),


   ]
