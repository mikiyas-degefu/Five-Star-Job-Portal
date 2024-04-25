from django.contrib import admin
from . import models
# Register your models here.





class MyModelAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(models.Candidate)
admin.site.register(models.Education)
admin.site.register(models.Experience)
admin.site.register(models.Skill, MyModelAdmin)
admin.site.register(models.Bookmarks)
admin.site.register(models.Sector)
admin.site.register(models.Job_Posting)
admin.site.register(models.Application)
admin.site.register(models.Interviews)
