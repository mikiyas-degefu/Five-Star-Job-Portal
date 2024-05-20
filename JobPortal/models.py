from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from froala_editor.fields import FroalaField
from UserManagement.models import CustomUser
from django.utils.text import slugify
from unidecode import unidecode
from Company.models import Company
import datetime
from auditlog.registry import auditlog

#Candidate
gender_list = [
    ('male', 'Male'),
    ('female', 'Female'),
]



class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=gender_list)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=40)
    phone1 = PhoneNumberField()
    phone2 = PhoneNumberField(blank = True)
    address = models.CharField(max_length=100)
    linked_in = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='Candidate/photo', null=True, blank=True)
    about = models.TextField() 
    skill = models.ManyToManyField("Skill", blank=False) 
    slug = models.SlugField(unique=True, blank=True,  max_length=200)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name
    
    def age(self):
        date = datetime.datetime.now()
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.user.username))
        super().save(*args, **kwargs)

education_status_list = [
    ('highschool', 'High School'),
    ('Certificate', 'Certificate'),
    ('diploma', 'Diploma'),
    ('bachelor-degree', "Bachelor's degree"),
    ('Master-degree', "Master's Degree"),
    ('doctorate', "Doctorate"),
    ('other', 'Other')
]


class UserSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    skill = models.ForeignKey("Skill" ,  on_delete=models.CASCADE)
    validated = models.BooleanField(default=False)
   

    def __str__(self) -> str:
        return self.candidate.user.first_name + "" + self.skill.title

class Education(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    education_status = models.CharField(max_length=40, choices=education_status_list)
    field_of_study = models.CharField(max_length=40)
    education_period_start = models.DateField()
    education_period_end = models.DateField()
    gpa = models.FloatField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.candidate.username)) + "-" + slugify(unidecode(self.institution_name)) + "-" + slugify(unidecode(self.field_of_study))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.institution_name
    

class Experience(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=40)
    work_time_line_start =models.DateField()
    work_time_line_end = models.DateField()
    job_title = models.CharField(max_length=50)
    reference_phone = PhoneNumberField()
    reference_name = models.CharField(max_length=40)
    reference_email = models.CharField(max_length=40)
    reference_job_title = models.CharField(max_length=40)
    responsibility = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True,  max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.candidate.username)) +"-"+slugify(unidecode(self.company_name))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.company_name
    
class Project(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    project_type = models.CharField(max_length=40)
    detail = FroalaField()

    def __str__(self) -> str:
        return self.project_type

class Skill(models.Model):
    title = models.CharField(unique=True, max_length=30)
    slug = models.SlugField(unique=True, blank=True,  max_length=200)
    validable = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']
   
    def __str__(self) -> str:
        return self.title
    

language_proficient = [
    ('basic', 'Basic'),
    ('limited_working_proficiency', 'Limited Working Proficiency'),
    ('professional_working_proficiency', 'Professional Working Proficiency'),
    ('native_proficiency', "Native Proficiency"),
]

class Language(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=30)
    proficient = models.CharField(max_length=40, choices=language_proficient)

    class Meta:
        ordering = ['language']
   
    def __str__(self) -> str:
        return self.language
    
class Bookmarks(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey('Job_Posting', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,blank=True,  max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.user.username)) + "-" + slugify(unidecode(self.job.title))+ '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.job.title


class Sector(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True,  max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def count_job_post(self) -> int:
        count = Job_Posting.objects.filter(sector_id = self.id).count()
        return count
    
    def count_interview_completed(self) -> int:
        applicant = Interviews.objects.filter(status='completed', application__job__sector_id = self.id).count()
        return applicant


    def __str__(self) -> str:
        return self.name
        


job_type = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('freelance', 'Freelance'),
    ('internship', 'Internship'),
    ('seasonal ','seasonal'),
    ('contract', 'Contract'),
    ('remote', 'Remote'),
]

compensation_types = [
    ('monthly','Monthly'),
    ('yearly','Yearly'),
    ('hourly','Hourly'),
    ('commission','Commission'),
    ('bonus','Bonus'),
    ('benefits','Benefits')
]




CITY_CHOICES = (
        ('Addis Ababa', 'Addis Ababa'),
        ('Ērer Sātā', 'Ērer Sātā'),
        ('Shashemenē', 'Shashemenē'),
        ('K’ebrī Dehar', 'K’ebrī Dehar'),
        ('Nazrēt', 'Nazrēt'),
        ('Mekele', 'Mekele'),
        ('Godē', 'Godē'),
        ('Āwasa', 'Āwasa'),
        ('Dire Dawa', 'Dire Dawa'),
        ('Bahir Dar', 'Bahir Dar'),
        ('Sodo', 'Sodo'),
        ('Ārba Minch’', 'Ārba Minch’'),
        ('Desē', 'Desē'),
        ('Hosa’ina', 'Hosa’ina'),
        ('K’ebrī Beyah', 'K’ebrī Beyah'),
        ('Jijiga', 'Jijiga'),
        ('Dīla', 'Dīla'),
        ('Nek’emtē', 'Nek’emtē'),
        ('Debre Birhan', 'Debre Birhan'),
        ('Debre Mark’os', 'Debre Mark’os'),
        ('Ferfer', 'Ferfer'),
        ('Āwarē', 'Āwarē'),
        ('Harar', 'Harar'),
        ('Kombolcha', 'Kombolcha'),
        ('Jīma', 'Jīma'),
        ('Debre Tabor', 'Debre Tabor'),
        ('Harshin', 'Harshin'),
        ('Ādīgrat', 'Ādīgrat'),
        ('Debre Zeyit', 'Debre Zeyit'),
        ('Gambēla', 'Gambēla'),
        ('Mīzan Teferī', 'Mīzan Teferī'),
        ('Ādwa', 'Ādwa'),
        ('Gonder', 'Gonder'),
        ('Bodītī', 'Bodītī'),
        ('Āsela', 'Āsela'),
        ('Āksum', 'Āksum'),
        ('Bonga', 'Bonga'),
        ('Finote Selam', 'Finote Selam'),
        ('Semera', 'Semera'),
        ('Goba', 'Goba'),
        ('Hāgere Hiywet', 'Hāgere Hiywet'),
        ('Robē', 'Robē'),
        ('Yirga ‘Alem', 'Yirga ‘Alem'),
        ('Giyon', 'Giyon'),
        ('Bedēsa', 'Bedēsa'),
        ('Āzezo', 'Āzezo'),
        ('Butajīra', 'Butajīra'),
        ('Ālamat’ā', 'Ālamat’ā'),
        ('Āreka', 'Āreka'),
        ('Gīmbī', 'Gīmbī'),
        ('Wik’ro', 'Wik’ro'),
        ('Welk’īt’ē', 'Welk’īt’ē'),
        ('Metu', 'Metu'),
        ('Fichē', 'Fichē'),
        ('K’olīto', 'K’olīto'),
        ('Genet', 'Genet'),
        ('Āgaro', 'Āgaro'),
        ('Gelemso', 'Gelemso'),
        ('Āsosa', 'Āsosa'),
    )

    
class Job_Posting(models.Model):
    company = models.ForeignKey(Company , on_delete=models.CASCADE , null=True , blank=True)
    title = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)  # Related With Sector
    description = FroalaField()
    vacancies = models.IntegerField()
    experience = models.CharField(max_length=20)
    skills = models.ManyToManyField(Skill)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, choices=CITY_CHOICES , default=True)
    salary_range_start = models.FloatField()
    salary_range_final = models.FloatField()
    type = models.CharField( choices=job_type, max_length=30)
    compensation_type = models.CharField( choices=compensation_types, max_length=30 , blank=True , null=True)
    job_status = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(auto_now=False , auto_now_add=False)
    slug = models.SlugField(unique=True,  max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.title)) + slugify(unidecode(self.company.name)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
  
    class Meta:
        ordering = ['sector', '-date_posted','-date_closed']

    def count_applicant(self) -> int:
        applicant = Application.objects.filter(job__id = self.id).count()
        return applicant
    
    def count_interview_pending(self) -> int:
        applicant = Application.objects.filter(status='pending', job__id = self.id).count()
        return applicant
    
    def count_interview_completed(self) -> int:
        applicant = Interviews.objects.filter(status='completed', application__job__id = self.id).count()
        return applicant

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

application_status = [
    ('pending', 'Pending'),
    ('in_review', 'In Review'),
    ('rejected', 'Rejected'),
    ('hired', 'Hired')
]

class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Related with Candidate
    job = models.ForeignKey(Job_Posting, on_delete=models.SET_NULL, null=True)  # Related with Job_Post
    cover_letter = FroalaField(null =True, blank = True)
    read = models.BooleanField(default=False)
    date_applied = models.DateField(auto_now_add=True) # Select Option from application_status
    status = models.CharField(max_length=15, choices=application_status, default='pending')
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=200)
    cover_letter = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.user.username)) + '-' + slugify(unidecode(self.job.title)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.user.username)+" - "+str(self.job)
    
    class Meta:
       ordering = ['-date_applied']

interview_status = [
    ('pending', 'Pending'),
    ('scheduled', 'Scheduled'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
]

job_status_interview = [
    ('pending', 'Pending'),
    ('rejected', 'Rejected'),
    ('hired', 'hired'),
]

interview_type = [
    ('phone', 'Phone'),
    ('in-person', 'In-Person'),
    ('video', 'Video')
]

class Interviews(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, null=True, blank=True)
    interviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Related with User
    date_schedule = models.DateField(null=True, blank=True)
    time_schedule = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=interview_status, default='pending', null=True, blank=True)
    type = models.CharField(max_length=15, choices=interview_type, null=True, blank=True)
    note = FroalaField( null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=600)
    read = models.BooleanField(default=False)

    try:
        def save(self, *args, **kwargs):
            if not self.slug:
                now = datetime.datetime.now()
                self.slug = slugify(unidecode(self.application.user.username)) + '-' + slugify(unidecode(self.interviewer.username)) + '-' + slugify(unidecode(self.application.job.title))+ '-' + now.strftime("%Y-%m-%d")
            super().save(*args, **kwargs)
    except: None
    def __str__(self) -> str:
        return self.interviewer.username + '-'+self.application.user.username
    
    class Meta:
       ordering = ['date_schedule']




auditlog.register(Candidate)
auditlog.register(Skill)
auditlog.register(Sector)
auditlog.register(Job_Posting)
    






class Choice(models.Model):
    text = models.CharField(max_length=150)
    for_question = models.ForeignKey("Question" ,on_delete=models.SET_NULL , null=True)

    
    def __str__(self) -> str:
        return str(self.text)

class Question(models.Model):
    text = models.CharField(max_length=200)
    for_skill = models.ForeignKey(Skill , on_delete=models.SET_NULL , null=True)
    answer = models.ForeignKey(Choice , on_delete=models.SET_NULL , null=True)

    def __str__(self) -> str:
        return str(self.text)




