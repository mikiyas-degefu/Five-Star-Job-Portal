import telebot, os
import threading


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


        