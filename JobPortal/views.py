from django.shortcuts import render, redirect
from Company.models import Social_Media, Contact
from .forms import CandidateForm, EducationForm, ExperienceForm, InterviewerForm as InterviewFormInterview, ApplicationForm, InterviewerNoteForm , CompanyFormFront , CustomUserFormFront
from .models import Skill,Sector, Candidate, Education, Experience, Job_Posting, Bookmarks, Application,Interviews , Question , Choice , UserSkill
from Company.models import Company
from django.shortcuts import render, redirect
from Company.models import Social_Media, Contact,Company
from .forms import LanguageForm,ProjectForm,CandidateForm, EducationForm, ExperienceForm, InterviewerForm as InterviewFormInterview, ApplicationForm, InterviewerNoteForm , CompanyFormFront , CustomUserFormFront, ApplicationCoverLetterForm
from .models import Skill,Sector, Candidate, Education, Experience, Job_Posting, Bookmarks, Application,Interviews, Language, Project
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from UserManagement.forms import CustomUserCreationForm, Login_Form, InterviewerForm
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
from UserManagement.decorators import interviewer_user_required
from UserManagement.forms import ( ChangePasswordForm)
import threading
from .resource import (handle_registration_email, handle_successfully_applied_send_email, handle_scheduled_send_email, handle_rescheduled_send_email)


social_medias = Social_Media.objects.all()

#Session
def login_view(request):
    form = Login_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email,password=password)
        if (user is not None and user.is_superuser and user.is_active):
            login(request, user)
            return redirect('admin-dashboard')
        elif user is not None and user.is_interviewer and user.is_active:
            login(request, user)
            return redirect('interviewer-dashboard')
        elif user is not None and not user.is_active:
            messages.error(request, 'Your account is in review please try again later!')
        elif user is not None and user.is_admin and user.is_active and user.company.active:
            login(request, user)
            return redirect('company-admin-dashboard')
        elif user is not None and user.is_admin and user.is_active and not user.company.active:
            messages.error(request, 'Your Company is not active, Please contact us')
        elif user is not None and user.is_candidate :
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Password or Email')
    context = {
        'form' : form
    }
    return render(request, 'RMS/sign-in.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'RMS/sign-out.html')



def choose_register(request):
    return render(request, 'RMS/choose_sign_up.html')    

def registration_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            user = form.save(commit=False)
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.is_candidate = True
            user.save()


            stop_event = threading.Event()
            background_thread = threading.Thread(target=handle_registration_email, args=(request,email,first_name,last_name, 'candidate',stop_event), daemon=True)
            background_thread.start()
            stop_event.set()


            messages.success(request, 'Your Account has been Successfully Created! Please Login')
            return redirect('/login') 
        else:
            messages.error(request, 'Hello User , An error occurred while Creating Account Please try again')

    context = {
        'form' : form
    }

    return render(request, 'RMS/registrations.html', context)


def register_company_front(request):
    company_form = CompanyFormFront(request.POST or None, request.FILES or None)
    user_form = CustomUserFormFront(request.POST or None)

    if request.method == 'POST':
        if company_form.is_valid() and user_form.is_valid():
            company = company_form.save()

            user = user_form.save(commit=False)
            user.is_admin = True
            user.company = company
            user.save()

            company_name = company.name
            
            


            stop_event = threading.Event()
            background_thread = threading.Thread(target=handle_registration_email, args=(request,company.email,None, None, 'company' ,stop_event, company_name), daemon=True)
            background_thread.start()
            stop_event.set()
            
            messages.success(request, "Welcome user! Your company is successfully registered. We're excited to review your information and get you started! We'll be in touch within 48 hours to confirm approval")
            return redirect('login')
    
    context = {
        'company_form': company_form,
        'user_form': user_form,
    }
    return render(request, 'RMS/company-register.html', context)


#Lists
def index(request):
    try: bookmark = Bookmarks.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: bookmark = None
    try: candidate = Candidate.objects.get(user = request.user)
    except: candidate = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None
    try: count_skill = candidate.skill.all()
    except: count_skill = 0
    sector = Sector.objects.all()
    sector_popular = Sector.objects.all()[0:12]
    job = None
    user = request.user
    if request.user :
        try:
            candidate = Candidate.objects.get(user=request.user)
            ser_skills = candidate.skill.all()
            job = Job_Posting.objects.filter(job_status=True, skills__in=ser_skills).distinct()[0:5]
           
        except:
            job = Job_Posting.objects.filter(job_status = True)[0:5]  
           
       
    else :
       job = Job_Posting.objects.filter(job_status = True)[0:5]
    job_number = Job_Posting.objects.filter(job_status = True)
    company = Company.objects.all()


    
    context = {
        'social_medias' : social_medias,
        'job_list' : job,
        "job_number" : job_number,
        'bookmark' : bookmark,
        'candidate' : candidate,
        'application' : application,
        'sector' : sector,
        'sector_popular' : sector_popular,
        "company" : company
    }
    return render(request, 'RMS/index.html', context)

def job_list(request):
    try: bookmark = Bookmarks.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: bookmark = None
    try: candidate = Candidate.objects.get(user = request.user)
    except: candidate = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None
    try: count_skill = candidate.skill.all()
    except: count_skill = 0

    sector_new = []
    sector = Sector.objects.all()
    for i in sector:
        if i.count_job_post() > 0:
            sector_new.append(i)

          


    sector_popular = Sector.objects.all()[0:5]
    job = Job_Posting.objects.filter(job_status = True)
    

    
    if 'q' in request.GET:
        q = request.GET['q']
        job = Job_Posting.objects.filter( job_status= True).filter(Q(title=q) | Q(sector__name=q) | Q(company__name=q))
       

    paginator = Paginator(job,5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    company = Company.objects.all()    
   

    context = {
        'social_medias' : social_medias,
        'job_list' : page,
        'bookmark' : bookmark,
        'candidate' : candidate,
        'application' : application,
        'sector' : sector_new,
        'company':company,
        'sector_popular' : sector_popular
    }
    return render(request, 'RMS/job-list.html', context)





def job_search(request, job , city ):
    try: bookmark = Bookmarks.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: bookmark = None
    try: candidate = Candidate.objects.get(user = request.user)
    except: candidate = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None


    
   

    paginator = Paginator(job,5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)


    for job_listing in Job.objects.all():
        if job is None or job_listing["title"].lower() == job.lower():
            if city is None or job_listing["city"].lower() == city.lower():
                    job_listings.append(job_listing)


    context = {
        'social_medias' : social_medias,
        'job_listing' : page,
        'bookmark' : bookmark,
        'candidate' : candidate,
        'application' : application,
        'sector' : sector,
        'company' : company,
        'sector_popular' : sector_popular
    }
    return render(request, 'RMS/job-search.html', context)


def job_sector_categories(request, slug):
    try: bookmark = Bookmarks.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: bookmark = None
    try: candidate = Candidate.objects.get(user = request.user)
    except: candidate = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None


    
 
    sector_popular = Sector.objects.all()[0:5]
    sector1 = None
    company1 = None
    try:
      company1 = Company.objects.get(id = slug)
      q = company1
    except :
      sector1 = Sector.objects.get(slug = slug)
      q = sector1
    sector = Sector.objects.all()
    company = Company.objects.all()
    job = Job_Posting.objects.filter(job_status = True).filter(Q(sector=sector1) | Q(company=company1))

    if 'q' in request.GET:
        q = request.GET['q']
        job = Job_Posting.objects.filter( job_status= True).filter(Q(title=q) | Q(sector__name=q) | Q(company__name=q))
   
    

    paginator = Paginator(job,5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'social_medias' : social_medias,
        'job_list' : page,
        'bookmark' : bookmark,
        'candidate' : candidate,
        'application' : application,
        'sector' : sector,
        'company' : company,
        'sector_popular' : sector_popular
    }
    return render(request, 'RMS/job-list.html', context)

    


def job_detail(request, slug):
    job = Job_Posting.objects.get(slug=slug)
    company = job.company
    company.views = company.views + 1
    company.save()  # Increase Company views by 1 
    
    company_info = Contact.objects.all().first()
    social_media = Social_Media.objects.all().first()

    #cover letter
    application_form = ApplicationCoverLetterForm(request.POST or None)

    try: applied = Application.objects.get(user = request.user, job__slug = slug)
    except: applied = None

    try : candidate = Candidate.objects.get(user = request.user)
    except : candidate = None

    try: education = Education.objects.filter(candidate = request.user).count()
    except : education = None

    

    if request.method == 'POST':
        if application_form.is_valid():
            if request.user.id is None:
                messages.error(request, 'Please Login')
                return redirect('login')
            if applied is not None:
                messages.error(request, 'You are already Applied on this JOB please Check your Applied Jobs Lists')
                return redirect(request.META.get('HTTP_REFERER'))
            elif candidate is None:
                messages.error(request, 'Please Add Personal Information! ')
                return redirect('user-resume')
            elif education < 1:
                messages.error(request, 'Please at least add One Education Background!')
                return redirect('user-add-education')
            else:
                obj = application_form.save(commit=False)
                app = Application()
                app.user = request.user
                app.job = job
                app.cover_letter = obj.cover_letter
                app.save()

                stop_event = threading.Event()
                background_thread = threading.Thread(target=handle_successfully_applied_send_email, args=(request,request.user.first_name,request.user.last_name, job.title, job.company.name, request.user.email,stop_event ), daemon=True)
                background_thread.start()
                stop_event.set()
        
                messages.success(request, 'Successfully Applied Check your Applied Jobs')
                return redirect(request.META.get('HTTP_REFERER'))


    try: bookmark = Bookmarks.objects.get(user = request.user, job = job)
    except: bookmark = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None
    context = {
        'social_medias' : social_medias,
        'job' : job,
        'company_info' : company_info,
        'social_media' : social_media,
        'bookmark' : bookmark,
        'application'  :application,
        'application_form' : application_form
    }
    return render(request, 'RMS/job-details.html', context)



#Password
@login_required
def reset_password(request):
    context = {
        'social_medias' : social_medias,
    }
    return render(request, 'RMS/reset-password.html', context)

@login_required
def user_change_password(request):
    return render(request, 'RMS/user/dashboard-change-password.html')


#User Dashboard
@login_required
def user_dashboard(request):
    application = Application.objects.filter(user = request.user).count()
    bookmark  = Bookmarks.objects.filter(user = request.user).count()
    context = {
        'count_application' : application,
        'count_bookmark' : bookmark
    }
    return render(request, 'RMS/user/candidate-dashboard.html', context)

@login_required
def user_profile(request):
    try: 
        candidate = Candidate.objects.get(user = request.user)
        education = Education.objects.filter(candidate = request.user)
        experience = Experience.objects.filter(candidate = request.user)
        project = Project.objects.filter(candidate = request.user)
        language = Language.objects.filter(candidate = request.user)
    except:
        candidate = None 
        education = None
        experience = None
        project = None
        language = None
    
    context = {
        'candidate' : candidate,
        'social_medias' : social_medias,
        'education' : education,
        'experience': experience,
        'projects' : project,
        'language' : language
        
    }
    return render(request, 'RMS/user/dashboard-my-profile.html', context)



#Resume
@login_required
def user_resume(request):
    skills = Skill.objects.all()
    try:
        user_per_info = Candidate.objects.get(user = request.user)
    except: 
        user_per_info = None

    form_personal_info = CandidateForm(request.POST or None, request.FILES or None, instance=user_per_info)

    if request.method == 'POST':
        if form_personal_info.is_valid():
            obj = form_personal_info.save(commit=False)
            obj.user = request.user
            obj.save()

            for skill in form_personal_info.cleaned_data['skill']:
                try:
                    UserSkill.objects.get(candidate = obj, skill = skill)
                except:
                    if skill.validable:
                        UserSkill.objects.create(candidate = obj, skill = skill)

            
            form_personal_info.save_m2m()
            messages.success(request, 'Your Resume has been successfully Created!')
            form_personal_info =  CandidateForm(request.POST or None, request.FILES or None, instance=user_per_info)
            return redirect('user-resume')
        else :
            messages.error(request, 'You request han not been successful please try again! ')
    context = {
        'form' : form_personal_info,
        'skills' : skills,
        'candidate' : user_per_info
        }
    return render(request, 'RMS/user/dashboard-add-personal-info.html', context)



#Education
@login_required
def user_add_education(request):
    education = Education.objects.filter(candidate = request.user)
    form_education = EducationForm(request.POST or None)
    if request.method == 'POST':
        if form_education.is_valid():
            obj = form_education.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Education Status has been successfully Updated!')
            form_education = EducationForm()

    context = {
        'form' : form_education,
        'user_education' : education
        }
    return render(request, 'RMS/user/dashboard-add-education.html', context)

@login_required
def user_delete_education(request, slug):
    education = Education.objects.get(slug = slug)

    if education.delete():
        messages.success(request, 'Successfully Deleted!')
        return redirect('user-add-education')
    else:
        messages.error(request,'Your request has not been Unsuccessful Please try again!')
        return redirect('user-add-education')
    
@login_required
def detail_user_education(request, slug):
    education =  Education.objects.get(slug = slug)
    form = EducationForm(request.POST or None, instance=education)
    education_list = Education.objects.filter(candidate = request.user).exclude(slug = slug)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Education Status has been successfully Updated!')
            redirect('user-add-education')
    context = {
        'form' : form,
        'education': education,
        'user_education':education_list,
    }
    return render(request, 'RMS/user/dashboard-education-detail.html', context)


#Education
@login_required
def user_add_project(request):
    project = Project.objects.filter(candidate = request.user)
    form_project = ProjectForm(request.POST or None)
    if request.method == 'POST':
        if form_project.is_valid():
            obj = form_project.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Project Status has been successfully Updated!')
            form_project = ProjectForm()
        else:
             messages.error(request, 'Hello User , An error occurred while Adding Project')

    context = {
        'form' : form_project,
        'user_project' : project
        }
    return render(request, 'RMS/user/dashboard-add-project.html', context)

@login_required
def detail_user_project(request, id):
    project =  Project.objects.get(id = id)
    form = ProjectForm(request.POST or None, instance=project)
    project_list = Project.objects.filter(candidate = request.user)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Project Status has been successfully Updated!')
            redirect('user-add-project')
        else:
            messages.error(request, 'Hello User , An error occurred while Updating Project')
    context = {
        'form' : form,
        'project': project,
        'user_project':project_list,
    }
    return render(request, 'RMS/user/dashboard-project-detail.html', context)


@login_required
def user_delete_project(request, id):
    project = Project.objects.get(id = id)

    if project.delete():
        messages.success(request, 'Successfully Deleted!')
        return redirect('user-add-project')
    else:
        messages.error(request,'Your request has not been Unsuccessful Please try again!')
        return redirect('user-add-project')
    


#Education
@login_required
def user_add_language(request):
    language = Language.objects.filter(candidate = request.user)
    form_language = LanguageForm(request.POST or None)
    if request.method == 'POST':
        if form_language.is_valid():
            obj = form_language.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Language Status has been successfully Updated!')
            form_language = LanguageForm()
        else:
             messages.error(request, 'Hello User , An error occurred while Adding Language')

    context = {
        'form' : form_language,
        'user_language' : language
        }
    return render(request, 'RMS/user/dashboard-add-language.html', context)

@login_required
def detail_user_language(request, id):
    language =  Language.objects.get(id = id)
    form = LanguageForm(request.POST or None, instance=language)
    language_list = Language.objects.filter(candidate = request.user)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Language Status has been successfully Updated!')
            redirect('user-add-project')
        else:
            messages.error(request, 'Hello User , An error occurred while Updating Language')
    context = {
        'form' : form,
        'language': language,
        'user_language':language_list,
    }
    return render(request, 'RMS/user/dashboard-language-detail.html', context)

@login_required
def user_delete_language(request, id):
    language = Language.objects.get(id = id)

    if language.delete():
        messages.success(request, 'Successfully Deleted!')
        return redirect('user-add-language')
    else:
        messages.error(request,'Your request has not been Unsuccessful Please try again!')
        return redirect('user-add-language')


#Experience 
@login_required
def user_add_experience(request):
    form_experience = ExperienceForm(request.POST or None)
    experience = Experience.objects.all()
    if request.method == 'POST':
        if form_experience.is_valid():
            obj = form_experience.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Experience Status has been successfully Updated!')
            form_experience = EducationForm()

    context = {
        'form' : form_experience,
        'user_experience' : experience
        }
    return render(request, 'RMS/user/dashboard-add-experience.html', context)

@login_required
def detail_user_experience(request, slug):
    experience = Experience.objects.get(slug = slug)
    form = ExperienceForm(request.POST or None, instance=experience)
    experience_list = Experience.objects.filter(candidate = request.user).exclude(slug = slug)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.candidate = request.user
            obj.save()
            messages.success(request, 'Your Experience Status has been successfully Updated!')
            redirect('user-add-experience')
    context = {
        'form' : form,
        'experience' : experience,
        'user_experience' : experience_list
    }

    return render(request,'RMS/user/dashboard-experience-detail.html', context)

@login_required
def user_delete_experience(request, slug):
    experience = Experience.objects.get(slug = slug)

    if experience.delete():
        messages.success(request, 'Successfully Deleted!')
        return redirect('user-add-experience')
    else:
        messages.error(request,'Your request has not been Unsuccessful Please try again!')
        return redirect('user-add-experience')



#User Job
@login_required
def user_applied_jobs(request):
    application = Application.objects.filter(user = request.user)
    interview = Interviews.objects.filter(application__user = request.user)
    context = {
        'application' : application,
        'interviews' : interview
    }
    return render(request, 'RMS/user/dashboard-applied-jobs.html', context)

@login_required
def user_apply_job(request, slug):
    try: applied = Application.objects.get(user = request.user, job__slug = slug)
    except: applied = None

    try : candidate = Candidate.objects.get(user = request.user)
    except : candidate = None

    education = Education.objects.filter(candidate = request.user).count()
    
    if applied is not None:
        messages.error(request, 'You are already Applied on this JOB please Check your Applied Jobs Lists')
        return redirect(request.META.get('HTTP_REFERER'))
    elif candidate is None:
        messages.error(request, 'Please Add Personal Information! ')
        return redirect('user-resume')
    elif education < 1:
        messages.error(request, 'Please at least add One Education Background!')
        return redirect('user-add-education')
    else:
        job = Job_Posting.objects.get(slug=slug)
        obj = Application()
        obj.user = request.user
        obj.job = job
        obj.save()

        stop_event = threading.Event()
        background_thread = threading.Thread(target=handle_successfully_applied_send_email, args=(request,obj.user.first_name,obj.user.last_name, job.title, job.company.name, obj.user.email,stop_event ), daemon=True)
        background_thread.start()
        stop_event.set()

        messages.success(request, 'Successfully Applied Check your Applied Jobs')
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def user_cancel_job(request, slug):
    application = Application.objects.get(user = request.user, job__slug=slug)
    if application.delete():
        messages.success(request, 'Successfully Canceled')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Your request has not been Successfully please try again!')
        return redirect(request.META.get('HTTP_REFERER'))



#Bookmark
@login_required
def user_bookmark(request):
    bookmarks = Bookmarks.objects.filter(user = request.user)
    context = {
        'bookmarks' : bookmarks
    }
    return render(request, 'RMS/user/dashboard-saved-jobs.html', context)

@login_required
def user_add_bookmark(request, slug):
    try:
        check_job = Bookmarks.objects.get(job__slug = slug, user = request.user)
        check_job = True
    except: 
        check_job = False
    job = Job_Posting.objects.get(slug = slug)

    if check_job:
        messages.error(request, 'You already Bookmarked this job')
        return redirect(request.META.get('HTTP_REFERER'))    
    else:
        user = request.user
        obj = Bookmarks()
        obj.user = user
        obj.job = job
        obj.save()
        messages.success(request, 'Successfully Bookmarked')
        return redirect(request.META.get('HTTP_REFERER')) 

@login_required
def user_delete_bookmark(request, slug):
    job = Bookmarks.objects.get(job__slug=slug, user=request.user)

    if job.delete():
        messages.success(request, 'Successfully Removed')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Your request has not been Successfully please try again!')
        return redirect(request.META.get('HTTP_REFERER'))



#Interviewer
@login_required
@interviewer_user_required
def interviewer_dashboard(request):
    total_application = Application.objects.filter(user__company = request.user.company).count()
    total_jobs = Job_Posting.objects.filter(company = request.user.company).count()
    total_interviews = Interviews.objects.filter(interviewer = request.user).count()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    today_interviews = Interviews.objects.filter(~Q(application__status = 'canceled'), Q(status = 'scheduled') | Q(status = 'completed') , interviewer = request.user,date_schedule = date )
    applicant_status = Interviews.objects.filter()[:6]
    context = {
        'total_application' : total_application,
        'total_jobs' : total_jobs,
        'total_interview' : total_interviews,
        'today_interviews' : today_interviews,
        'applicant_status' : applicant_status
    }
    return render(request, 'RMS/interviewer/dashboard.html', context)

@login_required
@interviewer_user_required
def interviewer_job_list(request):
    job_lists = Job_Posting.objects.filter(job_status = True , company = request.user.company)
    context = {
        'job_lists' : job_lists
    }
    return render(request, 'RMS/interviewer/job-list.html', context)

@login_required
@interviewer_user_required
def interviewer_personal_info(request):
    form = InterviewerForm(request.POST or None, request.FILES or None, instance = request.user)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Information has been successfully updated')
            return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'form' : form
    }
    return render(request, 'RMS/interviewer/personal-info.html', context)

@login_required
@interviewer_user_required
def interviewer_job_detail(request, slug):
    job = Job_Posting.objects.get(slug=slug)

    context = {
        'job' : job,
    }
    return render(request, 'RMS/interviewer/job-detail.html', context)

@login_required
@interviewer_user_required
def interviewer_interviews_lists(request):
    interviews = Interviews.objects.filter(~Q(application__status = 'canceled'), status = 'pending', interviewer = request.user)
    context = {
        'interviews' : interviews,
    }
    return render(request, 'RMS/interviewer/interview.html', context)

@login_required
@interviewer_user_required
def interview_detail(request, slug):
    interview = Interviews.objects.get(slug = slug)
    user =  interview.application.user 
    education = Education.objects.filter(candidate = interview.application.user).select_related()
    experience = Experience.objects.filter(candidate = interview.application.user).select_related()
    project = Project.objects.filter(candidate = interview.application.user).select_related()
    language = Language.objects.filter(candidate = interview.application.user).select_related()


    interview_form = InterviewFormInterview(request.POST or None, instance=interview)
    job_status_form = ApplicationForm(request.POST or None, instance=interview.application)

    if request.method == 'POST':
        if interview_form.is_valid():
            obj = interview_form.save(commit=False)

            status =  0 if obj.status == None else 1 

            obj.status = 'scheduled'
            obj.save()

            time = str(interview.time_schedule.strftime('%I:%M %p'))

            stop_event = threading.Event()
            
            background_thread = threading.Thread(target=handle_scheduled_send_email if not status else handle_rescheduled_send_email, args=(request,user.first_name,
                                                                                           user.last_name, 
                                                                                           interview.application.job.title,
                                                                                           interview.application.job.company.name,
                                                                                           user.email,
                                                                                           interview.date_schedule,
                                                                                           time, 
                                                                                           interview.type, 
                                                                                           interview.application.job.company.address,
                                                                                           interview.interviewer.phone,
                                                                                           stop_event
                                                                                           ), 
                                                                                           daemon=True)
            background_thread.start()
            stop_event.set()
            
            messages.success(request, 'Successfully Scheduled. ')        
        return redirect('interview-scheduled')


    context = {
        'user' : user,
        'interview' : interview,
        'education': education,
        'experience' : experience,
        'project' : project,
        'language' : language,
        'interview_form' : interview_form,
        'job_status_form' : job_status_form
    }
    
    return render(request, 'RMS/interviewer/interview-detail.html', context)


@login_required
@interviewer_user_required
def interview_scheduled(request):
    interviews = Interviews.objects.filter(~Q(application__status = 'canceled'), status = 'scheduled', interviewer = request.user)

    context = {
        'interviews' : interviews,
    }

    return render(request, 'RMS/interviewer/interview-scheduled.html', context)

@login_required
@interviewer_user_required
def interview_today_interview_list(request):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
 
    interviews = Interviews.objects.filter(~Q(application__status = 'canceled'), Q(status = 'scheduled') | Q(status = 'completed') , interviewer = request.user,date_schedule = date )
    context = {
        'interviews' : interviews,
    }

    return render(request, 'RMS/interviewer/interview-scheduled.html', context)

@login_required
@interviewer_user_required
def interview_individual_now(request, slug):
    interview = Interviews.objects.get(slug = slug)
    user =  interview.application.user 
    education = Education.objects.filter(candidate = interview.application.user).select_related()
    experience = Experience.objects.filter(candidate = interview.application.user).select_related()
    project = Project.objects.filter(candidate = interview.application.user).select_related()
    language = Language.objects.filter(candidate = interview.application.user).select_related()
    interview_form = InterviewerNoteForm(request.POST or None, instance=interview)
    application_form = ApplicationForm()

    if request.method == 'POST':
        if interview_form.is_valid():
            obj = interview_form.save(commit=False)
            obj.status = 'completed'
            obj.save()
            messages.success(request, 'Successfully Completed. ')
            return redirect('interview-scheduled')

    context = {
        'interview' : interview,
        'user' : user,
        'education': education,
        'experience' : experience,
        'project' : project,
        'language' : language,
        'interview_form' : interview_form,
    }
    return render(request, 'RMS/interviewer/today-interview.html', context)

@login_required
@interviewer_user_required
def interview_candidate_job_status(request):
    interview = Interviews.objects.filter(status = 'completed', application__status= 'in_review')
    job_post = Job_Posting.objects.filter(job_status =True)
    sector = Sector.objects.filter()
    applicants = Interviews.objects.filter(application__status = 'in_review', status = 'completed')


    paginator = Paginator(interview,15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'sectors' : sector,
        'job_list' : job_post,
        'interview' : page,
        'applicants' : applicants
    }
    return render(request, 'RMS/interviewer/job-candidate-status.html', context)

@login_required
@interviewer_user_required
def interview_applicant_category(request, slug):
    selected_job = Job_Posting.objects.get(slug = slug)
    interview = Interviews.objects.filter(status = 'completed', application__status= 'in_review')
    job_post = Job_Posting.objects.filter(job_status =True)
    sector = Sector.objects.filter()
    applicants = Interviews.objects.filter(application__job = selected_job,application__status = 'in_review', status = 'completed')


    paginator = Paginator(interview,15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'sectors' : sector,
        'job_list' : job_post,
        'interview' : page,
        'applicants' : applicants
    }
    return render(request, 'RMS/interviewer/job-candidate-status.html', context)



@login_required
@interviewer_user_required
def company_interviewer_change_password(request):
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

    
    return render(request,'RMS/interviewer/change_password.html', {'form': form})  













import random


def validate_skill_list(request):
    try :
        candidate = Candidate.objects.get(user=request.user)
        user_skills = UserSkill.objects.filter(candidate=candidate)
    except:
        user_skills = None
    
    


    context = {
       "user_skills" : user_skills, 
    }
    

    
    return render(request , 'RMS/user/skill_validate_list.html', context)



def instruction(request , id):
    candidate = Candidate.objects.get(user=request.user)
    user_skill = UserSkill.objects.get(skill__id=id , candidate=candidate).skill
    questions = Question.objects.filter(for_skill=user_skill).count


    context = {
       "questions" : questions, 
       "skill" : user_skill,
    }
    

    
    return render(request , 'RMS/user/question_instruction.html', context)



def validate_skill(request , id):
    candidate = Candidate.objects.get(user=request.user)
    user_skills = UserSkill.objects.get(candidate=candidate , skill__id=id).skill
    questions = Question.objects.filter(for_skill=user_skills)[:5]
    questions_num = Question.objects.filter(for_skill=user_skills).count()

    count = 0 
    if request.method == 'POST':
        selected_answers = {}
        for question in questions:
            try :
                id = int(request.POST.get(f'choice_{question.id}'))
            except:
                id = None    
            if int(question.answer.id) == id:
              count = count + 1
        if int(count) >= int(questions.count() * 0.7):
            user_skills.validated = True
            user_skills.save()
            messages.success(request , "Congradulations You have answered {count} questions correctly from {questions_num} questions there for yout skill is verified.") 
        else :
            messages.error(request , "Sorry You have answered {count} questions correctly from {questions_num} questions there for you have faild the test try agian")        
        return redirect("validate_skill_list")    

    context = {
       "questions" : questions,
       'choices' : Choice.objects.all() ,
       "skill" : user_skills
    }
    

    
    return render(request , 'RMS/user/question.html', context)

