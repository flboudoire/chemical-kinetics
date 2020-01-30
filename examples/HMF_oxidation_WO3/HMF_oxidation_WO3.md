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
from chemical_kinetics import fit
import model

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


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_2_0.svg
></p>


```python
plot.plot_c(ds, ["DFF", "HMFCA", "FFCA", "FDCA"])
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_3_0.svg
></p>


```python
plot.plot_q(ds)
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_4_0.svg
></p>


```python
plot.plot_ks(ds)
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_5_0.svg
></p>
