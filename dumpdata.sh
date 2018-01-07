#!/usr/bin/env bash

/Users/pieter/Documents/Projects/startpage/.venv/bin/python /Users/pieter/Documents/Projects/startpage/manage.py  dumpdata --indent 4 --natural-primary -e contenttypes -e auth --output $1