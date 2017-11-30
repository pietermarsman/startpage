import datetime
import json

from django.core.management.base import BaseCommand


def prepare_actions(data):
    data = filter(lambda d: d['type'] == 'createCard', data)
    card_creations = {d['data']['card']['id']: d['date'] for d in data}
    card_creations = {k: datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ') for k, v in card_creations.items()}

    return card_creations


def prepare_card(data):
    card = {k: data[k] for k in ['id', 'dateLastActivity', 'name']}
    card['dateLastActivity'] = datetime.datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ')

    return card


def create_django_serialization(date_start, date_end, text):
    return {
        "model": "todo.todo",
        "fields": {
            "state": 3,
            "created": date_start.strftime('%Y-%m-%d %H:%M:%SZ'),
            "finished": date_end.strftime('%Y-%m-%d %H:%M:%SZ'),
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
            data = json.load(f)

        print(data.keys())
        print({k: len(v) for k, v in data.items() if type(v) is list})

        create_actions = prepare_actions(data['actions'])
        cards = map(prepare_card, data['cards'])

        serialization = [create_django_serialization(
            create_actions.get(card["id"], card['dateLastActivity']) - datetime.timedelta(days=7),
            card["dateLastActivity"], card["name"]) for card in cards]
        
        with open(options['output_path'], 'w') as f:
            json.dump(serialization, f, sort_keys=True, indent=4)
