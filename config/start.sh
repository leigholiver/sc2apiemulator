#!/bin/sh
redis-server 2> /dev/null &
nginx
uwsgi --lazy --ini /config/uwsgi.ini --py-autoreload 1