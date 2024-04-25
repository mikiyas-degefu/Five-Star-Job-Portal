from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from Company.models import Social_Media, Contact
from .forms import CandidateForm, EducationForm, ExperienceForm, InterviewerForm as InterviewFormInterview, ApplicationForm, InterviewerNoteForm
from .models import Skill,Sector, Candidate, Education, Experience, Job_Posting, Bookmarks, Application,Interviews
from django.contrib import messages
import csv
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from UserManagement.forms import CustomUserCreationForm, Login_Form, InterviewerForm
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
from UserManagement.decorators import interviewer_user_required
from django.core.mail import send_mail, EmailMultiAlternatives
import os
import telebot
import requests
from bs4 import BeautifulSoup


def scrap_skill():
    url = 'https://www.freelancer.com/job/'
    
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    
    skill = soup.find_all('a', {'class': 'PageJob-category-link PageJob-category-link--contest'})#.attrs.get('title')
    skill2 = soup.find_all('a', {'class' : 'PageJob-category-link'})
    for i in skill2:
        k = i.attrs.get('title')
        skill_list = k.replace('Contests', "")
        obj = Sector()
        obj.name = skill_list
        try: obj.save()
        except: pass

def csv_file_reader():
    with open('skill_data.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            for j in i:
                    Skill.objects.create(title = j)

social_medias = Social_Media.objects.all()

#Session
def login_view(request):
    form = Login_Form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email,password=password)
        if (user is not None and user.is_superuser) or (user is not None and user.is_admin):
            login(request, user)
            return redirect('admin-dashboard')
        elif user is not None and user.is_interviewer:
            login(request, user)
            return redirect('interviewer-dashboard')
        elif user is not None and user.is_candidate:
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

def registration_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_candidate = True
            user.save()
            messages.success(request, 'Your Account has been Successfully Created! Please Login')
            return redirect('/login')    
    context = {
        'form' : form
    }

    return render(request, 'RMS/registrations.html', context)



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
    print(count_skill)
    sector = Sector.objects.all()
    sector_popular = Sector.objects.all()[0:5]
    job = Job_Posting.objects.filter(job_status = True)
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
        'sector_popular' : sector_popular
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
    paginator = Paginator(job,5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'social_medias' : social_medias,
        'job_list' : page,
        'bookmark' : bookmark,
        'candidate' : candidate,
        'application' : application,
        'sector' : sector_new,
        'sector_popular' : sector_popular
    }
    return render(request, 'RMS/job-list.html', context)


def job_sector_categories(request, slug):
    try: bookmark = Bookmarks.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: bookmark = None
    try: candidate = Candidate.objects.get(user = request.user)
    except: candidate = None
    try: application = Application.objects.filter(user=request.user).values_list('job__id', flat=True)
    except: application = None


    
 
    sector_popular = Sector.objects.all()[0:5]
    sector1 = Sector.objects.get(slug = slug)
    sector = Sector.objects.all()
    job = Job_Posting.objects.filter(job_status = True, sector = sector1)

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
        'sector_popular' : sector_popular
    }
    return render(request, 'RMS/job-list.html', context)


def job_detail(request, slug):
    job = Job_Posting.objects.get(slug=slug)
    company_info = Contact.objects.all().first()
    social_media = Social_Media.objects.all().first()

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
    except:
        candidate = None 
        education = None
        experience = None
    
    context = {
        'candidate' : candidate,
        'social_medias' : social_medias,
        'education' : education,
        'experience': experience
        
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
        check_job = Bookmarks.objects.get(job_slug = slug, user = request.user)
    except: 
        check_job = False
    job = Job_Posting.objects.get(slug = slug)

    if check_job:
        messages.error(request, 'You are already Bookmarked')
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
    total_application = Application.objects.all().count()
    total_jobs = Job_Posting.objects.all().count()
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
    job_lists = Job_Posting.objects.filter(job_status = True)
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
    education = Education.objects.filter(candidate = interview.application.user)
    experience = Experience.objects.filter(candidate = interview.application.user)
    interview_form = InterviewFormInterview(request.POST or None, instance=interview)
    job_status_form = ApplicationForm(request.POST or None, instance=interview.application)

    if request.method == 'POST':
        if interview_form.is_valid():
            obj = interview_form.save(commit=False)
            obj.status = 'scheduled'
            obj.save()
            time = str(interview.time_schedule.strftime('%I:%M %p'))
            
            content = f'''
             <p>  Hi {interview.application.user.first_name} {interview.application.user.last_name} </p>

             <p> Your interview is scheduled for {interview.date_schedule} at {time} in the position of {interview.application.job.title} and will take place at our office located at {interview.application.job.location}. 
               Please plan to arrive a few minutes early to allow time for check-in.</p>

             <p> During the interview, you'll have the opportunity to meet with our team and learn more about the position and our company culture. We're excited to get to know you better
               and learn about your experience and qualifications.</p>

            <p> Best regards,</p>
            <p> {interview.interviewer.first_name} {interview.interviewer.last_name},</p>
            <p> ACT American College Of Technology HR </p> '''

            def send_email_interview_schedule():
                subject = 'Interview Schedule'
                from_email = 'mikiyasmebrate2656@gmail.com'
                to_email = interview.application.user.candidate.email
                text_content = '<!DOCTYPE html>'
                html_content = content
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                if msg.send():
                    messages.success(request, 'Successfully email sent.')

            send_email_interview_schedule()
            messages.success(request, 'Successfully Scheduled. ')
        
        if job_status_form.is_valid():
            obj1 = job_status_form.save(commit=False)
            value = obj1.status
            obj1.save()
            if value == 'hired':
                content = f'''
                        <p> Hi {interview.application.user.first_name} {interview.application.user.last_name}, </p>
                          
                        <p> I'm thrilled to inform you that you've been selected for the {interview.application.job.title} role at ACT American College of Technology! 
                            On behalf of the entire team, I want to congratulate you and welcome you to our organization.</p>
                          
                        <p> We were impressed by your skills, experience, and enthusiasm for the role. We believe that you'll be a valuable addition to our team and contribute
                            greatly to our mission.</p>
                          
                        <p>In the coming days, you'll receive an email from our HR department with details about your start date, onboarding process, and other important information.
                           If you have any questions in the meantime, please don't hesitate to reach out to me directly.</p>
                          
                        <p> Once again, congratulations on your new role, and we look forward to having you on board! </p>
                          
                         <p> Best regards,</p>
                          
                        <p> {interview.interviewer.first_name} {interview.interviewer.last_name},</p>
                        <p> ACT American College Of Technology HR </p>
                          
                     '''
            elif value == 'rejected':
                content = f'''
                        <p>Dear {interview.application.user.first_name} {interview.application.user.last_name}, </p>

                        <p>Thanks you for taking the time to meet with our team for the role of {interview.application.job.title}.
                        It was a pleasure to learn about your skill and accomplishments.</p>

                        <p>We received a large number of job applications and after carefully reviewing all of them. we unfortunately 
                        have to inform you that we will be selecting another candidate at this time.</P>

                        <p>We want to note that competition for jobs is strong and that we often have to make difficult choices between 
                        many high-caliber candidates. Now that we've had chance to know more about your skills, we will be keeping
                        your resume on file for future openings. </p>

                        <p>We wish you every personal and professional success in your endeavors. Please fell free to reach out
                        to us if you have any questions. </p> 

                        <p> Best regards,</p>
                          
                        <p> {interview.interviewer.first_name} {interview.interviewer.last_name},</p>
                        <p> ACT American College Of Technology HR </p>
                        '''

            def send_email_interview_schedule():
                subject = 'Interview Schedule'
                from_email = 'mikiyasmebrate2656@gmail.com'
                to_email = interview.application.user.candidate.email
                text_content = '<!DOCTYPE html>'
                html_content = content
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                if msg.send():
                    messages.success(request, 'Successfully email sent.')


            send_email_interview_schedule()
            messages.success(request, f'Successfully {value}')
        
        return redirect('interview-scheduled')


    context = {
        'interview' : interview,
        'educations': education,
        'experiences' : experience,
        'interview_form' : interview_form,
        'job_status_form' : job_status_form
    }
    return render(request, 'RMS/interviewer/interview-detail.html', context)

@login_required
@interviewer_user_required
def interview_cancel(request, slug):
    interview = Interviews.objects.get(slug = slug)
    application = Application.objects.get(id = interview.application.id)

    application.status = 'rejected'
    interview.status = 'canceled'
    
    application.save()
    interview.save()
    content = f'''
              <p>Dear {interview.application.user.first_name} {interview.application.user.last_name}, </p>

              <p>Thanks you for taking the time to meet with our team for the role of {interview.application.job.title}.
              It was a pleasure to learn about your skill and accomplishments.</p>

              <p>We received a large number of job applications and after carefully reviewing all of them. we unfortunately 
              have to inform you that we will be selecting another candidate at this time.</P>

              <p>We want to note that competition for jobs is strong and that we often have to make difficult choices between 
              many high-caliber candidates. Now that we've had chance to know more about your skills, we will be keeping
              your resume on file for future openings. </p>

              <p>We wish you every personal and professional success in your endeavors. Please fell free to reach out
              to us if you have any questions. </p>

              <p> Best regards,</p>
                          
             <p> {interview.interviewer.first_name} {interview.interviewer.last_name},</p>
            <p> ACT American College Of Technology HR </p>
 
'''

    def send_email_interview_schedule():
        subject = 'Interview Feedback'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = interview.application.user.candidate.email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            messages.success(request, 'Email Successfully sent.')

    send_email_interview_schedule()
            
    messages.success(request, 'Successfully Cancelled')
    return redirect('interviewer-interviews-list')

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
    education = Education.objects.filter(candidate = interview.application.user)
    experience = Experience.objects.filter(candidate = interview.application.user)
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
        'educations': education,
        'experiences' : experience,
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
