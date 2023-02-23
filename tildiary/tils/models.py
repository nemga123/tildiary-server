from django.db import models

from subjects.models import Subject


class Til(models.Model):
    title = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)

    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="tils",
    )

    is_opened = models.BooleanField(default=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)