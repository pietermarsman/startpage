import re
from datetime import timedelta

from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.utils.timezone import localtime, now


def strf_timedelta(duration):
    days = duration.days
    hours, rem = divmod(duration.seconds, 3600)
    minutes = divmod(rem, 60)[0]
    seconds = divmod(rem, 60)[1]

    if days == 0:
        if hours == 0:
            if minutes == 0:
                if seconds == 0:
                    return "0 seconds"
                elif seconds == 1:
                    return "1 second"
                else:
                    return "%d seconds" % seconds
            if minutes == 1:
                if seconds == 0:
                    return "1 minute"
                elif seconds == 1:
                    return "1 minute and 1 second"
                else:
                    return "1 minute and %d seconds" % seconds
            else:
                if seconds == 0:
                    return "%d minutes" % minutes
                elif seconds == 1:
                    return "%d minutes and 1 second" % minutes
                else:
                    return "%d minutes and %d seconds" % (minutes, seconds)
        elif hours == 1:
            if minutes == 0:
                return "1 hour"
            elif minutes == 1:
                return "1 hour and 1 minute"
            else:
                return "1 hour and %d minutes" % minutes
        else:
            if minutes == 0:
                return "%d hours" % hours
            elif minutes == 1:
                return "%d hours and 1 minute" % hours
            else:
                return "%d hours and %d minutes" % (hours, minutes)
    elif days == 1:
        if hours == 0:
            return "1 day"
        elif hours == 1:
            return "1 day and 1 hour"
        else:
            return "1 day and %d hours" % hours
    else:
        if hours == 0:
            return "%d days" % days
        elif hours == 1:
            return "%d days and 1 hour" % days
        else:
            return "%d days and %d hours" % (days, hours)


def daterange(start_date, end_date):
    """
    Generate an iterator of dates between the two given dates.
    taken from http://stackoverflow.com/questions/1060279/
    """
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


class TodoState(models.Model):
    human_readable_text = models.TextField(max_length=128)
    computer_readable_text = models.TextField(max_length=128, default='error', unique=True)
    priority = models.PositiveIntegerField(default=0)
    timer_running = models.BooleanField(default=True)

    @classmethod
    def completed_in_last(cls, days):
        startdate = localtime(now() - timedelta(days=days + 1)).date()
        enddate = localtime(now()).date()

        completed = Todo.objects. \
            filter(finished__gte=startdate). \
            annotate(day=TruncDate('finished')). \
            values('day'). \
            annotate(count=Count('day')). \
            values('day', 'count')
        completed = {x['day']: x['count'] for x in completed}
        completed = {day: completed[day] if day in completed else 0 for day in daterange(startdate, enddate)}

        return completed

    @classmethod
    def get_default(cls):
        if TodoState.objects.count() == 0:
            TodoState(human_readable_text='open').save()

        return TodoState.objects.order_by('-priority')[0]

    @property
    def url(self):
        return '/todo/filtered/%s/' % self.computer_readable_text

    def save(self, *args, **kwargs):
        self.computer_readable_text = re.sub('[^0-9a-zA-Z]+', '_', self.human_readable_text.lower())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.human_readable_text


class Todo(models.Model):
    state = models.ForeignKey(TodoState, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(default=None, null=True)
    text = models.TextField()

    @classmethod
    def create_with_state(cls, *args, **kwargs):
        state = TodoState.get_default()
        return Todo(state=state, *args, **kwargs)

    @property
    def duration(self):
        if self.state.timer_running:
            return timezone.now() - self.created
        else:
            return self.finished - self.created

    @property
    def duration_str(self):
        return strf_timedelta(self.duration)

    def __str__(self):
        return self.text

    def set_state(self, new_state):
        if new_state.timer_running:
            self.finished = None
        if (not new_state.timer_running) and (self.finished is None):
            self.finished = timezone.now()
        self.state = new_state
        self.save()
