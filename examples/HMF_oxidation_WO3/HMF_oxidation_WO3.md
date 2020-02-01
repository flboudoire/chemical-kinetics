This example emphasizes two scenarii not covered in the simple example:
- using charge passed over time data, which can be acquired when performing electrochemical measurements, and that can help improve the accuracy of the time constants obtained from the fit
- fitting when the concentration evolution over time experimental data only covers some of the species considered in the model

**TODO: comment each steps presented here**

### Kinetic model

$$\frac{d[HMF]}{dt} = -(k_{\textbf{1}1} + k_{\textbf{1}2} + k_{H\textbf{1}})[HMF]$$

$$\frac{d[DFF]}{dt} = k_{\textbf{1}1}[HMF] - (k_{\textbf{2}1} + k_{H\textbf{2}1})[DFF]$$

$$\frac{d[HMFCA]}{dt} = k_{\textbf{1}2}[HMF] - (k_{\textbf{2}2} + k_{H\textbf{2}2})[HMFCA]$$

$$\frac{d[FFCA]}{dt} = k_{\textbf{2}1}[DFF] + k_{\textbf{2}2}[HMFCA] - (k_{\textbf{3}} + k_{H\textbf{3}})[FFCA]$$

$$\frac{d[FDCA]}{dt} = k_{\textbf{3}}[FFCA] - k_{H\textbf{4}}[FDCA]$$

$$\frac{d[humins]}{dt} = k_{H\textbf{1}}[HMF] + k_{H\textbf{2}1}[DFF] + k_{H\textbf{2}2}[HMFCA]$$
$$+ k_{H\textbf{3}}[FFCA] + k_{H\textbf{4}}[FDCA] - k_{H^*}[humins]$$

$$\frac{d[humins^*]}{dt} = k_{H^*}[humins]$$


```python
species_tracked = [
    "HMF", "DFF", "HMFCA", "FFCA", "FDCA"
]
species_untracked = [
    "H_HMF",  "H_DFF",  "H_HMFCA",  "H_FFCA",  "H_FDCA",
    "Hx_HMF", "Hx_DFF", "Hx_HMFCA", "Hx_FFCA", "Hx_FDCA"
]
species = species_tracked.copy()
species.extend(species_untracked)
```


```python
def derivatives(y, t, p):

    """
    Calculates the derivatives from local values, used by scipy.integrate.solve_ivp
    """
    
    c = {s:y[i] for i, s in enumerate(species)}
    
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
    
    dy = [dc[name] for name in species]

    return dy
```

$$Q = \frac{q}{N_A} \sum_i n_i [i]$$


```python
import numpy as np
import scipy.constants as constants

def c_to_q(c):

    c_e = list()
    for i, s in enumerate(species):
        c_e.append(2*(i%5 + int(i/5))*c[:,i])

    c_e = np.sum(c_e, axis = 0) # uM
    c_e *= 1e-6 # M

    V = 100e-3 # L

    q = c_e*V*constants.N_A*constants.e # number of charge in coulombs

    return q
```

### Load concentrations and charge passed evolution over time


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

### Fitting

Define parameters


```python
parameter_vars = dict(value = 0.05, min = 0)
parameter_names = [
    "k11","k12","k21","k22","k3",
    "kH1","kH21","kH22","kH3","kH4",
    "kHx"
    ]
parameters = {name: parameter_vars for name in parameter_names}
```

Define c0


```python
c0 = {name: dict(vary = False) for name in species_tracked}
```

Define c0_untracked


```python
from collections import OrderedDict
c0_untracked = OrderedDict({
    name: dict(value = 0, vary = False) for name in species_untracked
})
```


```python
from chemical_kinetics import fit

fit.fit_dataset(
    dataset = ds,
    derivatives = derivatives,
    c_to_q = c_to_q,
    parameters = parameters,
    c0 = c0,
    c0_untracked = c0_untracked
)
```

    Fit succeeded.


### Fit results


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
      <td>k11</td>
      <td>0.00554</td>
      <td>0.000194</td>
      <td>3.51</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>1</th>
      <td>k12</td>
      <td>0.00181</td>
      <td>5.24e-05</td>
      <td>2.89</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>2</th>
      <td>k21</td>
      <td>0.0649</td>
      <td>0.00333</td>
      <td>5.13</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>3</th>
      <td>k22</td>
      <td>0.038</td>
      <td>0.00303</td>
      <td>7.98</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>4</th>
      <td>k3</td>
      <td>0.00731</td>
      <td>0.000395</td>
      <td>5.41</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>5</th>
      <td>kH1</td>
      <td>0.0302</td>
      <td>0.000366</td>
      <td>1.21</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>6</th>
      <td>kH21</td>
      <td>0.0435</td>
      <td>0.00659</td>
      <td>15.1</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>7</th>
      <td>kH22</td>
      <td>5.87e-06</td>
      <td>0.00251</td>
      <td>4.27e+04</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>8</th>
      <td>kH3</td>
      <td>0.0545</td>
      <td>0.00317</td>
      <td>5.81</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>9</th>
      <td>kH4</td>
      <td>0.0728</td>
      <td>0.00594</td>
      <td>8.17</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>10</th>
      <td>kHx</td>
      <td>0.00173</td>
      <td>0.00027</td>
      <td>15.6</td>
      <td>0.05</td>
      <td>True</td>
      <td>0.0</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>11</th>
      <td>c0_HMF</td>
      <td>4.86e+03</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.86e+03</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>12</th>
      <td>c0_DFF</td>
      <td>4.57</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>4.57</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>13</th>
      <td>c0_HMFCA</td>
      <td>0.453</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.453</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>14</th>
      <td>c0_FFCA</td>
      <td>0.248</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.248</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>15</th>
      <td>c0_FDCA</td>
      <td>0.112</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.112</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>16</th>
      <td>c0_H_HMF</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>17</th>
      <td>c0_H_DFF</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>18</th>
      <td>c0_H_HMFCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>19</th>
      <td>c0_H_FFCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>20</th>
      <td>c0_H_FDCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>21</th>
      <td>c0_Hx_HMF</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>22</th>
      <td>c0_Hx_DFF</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>23</th>
      <td>c0_Hx_HMFCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>24</th>
      <td>c0_Hx_FFCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
    <tr>
      <th>25</th>
      <td>c0_Hx_FDCA</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>nan</td>
      <td>0.0</td>
      <td>False</td>
      <td>-inf</td>
      <td>inf</td>
    </tr>
  </tbody>
</table>
</div>



```python
from chemical_kinetics import plot

plot.plot_c(ds, ["HMF"])
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_19_0.svg
></p>


```python
plot.plot_c(ds, ["DFF", "HMFCA", "FFCA", "FDCA"])
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_20_0.svg
></p>


```python
plot.plot_q(ds)
```


<p align='center'><img src = HMF_oxidation_WO3_files/HMF_oxidation_WO3_21_0.svg
></p>
