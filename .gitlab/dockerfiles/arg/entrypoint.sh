#!/bin/sh

Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
source /arg/venv/bin/activate
for var in "$@"
do
    eval "$var"
done