from django.contrib.auth.models import User
from django.contrib.auth import models as auth_models
from django.db import models
from komitets.models import Committee


class Card(models.Model):
    TYPES = (
        ('ANNOUNCE', 'Announcement'),
        ('PAY', 'Payment'),
        ('YNPOLL', 'Yes/No poll'),
        ('MAPOLL', 'Multi-answers poll'),
        ('MOPOLL', 'Multi-options poll'),
    )
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    type = models.CharField(max_length=15, choices=TYPES)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_voted_by(self, user):
        answers = Answer.objects.filter(answer_option__card=self)
        answers = answers.filter(user_id=user)
        if len(answers) != 0:
            return True
        return False


class Answer(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    answer_option = models.ForeignKey('AnswerOption', on_delete=models.CASCADE)


class AnswerOption(models.Model):
    answerers = models.ManyToManyField(auth_models.User, through=Answer)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer_content = models.CharField(max_length=50)

    def get_amount(self):
        return self.answer_set.count()

# class Attachment(models.Model):
#     card = models.ForeignKey(Card)
#     file = models.FileField()
