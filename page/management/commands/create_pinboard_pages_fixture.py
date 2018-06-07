import datetime
import json

import os

import pytz
from django.core.management.base import BaseCommand
from django.db.models import Max

from page.models import Label


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--input_path', type=str)
        parser.add_argument('--output_path', type=str)

    def handle(self, *args, **options):
        with open(options['input_path'], 'r') as f:
            data = json.load(f)

        print('Number of records from pinboard:', len(data))

        label_id = Label.objects.aggregate(Max('id'))['id__max']
        if label_id is None:
            label_id = 0
        else:
            label_id += 1

        labels = {}
        pages = []
        for page in data:
            page_labels = page['tags'].split()

            for label in page_labels:
                if label not in labels:
                    labels[label] = {
                        'model': 'page.label',
                        'fields': {
                            'id': label_id,
                            'name': label
                        }
                    }
                label_id += 1

            pages.append({
                'model': 'page.page',
                'fields': {
                    'url': page['href'],
                    'name': page['description'],
                    'description': page['extended'],
                    'labels': [labels[label]['fields']['id'] for label in page_labels],
                    'created': pytz.utc.localize(datetime.datetime.strptime(page['time'], '%Y-%m-%dT%H:%M:%SZ')).isoformat(),
                    'modified': pytz.utc.localize(datetime.datetime.utcnow()).isoformat()
                }
            })

        labels = list(labels.values())

        with open(os.path.join(options['output_path'], 'pinboard_labels.json'), 'w') as f:
            json.dump(labels, f, sort_keys=True, indent=4)

        with open(os.path.join(options['output_path'], 'pinboard_pages.json'), 'w') as f:
            json.dump(pages, f, sort_keys=True, indent=4)
