.. $Id$

===========
Known bugs
===========

* Duplicate ID warnings, for now, ignore them, the warning will be resolved in a future revision
* roles should link to directives, see *example.mac* to illustrate the problem
* fix the signature recognition for roles
* fix the signature handling for roles and directives
* grep detection of macros fails for def declarations in extended comments (TRAC ticket #11)::

	> I found the cause of the processing error. It must have something to do
	> the the regex you use to identify definitions. Line 65 in the header
	> docstring started with the word "defined". Somehow that triggered the
	> regexp, which collected everything up to the next "(", which happens to be
	> on line 69 "(2*AUTO_FILTER_FACTOR)".
	> I temporarily fixed the problem by moving the word "defined" to the end of
	> the previous line, but this fluke could potentially arise again. Is there
	> a way of not searching for any of the function declarations (def, cdef,
	> rdef, global, ...) inside a docstring? Otherwise, you may have to improve
	> the regex.
