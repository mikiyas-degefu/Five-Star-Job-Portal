from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Blog)
admin.site.register(models.Blog_Categories)
admin.site.register(models.Comment)
admin.site.register(models.Contact)
admin.site.register(models.Social_Media)
admin.site.register(models.Contact_Message)
admin.site.register(models.Company)