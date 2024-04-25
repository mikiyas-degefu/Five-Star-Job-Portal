from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user-admin-index'),
    path('company/', views.company, name='user-admin-company'),
   ]
