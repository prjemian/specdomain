.. $Id$

Documenting SPEC Code
========================

.. _spec-directives:

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
