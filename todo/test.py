import datetime

from django.test import TestCase

from .models import Todo, TodoState, strf_timedelta


class TestTimeDeltaFormaating(TestCase):
    def setUp(self):
        self.date1 = datetime.datetime(2017, 1, 1, 0, 0, 0)
        self.date2 = datetime.datetime(2017, 1, 1, 0, 0, 1)
        self.date3 = datetime.datetime(2017, 1, 1, 0, 0, 2)
        self.date4 = datetime.datetime(2017, 1, 1, 0, 1, 2)
        self.date5 = datetime.datetime(2017, 1, 5, 4, 30, 12)

    def test_second(self):
        duration = self.date2 - self.date1
        duration_str = strf_timedelta(duration)

        self.assertEqual(duration_str, '1 second')

    def test_two_seconds(self):
        duration = self.date3 - self.date1
        duration_str = strf_timedelta(duration)

        self.assertEqual(duration_str, '2 seconds')

    def test_one_minute_one_second(self):
        duration = self.date4 - self.date1
        duration_str = strf_timedelta(duration)

        self.assertEqual(duration_str, '1 minute and 2 seconds')

    def test_four_days_and_four_hours(self):
        duration = self.date5 - self.date1
        duration_str = strf_timedelta(duration)

        self.assertEqual(duration_str, '4 days and 4 hours')


class TestTodoState(TestCase):
    def setUp(self):
        TodoState.objects.create(human_readable_text='open')

    def test_computer_readable_text(self):
        state = TodoState.objects.get(pk=1)

        self.assertEqual(state.computer_readable_text, 'open')

    def test_url(self):
        state = TodoState.objects.get(pk=1)

        self.assertEqual(state.url, '/filtered/open/')


class TestTodo(TestCase):
    def setUp(self):
        state_open = TodoState.objects.create(human_readable_text='open')
        TodoState.objects.create(human_readable_text='closed', timer_running=False)
        Todo.objects.create(state=state_open, text='My first test')

    def test_setting_finished_datetime(self):
        todo = Todo.objects.get(pk=1)
        closed_state = TodoState.objects.get(human_readable_text='closed')
        todo.set_state(closed_state)

        self.assertIsNotNone(todo.finished)
        self.assertGreater(todo.duration.microseconds, 0)

    def test_closing_fixes_duration(self):
        todo = Todo.objects.get(pk=1)
        closed_state = TodoState.objects.get(human_readable_text='closed')
        todo.set_state(closed_state)

        self.assertEqual(todo.duration, todo.duration)

    def test_open_increases_duration(self):
        todo = Todo.objects.get(pk=1)
        self.assertLess(todo.duration, todo.duration)
