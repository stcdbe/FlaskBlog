#!/bin/bash

function run_app() {
    set FLASK_APP=wsgi.py;
    flask db upgrade;
    gunicorn -c gunicorn.conf.py wsgi:app;
}

run_app
