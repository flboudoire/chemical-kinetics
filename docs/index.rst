.. Chemical kinetics documentation master file, created by
   sphinx-quickstart on Thu Jan 30 10:19:01 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

chemical_kinetics
=================

.. toctree::

   simple_example
   advanced_example
   docs

A python module to load, fit and plot chemical kinetics data. It is used to extract reaction time constants from experimental data. This data should at least describe the evolution of some of the species concentration over time. Optionally, if an electrochemical measurement was performed, the fit can also include the charge passed over time in order to improve the fit precision.

Instalation
-----------

Using pip:

.. code:: bash

    pip install chemical_kinetics

Or download the chemical_kinetics folder on `Github <#TODO: add link>`_ and add it to your python path.

Examples
--------

- :ref:`Simple theoretical example<Simple example>`: homogeneous reversible reaction. Demonstrates the fit of species concentration evolution over time.

- :ref:`Example using real experimental data<Advanced example>`: published in `this <#TODO: add link>`_ scientific paper. Demonstrates the simultaneous fit of the species concentrations and charge passed evolution over time in an electrochemical experiment.