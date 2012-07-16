'''
Created on Jul 11, 2012

@author: Pete
'''


import re
import pyparsing


string_start                = r'^'
string_end                  = r'$'
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
non_greedy_whitespace       = r'\s*?'

spec_cdef_declaration_match_re = re.compile( 
            r''
            + non_greedy_filler         # optional any kind of preceding stuff, was \s*? (optional blank space) 
            + non_greedy_whitespace
            + r'(cdef)'                 # 0: cdef
            + r'\('                     # opening parenthesis 
#                + r'(.*?)'                 # 1: args (anything between the parentheses) 
            + r'(.*?)'                   # 1: args (anything between the parentheses) 
            + r'\)',                    # closing parenthesis
            re.DOTALL | re.MULTILINE | re.VERBOSE
         )


barrage = """
cdef("test1")
cdef("test2","\nwait(1);\n","waitmove_hack","0x20")
cdef("test3",
     "\nwait(1);\n",
     "waitmove_hack",
     "0x20")
cdef("test4", "", "scan_cleanup", "delete")
cdef("test5", sprintf("dscan_cleanup $1 %s;", _c1), "dscan")
"""


for mo in spec_cdef_declaration_match_re.finditer(barrage):
    print mo.groups(), mo.start(), mo.end(), mo.span()

print """
It is not possible to identify properly all these cases with a regular expression

Instead, search for the beginnings of a potential cdef declaration 
'cdef\(' and start watching the code, incrementing and decrementing 
on ( and ) until the counter gets back to zero.
"""