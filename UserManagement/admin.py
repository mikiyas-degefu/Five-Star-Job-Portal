from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from import_export.admin import ImportExportModelAdmin #Admin 
from JobPortal.resource import UserResource
from .models import CustomUser
# Register your models here.



class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = ['username','first_name', 'last_name' , 'is_active' ,'email', 'company', 'is_candidate', 'is_admin','is_interviewer' ,'is_superuser',]

admin.site.register(CustomUser, UserAdmin)

