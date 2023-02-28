from django.db import models

from tags.models import Tag
from tils.models import Til


class TilTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, related_name="tils")
    til = models.ForeignKey(Til, on_delete=models.CASCADE, related_name="tags")
