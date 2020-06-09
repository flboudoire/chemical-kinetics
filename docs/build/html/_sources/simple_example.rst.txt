Simple example
==============

This example is meant to showcase the basic steps needed to fit the
concentration evolution over time of different species. These steps are
the following:

-  create a kinetic model that can be used by the **chemical_kinetics**
   module

-  loading and plotting the data

-  fitting and displaying the fit results

Kinetic model
~~~~~~~~~~~~~

We consider in this example the following reactions:

-  Forward reaction 1: A :math:`\rightarrow` B with time constant
   :math:`\rm k_{1, fw}`

-  Backward reaction 1: B :math:`\rightarrow` A with time constant
   :math:`\rm k_{1, bw}`

-  Forward reaction 2: B :math:`\rightarrow` C with time constant
   :math:`\rm k_{2}`

Which gives the following differential equations according to the law of
mass action:

.. math:: \rm \frac{dA}{dt} = k_{1,bw}[B] - k_{1,fw}[A]

.. math:: \rm \frac{dB}{dt} = k_{1,fw}[A] - k_{1,bw}[B] - k_{2}[B]

.. math:: \rm \frac{dC}{dt} = k_{2}[B]

This system of differential equations will be computed at a given time t
using the following function:

.. code:: python3

    def derivatives(y, t, p):
        
        """Calculates the derivatives of the concentrations at t.
        
        Used scipy.integrate.odeint to numerically solve the differential
        equations in a given time range.
        
        Lists ("y" and "dy") used by scipy.integrate.odeint are converted
        to dictionaries ("c" and "dc") in order to make the differentials
        easier to write and read for humans.
        
        Parameters:
            y (list): concentration values at t
            t (float): time value where the derivatives are calculated
            p (dict): dictionary containing the parameters used to
            calculate the derivatives e.g. time constants
        """
        
        # list ("y") to dict ("c") conversion
        c = {"A" : y[0], "B" : y[1], "C" : y[2]}
        
        # calculate the differentials
        dc = dict()
        dc["A"] = p["k_1bw"]*c["B"] - p["k_1fw"]*c["A"]
        dc["B"] = p["k_1fw"]*c["A"] - p["k_1bw"]*c["B"] - p["k_2"]*c["B"]
        dc["C"] = p["k_2"]*c["B"]
        
        # dict ("dc") to list ("dy") conversion
        dy = [dc["A"], dc["B"], dc["C"]]
    
        return dy

Caution: when defining the **derivatives()** function, do not use keys
for the **p** parameters dictionary containing the string **c0\_** (if
you do an error will be raised). These keys are reserved for the initial
concentrations and will be defined and used in the
:func:`fit.fit_dataset` function.

Loading and plotting the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dataset “data/concentrations vs time.csv” is loaded in an object of
class :class:`data.Dataset`. This object stores the raw data and the
fit results and makes these parameters easy to access.

Yon can consult the recomendations for the .csv files formatting in the
:meth:`data.Dataset.load_c` method documentation. The file loaded in
this example can be found `here <https://is.gd/GZPZFK>`__.

.. code:: python3

    from chemical_kinetics import data
    
    ds = data.Dataset(
        files_c = ["data/concentrations vs time.csv"],
        t_label = "Time [a.u.]",
        c_label = "Concentration [a.u.]"
    )

You can check if the data was loaded properly by plotting it using the
:func:`plot.plot_c` function:

.. code:: python3

    from chemical_kinetics import plot
    
    plot.plot_c(ds)



.. image:: simple_example_files/simple_example_9_0.svg
  :align: center

Fitting and displaying the fit results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We already defined the derivatives to be used by the fit in the
derivatives function above. However, we also need to provide an initial
guess for the time constants.

Note: In this case, only time constants constitute parameters stored in
the **p** parameter of the **derivatives()** function. However, a
different **derivatives()** function definition can require parameters
that are not time constants. These parameters can still be passed in the
**p** dictionnary, the parameters in **p** are not required to be time
constant, they can be any parameter needed by the model.

These parameters are given as a dictionary (**p** in the
**derivatives()** function definition) where the keys are the time
constant names. The corresponding values are a dictionary containing the
parameters, used to initialize a **lmfit.Parameter** object. The
parameters that can be passed via this dictionary are in particular:
value, vary, min, max and expr. Details on these parameters, and more
generally on the **lmfit.Parameter** class can be found `in the lmfit
documentation <https://lmfit.github.io/lmfit-py/parameters.html>`__.

.. code:: python3

    parameters = {
        "k_1fw": dict(value = 0.1, min = 0),
        "k_1bw": dict(value = 0.1, min = 0),
        "k_2": dict(value = 0.1, min = 0)
    }

Another parameter to be passed to the fit function are the initial
concentrations. These are defined in a similar way as the **parameters**
variable defined above, since they are also fit parameters. It is
mandatory to give the same names for theses parameters as the
corresponding names given to the columns in the .csv file that was
loaded in your dataset object. If you do not declare a value for the
initial concentration for one of the species tracked in your .csv file
then this value will be the first concentration value from this file by
default.

For demonstration, in this example we consider that: - the initial
concentration of A is at least 0.5 and we default its initial value -
the initial concentration of B is known and fixed to 0 - the initial
concentration of C is unknown and we use a default value for this
parameter by not declaring it at all. The default value is the initial
concentration for C in the dataset

.. code:: python3

    c0 = {
        "A": dict(min = 0.5),
        "B": dict(value = 0., vary = False)
    }

We can now pass these parameters to the :func:`fit.fit_dataset`
function. Once the fit converged a message generated by the
**lmfit.MinimizerResult** class is displayed (`see the lmfit
documentation <https://lmfit.github.io/lmfit-py/fitting.html>`__ for
details on this message significance).

.. code:: python3

    from chemical_kinetics import fit
    
    fit.fit_dataset(
        dataset = ds,
        derivatives = derivatives,
        parameters = parameters,
        c0 = c0
    )


.. parsed-literal::

    Fit succeeded.


The fit results can be printed and plotted using respectively the
:func:`fit.print_result` and :func:`plot.plot_c` functions:

.. code:: python3

    fit.print_result(ds)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class = 'docutils'>
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>name</th>
          <th>value</th>
          <th>stderr</th>
          <th>stderr/value %</th>
          <th>init. val.</th>
          <th>vary</th>
          <th>min</th>
          <th>max</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>k_1fw</td>
          <td>0.103</td>
          <td>0.002</td>
          <td>1.95</td>
          <td>0.1</td>
          <td>True</td>
          <td>0</td>
          <td>inf</td>
        </tr>
        <tr>
          <th>1</th>
          <td>k_1bw</td>
          <td>0.0211</td>
          <td>0.000645</td>
          <td>3.06</td>
          <td>0.1</td>
          <td>True</td>
          <td>0</td>
          <td>inf</td>
        </tr>
        <tr>
          <th>2</th>
          <td>k_2</td>
          <td>0.0197</td>
          <td>0.000209</td>
          <td>1.06</td>
          <td>0.1</td>
          <td>True</td>
          <td>0</td>
          <td>inf</td>
        </tr>
        <tr>
          <th>3</th>
          <td>c0_A</td>
          <td>0.989</td>
          <td>0.00758</td>
          <td>0.767</td>
          <td>0.965</td>
          <td>True</td>
          <td>0.5</td>
          <td>inf</td>
        </tr>
        <tr>
          <th>4</th>
          <td>c0_B</td>
          <td>0</td>
          <td>0</td>
          <td>nan</td>
          <td>0</td>
          <td>False</td>
          <td>-inf</td>
          <td>inf</td>
        </tr>
        <tr>
          <th>5</th>
          <td>c0_C</td>
          <td>0.204</td>
          <td>0.0045</td>
          <td>2.2</td>
          <td>0.202</td>
          <td>True</td>
          <td>-inf</td>
          <td>inf</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python3

    from chemical_kinetics import plot
    plot.plot_c(ds)



.. image:: simple_example_files/simple_example_18_0.svg
  :align: center

For information, here is the code that was used to generate the raw data
used in this example:

.. code:: python3

    from chemical_kinetics import fit
    import pandas as pd
    import numpy as np
    import lmfit
    
    # Time constantsand initial concentrations definitions
    params = lmfit.Parameters()
    params.add("k_1fw", value = 0.1)
    params.add("k_1bw", value = 0.02)
    params.add("k_2", value = 0.02)
    params.add("c0_A", value = 1)
    params.add("c0_B", value = 0)
    params.add("c0_C", value = 0.2)
    
    # Generate time and concentration evolution over time
    t = np.linspace(0,100,50)
    c = fit.evaluate(derivatives, params, t)
    
    # Add random noise
    c += c*0.2*(np.random.random(c.shape) - 0.5)
    
    # Create a DataFrame from t and c and save it as .csv
    data = np.hstack((t.reshape(-1,1), c))
    df = pd.DataFrame(columns = ["t", "A", "B", "C"], data = data)
    df.to_csv(r"data/concentrations vs time.csv", index = False)
