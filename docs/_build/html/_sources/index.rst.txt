
chemical_kinetics
=================

A python module to load, fit and plot chemical kinetics data. In particular, it is used to extract reaction time constants from experimental data. This data should at least describe the evolution of some of the species concentration over time. Optionally, if an electrochemical measurement was performed, the fit can also include the charge passed over time in order to improve the time constants estimation.

.. toctree::

   simple_example
   advanced_example
   docs

Installation
-----------

Using pip:

.. code:: bash

    pip install chemical_kinetics

Or download the chemical_kinetics folder on `Github <https://github.com/flboudoire/chemical-kinetics>`_ and add it to your python path.

Examples
--------

- :ref:`Simple theoretical example<Simple example>`: demonstrates the fit of species concentration evolution over time.

- :ref:`Example using real experimental data<Advanced example>`: published in `this scientific paper <#TODO: add link>`_. Demonstrates the simultaneous fit of the species concentrations and charge passed evolution over time in an electrochemical experiment.

Dependencies
------------

This code relies on the use of scipy, numpy, pandas and matplotlib packages. It also uses the `lmfit package <https://lmfit.github.io/lmfit-py/intro.html>`_ (Matt Newville et al., LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python).

License
-------

Licensed under the `MIT License <https://github.com/flboudoire/chemical-kinetics/blob/master/LICENSE>`_.