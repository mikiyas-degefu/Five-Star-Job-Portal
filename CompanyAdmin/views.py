from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from JobPortal.forms import (JobPostingCompanyAdminForm)
from JobPortal.models import ( Job_Posting, Application)
from django.db.models import Q
from django.contrib import messages 

# Create your views here.

def index(request):
    context = {
        
    }
    return render(request, 'CompanyAdmin/index.html', context=context)


def job_posting(request):
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None)
    jobs = Job_Posting.objects.filter(company = request.user.company)
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Job_Posting.objects.filter( company = request.user.company).filter(Q(title__contains=q) | Q(sector__name__contains=q) | Q(salary_range_start__contains=q) | Q(salary_range_final__contains=q) | Q(type__contains=q))
    
    paginator = Paginator(jobs, 30) 
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
            obj.company = request.user.company
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
            return redirect('company-admin-job-posting')
    
    
    context = {
        'jobs' : page,
        'count' : count,
        'form' : form,
    }
    return render(request, 'CompanyAdmin/job_posting.html', context=context)


def job_delete(request, id):
    try:
        job = Job_Posting.objects.get(pk = id, company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')

    try:
        job.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('company-admin-job-posting')    

def job_detail(request, id):
    try:
        job = Job_Posting.objects.get(pk = id, company=request.user.company)
    except:
        return HttpResponse('You are not authorized to access this page!')
    
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None, instance=job)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'form': form,
    }
    return render(request, 'CompanyAdmin/job_detail.html', context=context)




def applicant(request):
    form = JobPostingCompanyAdminForm(request.POST or None, request.FILES or None)
    jobs = Application.objects.filter(job__company = request.user.company).select_related()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Job_Posting.objects.filter( job__company = request.user.company).select_related()
    
    paginator = Paginator(jobs, 30) 
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
            obj.company = request.user.company
            obj.save()
            form.save_m2m()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('company-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
            return redirect('company-admin-job-posting')
    
    
    context = {
        'jobs' : page,
        'count' : count,
        'form' : form,
    }
    return render(request, 'CompanyAdmin/applicant.html', context=context)