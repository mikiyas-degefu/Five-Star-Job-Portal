from django.shortcuts import render , redirect
from .forms import CustomUserCreationForm , CustomUserEditForm
from .models import CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import logout
from UserManagement.decorators import (admin_super_user_required)
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.



def send_reg_email(request,email,first_name,last_name,password, stop_event):
    while not stop_event.is_set():
        subject, from_email, to = 'Registration Successful', 'mikiyasmebrate2656@gmail.com', f"{email}"
        text_content = "Registration Successful"
        context = {
            'first_name': first_name,
            'last_name' : last_name,
            'email' : email,
            'password' : password
        }
        html_content = render_to_string('success-email.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            print('Email sent')






@admin_super_user_required
def admin_user(request):
    form = CustomUserCreationForm(request.POST or None, request.FILES or None)
    admin_user = CustomUser.objects.filter(is_superuser=True)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        admin_user = CustomUser.objects.filter( Q(first_name__contains=q) | Q(last_name__icontains=q) | Q(company__name__icontains=q) )
    
    paginator = Paginator(admin_user, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password1']
            obj.is_superuser = True
            stop_event = threading.Event()
            background_thread = threading.Thread(target=send_reg_email, args=(request,email,first_name,last_name,password, stop_event), daemon=True)
            background_thread.start()
            stop_event.set()
            obj.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    

    
    context = {
        'admin_user' : page,
        'count' : count,
        'form' : form
    }
    return render(request, 'UserAdmin/admin_users.html', context=context)

@admin_super_user_required
def admin_user_delete(request, id):
    try:
        admin_user = CustomUser.objects.get(pk = id)
        admin_user.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('admin_user')    


@admin_super_user_required
def admin_user_detail(request, id):
    try:
        user = CustomUser.objects.get(pk = id)
    except:
        user = None
    
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('admin_user')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'form': form
    }
    return render(request, 'UserAdmin/admin_user_detail.html', context=context)



@admin_super_user_required
def company_user(request):
    form = CustomUserCreationForm(request.POST or None, request.FILES or None)
    company_user = CustomUser.objects.filter(is_admin=True)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        company_user = CustomUser.objects.filter( Q(first_name__contains=q) | Q(last_name__icontains=q) | Q(company__name__icontains=q) )
    
    paginator = Paginator(company_user, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.is_admin = True
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    

    
    context = {
        'company_user' : page,
        'count' : count,
        'form' : form
    }
    return render(request, 'UserAdmin/company_users.html', context=context)
    
@admin_super_user_required
def company_user_delete(request, id):
    try:
        company_user = CustomUser.objects.get(pk = id)
        company_user.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('company_user')    

@admin_super_user_required
def company_user_detail(request, id):
    try:
        user = CustomUser.objects.get(pk = id)
    except:
        user = None
    
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company_user')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'form': form
    }
    return render(request, 'UserAdmin/company_user_detail.html', context=context)    


@admin_super_user_required
def candidate_user(request):
    form = CustomUserCreationForm(request.POST or None, request.FILES or None)
    candidate_user = CustomUser.objects.filter(is_candidate=True)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        candidate_user = CustomUser.objects.filter( Q(first_name__contains=q) | Q(last_name__icontains=q) | Q(company__name__icontains=q) )
    
    paginator = Paginator(candidate_user, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.is_candidate = True
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    

    
    context = {
        'candidate_user' : page,
        'count' : count,
        'form' : form
    }
    return render(request, 'UserAdmin/candidate_users.html', context=context)
    
@admin_super_user_required
def candidate_user_delete(request, id):
    try:
        candidate_user = CustomUser.objects.get(pk = id)
        candidate_user.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('candidate_user')    

@admin_super_user_required
def candidate_user_detail(request, id):
    try:
        user = CustomUser.objects.get(pk = id)
    except:
        user = None
    
    form = CustomUserEditForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('candidate_user')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'form': form
    }
    return render(request, 'UserAdmin/candidate_user_detail.html', context=context) 


def logout_view(request):
    logout(request)
    return redirect('login')