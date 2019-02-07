#!/bin/bash

source /opt/octoprint/venv/bin/activate 
python setup.py install || echo "Error: Cannot install LCD1602 Plugin"

echo "Starting octoprint server"
/opt/octoprint/venv/bin/octoprint serve >/tmp/logs & || echo "Error: Cannot start the server !"

echo "Looking for errors on logs"
sleep 10
ERRORS=$(grep -i -c error /tmp/logs )

if ( $ERRORS -gt 0 )
then
  exit 1
else
  echo "Plugin is installed and loaded"
fi
