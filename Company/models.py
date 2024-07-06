from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from unidecode import unidecode
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from auditlog.registry import auditlog

# Create your models here.


# Create your models here.
class CompanyCatagory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="company/logo", null=True, blank=True)
    slogan = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=False)
    about = FroalaField()
    email = models.EmailField( max_length=254)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField()
    since = models.DateField(auto_now=False, auto_now_add=False , null=True , blank=True)
    views = models.IntegerField(default=0)
    total_jobs = models.IntegerField(default=0)
    website = models.URLField(max_length=200,null=True , blank=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_created']

    
    

#Blog 
class Blog_Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True,blank=True, editable=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.name)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
    
    def count_categories(self):
        return Blog.objects.filter(__type = self.name).count()
    
    def __str__(self) -> str:
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    image = models.ImageField(upload_to='blog/')
    description = models.CharField(max_length=400)
    content = FroalaField()
    type = models.ManyToManyField(Blog_Categories)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            now = datetime.datetime.now()
            self.slug = slugify(unidecode(self.title)) + '-' + now.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
    
    def count_comment(self):
        return Comment.objects.filter(blog = self.id).count()
    
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    comment = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return self.name

#Contact 
class Contact(models.Model):
    phone = PhoneNumberField()
    email = models.EmailField()
    location = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.email

class Social_Media(models.Model):
    name = models.CharField(max_length=30)
    link = models.URLField()

    def __str__(self) -> str:
        return self.name


class Contact_Message(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-created_at'] #New's First



class FAQ(models.Model):
    question = models.CharField(max_length=70)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self) -> str:
        return self.question
    
    class Meta:
        ordering = ['-created_at'] #New's First



auditlog.register(CompanyCatagory)
auditlog.register(Blog_Categories)
auditlog.register(Blog)
auditlog.register(Social_Media)



