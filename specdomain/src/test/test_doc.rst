===============
Acceptance Test
===============

If all links are valid, test is done successfully.


A Real SPEC Macro
======================

This is the first example: :spec:macro:`lp`

.. and also the variable :spec:variable:`A2Rp0`

::

	#===============================================================
	# file lp.mac
	# Written by X. Jiao 06/02/2005 Version 1.0
	#
	# Generic SPEC macros
	#
	# used to send the output of spec commands to the printer
	#============================================================== 
	def lp '
		close("/var/tmp/foo1")
		unix("rm -f /var/tmp/foo1")
		on("/var/tmp/foo1")
		fprintf("/var/tmp/foo1","\n$*\n%s\n",date())
		$*
		off("/var/tmp/foo1")
		u a2ps -f7 /var/tmp/foo1 |lpr
	        u rm /var/tmp/foo1
		printf("$* has been sent to printer\n")
		
	'
	
	A2Rp0 = 15.759			;#  A2Rp center



Global(spec module's contents)
================================

.. spec:function:: function_out_of_module

.. spec:module:: test_module

Single Module 'test_module'
===========================

.. spec:function:: module_function(Identifier)

   test
   
   :param Identifier: identify sender
   :type  Identifier: str
   :return: status
   :rtype:  atom()

.. spec:function:: variable_function(Name[, Option]) -> ok

   test

   :param Name: identify sender
   :type  Name: str
   :param Option: option param
   :type  Option: atom()


..
	.. spec:macro:: HostName
	   
	   Host name of test server.

.. spec:record:: #user_address

   It contains user name, e-mail, address and so on

Test Case - Access Without Module Name in Same Module
-----------------------------------------------------

:spec:mod:`test_module`

:spec:func:`module_function/1`

:spec:func:`variable_function/1`

:spec:func:`variable_function/2`

.. :spec:macro:`HostName`

:spec:record:`#user_address`

Test Case - Access to Default Module Name
-----------------------------------------

:spec:func:`spec:function_out_of_module/0`

.. spec:module dummy_other_module

Test Case - Access With Module Name in Other Module
---------------------------------------------------

:spec:mod:`test_module`

:spec:func:`test_module:module_function`

:spec:func:`test_module:module_function/1`

:spec:func:`test_module:variable_function/1`

:spec:func:`test_module:variable_function/2`

:spec:func:`test_module:variable_function`

.. :spec:macro:`test_module:HostName`

:spec:record:`test_module:#user_address`
