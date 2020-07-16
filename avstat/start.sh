#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python ./manage.py migrate --noinput

gunicorn avstat.wsgi -w 2 --bind "$APP_BIND"
