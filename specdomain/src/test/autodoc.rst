.. $Id$

========================================
Automatically Document a SPEC macro file
========================================

Out goal is to automatically document an example SPEC macro file.  
A similar task in Python might use this SPHINX code::

	:mod:`pvMail` Module
	--------------------
	
	.. automodule:: PvMail.pvMail
	    :members:
	    :undoc-members:
	    :show-inheritance:

Now for the SPEC macro

.. note:: tba
.. awk language support requires Pygments 1.5+
.. literalinclude:: newuser.mac
	:language: guess
	:linenos:
	
