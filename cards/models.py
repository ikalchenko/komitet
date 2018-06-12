from django.contrib.auth.models import User
from django.db import models
from komitets.models import Committee


class Card(models.Model):
    TYPES = (
        ('ANNOUNCE', 'Announcement'),
        ('PAY', 'Payment'),
        ('ASSIGN', 'Assignment'),
        ('YNPOLL', 'Yes/No poll'),
        ('MPOLL', 'Multi-answers poll'),
    )
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    type = models.CharField(max_length=15, choices=TYPES)
    created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerOption(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)

# class Attachment(models.Model):
#     card = models.ForeignKey(Card)
#     file = models.FileField()
