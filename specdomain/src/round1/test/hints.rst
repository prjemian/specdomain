.. $Id$

Hints while developing the extension
===================================================================

Useful reading
---------------

* http://sphinx.pocoo.org/domains.html
* http://sphinx.pocoo.org/ext/appapi.html#domain-api
* http://sphinx.pocoo.org/ext/tutorial.html
* https://bitbucket.org/birkenfeld/sphinx-contrib/
* http://sphinx.pocoo.org/ext/appapi.html#sphinx.domains.Domain

.. note:: Per ``src/refs/sphinx-contrib/README``,
	*Use "make-ext.py" to set up your extension subdirectory.*
	
	There is also a useful comment about using ``ez_setup.py``.


Regular Expression Parts to Recognize ...
--------------------------------------------

the start of a macro definition (``def`` or ``rdef``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

====================  ===============================
regexp                description
====================  ===============================
``^``                 start of line
``[\s]*``             optional preceding white space
``[r]?``              rdef?
``def``               "def" declaration
``[\s]+``             required trailing space
``([a-zA-Z_][\w]*)``  macro name
====================  ===============================

the start of a chained macro definition (``cdef``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

=========  ================================
regexp     description
=========  ================================
``^``      start of line
``[\s]*``  optional preceding white space
``cdef``   "cdef" declaration
``[\s]+``  required trailing space
``\(``     start of argument list
=========  ================================

a global variable declaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  

=======================================   =================================
regexp                                    description
=======================================   =================================
``^``                                     start of line
``([\s]*)``                               optional preceding white space
``global``                                "global" declaration
``([\s]+[@]?[a-zA-Z_][\w]*(\[\])?)+``     one or more variable names
``([\s]+#.*)*``                           optional comment
``$``                                     end of line
=======================================   =================================

test cases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  

::

	global  BCDA_GM[]
	
	   global    billy[]
	   global    9billy[]
	   global    _billy[]
	
	global kohzu_PV kohzuMV_PV UND_PV Und_Off UNDE_TRACK_ON
	global       kohzuStop_PV kohzuMode_PV      kohzuMove_PV
	global CCD_PREFIX            # EPICS PV for CCD server
	global CCD_OVERHEAD_SECS        # readout time
	global CCD_OVERHEAD_SECS_MEASURED   # measured readout time
	
	    global @A_name[] @B_name[]
	       unglobal @A_name
	       unglobal @B_name
	global CCD_DARK_NUM CCDDARK CCD_THROW
	global MULTI_IMGS # useful 8-ID's imm fileformat; currently not used

	def _ascan ''
	
	kohzuMove_PV = "32ida:KohzuPutBO"
	Und_Delay = 0.1
	
	def kohzuE_cmd(mne,key,p1) '{
	     if (key == "set_position") {
	      return
	     }
	}'
	
	def show_und'
	   printf("\n%40.40s","Curent Undulator Status")
	'
	
	  # cleanup macro for ^C usage
	  rdef _cleanup3 \'resetUSAXS\'
	  rdef _cleanup3 \'\'
	     cdef("Fheader", fheader,  "UCOL", 0x20)
	     rdef Flabel \'""\'
