from django.contrib import admin

from .models import User, UserPermissions, UserProfile

admin.register(User)
admin.register(UserPermissions)
admin.register(UserProfile)
