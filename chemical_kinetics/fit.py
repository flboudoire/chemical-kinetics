

from scipy.integrate import odeint
import pandas as pd
import numpy as np
import lmfit


def evaluate(derivatives, params, t):

    """

    """

    c0 = [params[key].value for key in params if "c0_" in key]
    p = {key: params[key].value for key in params if "c0_" not in key}

    c = odeint(
        func = derivatives,
        y0 = c0,
        t = t,
        args = (p,)
        )

    return c


def calculate_residuals(df, fit, names):

    res = list()
    for i, name in enumerate(names):
        norm = df[name] + fit[:,i]
        idx_div0 = norm == 0
        partial_res = (df[name] - fit[:,i])/norm
        partial_res[idx_div0] = 0
        res.extend(partial_res)

    return res


def residuals(
    params,
    df_c,
    df_q,
    derivatives,
    c_to_q,
    tracked_species
    ):

    """

    """

    c = evaluate(
        derivatives = derivatives,
        params = params,
        t = df_c["t"]
        )

    res = calculate_residuals(df_c, c, tracked_species)

    if df_q is not None:

        c = evaluate(
            derivatives = derivatives,
            params = params,
            t = df_q["t"]
            )
        q = c_to_q(c)

        res.extend(calculate_residuals(df_q, q, "Q"))

    return res


def fit_dataset(
    dataset,
    derivatives,
    parameters,
    c_to_q = None,
    c0 = {},
    c0_untracked = {}
    ):

    """

    """

    tracked_species = dataset.names
    df_c = dataset.df_c
    df_q = dataset.df_q

    params = lmfit.Parameters()

    for key, value in parameters.items():
        if "c0_" in key:
            raise ValueError(
                f"parameters key: '{key}' is invalid," +
                " keys in this dictionary should not contain the string 'c0_'"
                )
        params.add(key, **value)

    for name in tracked_species:
        key = fr"c0_{name}"
        c0_value_default = df_c[name][0]
        if name in c0:
            params.add(key, **c0[name])
            if "value" not in c0[name]:
                params[key].value = c0_value_default
        else:
            params.add(key, value = c0_value_default)

    for name in c0_untracked:
        key = fr"c0_{name}"
        params.add(key, **c0[name])

    dataset.init_params = params

    result = lmfit.minimize(
        residuals,
        params,
        args = [
            df_c,
            df_q,
            derivatives,
            c_to_q,
            tracked_species
            ],
        nan_policy='omit'
        )

    print(result.message)

    dataset.fit_result = result
    
    t_fit = np.linspace(df_c["t"].iloc[0], df_c["t"].iloc[-1], 150)
    c_fit = evaluate(derivatives, result.params, t_fit)
    dataset.df_c_fit = pd.DataFrame({"t": t_fit})
    for i, s in enumerate(tracked_species): dataset.df_c_fit[s] = c_fit[:,i]

    if df_q is not None and c_to_q is not None:
        dataset.df_q_fit = pd.DataFrame({"t": t_fit})
        dataset.df_q_fit["Q"] = c_to_q(c_fit)

def print_result(dataset):

    params = dataset.fit_result.params
    init_params = dataset.init_params
    stderr = {
        p: params[p].stderr if dataset.fit_result.errorbars else np.nan for p in params
        }

    stderr_perc = {
        p: stderr[p]/params[p].value*100 if params[p].value != 0 else np.nan for p in params
        }

    clean = lambda value: f"{float(value):.3}"
    data = [
        [
            p,
            clean(params[p].value),
            clean(stderr[p]),
            clean(stderr_perc[p]),
            clean(init_params[p].value),
            init_params[p].vary,
            clean(init_params[p].min),
            clean(init_params[p].max)
        ]
        for p in params
        ]
    
    df = pd.DataFrame(
        data = data,
        columns = ["name", "value", "stderr", "stderr/value %", "init. val.", "vary", "min", "max"]
        )

    display(df)
