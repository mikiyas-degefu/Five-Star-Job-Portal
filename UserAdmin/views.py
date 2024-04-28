from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from Company.models import (Company, Blog_Categories, Blog, Social_Media, Contact_Message)
from Company.forms import (CompanyForm, BlogCategoriesForm, BlogForm, SocialMediaForm)
from  JobPortal.forms import (SectorForm, SkillForm , JobPostingForm)
from JobPortal.models import (Sector, Skill , Job_Posting)
from UserManagement.models import CustomUser
from django.db.models import Q
from UserManagement.decorators import (admin_super_user_required)
from UserManagement.forms import (CustomUserEditFormAdmin, ChangePasswordForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
# Create your views here.


@admin_super_user_required
def index(request):
    context = {
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/index.html', context=context)


@admin_super_user_required
def company(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    companies = Company.objects.all()
    count = 30
   
    if 'q' in request.GET:
        q = request.GET['q']
        companies = Company.objects.filter( Q(name__contains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(views__icontains=q) | Q(total_jobs__icontains=q))
    
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
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('user-admin-company')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Company')
    

    
    context = {
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
    except:
        company = None
    
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
            return redirect('user-admin-company-detail',f'{id}')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    context = {
        'form': form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/company_detail.html', context=context)

@admin_super_user_required
def company_delete(request, id):
    try:
        company = Company.objects.get(pk = id)
        company.delete()
        messages.success(request, '&#128515 Hello User, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello User , An error occurred while Deleting Company')
    
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
            messages.success(request, '&#128515 Hello User, Successfully Added')
            return redirect('user-admin-sector')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Sector')
    

    
    context = {
        'sectors' : page,
        'count' : count,
        'form' : form,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/sector.html', context=context)
    




    ########### Save Data


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
        jobs = Job_Posting.objects.filter( Q(company__name__contains=q) | Q(title__icontains=q) | Q(sector__name__icontains=q) | Q(salary_range_start__icontains=q) | Q(salary_range_final__icontains=q))
    
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
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while updating Company')
    

    
    context = {
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
        messages.success(request, '&#128515 Hello Job, Successfully Deleted')
    except:
        messages.error(request, '&#128532 Hello Job , An error occurred while Deleting Company')
    
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
            form.save()
            messages.success(request, '&#128515 Hello Job, Successfully Updated')
            return redirect('user-admin-job-posting')
        else:
            messages.error(request, '&#128532 Hello Job , An error occurred while updating job')
    context = {
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
    form =  CustomUserEditFormAdmin(request.POST or None, request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128515 Hello User, Successfully Updated')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Updating User Information ')

    context = {
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
        'contact_message': contact_message,
        'contact_messages' : page,
        'count' : count,
        'count_messages' : Contact_Message.objects.filter(is_read = False).count()
    }
    return render(request, 'UserAdmin/contact_messages.html', context=context)
    
