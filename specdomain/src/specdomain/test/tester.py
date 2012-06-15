#!/usr/bin/env python

#  $Id$


import re

#  http://regexpal.com/
#  http://www.txt2re.com/index-python.php3

def tester(test_cases, regexp):
    for s in test_cases.split('\n'):
        if len(s) > 0:
            print s, ":",
            m = regexp.match(s)
            if m is None:
                print ""
            else:
                parselist = m.groups()
                print parselist
    print "#" + "-"*59

##################################################################################

re_spec_global_declaration = re.compile(
    r'''
    ^                                  # start of line
    (\s*)                              # optional preceding white space
    global                             # "global" declaration
            #
            # FIXME: only finds the last symbol
    ([\s]+[@]?[a-zA-Z_][\w]*(\[\])?)+  # variable name(s) + optional array braces
            #
    (\s+\#.*)*                         # optional comments
    $                                  # end of line
    ''', re.VERBOSE
)

test_cases = '''
global  BCDA_GM[]

   global    theta[]
   global    2theta[]  # this will not be found
   global    _motor[]

global kohzu_PV kohzuMV_PV UND_PV Und_Off UNDE_TRACK_ON
global       kohzuStop_PV kohzuMode_PV      kohzuMove_PV
    global CCD_OVERHEAD_SECS_MEASURED   # measured readout time

    global @A_name[] @B_name[]
       unglobal @A_name
       unglobal @B_name
'''

tester(test_cases, re_spec_global_declaration)

##################################################################################

py_sig_re = re.compile(
    r'''^ ([\w.]*\.)?            # class name(s)
          (\w+)  \s*             # thing name
          (?: \((.*)\)           # optional: arguments
           (?:\s* -> \s* (.*))?  #           return annotation
          )? $                   # and nothing more
          ''', re.VERBOSE)

test_cases = '''
the.parent.class.myFunc(a, b) -> answer
f2()
f4(1, None, "four", four, 4, 4.0, "4.0")
'''

tester(test_cases, py_sig_re)

##################################################################################


match_all = '.*'
non_greedy_filler = match_all+'?'
double_quote_string = '("'+non_greedy_filler+'")'
word_match = '((?:[a-z_][\w]*))'
cdef_match = '(cdef)'

regexp_str = ''
regexp_str += non_greedy_filler + double_quote_string
regexp_str += non_greedy_filler + word_match+'?'
regexp_str += non_greedy_filler + word_match+'?'
regexp_str += non_greedy_filler + word_match+'?'

spec_func_re = re.compile(regexp_str, re.IGNORECASE|re.DOTALL)

test_cases = '''
cdef("macro_name", "commands", "partname", "delete")
cdef("macro_name", "commands", "partname", flags)
cdef("cleanup_once", sprintf("dscan_cleanup $1 %s;", _c1), "dscan")
cdef("macro_name", "commands", "partname")
cdef("macro_name")
thing(arg1,arg2)
afunc("tires")
Afunc()
aFunc(parm1)
cdef("geo_ub_default", "", "ub.mac")
cdef("config_mac", "{PLOT_CNTRS_MAX = COUNTERS}", "PLOT_Y", 0x10 )
'''
f = open('cdef-examples.mac', 'r')
buf = f.read()
f.close()
test_cases += buf
tester(test_cases, spec_func_re)

cdef1_re = re.compile(cdef_match+'\('
                      + '('+match_all+')' 
                      + '\)', 
                      re.IGNORECASE|re.DOTALL)
#cdef2_re = re.compile(cdef_match+'\('
#                      + non_greedy_filler + word_match
#                      + non_greedy_filler + word_match
#                      +'\)', 
#                      re.IGNORECASE|re.DOTALL)
func_start_re = re.compile(word_match+'\(',
                      re.IGNORECASE|re.DOTALL)
func_match_re = re.compile(word_match+'\('
                      + '('+match_all+')' 
                      + '\)', 
                      re.IGNORECASE|re.DOTALL)
# cdef1_re is most general for recognizing any of the different cdef signatures
# func_match_re is most general for recognizing any of the different cdef signatures
tester(test_cases, func_match_re)


##################################################################################

txt='\'"macro_name", "content", "groupname", flags\''

uninteresting_csv = non_greedy_filler+','
csv_match = '(' + non_greedy_filler + '),'

re_str=non_greedy_filler        # Non-greedy match on filler
re_str += double_quote_string   # Double Quote String 1
re_str += non_greedy_filler     # Non-greedy match on filler
re_str += uninteresting_csv     # Uninteresting: csv
re_str += non_greedy_filler     # Non-greedy match on filler
re_str += csv_match             # Command Seperated Values 1
re_str += non_greedy_filler     # Non-greedy match on filler
re_str += uninteresting_csv     # Uninteresting: csv
re_str += non_greedy_filler     # Non-greedy match on filler
re_str += csv_match             # Command Seperated Values 2

re_str = "(.*)"

rg = re.compile(re_str, re.IGNORECASE|re.DOTALL)

test_cases = '''
'"macro_name", "commands", "partname", "delete"'
'"macro_name", "commands", "partname", flags'
'"cleanup_once", sprintf("dscan_cleanup $1 %s;", _c1), "dscan"'
'"macro_name", "commands", "partname"'
'"macro_name"'
'"geo_ub_default", "", "ub.mac"'
'"config_mac", "{PLOT_CNTRS_MAX = COUNTERS}", "PLOT_Y", 0x10'
'''
print re_str
tester(test_cases, rg)
