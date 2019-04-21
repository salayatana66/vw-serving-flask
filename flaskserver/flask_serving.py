"""
Flask app to serve a VW model
"""

import sys
import yaml


from flask import request
from flask_vw_server import VWFlaskServer
from vw_model import VWError, VWModelDown

# for gunicorn the naming convention
# 'application' is very important
application = VWFlaskServer(__name__)

# canonically trailing slash to path
@application.route('/hello/')
def hello_world():
    """ @Useless """
    return "Hello, World! I'm serving a VW model"


# scoring an example is done via POST
@application.route('/serve/', methods=["POST"])
def score():
    """ Score example via POST call """
    if request.method == 'POST':
        try:
            json_data = yaml.safe_load(request.data)
        except Exception as inst:
            return "Failed to load input json\n" + str(inst)

        if json_data is None:
            return "Failed to load input json: it is None\n"

        # if the model is down we make a call to sys to
        # shut it down; in kubernetes we will get a new
        # container if we have a minimum # of replicas specified
        try:
            output = application.model.score(json_data)
        except VWError as vwerror:
            output = "Failed to score example\n" + str(vwerror)
        except VWModelDown:
            sys.exit(-1)

        return str(output)


if __name__ == '__main__':
    application.run()
