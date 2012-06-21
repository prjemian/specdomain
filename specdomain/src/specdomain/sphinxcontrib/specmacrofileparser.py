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

:copyright: Copyright 2012 by BCDA, Advanced Photon Source, Argonne National Laboratory
:license: ANL Open Source License, see LICENSE for details.
"""

import os
import re


#   http://www.txt2re.com/index-python.php3
#  http://regexpal.com/

string_start                = r'^'
string_end                  = r'$'
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
non_greedy_whitespace       = r'\s*?'
double_quote_string_match   = r'("' + non_greedy_filler + r'")'
prog_name_match             = r'([a-z_]\w*)'
word_match                  = r'((?:[a-z_]\w*))'
cdef_match                  = r'(cdef)'
extended_comment_marker     = r'\"{3}'
extended_comment_match      = r'(' + extended_comment_marker + r')'

macro_sig_re = re.compile(
                               r'''^ ([a-zA-Z_]\w*)         # macro name
                               ''', re.VERBOSE)

func_sig_re = re.compile(word_match + r'\('
                      + r'(' + match_all + r')' 
                      + r'\)', 
                      re.IGNORECASE|re.DOTALL)

cdef_name_sig_re = re.compile(double_quote_string_match, 
                                   re.IGNORECASE|re.DOTALL)


extended_comment_flag_sig_re = re.compile(extended_comment_marker, 
                                               re.IGNORECASE|re.DOTALL)
extended_comment_start_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_match, 
                                                re.IGNORECASE|re.VERBOSE)
extended_comment_end_sig_re = re.compile(non_greedy_whitespace
                                                + extended_comment_match
                                                + non_greedy_whitespace
                                                + r'#' + non_greedy_filler
                                                + string_end,
                                                re.IGNORECASE|re.VERBOSE)
extended_comment_block_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_marker
                                                + r'(' + non_greedy_filler + r')'
                                                + extended_comment_marker
                                                + non_greedy_filler
                                                + string_end, 
                                                re.IGNORECASE|re.DOTALL|re.MULTILINE)
lgc_variable_sig_re = re.compile(string_start
                                    + non_greedy_whitespace
                                    + r'(local|global|constant)'
                                    + r'((?:\s*@?[\w.eE+-]+\[?\]?)*)'
                                    + non_greedy_whitespace
                                    + r'#' + non_greedy_filler
                                    + string_end, 
                                    re.VERBOSE)


class SpecMacrofileParser:
    '''
    Parse a SPEC macro file for macro definitions, 
    variable declarations, and extended comments.
    '''

    states = (                  # assume SPEC def macros cannot be nested
        'global',               # the level that provides the SPEC command prompt 
        'extended comment',     # inside a multiline extended comment
        'def macro',            # inside a multiline def macro definition
        'rdef macro',           # inside a multiline rdef macro definition
        'cdef macro',           # inside a multiline cdef macro definition
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
        state = 'global'
        state_stack = []
        for line in self.buf.split('\n'):
            if state not in self.states:
                raise RuntimeError, "unexpected parser state: " + state
            line_number += 1
            if state == 'global':

                m = self._match(lgc_variable_sig_re, line)
                if m is not None:           # local, global, or constant variable declaration
                    objtype, args = lgc_variable_sig_re.match(line).groups()
                    pos = args.find('#')
                    if pos > -1:
                        args = args[:pos]
                    m['objtype'] = objtype
                    m['start_line'] = m['end_line'] = line_number
                    del m['start'], m['end'], m['line']
                    if objtype == 'constant':
                        var, _ = args.split()
                        m['text'] = var
                        self.findings.append(dict(m))
                    else:
                        # TODO: consider not indexing "global" inside a def
                        # TODO: consider not indexing "local" at global level
                        for var in args.split():
                            m['text'] = var
                            self.findings.append(dict(m))
                            # TODO: to what is this local?  (remember the def it belongs to)
                    continue

                # test if one-line extended comment
                m = self._match(extended_comment_block_sig_re, line)
                if m is not None:
                    del m['start'], m['end'], m['line']
                    m['objtype'] = 'extended comment'
                    m['start_line'] = m['end_line'] = line_number
                    self.findings.append(dict(m))
                    continue
                
                # test if start of multiline extended comment
                m = self._match(extended_comment_start_sig_re, line)
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
                m = self._match(extended_comment_end_sig_re, line)
                if m is not None:
                    text = m['line'][:m['start']]
                    ec['text'].append(text)
                    ec['text'] = '\n'.join(ec['text'])
                    ec['end_line'] = line_number
                    self.findings.append(dict(ec))
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
            'filename':  self.filename,
        }
        return d

    def __str__(self):
        s = []
        for r in self.findings:
            s.append( '' )
            t = '%s %s %d %d %s' % ('*'*20, 
                                    r['objtype'], 
                                    r['start_line'], 
                                    r['end_line'], 
                                    '*'*20)
            s.append( t )
            s.append( r['text'] )
        return '\n'.join(s)

    def ReST(self):
        """create the ReStructured Text from what has been found"""
        s = []
        for r in self.findings:
            if r['objtype'] == 'extended comment':
                s.append( '' )
                s.append( '.. %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append(r['text'])
            # TODO: other objtypes
        return '\n'.join(s)


if __name__ == '__main__':
    p = SpecMacrofileParser('../test/test-battery.mac')
    #print p.ReST()
    print p
    p = SpecMacrofileParser('../test/cdef-examples.mac')
    #print p.ReST()
