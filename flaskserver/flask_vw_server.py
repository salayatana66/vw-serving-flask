import yaml
import os
import json

# TODO make production useful by chaning the server
# Need to load from a file the yaml configuration


from flask import Flask
from vw_model import VWModel


class VWFlaskServer(Flask):
    """Serves VW model via Flask """

    def __init__(self, name):
        super(VWFlaskServer, self).__init__(name)
        self.model_file_var = os.environ["MODEL_FILE"]
        self.model_conf_var = os.environ["MODEL_CONF"]
        self.load_model()

    def load_model(self):
        """Loads the model using environment variables
           MODEL_FILE: path of model file
           MODEL_CONF: model configuration file
        """

        self.model_file = os.path.expanduser(
            os.path.expandvars(self.model_file_var)
        )
        self.model_conf = os.path.expanduser(
            os.path.expandvars(self.model_conf_var)
        )

        # configuration is a json file

        fcfg = open(self.model_conf, 'r')
        jcfg = json.load(fcfg)
        fcfg.close()

        link = jcfg.get("link", None)
        sort_features = jcfg.get("sort_features", False)

        # model instantiation & creation
        self.model = VWModel(self.model_file, link=link,
                             sort_features=sort_features)
        self.model.start()
