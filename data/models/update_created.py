from django.db import models


class UpdatedCreated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uptated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
