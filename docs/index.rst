.. STIX-Shifter documentation master file, created by
   sphinx-quickstart on Fri Jul 28 11:31:22 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to STIX-Shifter's documentation!
========================================

*Introduction to STIX-Shifter*

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data by using these patterns, STIX-Shifter also transforms the output into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, 

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   readme

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
