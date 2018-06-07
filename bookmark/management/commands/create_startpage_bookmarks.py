import json

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError


labels = {}


def create_label_fixture(name):
    if name not in labels:
        labels[name] = {
            "model": "bookmark.label",
            "fields": {
                "id": len(labels)+1,
                "name": name
                }
            }
    return labels[name]


def create_bookmark_fixture(url, name, label):
    label = create_label_fixture(label)["fields"]["id"]
    return {
        "model": "bookmark.bookmark",
        "fields": {
                "url": url,
                "name": name,
                "label": label
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

        serialization = []

        soup = BeautifulSoup("".join(texts), 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'col-sm-3'})

        for div in divs:
            label = div.h2.text.strip()

            hyperlinks = div.find_all('a')
            for hyperlink in hyperlinks:
                bookmark_name = hyperlink.text.strip()
                bookmark_link = hyperlink.get('href')

                serialization.append(create_bookmark_fixture(bookmark_link, bookmark_name, label))

        serialization.extend(labels.values())

        json.dump(serialization, open(options['output_path'], 'w'), indent=4, sort_keys=True)