# Simple example: reversible monomolecular reaction

## Model

The reaction we consider in this example is the following:

$$\rm A \rightarrow B$$


```python
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
```


```python
from chemical_kinetics import fit

fit.evaluate(derivatives, )
```


```python
from chemical_kinetics import data_processing

folders = [f"data/run{i}/" for i in range(1,4)]
files_c = [f"{folder}Reaction Monitoring.csv" for folder in folders]
files_q = [f"{folder}Charge Passed.csv" for folder in folders]

ds = data_processing.Dataset(
    files_c = files_c,
    files_q = files_q,
    t_label = "Time [h]",
    c_label = r"Concentration [$\rm\mu$M]",
    q_label = "Charge passed [C]"
)
```


```python
from chemical_kinetics import model, fit

parameter_vars = dict(value = 0.05, min = 0)
parameter_names = [
    "11","12","21","22","3",
    "H1","H21","H22","H3","H4",
    "Hx"
    ]
parameters = {"k" + name: parameter_vars for name in parameter_names}

fit.fit_dataset(
    ds,
    model = model,
    parameters = parameters,
    untracked_c0 = np.zeros(10),
)
```

    Fit succeeded.



```python
from chemical_kinetics import plot

plot.plot_c(ds, ["HMF"])
```


<p align='center'><img src = simple_example_files/simple_example_5_0.svg
></p>


```python
plot.plot_c(ds, ["DFF", "HMFCA", "FFCA", "FDCA"])
```


<p align='center'><img src = simple_example_files/simple_example_6_0.svg
></p>


```python
plot.plot_q(ds)
```


<p align='center'><img src = simple_example_files/simple_example_7_0.svg
></p>


```python
plot.plot_ks(ds)
```


<p align='center'><img src = simple_example_files/simple_example_8_0.svg
></p>
