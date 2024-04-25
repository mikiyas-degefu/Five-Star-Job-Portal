from django.urls import path
from . import views
urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>',views.single_blog, name='single_blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('privacy-and-policy/', views.privacy_and_policy, name='Privacy-policy'),
    path('faqs/', views.faqs, name='faqs')
]
