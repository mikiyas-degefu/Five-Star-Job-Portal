from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from Company.models import (Company, Blog_Categories, Blog, Social_Media, Contact_Message , FAQ)
from Company.forms import (CompanyForm, BlogCategoriesForm, BlogForm, SocialMediaForm)
from  JobPortal.forms import (SectorForm, SkillForm , JobPostingForm , QuestionForm , FAQForm)
from JobPortal.models import (Sector, Skill , Job_Posting, Application , Question , Choice )
from UserManagement.models import CustomUser
from django.db.models import Q
from UserManagement.decorators import (admin_super_user_required)
from UserManagement.forms import (CustomUserEditFormAdmin, ChangePasswordForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from auditlog.models import LogEntry
from django.db.models import Count
import threading
from JobPortal.resource import handle_telegram_post, handle_registration_email, handle_inactive_send_email
from bs4 import BeautifulSoup
import random
from JobPortal.resource import (CompanyResource, SectorResource, JobResource, SkillResource, UserResource)
# Create your views here.

notification_company = Company.objects.filter(read = False).select_related()


@admin_super_user_required
def index(request):
    total_users = CustomUser.objects.all().count()
    total_companies = Company.objects.all().count()
    total_jobs = Job_Posting.objects.all().count()
    total_application = Application.objects.all().count()
    auditlog_entries = LogEntry.objects.select_related('content_type', 'actor')[:10]
    company_views = Company.objects.filter().order_by('-views')[:3]

    sectors_with_job_counts = Sector.objects.annotate(job_posting_count=Count('job_posting')).order_by('-job_posting_count')[:6]
    
    contact_messages = Contact_Message.objects.all()[:5]
    blogs = Blog.objects.all()[:5]
    job_posting = Job_Posting.objects.all()[:10]
    companies = Company.objects.all()[:10]

    companies_with_job_count = Company.objects.annotate(job_posting_count=Count('job_posting')).order_by('-job_posting_count')[:6]



    companies_graph_name = []
    companies_graph_jobs = []
    companies_graph_views = []

    for i in companies_with_job_count:
        companies_graph_name.append(i.name)
        companies_graph_jobs.append(i.job_posting_count)
        companies_graph_views.append(i.views)



    context = {
        'notification_company': notification_company,
        'total_user' : total_users,
        'total_companies' : total_companies,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count(),
        'total_jobs' : total_jobs,
        'total_application' : total_application,
        'auditlog_entries': auditlog_entries,
        'company_views' : company_views,
        'sectors_with_job_counts' : sectors_with_job_counts,
        'contact_messages' : contact_messages,
        'blogs' : blogs,
        'job_posting':job_posting,
        'companies' : companies,
        'companies_graph_name' : companies_graph_name,
        'companies_graph_jobs': companies_graph_jobs,
        'companies_graph_views' : companies_graph_views,
        'notification_company': notification_company,
    }
    return render(request, 'UserAdmin/index.html', context=context)


@admin_super_user_required
def company(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    companies = Company.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        companies = Company.objects.filter( Q(name__contains=q) | Q(phone__contains=q) | Q(email__contains=q) | Q(views__contains=q) | Q(total_jobs__contains=q))
    
    paginator = Paginator(companies, 30) 
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
            form.save()
            messages.success(request, '&#128515 Hello User, Company Successfully Added')
            return redirect('user-admin-company')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Company')
    

    
    context = {
        'notification_company': notification_company,
        'companies' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/company.html', context=context)
    

    
@admin_super_user_required
def company_detail(request, id):
    try:
        company = Company.objects.get(pk = id)
        company.read = True
        company.save()
    except:
        company = None
    
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Company successfully updated')
            return redirect('user-admin-company-detail',f'{id}')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    context = {
        'notification_company': notification_company,
        'form': form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/company_detail.html', context=context)


@admin_super_user_required
def company_delete(request, id):
    try:
        company = Company.objects.get(pk = id)
        company.delete()
        messages.success(request, '&#128515 Hello User,Company successfully deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('user-admin-company')


def company_status(request, company_id):
    company = Company.objects.get(id=company_id)
    company_admins = CustomUser.objects.filter(company = company)

    try:
        #Deactivate 
        if company.active:
            company.active = False
            company.save()

            for admin in company_admins:
                admin.is_active = True
                admin.save()
        
            stop_event = threading.Event()
            background_thread = threading.Thread(target=handle_inactive_send_email, args=(request, company.name, company.email,stop_event), daemon=True)
            background_thread.start()
            stop_event.set()
            messages.success(request, 'Successfully Deactivated')

         #Activate  
        else:
            company.active = True
            company.save()

            for admin in company_admins:
                admin.is_active = True
                admin.save()


            stop_event = threading.Event()
            background_thread = threading.Thread(target=handle_registration_email, args=(request,company.email,'first_name','last_name','company_activations',stop_event, company.name ), daemon=True)
            background_thread.start()
            stop_event.set()

            messages.success(request, 'Successfully Activated')
    except:
        pass
    return redirect('user-admin-company')


 

@admin_super_user_required
def job_sector(request):
    form = SectorForm(request.POST or None)
    sector = Sector.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        sector = Sector.objects.filter( Q(name__contains=q))
    
    paginator = Paginator(sector, 30) 
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
            form.save()
            messages.success(request, '&#128515 Hello User, Job sector successfully added')
            return redirect('user-admin-sector')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Sector')
    

    
    context = {
        'notification_company': notification_company,
        'sectors' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/sector.html', context=context)
    

@admin_super_user_required
def update_sector(request):
    id = request.POST['id']
    name = request.POST['name']

    try:
        sector = Sector.objects.get(id = id)
        sector.name = name
        sector.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)



@admin_super_user_required
def job_posting(request):
    form = JobPostingForm(request.POST or None, request.FILES or None)
    jobs = Job_Posting.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        jobs = Job_Posting.objects.filter( Q(company__name__contains=q) | Q(title__contains=q) | Q(sector__name__contains=q) | Q(salary_range_start__contains=q) | Q(salary_range_final__contains=q))
    
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
            obj.save()
            form.save_m2m()

            slug = obj.slug
            title = obj.title
            sector = obj.sector
            description = BeautifulSoup(obj.description, 'html.parser').text
            experience = obj.experience
            vacancies = obj.vacancies
            location = obj.location 
            salary_range_start = obj.salary_range_start
            salary_range_final  = obj.salary_range_final
            type = obj.type
            date_closed = obj.date_closed
            skills = obj.skills.all()
            skill_names = [str(skill) for skill in skills]
            skills = ', '.join(skill_names)

            if obj.job_status:
                stop_event = threading.Event()
                background_thread = threading.Thread(target=handle_telegram_post, args=(request,slug,request.user.company, title, sector, vacancies, type, experience, description, skills, location, date_closed, salary_range_start, salary_range_final, stop_event), daemon=True)
                background_thread.start()
                stop_event.set()
            messages.success(request, '&#128515 Hello User, Job Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    

    
    context = {
        'notification_company': notification_company,
        'jobs' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/job_posting.html', context=context)
    

@admin_super_user_required    
def job_delete(request, id):
    try:
        job = Job_Posting.objects.get(pk = id)
        job.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
    return redirect('user-admin-job-posting')    

@admin_super_user_required
def job_detail(request, id):
    try:
        job = Job_Posting.objects.get(pk = id)
    except:
        job = None
    
    form = JobPostingForm(request.POST or None, request.FILES or None, instance=job)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()

            slug = obj.slug
            title = obj.title
            sector = obj.sector
            description = BeautifulSoup(obj.description, 'html.parser').text
            experience = obj.experience
            vacancies = obj.vacancies
            location = obj.location 
            salary_range_start = obj.salary_range_start
            salary_range_final  = obj.salary_range_final
            type = obj.type
            date_closed = obj.date_closed
            skills = obj.skills.all()
            skill_names = [str(skill) for skill in skills]
            skills = ', '.join(skill_names)

            if obj.job_status:
                stop_event = threading.Event()
                background_thread = threading.Thread(target=handle_telegram_post, args=(request,slug,request.user.company, title, sector, vacancies, type, experience, description, skills, location, date_closed, salary_range_start, salary_range_final, stop_event), daemon=True)
                background_thread.start()
                stop_event.set()
            messages.success(request, '&#128515 Hello User, Successfully Updated')


            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('user-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating job')
    context = {
        'notification_company': notification_company,
        'form': form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/job_detail.html', context=context)


@admin_super_user_required
def sector_delete(request, id):
    try:
        sector = Sector.objects.get(pk = id)
        sector.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Sector')
    
    return redirect('user-admin-sector')

@admin_super_user_required
def skills(request):
    form = SkillForm(request.POST or None)
    skills = Skill.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        skills = Skill.objects.filter( Q(title__contains=q))
    
    paginator = Paginator(skills, 30) 
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
            try:
                form.save()
                messages.success(request, '&#128515 Hello User, Successfully Added')
                return redirect('user-admin-skills')
            except:
                messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill or Skill Exist')
                return redirect('user-admin-skills')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill')
    

    
    context = {
        'notification_company': notification_company,
        'skills' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/skills.html', context=context)
    
@admin_super_user_required
def skill_delete(request, id):
    try:
        skill = Skill.objects.get(pk = id)
        skill.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Skill')
    
    return redirect('user-admin-skills')

@admin_super_user_required
def update_skill(request):
    id = request.POST['id']
    title = request.POST['title']

    try:
        skill = Skill.objects.get(id = id)
        skill.title = title
        skill.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)


@admin_super_user_required
def blog_category(request):
    form = BlogCategoriesForm(request.POST or None, request.FILES or None)
    categories = Blog_Categories.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        categories = Blog_Categories.objects.filter(Q(name__contains=q))
    
    paginator = Paginator(categories, 30) 
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
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('user-admin-blog-category')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Blog Category')
    

    
    context = {
        'notification_company': notification_company,
        'categories' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/blog_category.html', context=context)


@admin_super_user_required
def blog_category_delete(request, id):
    try:
        blog = Blog_Categories.objects.get(pk = id)
        blog.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Blog Category')
    
    return redirect('user-admin-blog-category')


@admin_super_user_required
def update_blog_category(request):
    id = request.POST['id']
    name = request.POST['name']


    try:
        category = Blog_Categories.objects.get(pk = id)
        category.name = name
        category.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)


@admin_super_user_required
def blog(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    blogs = Blog.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        blogs = Blog.objects.filter(Q(title__contains=q))
    
    paginator = Paginator(blogs, 30) 
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
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('user-admin-blog')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Blog')
    

    
    context = {
        'notification_company': notification_company,
        'blogs' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/blog.html', context=context)

@admin_super_user_required
def blog_detail(request, id):
    try:
        blog = Blog.objects.get(pk = id)
    except:
        blog = None
    
    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('user-admin-blog-detail',f'{id}')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    context = {
        'notification_company': notification_company,
        'form': form,
        'blog' : blog,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/blog_detail.html', context=context)

@admin_super_user_required
def blog_delete(request, id):
    try:
        blog = Blog.objects.get(pk = id)
        blog.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Blog')
    
    return redirect('user-admin-blog')


@admin_super_user_required
def admin_profile(request):
    user = request.user
    form =  CustomUserEditFormAdmin(request.POST or None,request.FILES or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating User Information ')

    context = {
        'notification_company': notification_company,
        'user' : user,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }

    return render(request, 'UserAdmin/profile.html', context=context)



@admin_super_user_required
def admin_change_password(request):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hello User,Password Successfully Updated')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating User Password! ')

    
    return render(request,'UserAdmin/change_password.html', {'form': form})



@admin_super_user_required
def admin_social_media(request):
    form = SocialMediaForm(request.POST or None)
    social_media = Social_Media.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Hello User,Password Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating Social Media! ')



    context = {
        'notification_company': notification_company,
        'social_medias' : social_media,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }

    return render(request, 'UserAdmin/social_media.html', context=context)


@admin_super_user_required
def admin_social_media_detail(request, id):
    try:
        social = Social_Media.objects.get(pk = id)
    except:
        social = None
    
    form = SocialMediaForm(request.POST or None, instance=social)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('admin-social-media')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Social Media')
    context = {
        'notification_company': notification_company,
        'form': form,
        'social_media' : social,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/social_media_detail.html', context=context)



@admin_super_user_required
def delete_social_media(request, id):
    try:
        social = Social_Media.objects.get(pk = id)
        social.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Social Media')
    
    return redirect('admin-social-media')


@admin_super_user_required
def contact_messages(request):
    message = Contact_Message.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        message = Contact_Message.objects.filter(Q(name__contains=q) | Q(email__contains=q) | Q(subject__contains=q))
    
    paginator = Paginator(message, 30) 
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
    

    
    context = {
        'notification_company': notification_company,
        'contact_messages' : page,
        'count' : count,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/contact_messages.html', context=context)




@admin_super_user_required
def contact_messages_detail(request, id):
    try:
        contact_message = Contact_Message.objects.get(pk = id)
    except:
        contact_message = None

    contact_message.is_read=True
    contact_message.save()
    
    message = Contact_Message.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        message = Contact_Message.objects.filter(Q(name__contains=q) | Q(email__contains=q) | Q(subject__contains=q))
    
    paginator = Paginator(message, 30) 
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
    

    
    context = {
        'notification_company': notification_company,
        'contact_message': contact_message,
        'contact_messages' : page,
        'count' : count,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/contact_messages.html', context=context)
    

@admin_super_user_required
def audit(request):
    log = LogEntry.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        log = LogEntry.objects.filter()
    
    paginator = Paginator(log, 30) 
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
    

    
    context = {
        'notification_company': notification_company,
        'auditlog_entries' : page,
        'count' : count,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/log.html', context=context)
    

@admin_super_user_required
def skill_questions(request):
    form = QuestionForm(request.POST or None)
    questions = Question.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        questions = Question.objects.filter( Q(title__contains=q))
    
    paginator = Paginator(questions, 30) 
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
            try:
                question = form.save()

                options = request.POST.getlist('option')
                selected_option = request.POST.get('selected-option')
                print(selected_option)
                for count , option_text in enumerate(options):
                        choice = Choice.objects.create(text=option_text, for_question=question)
                        choice.save()
                        print(count)
                        if count + 1 == int(selected_option):
                           print("inner",count)
                           question.answer = choice
                           question.save()
                messages.success(request, '&#128515 Hello User, Successfully Added')
                return redirect('skill-questions')
            except:
                messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill or Skill Exist')
                return redirect('skill-questions')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill')
    

    
    context = {
        'notification_company': notification_company,
        'questions' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/skill_questions.html', context=context)
    
@admin_super_user_required
def question_delete(request, id):
    try:
        question = Question.objects.get(pk = id)
        question.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Skill')
    
    return redirect('skill_questions')

@admin_super_user_required
def update_question(request):
    id = request.POST['id']
    text = request.POST['text']
    for_skill = request.POST['for_skill']
    answer = request.POST['answer']

    try:
        question = Question.objects.get(id = id)
        question.text = text
        question.anser = answer
        question.for_skill = for_skill
        question.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)







@admin_super_user_required
def faq(request):
    form = FAQForm(request.POST or None)
    faqs = FAQ.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        faqs = FAQ.objects.filter( Q(title__contains=q))
    
    paginator = Paginator(faqs, 30) 
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
            try:
                form.save()
                messages.success(request, '&#128515 Hello User, Successfully Added')
                return redirect('faq')
            except:
                messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill or Skill Exist')
                return redirect('faq')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Skill')
    

    
    context = {
        'notification_company': notification_company,
        'faqs' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/faq.html', context=context)
    
@admin_super_user_required
def faq_delete(request, id):
    try:
        faq = FAQ.objects.get(pk = id)
        faq.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Skill')
    
    return redirect('skill_questions')

@admin_super_user_required
def update_faq(request):
    id = request.POST['id']
    question = request.POST['question']
    answer = request.POST['answer']

    try:
        faq = FAQ.objects.get(id = id)
        faq.question = question
        faq.answer = question
        faq.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse(response)




@admin_super_user_required
def account_delete(request):
    try:
        user = request.user
        user.delete()
        user.success(request, '&#128515 Hello User, Successfully Deleted')
        return redirect('index')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Skill')
    
    return redirect('user-profile')






######EXPORT

@admin_super_user_required
def export_companies(request):
    companies = CompanyResource()
    dataset = companies.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="companies.csv"'
    return response


@admin_super_user_required
def export_job_sector(request):
    sectors = SectorResource()
    dataset = sectors.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sectors.csv"'
    return response

@admin_super_user_required
def export_job(request):
    jobs = JobResource()
    dataset = jobs.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="job.csv"'
    return response

@admin_super_user_required
def export_skill(request):
    skills = SkillResource()
    dataset = skills.export()
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="skill.csv"'
    return response


@admin_super_user_required
def export_superusers(request):
    active_year = CustomUser.objects.filter(is_superuser = True)
    annual = UserResource()
    dataset = annual.export(active_year)
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="superusers.csv"'
    return response

@admin_super_user_required
def export_company_admin(request):
    active_year = CustomUser.objects.filter(is_admin = True)
    annual = UserResource()
    dataset = annual.export(active_year)
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="admins.csv"'
    return response

@admin_super_user_required
def export_candidates(request):
    active_year = CustomUser.objects.filter(is_candidate = True)
    annual = UserResource()
    dataset = annual.export(active_year)
    response = HttpResponse(dataset.csv, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="candidates.csv"'
    return response
