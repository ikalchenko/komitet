from django.db import models


class CommitteeQuerySet(models.QuerySet):
    def committees(self, user=None):
        if user:
            return self.filter(members__id=user.id)\
                .exclude(userpermissions__permission='B')\
                .order_by('-updated')
        return self
