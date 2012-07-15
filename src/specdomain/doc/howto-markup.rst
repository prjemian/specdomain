.. $Id$

==========================================================
How to Markup a SPEC Macro File
==========================================================

#. start with SPEC macro file that is not marked up
#. create a Sphinx documentation project
#. apply markup
#. test

Basic SPEC Macro file
==============================

This example is a SPEC macro file from the APS subversion repository:
https://subversion.xor.aps.anl.gov/spec/macros/trunk/common/hkl_ioc.mac
because it is simple, brief, does not contain references to other
macro files, provides its documentation in SPEC comments, and has not been
marked up previously for documentation with Sphinx.  Here is the file 
``hkl_ioc.mac`` in its entirety.

.. literalinclude:: ex_markup/hkl_ioc.mac
    :tab-width: 4
    :linenos:
    :language: guess



Create a Sphinx Project
==============================

.. tip:: Use an *in-source* configuration
.. make a reference to in-source

--tba--

Apply Markup
==============================

#. normal SPEC comments
#. extended comments (docstrings)
   #. global docstring
   #. macro docstring
   #. others are ignored by Sphinx
#. descriptive comments

--tba--

Test
-----------

--tba--
