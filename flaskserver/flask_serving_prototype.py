import logging
import yaml
from flask import Flask, request
from vw_model import VWModel
from flask_vw_server import VWFlaskServer

app = VWFlaskServer(__name__)

# canonical trailing slash
@app.route('/hello/')
def hello_world():
    return "Hello, World! I'm serving a VW model"


@app.route('/serve/', methods=["POST"])
def score():
    if request.method == 'POST':
        try:
            json_data = yaml.safe_load(request.data)
        except Exception as inst:
            return "Failed to load input json\n" + str(inst)

        output = app.model.score(json_data)
        # Q should we put the exception handling into the VWserve model?
        return str(output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)

