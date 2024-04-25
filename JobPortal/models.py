from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from froala_editor.fields import FroalaField
from UserManagement.models import CustomUser
from django.utils.text import slugify
from unidecode import unidecode
from Company.models import Company
import datetime
#Candidate
gender_list = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=gender_list)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=40)
    phone1 = PhoneNumberField()
    phone2 = PhoneNumberField(blank = True)
    address = models.CharField(max_length=100)
    linked_in = models.URLField(blank=True, null=True)
    git_hub = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to='Candidate/photo', null=True, blank=True)
    resume = models.FileField(upload_to='Candidate/Resume', null=True, blank=True)
    about = models.TextField()
    skill = models.ManyToManyField("Skill", blank=False) 
    slug = models.SlugField(unique=True, blank=True,  max_length=200)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
    
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

class Education(models.Model):
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    education_status = models.CharField(max_length=40, choices=education_status_list)
    field_of_study = models.CharField(max_length=40)
    education_period_start = models.DateField()
    education_period_end = models.DateField()
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

class Skill(models.Model):
    title = models.CharField(unique=True, max_length=30)
    slug = models.SlugField(unique=True, blank=True,  max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']
   
    def __str__(self) -> str:
        return self.title
    
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


class Job_Posting(models.Model):
    company = models.ForeignKey(Company , on_delete=models.CASCADE , null=True , blank=True)
    title = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)  # Related With Sector
    description = FroalaField()
    vacancies = models.IntegerField()
    experience = models.CharField(max_length=20)
    skills = models.ManyToManyField(Skill)
    location = models.CharField(max_length=200)
    salary_range_start = models.FloatField()
    salary_range_final = models.FloatField()
    type = models.CharField( choices=job_type, max_length=30)
    job_status = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateField()
    slug = models.SlugField(unique=True,  max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.title)) + slugify(unidecode(self.company.name)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
  
    class Meta:
        ordering = ['-date_posted','-date_closed']

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

application_status = [
    ('pending', 'Pending'),
    ('in_review', 'In review'),
    ('rejected', 'Rejected'),
    ('hired', 'Hired')
]

class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Related with Candidate
    job = models.ForeignKey(Job_Posting, on_delete=models.SET_NULL, null=True)  # Related with Job_Post
    date_applied = models.DateField(auto_now_add=True) # Select Option from application_status
    status = models.CharField(max_length=15, choices=application_status, default='pending')
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=200)

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
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    interviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Related with User
    date_schedule = models.DateField(null=True, blank=True)
    time_schedule = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=interview_status, default='pending', null=True, blank=True)
    type = models.CharField(max_length=15, choices=interview_type, null=True, blank=True)
    note = FroalaField( null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=600)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.application.user.username)) + '-' + slugify(unidecode(self.interviewer.username)) + '-' + slugify(unidecode(self.application.job.title))+ '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        return self.interviewer.username + '-'+self.application.user.username
    
    class Meta:
       ordering = ['date_schedule']



    

