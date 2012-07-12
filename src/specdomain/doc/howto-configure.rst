.. $Id$

====================================================================
How to Create and Configure a Sphinx project to Document SPEC Macros
====================================================================

Decide which configuration
=================================

**In-source** configuration or
**Out-of-source** configuration?

.. tip:: Most likely, you will want to keep the Sphinx documentation 
			files in a separate directory from the SPEC macros.  
			Then again, maybe not.

.. index:: ! in-source configuration

In-source configuration
---------------------------------

An *in-source* configuration is where the Sphinx ``.rst`` 
files are in **the same directory** as the SPEC macro files.

Here is a graphical example:  --tba--

.. index:: ! out-of-source configuration

Out-of-source configuration
---------------------------------

An *out-of-source* configuration is where the Sphinx ``.rst`` 
files are in **a separate directory** from the SPEC macro files.

Here is a graphical example:  --tba--

Create the Sphinx documentation tree
=====================================

::

	sphinx-quickstart

.. TODO: Show a blow-by-blow of what this looks like.

Configure: Changes to ``conf.py``
=====================================

tba
