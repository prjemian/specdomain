.. $Id$

.. index::  ! SPEC conventions
	see: conventions; SPEC conventions

====================================================================
Common Conventions
====================================================================

There are several conventions 
for documenting SPEC macro source code files
to help provide consistency.
These are not requirements.

.. index:: 
	pair:	SPEC conventions; extended comments

.. _convention for extended comment:

extended comment
-----------------

Only the first extended comment in a "section" should be documented.
(This setting could be changed with an optional switch.)

A *section* might be the global scope of a .mac file or a macro definition block.

As much as possible, use the python documentation style (that is, 
first comment is module documentation, first comment inside 
macro definition is the macro documentation).

The first paragraph should be very short, preferably one line.
It is assumed to be the summary.
If the first paragraph starts with a ":", no summary text will be assumed.



.. index:: ! descriptive comments
	pair:	SPEC conventions; descriptive comments

.. _descriptive comment:

descriptive comment
---------------------

.. caution::  This is not a confirmed convention yet, 
				but it does not violate any SPEC rules.
				It *is* awfully useful!
.. Is it used to document Python code?

Descriptive comments are used to document items that cannot contain
extended comments (triple-quoted strings) such as variable declarations
or *rdef* or *cdef* macro declarations.  They appear either in-line
with the declaration or on the preceding line.

Descriptive comment example that documents *tth*, a global variable declaration::
    
    global tth    #: two-theta, the scattering angle

Descriptive comment example that documents *ccdset_shutter*, a *rdef* declaration::

    #: clear the ccd shutter handler
    rdef ccdset_shutter ''

.. spec:global:: tth    #: two-theta, the scattering angle




.. index:: ! hidden objects
	pair:	SPEC conventions; hidden objects

hidden objects
----------------

*Hidden* objects begin with at least one underline character, 
such as ``_hidden``.  This includes macros and variables.
These should be optional in the documentation.

*Anonymous* objects begin with at least two underline characters,
such as ``___anon``.  This includes macros and variables.
These should not be documented unless specifically requested and 
only then if hidden objects are documented. 

undeclared variables
---------------------

Undeclared variables (those with no formal global, local, constant, 
or array declaration) will not be documented.  At least for now.

parameter descriptions
----------------------------

Use the same syntax as parameter declarations for Python modules.  
Here is an example SPEC macro with reST markup::

	def my_comment '{
	    """
	    Make a comment
	    
	    **usage**: ``my_comment "AR aligned to 15.14063 degrees"``
	    
	    :param str text: message to be printed
	    """
	    qcomment "%s" $1
	}'

which documentation looks like this:

.. spec:def:: my_comment text
	    
	    Make a comment
	    
	    **usage**: ``my_comment "AR aligned to 15.14063 degrees"``
	    
	    :param str text: message to be printed
