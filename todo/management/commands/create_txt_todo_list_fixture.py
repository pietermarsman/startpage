import json
import re

import datetime
from django.core.management.base import BaseCommand, CommandError


def remove_text(s, pattern):
    return re.sub(pattern, '', s)


def split_date_text(s, date_pattern=r'\[.+\]'):
    pattern = re.compile(date_pattern)
    if pattern.match(s):
        date = pattern.search(s)[0]
        text = pattern.sub('', s)
        return date, text
    else:
        return None, s


def interpret_datetime(s, format='[%Y-%m-%d-%H:%M:%S]'):
    if s is not None:
        return datetime.datetime.strptime(s, format)
    else:
        return None


def replace_none(v, default):
    if v is None:
        return default
    else:
        return v


def create_django_serialization(date, text):
    return {
        "model": "todo.todo",
        "fields": {
                "state": 3,
                "created": date.strftime('%Y-%m-%d %H:%M:%SZ'),
                "finished": (date + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%SZ'),
                "text": text
            }
        }


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--input_path', type=str)
        parser.add_argument('--output_path', type=str)

    def handle(self, *args, **options):
        with open(options['input_path'], 'r') as f:
            texts = f.readlines()

        texts = [remove_text(s, '\[x\]') for s in texts]
        dates, texts = zip(*[split_date_text(s) for s in texts])
        dates = [interpret_datetime(d)for d in dates]
        dates = [replace_none(d, datetime.datetime(2017, 3, 1, 12, 00, 00)) for d in dates]
        texts = [s.strip() for s in texts]

        serialization = [create_django_serialization(*args) for args in zip(dates, texts)]

        json.dump(serialization, open(options['output_path'], 'w'), indent=4, sort_keys=True)