

import numpy as np

def derivatives(y, t, p):

    """
    Calculates the derivatives from local values, used by scipy.integrate.solve_ivp
    """
    
    c = {"A" : y[0], "B" : y[1]}
    
    dc = dict()

    dc["A"] = p["k2"]*c["B"] - p["k1"]*c["A"]
    dc["B"] = p["k1"]*c["A"] - p["k2"]*c["B"]
    
    dy = [dc["A"], dc["B"]]

    return dy