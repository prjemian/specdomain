#!/usr/bin/env python

########### SVN repository information ###################
# $Date$
# $Author$
# $Revision$
# $HeadURL$
# $Id$
########### SVN repository information ###################


"""
Construct a SPEC macro source code file parser for 
use by the specdomain for Sphinx.
"""

import os
import re


string_start                = r'^'
string_end                  = r'$'
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
non_greedy_whitespace       = r'\w*?'
double_quote_string_match   = r'("' + non_greedy_filler + r'")'
word_match                  = r'((?:[a-z_]\w*))'
cdef_match                  = r'(cdef)'
extended_comment_marker     = r'\"{3}'
extended_comment_match      = r'(' + extended_comment_marker + r')'

spec_macro_sig_re = re.compile(
                               r'''^ ([a-zA-Z_]\w*)         # macro name
                               ''', re.VERBOSE)

spec_func_sig_re = re.compile(word_match + r'\('
                      + r'(' + match_all + r')' 
                      + r'\)', 
                      re.IGNORECASE|re.DOTALL)

spec_cdef_name_sig_re = re.compile(double_quote_string_match, 
                                   re.IGNORECASE|re.DOTALL)


spec_extended_comment_flag_sig_re = re.compile(extended_comment_marker, 
                                               re.IGNORECASE|re.DOTALL)
spec_extended_comment_start_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_match, 
                                                re.IGNORECASE|re.VERBOSE)
spec_extended_comment_end_sig_re = re.compile(non_greedy_whitespace
                                                + extended_comment_match
                                                + non_greedy_whitespace
                                                + r'#' + non_greedy_filler
                                                + r'$',
                                                re.IGNORECASE|re.VERBOSE)
spec_extended_comment_block_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_marker
                                                + r'(' + non_greedy_filler + r')'
                                                + extended_comment_marker
                                                + non_greedy_filler
                                                + string_end, 
                                                re.IGNORECASE|re.DOTALL|re.MULTILINE)


class SpecMacrofileParser:
    '''
    Parse a SPEC macro file for macro definitions, 
    variable declarations, and extended comments.
    '''

    states = (
        'command level', 
        'extended comment', 
        'def macro', 
        'rdef macro', 
        'cdef macro'
              
    )

    def __init__(self, macrofile):
        '''
        Constructor
        '''
        self.buf = None
        self.findings = []
        self.filename = None
        self.read(macrofile)
        self.parse_macro_file()
    
    def read(self, filename):
        """
        load the SPEC macro source code file into an internal buffer
        
        :param str filename: name (with optional path) of SPEC macro file
            (The path is relative to the ``.rst`` document.)
        """
        if not os.path.exists(filename):
            raise RuntimeError, "file not found: " + filename
        self.filename = filename
        self.buf = open(filename, 'r').read()
    
    def parse_macro_file(self):
        """
        parse the internal buffer
        """
        line_number = 0
        state = 'command level'
        state_stack = []
        for line in self.buf.split('\n'):
            if state not in self.states:
                raise RuntimeError, "unexpected parser state: " + state
            line_number += 1
            if state == 'command level':
                # test if one-line extended comment
                m = self._match(spec_extended_comment_block_sig_re, line)
                if m is not None:
                    del m['start'], m['end'], m['line']
                    m['objtype'] = 'extended comment'
                    m['start_line'] = line_number
                    m['end_line'] = line_number
                    self.findings.append(m)
                    continue
                
                # test if start of multiline extended comment
                m = self._match(spec_extended_comment_start_sig_re, line)
                if m is not None:
                    text = m['line'][m['end']:]
                    del m['start'], m['end'], m['line']
                    m['objtype'] = 'extended comment'
                    m['start_line'] = line_number
                    ec = dict(m)    # container for extended comment data
                    ec['text'] = [text]
                    state_stack.append(state)
                    state = 'extended comment'
                    continue

            elif state == 'extended comment':
                # test if end of multiline extended comment
                if line_number > 250:
                    pass
                m = self._match(spec_extended_comment_end_sig_re, line)
                if m is not None:
                    text = m['line'][:m['start']]
                    ec['text'].append(text)
                    ec['text'] = '\n'.join(ec['text'])
                    ec['end_line'] = line_number
                    self.findings.append(ec)
                    state = state_stack.pop()
                    del ec
                else:
                    # multiline extended comment continues
                    ec['text'].append(line)
                continue
    
    def _match(self, regexp, line):
        m = regexp.search(line)
        if m is None:
            return None
        d = {
            'start': m.start(1),
            'end':   m.end(1),
            'text':  m.group(1),
            'line':  line,
        }
        return d

    def __str__(self):
        s = []
        for r in self.findings:
            s.append( '' )
            t = '%s %s %d %d %s' % ('*'*20, r['objtype'], r['start_line'], r['end_line'], '*'*20)
            s.append( t )
            s.append( r['text'] )
        return '\n'.join(s)


if __name__ == '__main__':
    print SpecMacrofileParser('test-battery.mac')
    print SpecMacrofileParser('cdef-examples.mac')
