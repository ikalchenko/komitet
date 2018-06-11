from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)


class Komitet(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=10)

