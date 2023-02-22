from django.db import models

from boards.models import Board


class Post(models.Model):
    title = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)

    board_id = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    is_opened = models.BooleanField(default=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
