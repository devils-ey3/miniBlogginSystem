from django.contrib import admin
# Register your models here.
from .models import UserProfile

admin.site.register(UserProfile) #add account section to localhost/admin