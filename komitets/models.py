from django.db import models


class Committee(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
