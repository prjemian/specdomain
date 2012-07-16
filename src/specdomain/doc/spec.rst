.. $Id$

.. TODO: rewrite this from a SPEC macro authors viewpoint.
	This reads from a SPHINX domain author's viewpoint.
	
	Note that most authors will not need the documentation primitives but rather just the
	*autospecmacro* and *autospecdir* directives.

Documenting SPEC Code
========================

.. _spec-directives:


.. _spec-autospecdir:
.. index:: ! autospecdir

Documenting SPEC File Directories
-----------------------------------

.. rst:directive:: .. autospecdir:: path

	:param str path: path (absolute or relative to the .rst file) 
		to an accessible directory with SPEC macro files
   
	::
   
   		.. autospecdir:: /home/user/spec.d/macros
   		
   	.. note::  options planned for future versions:

   		* document all subdirectories of *path*
   		* match files by a pattern (? glob *v.* re ?)

   

.. _spec-autospecmacro:
.. index:: ! autospecmacro

Documenting SPEC Files
-----------------------------------

.. rst:directive:: .. autospecmacro:: filename

	:param str filename: name (with optional path) of the SPEC macro file.
		The path component can be relative or absolute.  If relative,
		the path is relative to the *.rst* file.

	Document the contents of a SPEC macro source code file, including extended comments,
	*def*, *rdef*, and *cdef* macro declarations and changes, and *local*,
	*global*, and *constant* variable declarations.
   
	::
   
   		.. autospecmacro:: sixc.mac
   		
   	.. note::  options planned for future versions:

   		* standard documentation pattern
   		* include all extended comments
   		* ignore :index:`hidden objects` [#]_
   		* ignore :index:`anonymous objects` [#]_


.. _spec-extended-comments:
.. index:: ! extended comments

SPEC Extended Comments
--------------------------------

.. sidebar:: Do not use the single-quote character to mark an extended comment.

	In the Python language, a triple-quoted string is known as a docstring.
	But, **unlike Python**, SPEC does not recognize single quotes
	to mark extended comments.  Only use the double quote character for SPEC files.

Since 2002, SPEC has provided an *extended comment* block. [#]_
Such a block begins and ends
with three double-quotes, such as::

	"""This is an extended comment"""

Here, the extended comment block should be formatted according to the conventions of 
restructured text [#]_.  There is also a 
:ref:`recommended convention <convention for extended comment>` 
for using extended comments in SPEC macro files.



Describing SPEC objects
-----------------------------------

The following *directives* refer to objects in SPEC macro source code files 
and create index entries and identifiers:

.. rst:directive::  spec:def

   Declare the name of a SPEC ``def`` macro.
   
   +---------------------------+--------------------------+
   | ReST code                 | Displays like            |
   +===========================+==========================+
   | ::                        | .. spec:def:: demo_def   |
   |                           |                          |
   |   .. spec:def:: demo_def  |                          |
   +---------------------------+--------------------------+

.. rst:directive::  spec:rdef

   Declare the name of a SPEC ``rdef`` run-time-defined macro.
   
   +-----------------------------+----------------------------+
   | ReST code                   | Displays like              |
   +=============================+============================+
   | ::                          | .. spec:rdef:: demo_rdef   |
   |                             |                            |
   |   .. spec:rdef:: demo_rdef  |                            |
   +-----------------------------+----------------------------+

.. rst:directive::  spec:cdef

   Declare the name of a SPEC ``cdef`` chained macro.
   
   +-------------------------------------+------------------------------------+
   | ReST code                           | Displays like                      |
   +=====================================+====================================+
   | ::                                  | .. spec:cdef:: cdef("demo_cdef")   |
   |                                     |                                    |
   |   .. spec:cdef:: cdef("demo_cdef")  |                                    |
   +-------------------------------------+------------------------------------+

   More elaborate example showing how to call a 
   chained macro and also describe the arguments::
   
   		.. spec:cdef:: cdef("demo_cdef_more", "spec_code", "key", flags)
   		   
   		   :param str demo_cdef_more: name of chained macro
   		   :param str spec_code: SPEC code to be executed (usually a single macro name)
   		   :param str key: name of this part of the chained macro
   		   :param flags: see http://www.certif.com/spec_help/funcs.html
   		   :rtype: none
   		   
   		   This text is ignored (for now).
   
   Displays like:
   
   .. spec:cdef:: cdef("demo_cdef_more", "spec_code", "key", flags)

	   :param str demo_cdef_more: name of chained macro
	   :param str spec_code: SPEC code to be executed (usually a single macro name)
	   :param str key: name of this part of the chained macro
	   :param flags: see **SPEC** documentation for details
	   :rtype: none

.. rst:directive::  spec:global

   Declare the name of a SPEC global variable.
   
   +---------------------------------+--------------------------------+
   | ReST code                       | Displays like                  |
   +=================================+================================+
   | ::                              | .. spec:global:: demo_global   |
   |                                 |                                |
   |   .. spec:global:: demo_global  |                                |
   +---------------------------------+--------------------------------+

.. rst:directive::  spec:local

   Declare the name of a SPEC local variable.
   
   +--------------------------------+-------------------------------+
   | ReST code                      | Displays like                 |
   +================================+===============================+
   | ::                             | .. spec:local:: demo_local    |
   |                                |                               |
   |   .. spec:local:: demo_local   |                               |
   +--------------------------------+-------------------------------+

.. rst:directive::  spec:constant

   Declare the name of a SPEC constant.
   
   +-----------------------------------+----------------------------------+
   | ReST code                         | Displays like                    |
   +===================================+==================================+
   | ::                                | .. spec:constant:: demo_const    |
   |                                   |                                  |
   |   .. spec:constant:: demo_const   |                                  |
   +-----------------------------------+----------------------------------+


.. _spec-roles:

Cross-referencing SPEC objects
-----------------------------------

The following *roles* refer to objects in SPEC macro source code files 
and are possibly hyperlinked if a matching identifier is found:

.. rst:role:: spec:def

   Reference a SPEC macro definition by name.  
   (Do not include the argument list.)
   
   ::
   
   		An example ``def`` macro: :spec:def:`demo_def`
   		
   An example ``def`` macro: :spec:def:`demo_def`

.. rst:role:: spec:rdef

   Reference a SPEC run-time macro definition by name.  
   (Do not include the argument list.)
   
   ::
   
   		An example ``rdef`` macro: :spec:rdef:`demo_rdef`

   An example ``rdef`` macro: :spec:rdef:`demo_rdef`

.. rst:role:: spec:cdef

   Reference a SPEC chained macro definition by name.  
   (Do not include the argument list.)
   
   ::
   
		An example ``cdef`` macro: :spec:cdef:`cdef("demo_cdef")`
		An example ``cdef`` macro: :spec:cdef:`cdef("demo_cdef_more")`.

   An example ``cdef`` macro: :spec:cdef:`cdef("demo_cdef")`.
   An example ``cdef`` macro: :spec:cdef:`cdef("demo_cdef_more")`.

.. rst:role:: spec:global

   Reference a global-scope variable.
   
   ::
   
   		An example ``global`` variable: :spec:global:`demo_global`

   An example ``global`` variable: :spec:global:`demo_global`
   
.. rst:role:: spec:local

   Reference a local-scope variable.
   
   ::
   
   		An example ``local`` variable: :spec:local:`demo_local`

   An example ``local`` variable: :spec:local:`demo_local`
   
.. rst:role:: spec:constant

   Reference a local-scope variable.
   
   ::
   
   		An example ``local`` variable: :spec:constant:`demo_constant`

   An example ``local`` variable: :spec:constant:`demo_constant`



Undeclared Variables
---------------------

Undeclared variables (those with no formal global, local, constant, or 
array declaration) will not be documented.  At least for now.



------------

.. rubric:: Footnotes
.. [#] *hidden* objects begin with one underline character, such as ``_hidden``
.. [#] *anonymous* objects begin with at least two underline characters, such as ``__anon``
.. [#] SPEC extended comments:  http://www.certif.com/spec_help/chg5_01.html
.. [#] restructured text: http://docutils.sf.net/rst.html
.. [#] For now, the rendition is basic.  This will be improved in a future revision.
