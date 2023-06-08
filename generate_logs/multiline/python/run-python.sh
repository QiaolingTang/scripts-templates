#!/bin/bash

params=`cat /var/lib/logging/multiline-log.cfg`

python3 ./multiline-log.py ${params}
