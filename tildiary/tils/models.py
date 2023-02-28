from django.db import models

from subjects.models import Subject


class Til(models.Model):
    title = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)

    # TODO: Implement Foreign key after user model implementation
    author = models.SmallIntegerField(null=False)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="tils",
    )

    is_opened = models.BooleanField(default=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
