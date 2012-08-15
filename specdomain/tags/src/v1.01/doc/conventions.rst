.. $Id$

.. index::  ! SPEC conventions
	see: conventions; SPEC conventions

===============================================================================
SPEC Documentation Conventions
===============================================================================

This document lays out several conventions for documenting SPEC
macro source code files. The aim of these conventions is to to help provide
consistency for the "look and feel" of the resulting documentation. However,
these conventions are by no means strict requirements.

.. index:: 
	pair:	SPEC conventions; extended comments

.. _convention for extended comment:

Documentation in comment blocks
===============================

Inline source documentation resides inside comment blocks within the SPEC
macro files. It is important to note, however, that not every comment in the
source code is part of the documentation. Rather, the comments containing the
documentation need to be placed in a certain context, depending on the scope of
the documentations. In analogy to the python language, we will refer to these
documentation comments as *docstrings*, even though there are some differences
concerning how they are implemented.

Comments in SPEC
----------------

There are two ways to mark a comment in SPEC. The usual identifier is
the ``#``-sign preceding a comment::

  # This is a single comment line
  
  my_val = 2.0  # This is an in-line comment

A less well-known identifier to designate multi-line comments is the
use of triple double-quotes (``"""``), which were introduced specifically with
docstrings in mind [#spec_docstring]_::

  """
  This is an extended comment in SPEC.
  
  Note that it can span multiple lines and contain several paragraphs.
  
  """
  
.. warning::

    Do not use the single-quote characters (``'``) to mark an extended comment!
	In the Python language, a docstring can be included either in triple
	double-quotes (``"""``) or in triple single-quotes (``'''``).
	But, **unlike Python**, SPEC does not recognize single quotes
	to mark extended comments. Only use the double quote character for SPEC
	files.


Extended comments
-----------------

The first extended comment in a "section" should contain the docstring. Any
other extended comments will be ignored and not processed during the
documentation creation (this setting could be changed with an optional switch.)
In this context, a *section* refers to a particular "code object", which might
be the global scope of a .mac file or a macro definition block, for example.

The first paragraph of the docstring should be a concise summary line, followed
by a blank line. This summary will be parsed in a special way to be included as
a description of the code object in summary tables, indices, etc. If the first
paragraph starts with a colon (``:``), no summary text will be assumed.

Following the summary, a more elaborate description of the code object may be
given.

For macro definitions (``def, rdef``), the docstring should immediately follow
the declaration line and be indented to the same level as the code contained
within the definition. It is also recommended to insert a blank line between
the last paragraph in a multi-line docstring and its closing quotes, placing
the closing quotes on a line by themselves::

  def my_macro_def '{
    """
    This is the summary line.
    
    And here is some more elaborate discussion of the functionality, which may
    again extend over several lines or paragraphs, and contain all the required
    rst and sphinx markup.
    
    """
    
    my_var = 1.0
    
    # do some more stuff...
    
  }'

Finally, it is recommended to use the extended comment syntax with
triple-quotes only for docstrings, even though it is a valid syntax to include
longer blocks of comments about the code itself. To avoid confusion between the
two types of comments, non-documentation comments should be included by
preceding each line with the ``#``-sign::

  """
  This is my docstring.
  
  """
  
  # Here, I write down some
  # comments about how
  # exactly my code works:
  #
  # Increment x by 1 for each registered photon

  if(hit) x+=1

.. index:: ! descriptive comments
	pair:	SPEC conventions; descriptive comments

.. _descriptive comment:


Descriptive comments
--------------------

.. caution::  This is new convention, 
				yet it does not violate any SPEC rules.
				It *is* awfully useful!
.. Is it used to document Python code?

Descriptive comments are a new construct which can be used to document items
that cannot contain extended comments (triple-quoted strings) themselves, 
such as variable declarations or *rdef* or *cdef* macro declarations.
(They can also be used to document one-line *def* macros!)
They appear either as comments in the same line after the declaration (in-line)
or as a comment-only line immediately preceding the declaration (one-liner).
Descriptive comments are marked by a preceding ``#:``, which lets them appear
like normal SPEC comments, but the colon triggers the parser to process the
docstring.

Like the summary lines in extended comments, these descriptive comments are 
used as descriptions in summary tables, etc.

**Examples**:

Descriptive comment that documents **TTH**, a global variable declaration::
    
    global TTH    #: two-theta, the scattering angle

Descriptive comment that documents **ccdset_shutter**, an *rdef* declaration::

    #: clear the ccd shutter handler
    rdef ccdset_shutter ''

Descriptive comment that documents **do_nothing()**, a *function def* declaration::

    def do_nothing() ''      #: this macro does do anything



.. index:: ! hidden objects
	pair:	SPEC conventions; hidden objects


Hidden objects
----------------

*Hidden* objects begin with at least one underline character, 
such as ``_hidden``.  This includes macros and variables.
These should be optional in the documentation.

*Anonymous* objects begin with at least two underline characters,
such as ``___anon``.  This includes macros and variables.
These should not be documented unless specifically requested and 
only then if hidden objects are documented. 

Undeclared variables
---------------------

Undeclared variables (those with no formal global, local, constant, 
or array declaration) will not be documented.  At least for now.

Parameter descriptions
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


------------

.. rubric:: Footnotes
.. [#spec_docstring] SPEC extended comments for docstrings:
   http://www.certif.com/spec_help/chg5_01.html

