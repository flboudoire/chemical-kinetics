### Model

We consider in this example are the following reactions:

- Forward reaction 1: A :math:`\rightarrow` B with time constant k<sub>1, fw</sub>

- Backward reaction 1: B :math:`\rightarrow` A with time constant k<sub>1, bw</sub>

- Forward reaction 2: B :math:`\rightarrow` C with time constant k<sub>2</sub>

Which gives the following differential equations according to the law of mass action:

.. math:: \frac{dA}{dt} = k_{1,bw}[B] - k_{1,fw}[A]

.. math:: \frac{dB}{dt} = k_{1,fw}[A] - k_{1,bw}[B] - k_{2}[B]

.. math:: \frac{dC}{dt} = k_{2}[B]

This system of differential equation will be computed at a given time t using the following function:


```python
def derivatives(y, t, p):
    
    """ Calculates the derivatives of the concentrations at t
    
    Used scipy.integrate.odeint to numerically solve the differential
    equations in a given time range.
    
    Lists (y and dy) used by scipy.integrate.odeint are converted
    to dictionaries (c and dc) in order to make the differentials
    easier to write and read for humans.
    
    Arguments:
        y (list): concentration values at t
        t (float): time value where the derivatives are calculated
        p (dict): dictionary containing the parameters used to
        calculate the derivatives e.g. time constants
    """
    
    # list (y) to dict (c) conversion
    c = {"A" : y[0], "B" : y[1], "C" : y[2]}
    
    # calculate the differentials
    dc = dict()
    dc["A"] = p["k_1bw"]*c["B"] - p["k_1fw"]*c["A"]
    dc["B"] = p["k_1fw"]*c["A"] - p["k_1bw"]*c["B"] - p["k_2"]*c["B"]
    dc["C"] = p["k_2"]*c["B"]
    
    # dict (dc) to list (dy) conversion
    dy = [dc["A"], dc["B"], dc["C"]]

    return dy
```

**Caution:** when defining the "derivatives" function, do not use keys for the "p" parameters dictionary containing the string "c0_" (if you do an error will be raised). These keys are reserved for the initial concentrations and will be defined and used in the "fit.fit_dataset" function.

### Loading and plotting the dataset

The dataset "data/concentrations vs time.csv" is loaded in an object of class data_processing.Dataset (see [class documentation](#TODO add link) for details on the parameters that can be passed to this class). This object stores the raw data and the fit results and makes these parameters easy to access.

Its a good idea to consult the [recomendations for the .csv files format] (#TODO write and add link).


```python
from chemical_kinetics import data_processing

ds = data_processing.Dataset(
    files_c = ["data/concentrations vs time.csv"],
    t_label = "Time [a.u.]",
    c_label = "Concentration [a.u.]"
)
```

You can check if the data was loaded properly by plotting it:


```python
from chemical_kinetics import plot

plot.plot_c(ds)
```


<p align='center'><img src = simple_example_files/simple_example_6_0.svg
></p>

### Fitting

We already defined the derivatives to be used by the fit in the derivatives function above. However, we also need to provide an initial guess for the time constants. In this case only time constant are parameters of the "residuals" function but a different residuals definition can include other parameters.

These parameters are given as a dictionary where the keys are the time constant names. The corresponding values are a dictionary containing the parameter arguments (for a list of arguments consult the lmfit.Parameter [documentation](#TODO: add link)).

<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>


```python
parameters = {
    "k_1fw": dict(value = 0.1, min = 0),
    "k_1bw": dict(value = 0.1, min = 0),
    "k_2": dict(value = 0.1, min = 0)
}
```

Another argument to be passed to the fit function are the initial concentrations. These are defined in a similar way as the "parameters" variable since they are also fit parameters. It is mandatory to give the same names for theses parameters as the corresponding names given to the columns in the .csv file that was loaded in your dataset object. If you do not declare a value for the initial concentration for one of the species tracked in your .csv file then this value will be the first concentration value from this file by default.

For demonstration, in this example we consider that:
- the initial concentration of A is at least 0.5 and we default its initial value
- the initial concentration of B is known and fixed to 0
- the initial concentration of C is unknown and we use a default value for this parameter by not declaring it at all. The default value is the initial concentration for C in the dataset


```python
c0 = {
    "A": dict(min = 0.5),
    "B": dict(value = 0., vary = False)
}
```

We can now pass these parameters to the fit function. Once the fit converged a message generated by the lmfit.MinimizerResult class is displayed (see [this page](#TODO add link) for details on this message significance).


```python
from chemical_kinetics import fit

fit.fit_dataset(
    dataset = ds,
    derivatives = derivatives,
    parameters = parameters,
    c0 = c0
)
```

    Fit succeeded.


The fit results can be printed and plotted using the following functions:


```python
fit.print_result(ds)
```


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
<table border="1" class="dataframe">
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
      <td>0.102</td>
      <td>0.00191</td>
      <td>1.87</td>
      <td>0.1</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>1</th>
      <td>k_1bw</td>
      <td>0.0204</td>
      <td>0.000606</td>
      <td>2.96</td>
      <td>0.1</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>2</th>
      <td>k_2</td>
      <td>0.0201</td>
      <td>0.000204</td>
      <td>1.01</td>
      <td>0.1</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c0_A</td>
      <td>1.0</td>
      <td>0.00749</td>
      <td>0.747</td>
      <td>1.02</td>
      <td>True</td>
      <td>0.5</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>4</th>
      <td>c0_B</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>5</th>
      <td>c0_C</td>
      <td>0.205</td>
      <td>0.00443</td>
      <td>2.16</td>
      <td>0.204</td>
      <td>True</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
  </tbody>
</table>
</div>



```python
from chemical_kinetics import plot
plot.plot_c(ds)
```


<p align='center'><img src = simple_example_files/simple_example_16_0.svg
></p>


```python
from chemical_kinetics import fit
import pandas as pd
import numpy as np
import lmfit

params = lmfit.Parameters()
params.add("k_1fw", value = 0.1)
params.add("k_1bw", value = 0.02)
params.add("k_2", value = 0.02)
params.add("c0_A", value = 1)
params.add("c0_B", value = 0)
params.add("c0_C", value = 0.2)

t = np.linspace(0,100,50)
c = fit.evaluate(derivatives, params, t)

noise = lambda c : c + c*0.2*(np.random.random(c.shape) - 0.5)
c = noise(c)

data = np.hstack((t.reshape(-1,1), c))

df = pd.DataFrame(columns = ["t", "A", "B", "C"], data = data)

df.to_csv(r"data/concentrations vs time.csv", index = False)
```