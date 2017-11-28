from django.db import models
from django.utils import timezone


def strf_timedelta(duration):
    days = duration.days
    hours, rem = divmod(duration.seconds, 3600)
    minutes = divmod(rem, 60)[0]
    seconds = divmod(rem, 60)[1]

    if days > 0:
        if hours > 0:
            return "%d days and %d hours" % (days, hours)
        else:
            return "%d days" % days
    else:
        if hours > 0:
            if minutes > 0:
                return "%d hours and %d minutes" % (hours, minutes)
            else:
                return "%d hours" % hours
        else:
            if minutes > 0:
                if seconds > 0:
                    return "%d minutes and %d seconds" % (minutes, seconds)
                else:
                    return "%d minutes" % minutes
            else:
                return "%d seconds" % seconds


class Todo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(default=None, null=True)
    text = models.TextField()

    @property
    def done(self):
        return self.finished is not None

    @property
    def duration(self):
        if self.done:
            return self.finished - self.created
        else:
            return timezone.now() - self.created

    @property
    def duration_str(self):
        return strf_timedelta(self.duration)

    def __str__(self):
        return self.text