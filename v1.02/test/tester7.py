'''
Created on Jul 15, 2012

@author: Pete
'''


import os
import re


string_start                = r'^'
string_end                  = r'$'
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
non_greedy_whitespace       = r'\s*?'
extended_comment_marker     = r'\"{3}'
extended_comment_match      = r'(' + extended_comment_marker + r')'
macro_name                  = r'[a-zA-Z_][\w_]*'
macro_name_match            = r'(' + macro_name + r')'
arglist_match               = r'(' + match_all + r')'
non_greedy_filler_match     = r'(' + non_greedy_filler + r')'
variable_name_match         = r'(@?' + macro_name + r'\[?\]?)'


spec_macro_declaration_match_re = re.compile(
                        string_start
                        + r'\s*?'                           # optional blank space
                        + r'(r?def)\s'                      # 1: def_type (rdef | def)
                        + non_greedy_whitespace
                        + macro_name_match                  # 2: macro_name
                        + non_greedy_filler_match           # 3: optional arguments
                        + r'\'\{?'                          # start body section
                        + non_greedy_filler_match           # 4: body
                        + r'\}?\''                          # end body section
                        + r'(#.*?)?'                        # 5: optional comment
                        + string_end, 
                        re.IGNORECASE|re.DOTALL|re.MULTILINE)


TESTFILE = os.path.join('..', 'comparison', 'problem-auto.mac')
buf = open(TESTFILE, 'r').read()

for mo in spec_macro_declaration_match_re.finditer(buf):
    print mo.groups(), mo.start(), mo.end(), mo.span()

