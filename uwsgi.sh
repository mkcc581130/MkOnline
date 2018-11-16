#!/bin/bash
if [[ "$1" = "start" ]]; then
    uwsgi --ini uwsgi.ini
    echo "uwsgi already $1"
elif [[ "$1" = "restart" ]]; then
    uwsgi --reload uwsgi.pid
    echo "uwsgi already $1"
elif [[ "$1" = "stop" ]]; then
    uwsgi --stop uwsgi.pid
    echo "uwsgi already $1"
elif [[ "$1" = "status" ]]; then
    uwsgi --connect-and-read uwsgi.status
else
    echo "no effect $1"
fi