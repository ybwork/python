#!/bin/bash

python ./create_bootstrap.py &&
python ./bootstrap.py &&
./bin/pip install -r requirements.txt &&
cp ./conf/settings_local.py.template ./conf/settings_local.py

