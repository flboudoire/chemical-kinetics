

from scipy.integrate import odeint
import pandas as pd
import numpy as np
import lmfit


def evaluate(derivatives, params, t, c0):

    """

    """

    return odeint(
        func = derivatives,
        y0 = c0,
        t = t,
        args = (params.valuesdict(),)
        )

def residuals(
    params, 
    df_c, 
    df_q, 
    model, 
    c0, 
    tracked_species
    ):

    """

    """

    c = evaluate_c(
        derivatives = model.derivatives,
        params = params,
        t = df_c["t"],
        c0 = c0
        )

    res = list()
    for i, specie in enumerate(tracked_species):
        res.extend(
            (df_c[specie] - c[:,i])/(df_c[specie] + c[:,i])
            )

    if df_q is not None:
        c = evaluate(
            derivatives = model.derivatives,
            params = params,
            t = df_q["t"],
            c0 = c0
            )
        q = model.c_to_q(c)
        res.extend(
            (df_q["Q"] - q)/(df_q["Q"] + q)
            )

    return res


def fit_dataset(
    dataset,
    model,
    parameters,
    untracked_c0 = []
    ):

    """

    """

    tracked_species = dataset.names
    df_c = dataset.df_c
    df_q = dataset.df_q

    params = lmfit.Parameters()
    for key, value in parameters.items(): params.add(key, **value)

    c0 = [df_c[s][0] for s in tracked_species]
    c0.extend(untracked_c0)

    result = lmfit.minimize(
        residuals,
        params,
        args = [
            df_c,
            df_q,
            model,
            c0,
            tracked_species
            ],
        nan_policy='omit'
        )

    print(result.message)

    dataset.fit_result = result
    
    t_fit = np.linspace(df_c["t"].iloc[0], df_c["t"].iloc[-1], 150)
    c_fit = evaluate_c(model.derivatives, result.params, t_fit, c0)
    dataset.df_c_fit = pd.DataFrame({"t": t_fit})
    for i, s in enumerate(tracked_species): dataset.df_c_fit[s] = c_fit[:,i]

    dataset.df_q_fit = pd.DataFrame({"t": t_fit})
    dataset.df_q_fit["Q"] = model.c_to_q(c_fit)