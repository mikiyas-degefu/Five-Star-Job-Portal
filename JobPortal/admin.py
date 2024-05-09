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
<<<<<<< HEAD
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.UserSkill)
=======
admin.site.register(models.Language)
admin.site.register(models.Project)


class SectorAdmin(ImportExportModelAdmin):
    resource_classes = [SectorResource]

admin.site.register(models.Sector, SectorAdmin)


class JobAdmin(ImportExportModelAdmin):
    resource_classes = [JobResource]

admin.site.register(models.Job_Posting, JobAdmin)


class SkillAdmin(ImportExportModelAdmin):
    resource_classes = [SkillResource]

admin.site.register(models.Skill, SkillAdmin)
>>>>>>> 69c72478d577c5cb7ee679a2e902bf9bea82e8b7
