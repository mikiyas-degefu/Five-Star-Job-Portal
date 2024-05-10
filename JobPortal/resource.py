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
        

def handle_successfully_applied_send_email(request, company_name, company_email, stop_event):
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








        