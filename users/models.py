from django.db import models
from django.contrib.auth.models import User
from komitets.models import Committee


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    photo = models.ImageField()


class UserPermissions(models.Model):
    PERMISSIONS = (
        ('A', 'Admin'),
        ('RW', 'Read/Write'),
        ('R', 'Read'),
        ('B', 'Banned'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    permission = models.CharField(max_length=2, choices=PERMISSIONS)
