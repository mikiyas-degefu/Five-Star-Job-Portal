from django.db import models
from django.contrib.auth.models import AbstractUser
from Company.models import Company 
# Create your models here.
class CustomUser(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_interviewer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender_list = [
    ('male', 'Male'),
    ('female', 'Female'),
]
    gender = models.CharField( max_length=50  , choices=gender_list)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False , null=True , blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='User/Photo', null=True, blank=True)
    company = models.ForeignKey(Company ,  on_delete=models.SET_NULL , null=True , blank=True)
    address = models.CharField(max_length=100)
    linked_in = models.URLField(max_length=200)
    country = models.CharField( max_length=50)
    city = models.CharField( max_length=50)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','username','last_name']


    def __str__(self):
        return self.first_name + " " +  self.last_name 
    