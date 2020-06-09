
chemical_kinetics
=================

A python module to load, fit and plot chemical kinetics data. In particular, it can be used to extract reaction time constants from experimental data. This data should at least describe the evolution of some of the species concentration over time. Optionally, if an electrochemical measurement was performed, the fit can also include the charge passed over time in order to improve the fit of the model parameters.

Installation
------------

Using `pip <https://pypi.org/project/chemical-kinetics/>`_:

.. code:: bash

    pip install chemical-kinetics

Or download the chemical_kinetics folder on `Github <https://github.com/flboudoire/chemical-kinetics>`_ and add it to your python path.

Examples
--------

- :ref:`Simple theoretical example<Simple example>`: demonstrates the fit of species concentration evolution over time.

- :ref:`Example using real experimental data<Advanced example>`: demonstrates the simultaneous fit of the species concentrations and charge passed evolution over time in an electrochemical experiment.

.. TODO: add ref to paper when published

Dependencies
------------

This code relies on the use of the scipy, numpy, pandas and matplotlib packages. It also uses the `lmfit package <https://lmfit.github.io/lmfit-py/intro.html>`_ (Matt Newville et al., LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python).

License
-------

Licensed under the `MIT License <https://github.com/flboudoire/chemical-kinetics/blob/master/LICENSE>`_.

Content
-------

.. toctree::

   simple_example
   HMF_oxidation_WO3
   docs