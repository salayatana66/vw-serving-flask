""" Unit tests on model scoring """

import unittest
import json
from vw_model.vw_model import VWModel


class TestScoring(unittest.TestCase):

    def test_agreement(self):
        """Test aggreement of test_model.model
           on a prediction case
        """
        
        # Load lines as jsons
        jsf = open("json_test.json", "r")
        fea_dict = [json.loads(l) for l in jsf]

        # Load VW model in memory
        model = VWModel("test_model.model", link="logistic")
        model.start()

        # score everything 
        scored = [model.score(f) for f in fea_dict]

        # free resources
        model.close()
        jsf.close()

        # check scores are correct
        # we round at 3 because of VW's console output
        # truncation is showing floats
        for ssc in scored:
            self.assertEqual(round(ssc["target"], 3), round(ssc["pred"], 3))


if __name__ == '__main__':
    unittest.main()
