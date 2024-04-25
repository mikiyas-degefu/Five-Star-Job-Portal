from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class AdminCustomUSer(admin.ModelAdmin):
    list_display = ['company']

