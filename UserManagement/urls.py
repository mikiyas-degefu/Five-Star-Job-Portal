from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import UserPasswordResetForm, UserPasswordConfirmForm

    

urlpatterns = [
    path('admin-user/', views.admin_user, name='admin_user'),
    path('admin-user/<str:id>/', views.admin_user_detail, name='admin_user-detail'),
    path('admin-user-delete/<str:id>/', views.admin_user_delete, name='admin_user-delete'),

    path('company-user/', views.company_user, name='company_user'),
    path('company-user/<str:id>/', views.company_user_detail, name='company_user-detail'),
    path('company-user-delete/<str:id>/', views.company_user_delete, name='company_user-delete'),


    path('candidate-user/', views.candidate_user, name='candidate_user'),
    path('candidate-user/<str:id>/', views.candidate_user_detail, name='candidate_user-detail'),
    path('candidate-user-delete/<str:id>/', views.candidate_user_delete, name='candidate_user-delete'),


    path('logout/', views.logout_view, name="logout"),

    #### RESET PASSWORD
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset_password.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",form_class=UserPasswordConfirmForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),



   ]
