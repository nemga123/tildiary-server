from django.db import models

from users.models import User


class Subject(models.Model):
    title = models.CharField(max_length=100, null=False)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects",
        null=False,
    )

    is_opened = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
