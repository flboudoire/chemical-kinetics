

import numpy as np
from scipy import constants


measured_species = ["HMF", "DFF", "HMFCA", "FFCA", "FDCA"]
all_species = measured_species.copy()
all_species.extend(["H_" + s for s in measured_species])
all_species.extend(["Hx_" + s for s in measured_species])

def c_to_q(c):

    c_e = list()
    for i, s in enumerate(all_species):
        c_e.append(2*(i%5 + int(i/5))*c[:,i])

    c_e = np.sum(c_e, axis = 0) # uM
    c_e *= 1e-6 # M

    V = 100e-3 # L

    q = c_e*V*constants.N_A*constants.e # number of charge in coulombs

    return q

def derivatives(y, t, p):

    """
    Calculates the derivatives from local values, used by scipy.integrate.solve_ivp
    """
    
    c = {s:y[i] for i, s in enumerate(all_species)}
    
    dc = dict()

    dc["HMF"]      =  - (p["k11"] + p["k12"] + p["kH1"])*c["HMF"]
    dc["DFF"]      = p["k11"]*c["HMF"]                       - (p["k21"] + p["kH21"])*c["DFF"]
    dc["HMFCA"]    = p["k12"]*c["HMF"]                       - (p["k22"] + p["kH22"])*c["HMFCA"]
    dc["FFCA"]     = p["k21"]*c["DFF"] + p["k22"]*c["HMFCA"] - (p["k3"] + p["kH3"])*c["FFCA"]
    dc["FDCA"]     = p["k3"]*c["FFCA"]                       - p["kH4"]*c["FDCA"]
    
    dc["H_HMF"]    = p["kH1"]*c["HMF"]    - p["kHx"]*c["H_HMF"]
    dc["H_DFF"]    = p["kH21"]*c["DFF"]   - p["kHx"]*c["H_DFF"]
    dc["H_HMFCA"]  = p["kH22"]*c["HMFCA"] - p["kHx"]*c["H_HMFCA"]
    dc["H_FFCA"]   = p["kH3"]*c["FFCA"]   - p["kHx"]*c["H_FFCA"]
    dc["H_FDCA"]   = p["kH4"]*c["FDCA"]   - p["kHx"]*c["H_FDCA"]

    dc["Hx_HMF"]   = p["kHx"]*c["H_HMF"]
    dc["Hx_DFF"]   = p["kHx"]*c["H_DFF"]
    dc["Hx_HMFCA"] = p["kHx"]*c["H_HMFCA"]
    dc["Hx_FFCA"]  = p["kHx"]*c["H_FFCA"]
    dc["Hx_FDCA"]  = p["kHx"]*c["H_FDCA"]
    
    dy = [dc[name] for name in all_species]

    return dy