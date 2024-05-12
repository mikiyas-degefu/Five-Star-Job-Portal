import telebot, os
from import_export import resources
from Company.models import Company
from .models import (Sector, Job_Posting, Skill, Application)
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget  # For foreignkey
from UserManagement.models import CustomUser

import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



######
####TELEGRAM  


BOT_TOKEN = os.environ.get('6195701188:AAGYJvuebbXWUatD4MtOwJ8NNASCdMlXjwE')
bot = telebot.TeleBot('6195701188:AAGYJvuebbXWUatD4MtOwJ8NNASCdMlXjwE')
channel_name = '@act_job_board'


def handle_telegram_post(request,slug,company_name, title, sector, vacancies, type, experience, description, skills, location, date_closed, salary_range_start, salary_range_final, stop_event):
    while not stop_event.is_set():
        text = f'''
SERAYE - JOB PORTAL\n
- Company: {company_name}\n
- Job Title: {title}\n
- Sector: {sector}\n
- Vacancies: {vacancies}\n
- Job Type: {type}\n
- Experience: {experience}\n
- Description: {description}\n
- Skills: {skills}\n
- Location: {location}\n
- Date Close: {date_closed}\n
- Salary: {salary_range_start} - {salary_range_final}\n    
- Link: http://127.0.0.1:8000/job-detail/{slug}\n          
             '''
        try: bot.send_message(chat_id=channel_name, text=text)
        except Exception as e:
            None



######
#### EMAIL
def handle_registration_email(request,email,first_name,last_name,email_type,stop_event, company_name = None):
    while not stop_event.is_set():
        subject, from_email, to = 'Registration Successful', 'mikiyasmebrate2656@gmail.com', f"{email}"
        text_content = "Registration Successful"
        context = {
            'first_name': first_name,
            'last_name' : last_name,
            'email' : email,
            'company_name' : company_name,
            'company_email' : email
        }

        if email_type == 'company':
            html_content = render_to_string('success-email-company.html',context)
        elif email_type == 'candidate':
            html_content = render_to_string('success-email.html',context)
        elif email_type == 'company_activations':
            html_content = render_to_string('company-account-activated.html',context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            print('Email sent')

def handle_inactive_send_email(request, company_name, company_email, stop_event):
    while not stop_event.is_set():
        content = f'''
                <p>  Dear {company_name}, </p>
    
                <p>We're reaching out regarding your account with Seraye Job Portal. We noticed that your account has been inactive for some time, and additionally, we identified some inaccuracies in a previously posted job listing.</p>
    
                <p> Maintaining accurate job postings is crucial for both job seekers and employers on our platform. To ensure a positive experience for everyone</p>
    
                <h4> No longer need your account?</h4>
                <p>If you no longer wish to use [Company Name], there's no need to take any action. However, please note that inactive accounts are automatically deleted after 30 days, along with any associated data, in accordance with our data privacy policy</p>
    
                <h4>Support and Assistance:</h4>
                <p>If you have any questions about reactivating your account, updating your job postings, or our job board in general, our friendly support team is happy to help! You can reach them at seraye@gmail.com or by phone at +251942274410.</p>
    
                <p> We look forward to having you back on {company_name} and helping you connect with top talent!</p>
                <p> Sincerely,</p> 
                <p> The Seraye Job Portal Team </p> '''
        
        subject = f'{company_name} Account Deactivated - Update Job Postings to Re-activate'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = company_email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True
        

def handle_successfully_applied_send_email(request, fist_name, last_name, job_title,company_name,user_email,stop_event):
    while not stop_event.is_set():
        content = f'''
                <p>  Dear {fist_name} {last_name}, </p>
    
                <p>This email confirms that your application for the {job_title} position at {company_name} has been successfully submitted through Seraye Job Portal.</p>
    
                <p> We've forwarded your application directly to the hiring manager at  {company_name}. They will review your qualifications and reach out to you if they'd like to schedule an interview.</p>
    
                <p> We wish you the best of luck in your job search!</p>
                <p> Sincerely,</p> 
                <p> The Seraye Job Portal Team </p> '''
        
        subject = f'Successfully Applied for {job_title} at {company_name}!'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = user_email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True
        

def handle_rejected_send_email(request, fist_name, last_name, job_title,company_name,user_email,stop_event):
    while not stop_event.is_set():
        content = f'''
                <p>Dear {fist_name} {last_name}, </p>
    
                <p>Thank you for your interest in the {job_title} position at {company_name} that you applied for through Seraye Job Portal. We appreciate you taking the time to submit your application and learn more about our company.</p>
    
                <p>After careful consideration, we have decided to move forward with other candidates whose experience more closely aligns with the specific requirements of this role.</p>
                
                <h4>Here are some resources that may be helpful in your job search:</h4>
                
                <p> - You can access your dashboard to review your applications, update your profile, and explore other job opportunities (http://127.0.0.1:8000/user-dashboard/).</p>
                <p> - We offer a variety of resources to help with your job search, including interview tips and resume writing guides (http://127.0.0.1:8000/user-profile/).</p>
    
                <p> We encourage you to keep your profile updated on Seraye Job Portal as we frequently post new job openings. We wish you the very best of luck in your job search!</p>
                <p> Sincerely,</p> 
                <p> {company_name} Team </p>
                <p> Seraye Job Portal</p> '''
        
        subject = f'Application Update: {job_title} at {company_name}!'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = user_email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True
        

def handle_scheduled_send_email(request, fist_name, last_name, job_title,company_name,user_email,date,time,interview_type,company_location,interviewer_phone,stop_event):
    while not stop_event.is_set():
        content = f'''
                <p>Dear {fist_name} {last_name}, </p>
    
                <p>We're thrilled to inform you that your application for the {job_title} position at {company_name} has been shortlisted! Your background truly impressed us, and we're eager to learn more about how you can contribute to our team.</p>
    
                <p>Consider this a personal invitation to interview for the position on {date} at {time} {interview_type} interview. The interview will be held {company_location} or contact us {interviewer_phone}.</p>
                
                <h4>We look forward to meeting you and discussing this opportunity further!</h4>
                
                <p> Sincerely,</p> 
                <p> {company_name} Team </p>
                <p> Seraye Job Portal</p> '''
        
        subject = f'Application Update: {job_title} at {company_name}!'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = user_email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True

def handle_rescheduled_send_email(request, fist_name, last_name, job_title,company_name,user_email,date,time,interview_type,company_location,interviewer_phone,stop_event):
    while not stop_event.is_set():
        content = f'''
                <p>Dear {fist_name} {last_name}, </p>
    
                <p>We are writing to inform you that we need to reschedule your interview for the {job_title} position at {company_name}. We sincerely apologize for any inconvenience this may cause.</p>
    
                <p>We would like to reschedule your interview for {date} at {time}. The interview will still be held {interview_type}, {company_location} or contact us {interviewer_phone}.</p>
                
                <h4>We look forward to meeting you soon!</h4>
                
                <p> Sincerely,</p> 
                <p> {company_name} Team </p>
                <p> Seraye Job Portal</p> '''
        
        subject = f'Application Update: {job_title} at {company_name}!'
        from_email = 'mikiyasmebrate2656@gmail.com'
        to_email = user_email
        text_content = '<!DOCTYPE html>'
        html_content = content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            return True
        



######
## IMPORT EXPORT ##


class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        exclude = ('id', 'password')


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        exclude = ('id', 'logo')


class SkillResource(resources.ModelResource):
    class Meta:
        model = Skill
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'slug')
        import_id_fields = ('title', 'validable')


class SectorResource(resources.ModelResource):
    class Meta:
        model = Sector
        exclude = ('id', 'slug')

class JobResource(resources.ModelResource):
    company = fields.Field(
        column_name='company',
        attribute='company',
        widget=ForeignKeyWidget(Company, field='name'),
        saves_null_values = True,
        )
    sector = fields.Field(
        column_name='sector',
        attribute='sector',
        widget=ForeignKeyWidget(Sector, field='name'),
        saves_null_values = True,
        )
    class Meta:
        model = Job_Posting
        exclude = ('id', 'slug')


class ApplicationResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(CustomUser, field='first_name'),
        saves_null_values = True,
        )
    job = fields.Field(
        column_name='job',
        attribute='job',
        widget=ForeignKeyWidget(Job_Posting, field='title'),
        saves_null_values = True,
        )
    class Meta:
        model = Application
        exclude = ('id', 'slug')








        