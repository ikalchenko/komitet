import django.contrib.auth.models as auth_models
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        auth_models.User,
        on_delete=models.CASCADE,
        default=None
    )
    photo = models.ImageField(null=True, blank=True)


class UserPermissions(models.Model):
    PERMISSIONS = (
        ('A', 'Admin'),
        ('RW', 'Read/Write'),
        ('R', 'Read'),
        ('B', 'Banned'),
    )
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    committee = models.ForeignKey('komitets.Committee',
                                  on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSIONS)


def set_permission(self, committee, permission):
    user_permission = UserPermissions.objects.get(user=self, committee=committee)
    user_permission.permission = permission
    user_permission.save()


def get_name(self):
    if self.first_name or self.last_name:
        return self.first_name + ' ' + self.last_name
    return self.username


auth_models.User.add_to_class('get_name', get_name)
auth_models.User.add_to_class('set_permission', set_permission)
