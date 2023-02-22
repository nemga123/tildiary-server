from django.db import models

from posts.models import Post
from tags.models import Tag


class PostTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name="posts"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="tags"
    )
