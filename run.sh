#!/bin/bash
if [ ! -d $PWD/venv ]; then
    # virtualenv -p python3 venv
    pip install -r requirements.txt
fi
# source $PWD/venv/bin/activate
if [ "$1" == 'tests' ]; then
    python3 $PWD/tests.py
elif [ "$1" == 'server' ]; then
    python3 $PWD/app.py
else
    echo "Add and argument  (tests or server) "
fi