.. $Id$

.. index::  ! style guide

===============================================================================
SPEC Documentation Style Guide
===============================================================================

Some interesting and applicable words from the `Google Style Guide 
<http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_:

  BE CONSISTENT.
  
  If you're editing code, take a few minutes to look at the code around you 
  and determine its style. If they use spaces around all their arithmetic 
  operators, you should too. If their comments have little boxes of hash 
  marks around them, make your comments have little boxes of hash marks 
  around them too.
  
  The point of having style guidelines is to have a common vocabulary of 
  coding so people can concentrate on what you're saying rather than on 
  how you're saying it. We present global style rules here so people know 
  the vocabulary, but local style is also important. If code you add to a 
  file looks drastically different from the existing code around it, it 
  throws readers out of their rhythm when they go to read it. Avoid this. 

With these words in mind, this style guides documents the conventions set forth
to use for SPEC macros at the APS.

The concept of docstrings
=========================

In-line source documentation resides inside comment blocks directly within the
SPEC macro files. In analogy to the python language, we will refer to these
documentation comments as *docstrings*. These docstrings are processed by the
specdomain package for the Sphinx documentation creator to produce user or
reference manual in a variety of formats (html, pdf, man-pages, text files,
etc.)

The following section sets forth some formatting conventions for SPEC
docstrings.

One-line docstrings
-------------------

There are two distinct scenarios where one-line docstrings are appropriate or
even necessary:

#.  Obvious cases (where one line is completely sufficient to describe
    the code).
#.  Descriptive comments, that are used to document code objects
    (variables, one-line ``rdef`` or ``def`` declarations, or ```cdef``
    definitions) which cannot contain extended docstrings.
    
:Obvious cases:
  Obvious cases are those where the macro or macro function definition is so
  clear that no elaborate explanation is necessary. For example, the following
  macro function definition can probably be documented in a one-liner::
  
    def sind(x) '{
      """ Return the sine of x, where x is given in degrees."""
      
      return sin(x*PI/180)
    }'
    
  One-liners need to be enclosed in triple double-quotes (``"""``) which are
  placed on the same line as the docstring. A single space between the opening
  quotes and the docstring is optional. A blank line after the docstring helps
  to visually separate it from the actual code.
  
:Descriptive comments:
  Descriptive comments are a new a construct which can be used to document
  items that cannot contain extended comments (triple-quoted strings)
  themselves, such as variable declarations, one-line ``def`` or ``rdef``
  declarations, or ``cdef`` definitions.
  They appear either as comments in the same line after the declaration
  (in-line) or as a comment-only line immediately preceding the declaration
  (one-liner). Descriptive comments are marked by a preceding ``#:``, which
  lets them appear like normal SPEC comments, but the colon triggers the parser
  to process the docstring::
  
    global TTH            #: The scattering angle two-theta [float].

    #: Clear the ccd shutter handler
    rdef ccdset_shutter ''

    def do_nothing() ''   #: This macro does not do anything.


Multi-line docstrings
---------------------

Multi-line docstrings are surrounded by a pair of triple double-quotes
(``"""``), which should be placed on a line by themselves.
For macro definitions, the opening quotes should appear on the next
line immediately below the macro definition. It is recommended to insert a
blank line between the last paragraph in a multi-line docstring and its closing
quotes, followed by another blank line before the next code item begins.

The entire docstring is indented the same as the quotes at its first line.
Docstrings inside macro declarations should be indented from the definition
statement by the same level as the code contained in the definition.

Multi-line docstrings consist of a summary line just like a one-line docstring,
followed by a blank line and then a more elaborate description. The summary
line will be used by the specdomain indexing and summary tools. It is therefore
important to make the summary lines very clear and concise. They should always
be written as complete sentences, starting with a capital letter and ending
with a period.


Documentation of code objects
=============================

We will refer to certain types or components of the SPEC macro code as *code
objects*. These may include:

* Macro files
* Macro definitions (``def``, ``rdef``, ``cdef``)
* Variables (global, local, etc.)
* Entire collections of macro files

Each type of these code objects requires certain information to be included in
the documentation. The following sections should help to ensure that all the
required information is included and will appear in a consistent format.

File headers
------------
The macro file header docstring provides information about the macro file as a
whole (in the python world, this might be called a *module*).

As with any docstring, the first item should be a concise summary line of what
the macro file provides and which could be used in summary tables, indexes,
etc.

This is followed by sections about the detailed functionality, setup and
configuration instructions, file information, and so on. The full power of
Sphinx and ReST markup is available at this level, so sections can be broken up
in subsections and subsubsections, tables may be included as well as figures or
mathematical formulas.

The following information should be included, and the below layout may aid in
supplying a complete set of information. Note that this can always be changed
to meet the particular requirements of individual macro files:

**Description (top-level header)**:
  A more elaborate description of the functionality provided in the macro file.
  Include any number of subsections and subsubsections.

**Notes (top-level header)**:
  Any additional notes or comments about the file or its usage.
  
**Installation (top-level header)**:
  Information on how to set up the macro functionality. This includes,
  if applicable, the following subsections (second level headers):
  
  **Configuration**:
    Prerequisites in the SPEC configuration. For example, the configuration of
    dedicated counters may be necessary in order to use the macros.

  **Setup**:
    The steps necessary to set up the macro functionality. For example, loading
    the macro file (``qdo``) and running the ``macro_init`` function.

  **Dependencies**:
    List all the dependencies on other macros, hardware, software, EPICS
    channels, etc.

  **Impact**:
    Describe the impact that the use of the macro may have. For example, list
    all the changes made to other ``cdef`` macro definitions by this macro
    file.

**File Information (top-level header)**:
  All the information about the macro file itself, like authors, license,
  version, etc.
  
  It is recommended to build up this section as a definition list. The headings
  for each item are CAPITALIZED and end with a colon. The content under each of
  these items should be indented one level. This results in a more leightweight
  layout, and prevents cluttering the tables of content with too many
  subsections.
  
  The following items should be included, preferrably in this order::
  
    AUTHOR(S):
    CREATION DATE:
    COPYRIGHT:
    LICENSE::
    VERSION::
    CHANGE LOG:
    TO DO:
    KNOWN BUGS:
  
  See the below example for more details on each of these items.
  

Example of a file header docstring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

	"""
	Summary line: a concise sentence about what this macro file provides.
	
	Description
	===========
	A more detailed description of the macro file and the functionality that the
	library of macro definitions it contains provides.
	
	Note(s)
	=======
	Any special notes about the macro file, its usage, or its history can go here.
	
	Installation
	============
	Describe, as applicable, the installation procedure, necessary changes in the
	SPEC configuration, dependencies, and impact on chained macro definitions
	(``cdef``) or redefinitions (``rdef``). The sections below give hypothetical
	examples of what the content may look like.
	
	Configuration
	-------------
	For this macro to work, the SPEC configuration may need to be modified. The
	following counters are required:
	
		========  ============  ==============  =======================
		Counter   Mnemonic      Type            Description
		========  ============  ==============  =======================
		mycount1  mcnt1         None            My first counter
		mycount2  mcnt2         Macro counter   My second counter
		========  ============  ==============  =======================
	
	Setup
	-----
	With the above configuration change, simply load the macro file
	``template.mac`` and run :spec:def:`template_setup`::
	
		> qdo template.mac
		> template_setup
	
	Dependencies
	------------
	This macro depends on the following macro files and macros:
	
	* filter.mac
	
		- :spec:def:`filter_trans`
		- :spec:def:`filter_get_trans()`
	
	* bpm.mac
	
		- :spec:def:`bpm_get_pos`
	
	Impact
	------
	The following chained macro definitions are affected by template.mac:
	
	* :spec:def:`user_precount`:  Adding :spec:def:`template_precount`
	* :spec:def:`user_getcounts`: Adding :spec:def:`template_getcounts`
		to the end ``(0x20)``
	
	File information
	================
	
	AUTHOR(S):
	
		* A.B. Sample (AS, asamp), asamp@aps.anl.gov, Argonne National Laboratory
	
	CREATION DATE:
	
		YYYY/MM/DD
	
	COPYRIGHT:
	
		.. automatically retrieve the current year:
		.. |current_year| date:: %Y
	
		Copyright (c) 2010-|current_year|, UChicago Argonne, LLC
	
		All Rights Reserved
	
		APS SPEC macros
	
		APS SPEC development team,
		X-ray Science Division and APS Engineering Support Division,
		Argonne National Laboratory
	
	LICENSE::
	
		OPEN SOURCE LICENSE
	
		Redistribution and use in source and binary forms, with or without
		modification, are permitted provided that the following conditions are met:
	
		1. Redistributions of source code must retain the above copyright notice,
			 this list of conditions and the following disclaimer.  Software changes,
			 modifications, or derivative works, should be noted with comments and
			 the author and organization's name.
	
		2. Redistributions in binary form must reproduce the above copyright notice,
			 this list of conditions and the following disclaimer in the documentation
			 and/or other materials provided with the distribution.
	
		3. Neither the names of UChicago Argonne, LLC or the Department of Energy
			 nor the names of its contributors may be used to endorse or promote
			 products derived from this software without specific prior written
			 permission.
	
		4. The software and the end-user documentation included with the
			 redistribution, if any, must include the following acknowledgment:
	
			 "This product includes software produced by UChicago Argonne, LLC
			 under Contract No. DE-AC02-06CH11357 with the Department of Energy."
	
		*****************************************************************************
	
		DISCLAIMER
	
		THE SOFTWARE IS SUPPLIED "AS IS" WITHOUT WARRANTY OF ANY KIND.
	
		Neither the United States GOVERNMENT, nor the United States Department
		of Energy, NOR uchicago argonne, LLC, nor any of their employees, makes
		any warranty, express or implied, or assumes any legal liability or
		responsibility for the accuracy, completeness, or usefulness of any
		information, data, apparatus, product, or process disclosed, or
		represents that its use would not infringe privately owned rights.
	
		*****************************************************************************
	
	VERSION::
	
		$Revision$
		$Date$
		$Author$
		$URL$
	
	CHANGE LOG:
	
		YYYY/MM/DD (AS):
	
		- created first version of this macro.
		- tested on a dummy SPEC version not connected to a diffractometer.
	
		YYYY/MM/DD (AS):
	
		- added a new macro definition: :spec:def:`new_macro` to display the status.
	
	TO DO:
	
		- List all the TODO items
	
	KNOWN BUGS:
	
		- List all the known bugs and limitations
	
	"""

Macro definition docstrings
---------------------------

The docstring for a macro or macro function definition should summarize its
behavior and document its arguments, return value(s), side effects, and
restrictions on when it can be called (all if applicable). A docstring should
give enough information to write a call to the function without reading the
function's code. A docstring should describe the function's calling syntax and
its semantics, not its implementation.

Certain aspects of a macro definition should be documented in special sections, 
listed below. Since Sphinx does not generally allow for the presence of any
types of formal headings inside the code object docstrings, the docstring
should be build up as a ReST definition list (see example below). The section
titles are all CAPITALIZED for improved visibility and end with a colon. The
contents for each section are indented by two spaces with respect to the
section title.

Sections
~~~~~~~~

The following sections should be included in the macro docstring after the
summary line, in the below order, if applicable:

DESCRIPTION:
  A more elaborate description of the macro's functionality.
  
USAGE:
  The syntax for calling the macro. This should contain all possible variants
  of the macro call. Argument names are enclosed in angle brackets (``<>``) to
  indicate that they should be replaced by actual values in the macro call.
  Optional arguments are additionally enclosed in square brackets (``[]``).
  The actual USAGE syntax should appear as preformatted text, and each input
  line should start with a "``>``"-symbol to represent the SPEC command line
  prompt::
  
    USAGE::
    
      > my_macro <pos1> [<pos2>]
      > <return_value> = my_function(<input_value>)

ARGUMENTS:
  All the arguments to a function or macro call should be listed in the form of
  a ReST field list. The argument name is enclosed between colons (``:``),
  followed by the description, which can span several (indented) lines. It is
  useful to specify also the type of the argument in square brackets (``[]``).
  
  If a macro call has both mandatory and optional arguments, list them in
  separate lists::
  
    Required arguments:
      :pos1:    Target position for motor [float].
  
    Optional arguments:
      :timeout: The wait-time before giving up on serial port communication in
        seconds [float].
  
  Note that a number of python projects use a special kind of argument
  definition list which is processed by Sphinx to include more information,
  for example, the type of an argument. Other projects, however, actively
  discourage its use or prefer the above style for simplicity.
  The syntax is as follows::
  
    :param str motor_name: name of motor to use.
  
  This syntax is perfectly acceptable also for SPEC documentation, however it
  arguably results in harder to read in-line documentation and is often not
  rendered very neatly in the final Sphinx output. Use this at your own
  discretion.

EXAMPLE:
  A short example, illustrating the usage of the macro. As in the case of the
  USAGE section, the syntax should appear as pre-formatted text, and each input
  line should start with the "``>``"-symbol to represent the SPEC command line
  prompt. Short explanation lines can be inserted as indented comment lines::
  
    EXAMPLE::
    
      > set_temperatures 23.5 50.0
          # sets the two container temperatures to 23.5 and 50.0 degrees.

NOTE(S):
  Additional notes on the macro usage.

SEE ALSO:
  A list of other macros or documentation items to refer to for further
  information. If possible, these should be dynamically linked using the
  corresponding Sphinx specdomain roles::
  
    SEE ALSO:
      * :spec:def:`my_other_macro`
      * http://spec.examples.com/example3.html
      
Using the definition list syntax, other sections may be included, as necessary
or appropriate for the particular macro.

Example of a macro definition docstring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

	"""
	Concise summary line.
	
	USAGE::
		
		> my_move <motor> <position> [<sleep_time>]
		
	ARGUMENTS:
		
		Required arguments:
			:motor:    The motor to be moved [str].
			:position: The position to move the motor to [float].
		
		Optional arguments:
			:sleep_time: Settling time after the move has finished [float].
		
	EXAMPLE::
	
		> my_move del 23.2346 0.3
				# move del to 23.2346 and wait for 0.3 seconds after move finishes.
				
	NOTE: 
		Indicate any side effects, restrictions or other usage notes here.
		
	SEE ALSO:
		* :spec:def:`my_move2`
		* :spec:global:`MOVE_FLAG`
		* http://www.certif.com/spec_help/prdef.html
		
	"""

This results in the following:

	Concise summary line.
		
	USAGE::
		
		> my_move <motor> <position> [<sleep_time>]
		
	ARGUMENTS:
		
		Required arguments:
		  :motor:    The motor to be moved [str].
		  :position: The position to move the motor to [float].
		
		Optional arguments:
		  :sleep_time: Settling time after the move has finished [float].
		
	EXAMPLE::
	
		> my_move del 23.2346 0.3
				# move del to 23.2346 and wait for 0.3 seconds after move finishes.
				
	NOTE: 
		Indicate any side effects, restrictions or other usage notes here.
		
	SEE ALSO:
		* :spec:def:`my_move2`
		* :spec:global:`MOVE_FLAG`
		* http://www.certif.com/spec_help/prdef.html
    

One-line docstrings
-------------------

As mentioned previously, one-line docstrings (also called *descriptive
comments*) can be used to document code objects that cannot contain extended
docstrings. 

One-line docstrings begin with a capital letter and end with a period.

Variables
~~~~~~~~~
Docstrings for variables provide a short description of the variable. It is
also recommended to specify the type of the variable in square brackets
(``[]``). For example::

  global TTH     #: The scattering angle two-theta [float].
  local _ind     #: List index of the active reflection [int].
  
  #: Associate array with orientation reflection HKL-indices & angles [float].
  global ORIENTATION_REFLECTIONS


Macro definitions
~~~~~~~~~~~~~~~~~

One-line docstrings for macro definitions contain a short description of the
purpose for the (re-)definition. For example::

  #: Define the ccd shutter handler
  rdef ccdset_shutter '_ccdset_shutter'

  #: remove ccd_getcounts from user_getcounts
  cdef("user_getcounts", "", "ccd_key", "delete")


Macro collection docstrings
----------------------------

As of now, there is no standard yet for documenting entire collections of
macros, as, for example, those collected in particular directories of the SVN
source code repository.

The documentation for such a collection should be in the form of normal ReST
files (``*.rst``), residing in the same directory with the macro collection. There
is no way of automatically including this information in the global documents
yet, so it will need to be added manually somewhere in the documentation tree
(at least in the global ``index.rst`` file or some other file that is included
from the global scope).

