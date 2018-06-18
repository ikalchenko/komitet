import django.contrib.auth.models as auth_models
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE, default=None)
    photo = models.ImageField()


class UserPermissions(models.Model):
    PERMISSIONS = (
        ('A', 'Admin'),
        ('RW', 'Read/Write'),
        ('R', 'Read'),
        ('B', 'Banned'),
    )
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    committee = models.ForeignKey('komitets.Committee', on_delete=models.CASCADE)
    permission = models.CharField(max_length=2, choices=PERMISSIONS)
