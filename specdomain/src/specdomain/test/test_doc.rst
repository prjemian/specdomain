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

   :param str arg: list of arguments is optional

   This is a standard SPEC macro definition.

.. spec:rdef:: rdef_macro content

   This is a SPEC macro definition with symbols that are evaluated only at run-time.

.. spec:cdef:: cdef(macro_name, [content, groupname, [flags]])

   :param str macro_name: one-word name (quoted string) for this macro chain
   :param str content: SPEC code to be inserted (typically a single macro)
   :param str groupname: name of organizational group
   :param str flags: see the manual

SPEC Variables
^^^^^^^^^^^^^^

* global variable declaration: 
* local variable declaration: 
* array variable declaration: 

Python example
^^^^^^^^^^^^^^

.. py:function:: python_function(t = None)

   :param t: time_t object or None (defaults to ``now()``)
   :type  t: str

ReST example
^^^^^^^^^^^^^^

.. rst:directive:: rst_directive


Roles
=====

A *role* refers to a *directive* (makes a link to a *directive* defined elsewhere).
Each of these items should produce a valid link.  Additionally, every call to a 
*role* should produce an index entry.

SPEC Macros
^^^^^^^^^^^

* macro definition: :spec:def:`def_macro`
* runtime-defined macro definition: :spec:rdef:`rdef_macro`
* chained macro definition: :spec:cdef:`cdef(macro_name, content, groupname, flags)`

SPEC Variables
^^^^^^^^^^^^^^

* global variable declaration: 
* local variable declaration: 
* array variable declaration: 

Python example
^^^^^^^^^^^^^^

See the python method :py:func:`python_function()` (defined above)
