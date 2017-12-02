from django.db import models


class Label(models.Model):
    name = models.TextField()


class Bookmark(models.Model):
    url = models.URLField()
    name = models.TextField(default=None)
    label = models.ForeignKey(Label)
