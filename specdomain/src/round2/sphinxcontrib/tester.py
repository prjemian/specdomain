'''
Created on Jun 12, 2012

@author: Pete
'''


import re

# http://www.greenend.org.uk/rjk/tech/regexp.html

spec_func_sig_re = re.compile(
    r'''^ ([a-zA-Z_]\w*)         # macro name
          ((\s+\S+)*)            # optional: arguments
          $                      # and nothing more
          ''', re.VERBOSE)

test_group = """
example_runtime_defined_macro content
test_macro2 arg1   1.0 2     3
simple_macro
_do_this    4    5    7
5testmacro
"""

for phrase in test_group.split("\n"):
    print "testing:", phrase, "\t --> ",
    m = spec_func_sig_re.match(phrase)
    if m is None:
        print "no match"
    else:
        name, args, last = m.groups()
        print name, args.strip().split()

spec_macro_sig_re = re.compile(
    r'''^ ([a-zA-Z_]\w*)         # macro name
          ''', re.VERBOSE)

sig = u'cdef(macro_name, content, groupname, flags)'
m = spec_macro_sig_re.match(sig)
print m.groups()
print args

