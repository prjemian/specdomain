#!/usr/bin/env python


'''
$Id$

develop regular expression to match macro declarations
'''


import re
import os


spec_macro_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'\s*?'                   # optional blank space
                            + r'(r?def)'                # 0: def_type (rdef | def)
                            + r'\s*?'                   # optional blank space
                            + r'([a-zA-Z_][\w_]*)'      # 1: macro_name
                            + r'(.*?)'                  # 2: optional arguments
                            + r'(#.*?)?'                # 3: optional comment
                            + r'$'                      # line end
                        )
spec_cdef_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'\s*?'                   # optional blank space
                            + r'(cdef)'                 # 0: cdef
                            + r'\('                     # opening parenthesis
                            + r'(.*?)'                  # 1: args (anything between the parentheses)
                            + r'\)'                     # closing parenthesis
                            + r'\s*?'                   # optional blank space
                            + r'(#.*?)?'                # 2: optional comment
                            + r'$'                      # line end
                        )

spec_function_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'\s*?'                   # optional blank space
                            + r'(r?def)'                # 0: def_type (rdef | def)
                            + r'\s*?'                   # optional blank space
                            + r'([a-zA-Z_][\w_]*)'      # 1: function_name
                            + r'\('                     # opening parenthesis
                            + r'(.*?)'                  # 2: args (anything between the parentheses)
                            + r'\)'                     # closing parenthesis
                            + r'\s*?'                   # optional blank space
                            + r'\''                     # open macro content
                            + r'(.*?)'                  # 3: args (anything between the parentheses)
                            + r'(#.*?)?'                # 4: more_content
                            + r'$'                      # line end
                        )

TEST_DIR = os.path.join('..', 'macros')

tests = {
    'macro':    spec_macro_declaration_match_re,
    'cdef':     spec_cdef_declaration_match_re,
    'function': spec_function_declaration_match_re,
}

for f in sorted(os.listdir(TEST_DIR)):
    if f.endswith('.mac'):
        print '\n', f
        for linenumber, line in enumerate(open(os.path.join(TEST_DIR, f)).readlines()):
            for name in ('cdef', 'function', 'macro'):
                m = tests[name].match(line)
                if m is not None:
                    print name, linenumber+1, m.groups()
                    break
