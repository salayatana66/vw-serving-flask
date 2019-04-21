""" Generate a test model """

import numpy as np
import json

np.random.seed(15)

######################################################
# Model features
######################################################
model = {}
model['a'] = {"x1": ['a', 'b', 'c'],
              "x2": ""}
model['b'] = {"x3": ['q', 'r'],
              "x4": ['f', 'g', 'h']}

######################################################
# Model coefficients
######################################################
coefficients = {'a': -.55,
                'b': .33,
                'c': .12,
                "x2": .22,
                'q': -.25,
                'r': -.44,
                'f': -.66,
                'g': +.45,
                'h': 1.2
                }

# samples to draw
N_samples = 1000

# We save data both in vw & json format
fvw = open("test_data.vw", "w")
fjs = open("test_data.json", "w")

for i in range(N_samples):
    # construct string and raw score
    # which goes into the logistic function
    score = 0.0
    out_string = "|a "
    x1 = np.random.choice(model['a']["x1"], size=1)[0]
    score += coefficients[x1]

    # up to 3 significant digits
    x2 = round(np.random.uniform(size=1)[0], 3)
    score += x2 * coefficients["x2"]
    
    x3 = np.random.choice(model['b']["x3"], size=1)[0]
    score += coefficients[x3]
    
    x4 = np.random.choice(model['b']["x4"], size=1)[0]
    score += coefficients[x4]

    outcome = None

    # binary outcome
    if score > 0:
        outcome = 1
    else:
        outcome = 0
    
    out_string = f"{outcome} lab_{i}|a x1={x1} x2:{x2} |b x3={x3} x4={x4}"
    out_json = {"target": outcome,
                "label": f"lab_{i}",
                "namespaces": {'a': {"x1": x1, "x2": x2},
                               'b': {"x3": x3, "x4": x4}}}

    # writing & flushing
    fvw.write(out_string + '\n')
    fvw.flush()
    fjs.write(json.dumps(out_json) + '\n')
    fjs.flush()

fvw.close()
fjs.close()
   
