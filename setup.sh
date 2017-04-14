#!/bin/bash

if [ ! -d $PWD/venv ]; then
    virtualenv -p python3 venv
    pip install -r requirements.txt
fi
source $PWD/venv/bin/activate
if [ $1 == 'tests' ]; then
    python $PWD/tests.py
else
    python $PWD/app.py
fi