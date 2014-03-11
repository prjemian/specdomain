.. $Id$

====================================================
Example Python source file documentation
====================================================

Python example
^^^^^^^^^^^^^^

.. py:function:: python_function(t = None)

   :param t: time_t object or None (defaults to ``now()``)
   :type  t: str

See the python method :py:func:`python_function()` (defined above)


Python code supporting the **specdomain**
------------------------------------------

Declaration in the .rst file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: test.testdoc.radius(x, y)
	:noindex:
	
	:param float x: ordinate
	:param float y: abcissa
	:returns float: hypotenuse
	
	return math.sqrt(x*x + y*y)
	
	The radius function is based on an algorithm of Pythagorus.
	
	.. note:: The Pythagorean theorem was also cited in the movie *The Wizard of Oz*.

:class:`SpecVariableObject` (Python Class)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: sphinxcontrib.specdomain.SpecVariableObject
    :members:
    :undoc-members:
    :show-inheritance:

`sphinxcontrib.specdomain` (Python Module)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: sphinxcontrib.specdomain
    :members:

`sphinxcontrib.specmacrofileparser` (Python Module)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: sphinxcontrib.specmacrofileparser
    :members:
