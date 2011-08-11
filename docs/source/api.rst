.. _api:

===========================
High level API
===========================

Parsing timeserie scripts
==============================

.. autofunction:: dynts.parse


Evaluating expressions
====================================

.. autofunction:: dynts.evaluate



Creating Timeseries
===================

.. autofunction:: dynts.timeseries


Merging Timeseries
===========================

.. autofunction:: dynts.merge


Registered functions
====================================

.. py:data:: dynts.function_registry

    A dictionary of functions registered with the domain specific language.
    
dynts comes with several battery-included functions but if you need more you
can your own in a straightforward manner.

