from django.db import models

from tils.models import Til


class Tag(models.Model):
    til = models.ForeignKey(
        Til,
        on_delete=models.CASCADE,
        related_name="tags"
    )
    tag = models.CharField(max_length=10, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['til_id', 'tag'],
                name='unique tag on a til'
            )
        ]
