from django.db import models
from .querysets import CommitteeQuerySet


class CommitteeManager(models.Manager):
    def get_queryset(self):
        return CommitteeQuerySet(self.model, self._db)

    def committees(self, user=None):
        return self.get_queryset().committees(user=user)
