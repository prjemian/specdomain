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

.. spec:def:: example_defined_macro [arg1 [arg2 [...]]]

   :param arg1: anything
   :type  arg1: str
   :param arg2: another thing

.. spec:rdef:: example_runtime_defined_macro content

   :param content: SPEC code (single or multi-line but typically a single macro)
   :type  content: str

.. spec:cdef:: example_chained_macro(identifier, content, placement)

   :param identifier: one-word name for this macro chain
   :type  identifier: str
   :param content: SPEC code to be inserted (typically a single macro)
   :type  content: str
   :param placement: see the manual
   :type  placement: str

SPEC Variables
^^^^^^^^^^^^^^

* global variable declaration: 
* local variable declaration: 
* array variable declaration: 

Python example
^^^^^^^^^^^^^^

.. py:function:: the_time(t = None)

   :param t: time_t object or None (defaults to ``now()``)
   :type  t: str


Roles
=====

A *role* refers to a *directive* (makes a link to a *directive* defined elsewhere).
Each of these items should produce a valid link.

SPEC Macros
^^^^^^^^^^^

* macro definition: :spec:def:`example_defined_macro`
* runtime-defined macro definition: :spec:rdef:`example_runtime_defined_macro`
* chained macro definition: :spec:cdef:`example_chained_macro`

SPEC Variables
^^^^^^^^^^^^^^

* global variable declaration: 
* local variable declaration: 
* array variable declaration: 

Python example
^^^^^^^^^^^^^^

See the python method :py:func:`the_time()` (defined above)
