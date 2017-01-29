#!/bin/sh
python /project/src/manage.py collectstatic --noinput
/usr/local/bin/uwsgi /project/etc/uwsgi.ini
