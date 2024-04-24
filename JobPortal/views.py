from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    context = {
        "sectors" : Sector.objects.all()[:12]
    }
    return render(request , 'user/index.html' , context)

def jobs(request):
    return render(request , 'user/jobs.html')  

def blog(request):
    return render(request , 'user/blog.html')  

def about(request):
    return render(request , 'user/about-us.html')

def contact(request):
    return render(request , 'user/contact.html')                