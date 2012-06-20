.. $Id$

===============
Acceptance Test
===============

If all links are valid, test is done successfully.


Directives
==========

A *directive* can be used to define the anchor point of a reference.
Index entries will point back to the *directive*.  If the item 
defined in the directive is not obtained from the source code, 
then define it here, like these.  All of these directives should 
have entries in an Index.

SPEC Macros
^^^^^^^^^^^

.. spec:def:: def_macro content

   :param arg: list of arguments is optional
   :type arg: str

   This is a standard SPEC macro definition.

.. spec:def:: def_function(arguments)

   :param str arguments: named argument(s) to this function

.. spec:rdef:: rdef_macro content

   This is a SPEC macro definition with symbols that are evaluated only at run-time.

.. spec:cdef:: cdef("cdef_macro", "content", "cdef_part", flags)

   :param str cdef_macro: one-word name (quoted string) for this macro chain
   :param str content: SPEC code to be inserted (typically a single macro)
   :param str cdef_part: name for this part of the chained macro
   :param str flags: see the manual
   
SPEC cdef macro definitions
++++++++++++++++++++++++++++++++

.. TODO: pull this subsection once this part is made to work

There are several different signatures for SPEC's ``cdef`` macro definition.
Here are some examples pulled from the ``SPEC.D`` directory.

.. note::  At present, the argument list from ``cdef`` macro definitions
   is not being parsed or handled.  This will be fixed in a future revision.
   
.. literalinclude:: cdef-examples.mac
   :linenos:
   :language: guess

SPEC Variables
^^^^^^^^^^^^^^

These are some representative variable declarations in SPEC macro source files::

	global  BCDA_GM[]
	
	   global    theta[]
	   global    2theta[]  # this will not be found
	   global    _motor[]
	
	global kohzu_PV kohzuMV_PV UND_PV Und_Off UNDE_TRACK_ON
	global       kohzuStop_PV kohzuMode_PV      kohzuMove_PV
	    global CCD_OVERHEAD_SECS_MEASURED   # measured readout time
	
	    global @A_name[] @B_name[]
	       unglobal @A_name
	       unglobal @B_name

Variables in Directives
+++++++++++++++++++++++

global variable declaration: 

.. spec:global:: A[]

   ``A[]`` contains the values of all motors

local variable declaration:  

.. spec:local:: i

   ``i`` is a local loop counter

array variable declaration: 

	tba

Variables in Roles
+++++++++++++++++++++++

* global variable declaration: :spec:global:`A[]`
* local variable declaration:  :spec:local:`i`
* array variable declaration: 
* constant declaration:

Python example
^^^^^^^^^^^^^^

.. py:function:: python_function(t = None)

   :param t: time_t object or None (defaults to ``now()``)
   :type  t: str


Roles
=====

A *role* refers to a *directive* (makes a link to a *directive* defined elsewhere).
Each of these items should produce a valid link.  Additionally, every call to a 
*role* should produce an index entry.

SPEC Macros
^^^^^^^^^^^

* macro definition: :spec:def:`def_macro`
* function definition: :spec:def:`def_function(arguments)`
* runtime-defined macro definition: :spec:rdef:`rdef_macro`
* chained macro definition: :spec:cdef:`cdef("cdef_macro", "content", "cdef_part", flags)`

SPEC Variables
^^^^^^^^^^^^^^

The SPEC macro language provides for several types of variable:

* global variables, such as:  :spec:global:`A[]`
* local variable, such as:  :spec:local:`i`
* array variable declaration: 
* constant declaration:

Source code documentation
============================

Python example
^^^^^^^^^^^^^^

See the python method :py:func:`python_function()` (defined above)

..  This should document the Python module supporting the specdomain

.. py:function:: test.testdoc.radius(x, y)
	:noindex:
	
	:param float x: ordinate
	:param float y: abcissa
	:returns float: hypotenuse
	
	return math.sqrt(x*x + y*y)
	
	The radius function is based on an algorithm of Pythagorus.
	
	.. note:: The Pythagorean theorem was also cited in the movie *The Wizard of Oz*.

:class:`SpecVariableObject` (Python Module)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: sphinxcontrib.specdomain.SpecVariableObject
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: sphinxcontrib.specdomain
    :members:



SPEC macro source file: ``cdef-examples.mac``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. spec:macrofile:: cdef-examples.mac


SPEC macro source file: ``test-battery.mac``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. spec:macrofile:: test-battery.mac
