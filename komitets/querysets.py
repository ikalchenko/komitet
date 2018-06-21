from django.db import models
from django.db.models import Q


class CommitteeQuerySet(models.QuerySet):
    def committees(self, user=None):
        if user:
            return self.filter(
                Q(members__id=user.id) & ~Q(userpermissions__permission='B')) \
                .order_by('-updated')
        return self
