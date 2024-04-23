from django.urls import path 
from JobPortal import views

urlpatterns = [
     path('',views.index, name='index'),
     path('jobs/',views.jobs, name='jobs'),
     path('blog/',views.blog, name='blog'),
     path('about/',views.about, name='about'),
     path('contact/',views.contact, name='contact'),
]
