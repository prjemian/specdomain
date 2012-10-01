.. $Id$

==========================================================
How to Download and Install the SPEC support into Sphinx
==========================================================

#. download from the subversion repository
#. install into Python
#. test the installation

Requires [#]_
	* Python 2.7 or greater
	* Sphinx 1.1.1 or greater

Download
==========

Retrieve the support package from our subversion repository::

   svn co https://subversion.xray.aps.anl.gov/bcdaext/specdomain/trunk/src/specdomain/ /tmp/specdomain

.. Any tarballs available?

.. _Install:

Install
==========

Continuing from the download above, use the setup tools 
to install the package somewhere on your PYTHONPATH
(you may need admin rights to install into your Python).
This command shows how to install into Python's 
*site-packages* directory::

	cd /tmp/specdomain
	python setup.py install

---------------

.. rubric:: Footnotes
.. [#] The developer used Python 2.7.2 and Sphinx 1.1.2 while writing this support.
		Older versions may work but have not been tested.
