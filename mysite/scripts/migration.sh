#!/bin/bash

set -eu

python manage.py makemigrations managed_history
python manage.py migrate