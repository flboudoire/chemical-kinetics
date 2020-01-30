<!-- Chemical kinetics documentation master file, created by
sphinx-quickstart on Thu Jan 30 10:19:01 2020.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# chemical_kinetics module documentation

## data_processing.py


### class data_processing.Dataset(files_c, files_q=None, t_label='t [s]', c_label='C [M]', q_label='Q [C]')
Load and stores kinetics data, stores fit results and axes labels.

Attributes:

    df_c, df_c_std, df_c_fit:

        DataFrames used to store respectively the mean
        concentration, the concentration standard deviations and the
        corresponding fit results. Defined by the load_c method or
        directly at initialization using the files_c argument.

    df_q, df_q_std, df_q_fit:

        DataFrames used to store respectively the mean charge
        passed, the charge passed standard deviations and the
        corresponding fit results. Defined by the load_q method or
        directly at initialization using the files_q argument.

    t_label, c_label, q_label (str):

        Labels to be used for the x and y axes when plotting the
        datasets.

    fit_results:

        MinimizerResult from the lmfit module, stores the results of
        the fit, see:
        [https://lmfit.github.io/lmfit-py/fitting.html#lmfit.minimizer.MinimizerResult](https://lmfit.github.io/lmfit-py/fitting.html#lmfit.minimizer.MinimizerResult)
        for details. Defined when the fit.fit_dataset() function is
        run on the Dataset object.

    names:

        List of species names which concentration evolution over
        time is tracked. Used in particular to label the data when
        plotting. Defined in the load_c method.


#### load_c(files)
Loads / processes .csv files holding concentration over time data.

Recommendations for the .csv file formatting:

    
    * the files headers should be formatted in this fashion: “t,

species name 1, species name 2…”

    
    * first column should be the time, other columns are

concentrations

Example files can be found here: #TODO link to github folder
with raw data

Relies on the load() function from this module, see also this
function Docstring for more details.

Arguments:

    files:

        list of strings representing the paths of the .csv files


#### load_q(files)
Loads / processes .csv files holding charge passed over time data.

Recommendations for the .csv file formatting:

    
    * the files headers should be formatted in this fashion: “t, Q”


    * first column should be the time, second column charge passed


    * each columns in each files must have the same number of rows

and columns

Example files can be found here: #TODO link to github folder
with raw data

Relies on the load() function from this module, see also this
function Docstring for more details.

Arguments:

    files:

        list of strings representing the paths of the .csv files


### data_processing.load(files)
Loads and processes data from .csv files, stores it in Dataframes.

The .csv files should have the same headers, the same number of
columns and the same number of rows. The header should be held in
the first row.

These .csv files are typically generated from raw data files from
experiments using custom code to satisfy these requirements.

Arguments:

    files:

        List of string(s) representing the path(s) to the file(s),
        each column in each file must have the same number of rows.

Returns:

    df, df_std:

        DataFrames holding the averaged data (df) and standard
        deviation (df_std).

## fit.py


### fit.evaluate(derivatives, params, t, c0)

### fit.fit_dataset(dataset, model, parameters, untracked_c0=[])

### fit.residuals(params, df_c, df_q, model, c0, tracked_species)
## plot.py
