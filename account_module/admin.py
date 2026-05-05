from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account_module.models import User

# Register your models here.

admin.site.register(User)