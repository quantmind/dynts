.. _data:

.. module:: dynts.data

=============================
Data Providers and Loaders
=============================

The :ref:`domain specific language <index-dsl>` introduced the concept of :class:`dynts.dsl.Symbol`. A symbol
is string which have timeseres data associated with it.

*How does one access the underlying data?*
Using **data providers** and a **data loader**.

These two concepts are discussed in this section.

Data providers are classes which loads data from a particular source such as a web-service,
a streaming professional provider and so forth.
The data loader, on the other hand, coordinates which provider to use and
provides hooks for post-processing and storing data on your database if
required.

.. toctree::
   :maxdepth: 2
   
   evaluate
   provider
   loader