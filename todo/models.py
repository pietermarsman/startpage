import re

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


class TodoState(models.Model):
    human_readable_text = models.TextField(max_length=128)
    computer_readable_text = models.TextField(max_length=128, default='error', unique=True)
    priority = models.PositiveIntegerField(default=0)
    timer_running = models.BooleanField(default=True)

    @classmethod
    def get_default(cls):
        if TodoState.objects.count() == 0:
            TodoState(human_readable_text='open').save()

        return TodoState.objects.order_by('-priority')[0]

    def save(self, *args, **kwargs):
        self.computer_readable_text = re.sub('[^0-9a-zA-Z]+', '_', self.human_readable_text.lower())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.human_readable_text


class Todo(models.Model):
    state = models.ForeignKey(TodoState)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(default=None, null=True)
    text = models.TextField()

    @classmethod
    def create_with_state(cls, *args, **kwargs):
        state = TodoState.get_default()
        return Todo(state=state, *args, **kwargs)

    @property
    def get_possible_states(self):
        return TodoState.objects.all()

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
        print(new_state)
        print(not new_state.timer_running)
        print(self.finished is None)
        if new_state.timer_running:
            self.finished = None
        if (not new_state.timer_running) and (self.finished is None):
            self.finished = timezone.now()
        self.state = new_state
        self.save()
