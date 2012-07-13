.. $Id$


====================================================================
How to Build the Documentation from a Sphinx project
====================================================================

--tba--

::

	make html

Load the file ``index.html`` into your browser and examine the results.
The file path is different depending if you have an *in-source* or 
*out-of-source* configuration.


.. index:: in-source configuration
.. index:: out-of-source configuration

*in-source* path:
	``_build/html/index.html``
*out-of-source* path:
	``build/html/index.html``

Test
=====

For our testing purposes, we'll document the *aalength.mac* 
macro file from the :ref:`Install` section.
Edit the new file *index.rst* and add this line at line 14.  
Make sure it lines up at the left in column 1::
	
	.. autospecmacro:: ../specdomain/doc/aalength.mac

Build the HTML documentation::

    make html

View the documentation using a web browser such as *firefox*::

	firefox _build/html/index.html &

You should see a page that looks like this, if nothing went wrong.

.. figure:: test1.png
    :alt: view of aalength.mac HTML documentation

    Documentation of the **aalength.mac** file.
