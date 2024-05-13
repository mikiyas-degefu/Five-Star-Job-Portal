from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin #Admin 
from JobPortal.resource import CompanyResource
# Register your models here.

admin.site.register(models.Blog)
admin.site.register(models.Blog_Categories)
admin.site.register(models.Comment)
admin.site.register(models.Contact)
admin.site.register(models.Social_Media)
admin.site.register(models.Contact_Message)
admin.site.register(models.FAQ)


class CompanyAdmin(ImportExportModelAdmin):
    list_display = ['name', 'active', 'views', 'total_jobs']
    resource_classes = [CompanyResource]

admin.site.register(models.Company, CompanyAdmin)