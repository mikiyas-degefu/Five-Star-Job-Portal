from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin #Admin 
from .resource import (SectorResource, JobResource, SkillResource)
# Register your models here.





class MyModelAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(models.Candidate)
admin.site.register(models.Education)
admin.site.register(models.Experience)
admin.site.register(models.Bookmarks)
admin.site.register(models.Application)
admin.site.register(models.Interviews)


class SectorAdmin(ImportExportModelAdmin):
    resource_classes = [SectorResource]

admin.site.register(models.Sector, SectorAdmin)


class JobAdmin(ImportExportModelAdmin):
    resource_classes = [JobResource]

admin.site.register(models.Job_Posting, JobAdmin)


class SkillAdmin(ImportExportModelAdmin):
    resource_classes = [SkillResource]

admin.site.register(models.Skill, SkillAdmin)