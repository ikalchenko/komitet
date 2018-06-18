from django.contrib.auth.models import User
from django.db import models

from users.models import UserPermissions


class Committee(models.Model):
    members = models.ManyToManyField(User, through=UserPermissions)
    title = models.CharField(max_length=50)
    access_code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
