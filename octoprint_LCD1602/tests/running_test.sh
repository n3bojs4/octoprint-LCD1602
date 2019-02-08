#!/bin/bash

#export LCD1602_DOCKER=1

source /opt/octoprint/venv/bin/activate 
python setup.py install || echo "Error: Cannot install LCD1602 Plugin"

echo "Starting octoprint server"
/opt/octoprint/venv/bin/octoprint serve --iknowwhatimdoing >/tmp/logs &

echo "Checking octoprint is running"
sleep 3
RUNNING=$(pgrep -c octoprint)


if [ $RUNNING -eq 0 ]
then
  echo 'Octoprint failed to start' && exit 1
else
  echo 'Octoprint is started'
fi

echo "Looking for errors on logs"
sleep 10
ERRORS=$(grep -c "^| \!LCD1602 I2c display" /tmp/logs )

if [ $ERRORS -gt 0 ]
then
  echo 'Plugin errors detected, check logs below :'
  grep -A 100 -B 20 'LCD1602' /tmp/logs
  exit 1
else
  echo "Plugin is installed and loaded"
fi
