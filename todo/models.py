from django.db import models


class Todo(models.Model):
    created = models.DateTimeField(auto_now=True)
    finished = models.DateTimeField(default=None, null=True)
    text = models.TextField()

    @property
    def done(self):
        return self.finished is not None

    def __str__(self):
        return self.text