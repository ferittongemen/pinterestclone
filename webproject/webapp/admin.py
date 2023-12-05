from django.contrib import admin
from . import models
# Register your models here.


class WebAppAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Photo Group',{"fields":["image"]}),
        ('Nickname Group',{"fields":["username"]}),
        ('Description Group',{"fields":["description"]}),   
    ]


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Username Group',{"fields":["username"]}),
        ('Biography Group',{"fields":["bio"]}),
        ('Profile Pictur Group',{"fields":["profile_picture"]}), 
        ('Hobies Group',{"fields":["hobies"]})  
    ]


admin.site.register(models.UserProfile)
admin.site.register(models.WebAppModel)