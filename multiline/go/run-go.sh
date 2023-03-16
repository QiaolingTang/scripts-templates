#!/bin/bash

params=`cat /var/lib/logging/multiline-log.cfg`

./multiline-log ${params}
