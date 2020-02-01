A python module to load, fit and plot chemical kinetics data. It is used to extract reaction time constants from experimental data. This data should at least describe the evolution of some of the species concentration over time. Optionally, if an electrochemical measurement was performed, the fit can also include the charge passed over time in order to improve the fit precision.

### Instalation

Using pip:
```bash
pip install chemical_kinetics
```
Or download the [chemical_kinetics](chemical_kinetics/) folder and add it to your python path.

### Examples

- [Simple theoretical example](examples/simple_example/simple_example.md): homogeneous reversible reaction. Demonstrates the fit of species concentration evolution over time.

- [Example using real experimental data](examples/HMF_oxidation_WO3/HMF_oxidation_WO3.md): published in [this]() scientific paper. Demonstrates the simultaneous fit of the species concentrations and charge passed evolution over time in an electrochemical experiment.
