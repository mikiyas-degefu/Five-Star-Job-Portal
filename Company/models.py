from django.db import models
from froala_editor.fields import FroalaField

# Create your models here.
class CompanyCatagory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    about = FroalaField()
    email = models.EmailField( max_length=254)
    address = models.CharField(max_length=100)
    phone = models.TextField()
    since = models.DateField(auto_now=False, auto_now_add=False , null=True , blank=True)
    views = models.IntegerField(default=0)
    total_jobs = models.IntegerField(default=0)
    location = models.CharField(max_length=100) 
    website = models.URLField(max_length=200,null=True , blank=True)

    def __str__(self):
        return self.name
    

