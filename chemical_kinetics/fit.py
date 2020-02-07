

from scipy.integrate import odeint
import pandas as pd
import numpy as np
import lmfit


def evaluate(derivatives, params, t):

    """Evaluate the concentration(s) evolution(s) over time

    Arguments:
        derivatives (function):
            A function in the form dy = f(y, t, p) used to compute
            d(concentration)/dt at a time t for each species. Used by
            scipy.integrate.odeint
        params (lmfit.parameter.Parameters):
            The parameters values used to compute the derivatives
            function, for details on this object class see:
            https://lmfit.github.io/lmfit-py/parameters.html
        t (list):
            Time values at which the concentrations should be evaluated.
    """

    # convert the parameters corresponding to the species initial
    # concentrations to a list of values; these parameters are recognized by
    # the string 'c0_' in their key
    c0 = [params[key].value for key in params if "c0_" in key]

    # convert the parameters corresponding to other parameters used by the
    # derivatives function to a dictionary; these parameters have keys that
    # does not contain the string 'c_0'
    p = {key: params[key].value for key in params if "c0_" not in key}

    # use scipy.integrate.odeint to compute the concentrations for all times
    c = odeint(
        func = derivatives,
        y0 = c0,
        t = t,
        args = (p,)
        )

    return c


def calculate_residuals(df, fit, names):

    """Calculates residuals values by comparing values in df and in fit

    Arguments:
        df (pandas.DataFrame):
            Holds the data to be fitted. Either concentrations vs time
            or charge passed vs time depending on the situation.
        fit (numpy.ndarray):
            Holds the fit evaluation.
        names:
            Names of the columns in df that hold the data to be compared
            to the fit values. Necessary because in some cases not all
            of the data stored in df is fitted.
    """

    res = list()

    # if the fit data only has one dimension convert it to a two dimensional
    # array, this is necessary for parsing this array along its second
    # dimension in the following for loop
    if len(fit.shape) == 1:
        fit = fit.reshape(-1,1)

    for i, name in enumerate(names):

        # in order to obtain a similar quality of fit, independently from the
        # amplitude of the fitted data a normalization is required; here we
        # normalize the residuals by the sum of the fitted data and of the fit
        # result
        norm = df[name] + fit[:,i]
        partial_res = (df[name] - fit[:,i])/norm

        # to remove nan values due to division by zero (induces ValueError in
        # the lmfit.minimize function) the residuals are set to 0 when both the
        # fitted data and the fit result are 0
        idx_div0 = norm == 0
        partial_res[idx_div0] = 0

        res.extend(partial_res)

    return res


def residuals(
    params,
    df_c,
    derivatives,
    tracked_species,
    df_q = None,
    c_to_q = None
    ):

    """Calculates residuals for concentrations vs t and optionally charge vs t
    
    Arguments:
        params (lmfit.parameter.Parameters):
            The parameters values used to compute the derivatives
            function, for details on this object class see:
            https://lmfit.github.io/lmfit-py/parameters.html
        df_c (pandas.DataFrame):
            Holds the concentration vs time data to be fitted.
        derivatives (function):
            A function in the form dy = f(y, t, p) used to compute
            d(concentration)/dt at a time t for each species. Used by
            scipy.integrate.odeint
        tracked_species (list):
            Column names in df_c corresponding to the fitted data (used
            to exclude e.g. the "t" column)
        df_q (pandas.DataFrame, optional):
            Holds the charge passed vs time data to be fitted.
        c_to_q (function, optional):
            Used to convert the concentrations over time evolution into
            charge passed.
    Returns:
        list:
            Residuals values.
    """

    # get evaluation of the fitted concentrations vs time
    c = evaluate(
        derivatives = derivatives,
        params = params,
        t = df_c["t"]
        )

    # calculate residuals between data and fit for concentrations vs time
    res = calculate_residuals(df_c, c, tracked_species)

    # if the needed data and conversion function are given, fit charge passed
    # over time
    if df_q is not None and c_to_q is not None:

        # get evaluation of the fitted concentrations vs time (time in this
        # case is the time recorded in the charge passed vs time data)
        c = evaluate(
            derivatives = derivatives,
            params = params,
            t = df_q["t"]
            )

        # convert concentrations to charge passed
        q = c_to_q(c)
        
        # calculate residuals between data and fit for charge vs time and add
        # these residuals to the res array
        res.extend(calculate_residuals(df_q, q, "Q"))

    return res


def fit_dataset(
    dataset,
    derivatives,
    parameters,
    c0 = {},
    c0_untracked = {},
    c_to_q = None
    ):

    """Fit a dataset holding concentration vs t data and optionally charge vs t

    Arguments:
        dataset (chemical_kinetics.data_processing.Dataset):
            Object holding the different DataFrames containing the data
            to be fitted
        derivatives (function):
            A function in the form dy = f(y, t, p) used to compute
            d(concentration)/dt at a time t for each species. Used by
            scipy.integrate.odeint
        parameters (dict):
            Stores parameter names (str): arguments (dict) (e.g. value,
            min, max, vary) to be passed to the corresponding
            lmfit.Parameter. Represents all 
        c0 (dict, optional):
            Stores species name (str): arguments (dict) (e.g. value,
            min, max, vary) to be passed to the corresponding
            lmfit.Parameter. Represent concentration at initial time for
            the species whose concentration evolution over time is
            stored in dataset.df_c.
        c0_untracked (collections.OrderedDict, optional):
            Stores species name (str): arguments (dict) (e.g. value,
            min, max, vary) to be passed to the corresponding
            lmfit.Parameter. Represent concentration at initial time for
            the species whose concentration evolution over time is NOT
            stored in dataset.df_c. An ordered dictionary is necessary
            in this case to be able to pass arguments properly to the
            scipy.integrate.odeint solver.
        c_to_q (function, optional):
            Used to convert the concentrations over time evolution into
            charge passed.
    """

    # rename variables to simplify code
    tracked_species = dataset.names
    df_c = dataset.df_c
    df_q = dataset.df_q


    ############################################################################
    # create the lmfit.Parameters object with all parameters from the
    # "parameters", "c0" and "c0_untracked" variables
    ############################################################################

    params = lmfit.Parameters()

    # unpack arguments from "parameters"
    for key, value in parameters.items():
        # to avoid issues with having "c0_" in the key for these parameters an
        # error is raised in that case, else the unpacking proceeds
        if "c0_" in key:
            raise ValueError(
                f"parameters key: '{key}' is invalid," +
                " keys in this dictionary should not contain the string 'c0_'"
                )
        else: params.add(key, **value)

    # unpack arguments from "c0"
    for name in tracked_species:
        key = fr"c0_{name}"
        # default initial concentration value to be used if needed
        default_val = df_c[name][0]
        if name in c0:
            # unpacking if arguments are given for this specie
            params.add(key, **c0[name])
            if "value" not in c0[name]:
                # if the "value" argument was not give it the default value
                params[key].value = default_val
        else:
            # if no arguments were passed for this specie: initialize with the
            # default value
            params.add(key, value = default_val)

    # unpack arguments from "c0_untracked"
    for name, value in c0_untracked.items():
        key = fr"c0_{name}"
        params.add(key, **value)

    # store these parameters, used in the print_result function
    dataset.init_params = params


    ############################################################################
    # perform the fit
    ############################################################################

    result = lmfit.minimize(
        residuals,
        params,
        args = [
            df_c,
            derivatives,
            tracked_species,
            df_q,
            c_to_q
            ],
        nan_policy='omit'
        )

    print(result.message)


    ############################################################################
    # store the fit results in dataset
    ############################################################################

    # store the lmfit.MinimizerResult object
    dataset.fit_result = result
    
    # build and store the DataFrame holding the evaluation from the best fit of
    # the concentrations evolution over time
    t_fit = np.linspace(df_c["t"].min(), df_c["t"].max(), 150)
    c_fit = evaluate(derivatives, result.params, t_fit)
    dataset.df_c_fit = pd.DataFrame({"t": t_fit})
    for i, s in enumerate(tracked_species): dataset.df_c_fit[s] = c_fit[:,i]

    # build and store the DataFrame holding the evaluation from the best fit of
    # the charge passed over time best fit result
    if df_q is not None and c_to_q is not None:
        dataset.df_q_fit = pd.DataFrame({"t": t_fit})
        dataset.df_q_fit["Q"] = c_to_q(c_fit)

def print_result(dataset):

    """ Pretty printing of the fit parameters stored in dataset

    Arguments:
        dataset (chemical_kinetics.data_processing.Dataset):
            Object holding the different DataFrames containing the
            initial parameters and the fitted parameters 
    """

    # get the dictionaries of parameters
    params = dataset.fit_result.params
    init_params = dataset.init_params

    # none values are returned by lmfit.minimize for error-bars when they could
    # not be calculated, formatting NoneType is not possible so if None values
    # are obtained, they are converted to nan values
    stderr = {
        p: params[p].stderr if dataset.fit_result.errorbars else np.nan for p in params
        }

    # calculate stderr/value*100 for the fitted parameters
    stderr_perc = {
        p: stderr[p]/params[p].value*100 if params[p].value != 0 else np.nan for p in params
        }

    # define function used for formatting the values
    clean = lambda value: f"{float(value):.3}"

    # prepare data to be stored in DataFrame
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
    
    # store data in DataFrame for easy display
    df = pd.DataFrame(
        data = data,
        columns = ["name", "value", "stderr", "stderr/value %", "init. val.", "vary", "min", "max"]
        )

    display(df)
