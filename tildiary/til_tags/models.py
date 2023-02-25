from django.db import models

from tags.models import Tag
from tils.models import Til


class PostTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name="posts")
    post = models.ForeignKey(Til, on_delete=models.CASCADE, related_name="tils")
