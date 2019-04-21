#!/bin/bash

# we need to add to the PYTHONPATH the
# packages to serve vw
cd /home/vwserver/flaskserver
PYTHONPATH=/home/vwserver/vwmodel/vw_model:/home/vwserver/flaskserver:$PYTHONPATH \
	  gunicorn --bind 0.0.0.0:$MODEL_PORT flask_serving
