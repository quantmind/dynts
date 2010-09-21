.. _data:

.. module:: dynts.data

=============================
Data Providers and Loaders
=============================

The :ref:`domain specific language <index-dsl>` introduced the concept of :class:`dynts.dsl.Symbol`. A symbol
is string which have timeseres data associated with it. How does one access the data is accomplished
using **data providers** and a **data loader** which are discussed in this section.

Data providers are claases which loads data from a particular source,
while the data loader coordinate which provider to use and
provides hooks for post-processing and storing data on your database if
required.

.. toctree::
   :maxdepth: 2
   
   provider
   loader