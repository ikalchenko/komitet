from django.contrib import admin

from .models import UserPermissions, UserProfile

admin.register(UserPermissions)
admin.register(UserProfile)
