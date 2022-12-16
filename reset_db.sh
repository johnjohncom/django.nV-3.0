#!/bin/bash
rm db.sqlite3 &> /dev/null
python3 manage.py migrate
python3 manage.py loaddata fixtures/*
