from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=128, default=None, null=True)
    label = models.ForeignKey(Label, related_name='bookmarks')

    def __str__(self):
        return self.name
