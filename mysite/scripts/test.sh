#!/bin/bash

set -eu

black managed_history -l 120
mypy managed_history
flake8 managed_history
python manage.py test managed_history
