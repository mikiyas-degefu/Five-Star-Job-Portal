from django.urls import path
from . import views

urlpatterns = [
    path('admin-user/', views.admin_user, name='admin_user'),
    path('admin-user/<str:id>/', views.admin_user_detail, name='admin_user-detail'),
    path('admin-user-delete/<str:id>/', views.admin_user_delete, name='admin_user-delete')
   ]
