from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()


class Committee(models.Model):
    name = models.CharField(max_length=50)
    access_code = models.CharField(max_length=10)
    access_confirmation = models.BooleanField()
    created = models.DateTimeField()


class Question(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    CARD_TYPES = (
        ('announcement', 'announcement'),
        ('payment', 'payment'),
        ('assignment', 'assignment'),
        ('yes-no-poll', 'yes-no-poll'),
        ('multi-poll', 'multi-poll'),
    )
    card_type = models.CharField(max_length=15, choices=CARD_TYPES)
    created = models.DateTimeField()


class QuestionAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)


class UserPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    PERMISSIONS = (
        ('a', 'a'),
        ('rw', 'rw'),
        ('r', 'r'),
        ('b', 'b'),
    )
    permission = models.CharField(max_length=2, choices=PERMISSIONS)
