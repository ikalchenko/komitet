from django.db import models


class Committee(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=10)
    access_confirmation = models.BooleanField()
    created = models.DateTimeField()
