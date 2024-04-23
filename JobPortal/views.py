from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request , 'user/index.html')

def jobs(request):
    return render(request , 'user/jobs.html')  

def blog(request):
    return render(request , 'user/blog.html')  

def about(request):
    return render(request , 'user/about-us.html')

def contact(request):
    return render(request , 'user/contact.html')                