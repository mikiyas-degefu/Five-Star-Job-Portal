import telebot, os
from import_export import resources
from Company.models import Company
from .models import (Sector, Job_Posting, Skill)
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget  # For foreignkey
from UserManagement.models import CustomUser

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
        exclude = ('id', 'slug')


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








        