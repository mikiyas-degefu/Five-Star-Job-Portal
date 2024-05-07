from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from import_export.admin import ImportExportModelAdmin #Admin 
from JobPortal.resource import UserResource
from .models import CustomUser
# Register your models here.



class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = ['company']

admin.site.register(CustomUser, UserAdmin)

