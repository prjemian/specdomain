#!/usr/bin/env python

#  $Id$


"""
test various regular expressions to locate arguments 
to cdef for a particular case from standard.mac
"""

import re


s = u'"cdef_macro", sprintf("dscan_cleanup $1 %s;", _c1), "cdef_part", flags'

WORD_STRING_MATCH = '([a-z_]\w*)'
DOUBLE_QUOTE_STRING_MATCH = '(".*?")'
DELIMITER_STRING_MATCH = ",?\s*"
WORD_OR_DQS_MATCH = DOUBLE_QUOTE_STRING_MATCH+'|'+WORD_STRING_MATCH
WORD_OR_DQS_MATCH = '([a-z_]\w*|".*?")'

arg1_re = re.compile(DOUBLE_QUOTE_STRING_MATCH, re.IGNORECASE|re.DOTALL)
arg2_re = re.compile(DOUBLE_QUOTE_STRING_MATCH 
                     + DELIMITER_STRING_MATCH 
                     + DOUBLE_QUOTE_STRING_MATCH
                     , re.IGNORECASE|re.DOTALL)
arg3_re = re.compile(DOUBLE_QUOTE_STRING_MATCH 
                     + DELIMITER_STRING_MATCH 
                     + DOUBLE_QUOTE_STRING_MATCH
                     + DELIMITER_STRING_MATCH 
                     + DOUBLE_QUOTE_STRING_MATCH
                     , re.IGNORECASE|re.DOTALL)
arg4_re = re.compile(DOUBLE_QUOTE_STRING_MATCH 
                     + DELIMITER_STRING_MATCH 
                     + WORD_OR_DQS_MATCH
                     + DELIMITER_STRING_MATCH 
                     + DOUBLE_QUOTE_STRING_MATCH
                     + DELIMITER_STRING_MATCH 
                     + WORD_OR_DQS_MATCH
                     , re.IGNORECASE|re.DOTALL)

for i, regexp in enumerate((arg1_re, arg2_re, arg3_re, arg4_re)):
    m = regexp.match(s)
    if m is not None:
        print i, m.groups()
