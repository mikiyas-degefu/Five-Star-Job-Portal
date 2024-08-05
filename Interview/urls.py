from django.urls import path
from . import views
urlpatterns = [
    path('get_token' , views.getToken , name='get_token'),
    path('interview_home', views.interview_home, name='interview_home'),
    path('get_user', views.get_user, name='get_user'),
    path('', views.interview, name='interview'),
]