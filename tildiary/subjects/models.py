from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=100, null=False)

    # TODO: Implement Foreign key after user model implementation
    author = models.SmallIntegerField(null=False)

    is_opened = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
