from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from .managers import CommitteeManager
from users.models import UserPermissions


class Committee(models.Model):
    members = models.ManyToManyField(User, through=UserPermissions)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    background = models.ImageField(null=True, blank=True)
    access_code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CommitteeManager()

    def get_admins(self):
        return self.members.filter(userpermissions__permission='A')

    def get_writers(self):
        return self.members.filter(Q(userpermissions__permission='A')
                                   | Q(userpermissions__permission='RW'))

    def get_banned(self):
        return self.members.filter(userpermissions__permission='B')

    def get_not_banned(self):
        return self.members.exclude(userpermissions__permission='B')
