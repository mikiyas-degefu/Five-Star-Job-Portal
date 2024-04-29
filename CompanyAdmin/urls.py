from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='company-admin-dashboard'),
    path('job-posting/', views.job_posting, name='company-admin-job-posting'),
]