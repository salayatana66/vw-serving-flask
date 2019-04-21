"""
Wrapping a VW Model into a python class which supervises
a shell process running the model
"""

import subprocess
import os
import logging


class VWError(Exception):
    """ Class for errors """

    def __init__(self, message):
        super(VWError, self).__init__()
        self.message = message


class VWModelDown(Exception):
    """ When the model is down """

    def __init__(self):
        super(VWModelDown, self).__init__("The model is down")


class VWModel:
    """ Represents a VW model """

    def __init__(self, model_file, link=None, sort_features=False):
        """
        Args:
            model_file (str): location of the model
            link (str || None): link to apply to raw linear score
        """

        self.logger = logging.getLogger("vw_model.VWModel")
        self.logger.info("creating an instance of VWModel")

        self.model_file = os.path.expanduser(
            os.path.expandvars(model_file))

        # if a model is closed it cannot score
        # if a model does not have a current proc it is
        # uninitialized
        self.closed = False
        self.current_proc = None

        # command arguments for shell process
        # --progress=1 ensures we score one example each time
        # we redirect the score to /dev/stdout to catpure it
        self.cmd = ["vw", "--testonly", "--progress=1",
                    "-p", "/dev/stdout",
                    "--initial_regressor",
                    self.model_file]

        if link is not None:
            self.cmd.append("--link=" + link)
        if sort_features:
            self.cmd.append("--sort_features")

        self.logger.info("successfully created VWModel")
        self.logger.info("command: %s", self.cmd)

    def start(self):
        """
        Starts the model
        """

        if self.closed:
            raise VWError("Cannot start a closed model")
        if self.current_proc is not None:
            raise VWError("Cannot start a model with an active current_proc")

        # note bufsize=1 will make sure we immediately flush each output
        # line so that we can keep scoring the model
        self.current_proc = subprocess.Popen(self.cmd, bufsize=1,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

    def score(self, data_json):
        """
        Scores an example using the shell process
        Args:
            data_json (dict): must containt namespaces as a key containing the
                              features
        Returns:
            dict: {"label" : (optional if the example had a label),
                   "target": (target if the example had a target),
                   "pred" : the model prediction }

        """

        # parsed is a string read to be scored by VW
        parsed = self.parse_example(data_json["namespaces"]) + "\n"

        if self.current_proc is None:
            raise VWError("trying to score model when current_proc is None")

        if self.current_proc.returncode is not None:
            raise VWModelDown()

        # write the example through the shell process
        self.current_proc.stdin.write(parsed.encode())

        # we need to flush to score & collect the score
        # otherwise one needs to wait for the process to end
        self.current_proc.stdin.flush()
        self.current_proc.stdout.flush()

        score = float(self.current_proc.stdout.readline())

        out_list = [("pred", score)]

        # add optional info to response
        for k in ["label", "target"]:
            if k in data_json.keys():
                out_list.append([k, data_json[k]])

        return dict(out_list)

    @staticmethod
    def parse_example(fea_dict):
        """
        Parses the dictionary of namespaces to
        a feature string interpretable by VowpalWabbit
        """

        out_string = ""

        if not isinstance(fea_dict, dict):
            raise VWError("got an input which is not a dictionary")

        for namespace in fea_dict.keys():
            namespace_feas = fea_dict[namespace]

            if not isinstance(namespace_feas, dict):
                raise VWError("the features in the namespace must be a dictionary")

            out_string += "|" + namespace + " "

            for fea_name in namespace_feas.keys():
                fea = str(namespace_feas[fea_name])

                # checking wether feature is categorical or numerical
                if isinstance(fea, str):
                    out_string += fea_name + "=" + fea + " "
                elif isinstance(fea, float):
                    out_string += fea_name + ":" + fea + " "
                else:
                    raise VWError("Features must be str or float")

        return out_string

    def close(self):
        """
        Closes the model
        """
        if self.current_proc is not None:
            self.current_proc.stdin.close()
            self.current_proc.stdout.close()
            self.current_proc.stderr.close()

            # putting wait after terminate will
            # make sure the process is terminated
            # before going to the next line
            self.current_proc.terminate()
            self.current_proc.wait()

            self.current_proc = None

        self.closed = True
