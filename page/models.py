from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Page(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=256)
    description = models.TextField(default=None, null=True)
    label = models.ManyToManyField(Label)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.url)