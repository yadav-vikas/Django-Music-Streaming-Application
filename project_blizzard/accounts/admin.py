from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Account, Profile, EmailVerification

admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(EmailVerification)