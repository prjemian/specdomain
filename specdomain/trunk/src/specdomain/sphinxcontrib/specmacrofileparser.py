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


# TODO: handle "#: " indicating a description of a variable on the preceding line

class SpecMacrofileParser:
    '''
    Parse a SPEC macro file for macro definitions, 
    variable declarations, and extended comments.

        Since 2002, SPEC has allowed for triple-quoted 
        strings as extended comments.  Few, if any, have used them.
        Assume all extended comments contain ReST formatted comments, 
        *including initial section titles or transitions*.
        The first and simplest thing to do is to read the .mac file and only extract
        all the extended comments and add them as nodes to the current document.
    
    Assume macro definitions are not nested (but test for this).
        
    An additional step would be to parse for:
    * def
    * cdef
    * rdef
    * global    (done)
    * local    (done)
    * constant    (done)
    * array
    * ...
    '''

    # consider using:  docutils.statemachine here
    states = (                  # assume SPEC def macros cannot be nested
        'global',               # the level that provides the SPEC command prompt 
        'extended comment',     # inside a multiline extended comment
        'def macro',            # inside a multiline def macro definition
        'rdef macro',           # inside a multiline rdef macro definition
        'cdef macro',           # inside a multiline cdef macro definition
        'parsed',               # parsing of file is complete
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
        self.state = 'global'
        self.state_stack = []
        for line in self.buf.split('\n'):

            line_number += 1
            if self.state not in self.states:
                # this quickly points out a programmer error
                msg = "unexpected parser state: %s, line %s" % (self.state, line_number)
                raise RuntimeError, msg

            if self.state == 'global':
                if self._is_lgc_variable(line, line_number):
                    continue
                if self._is_one_line_extended_comment(line, line_number):
                    continue
                if self._is_multiline_start_extended_comment(line, line_number):
                    continue
            elif self.state == 'extended comment':
                if not self._is_multiline_end_extended_comment(line, line_number):
                    # multiline extended comment continues
                    self.ec['text'].append(line)
                continue
            elif self.state == 'def macro':
                pass
            elif self.state == 'cdef macro':
                pass
            elif self.state == 'rdef macro':
                pass
        
        if len(self.state_stack) > 0:
            fmt = "encountered EOF while parsing %s, line %d, in state %s, stack=%s"
            msg = fmt % (self.filename, line_number, self.state, self.state_stack)
            raise RuntimeWarning, msg

        self.state = 'parsed'
        
    lgc_variable_sig_re = re.compile(string_start
                                        + non_greedy_whitespace
                                        + r'(local|global|constant)'
                                        + r'((?:,?\s*@?[\w.eE+-]+\[?\]?)*)'
                                        + non_greedy_whitespace
                                        + r'#' + non_greedy_filler
                                        + string_end, 
                                        re.VERBOSE)

    def _is_lgc_variable(self, line, line_number):
        ''' local, global, or constant variable declaration '''
        m = self._search(self.lgc_variable_sig_re, line)
        if m is None:
            return False
        
        objtype, args = self.lgc_variable_sig_re.match(line).groups()
        pos = args.find('#')
        if pos > -1:
            args = args[:pos]
        m['objtype'] = objtype
        m['start_line'] = m['end_line'] = line_number
        del m['start'], m['end'], m['line']
        if objtype == 'constant':
            var, _ = args.split()
            m['text'] = var.rstrip(',')
            self.findings.append(dict(m))
        else:
            # TODO: consider not indexing "global" inside a def
            # TODO: consider not indexing "local" at global level
            #      or leave these decisions for later, including some kind of analyzer
            for var in args.split():
                m['text'] = var.rstrip(',')
                self.findings.append(dict(m))
                # TODO: to what is this local?  (remember the def it belongs to)
        return True
    
    extended_comment_block_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_marker
                                                + r'(' + non_greedy_filler + r')'
                                                + extended_comment_marker
                                                + non_greedy_filler
                                                + string_end, 
                                                re.IGNORECASE|re.DOTALL|re.MULTILINE)

    def _is_one_line_extended_comment(self, line, line_number):
        m = self._search(self.extended_comment_block_sig_re, line)
        if m is None:
            return False
        del m['start'], m['end'], m['line']
        m['objtype'] = 'extended comment'
        m['start_line'] = m['end_line'] = line_number
        m['text'] = m['text'].strip()
        self.findings.append(dict(m))
        return True
    extended_comment_start_sig_re = re.compile(string_start
                                                + non_greedy_whitespace
                                                + extended_comment_match, 
                                                re.IGNORECASE|re.VERBOSE)
    
    def _is_multiline_start_extended_comment(self, line, line_number):
        m = self._search(self.extended_comment_start_sig_re, line)
        if m is None:
            return False
        text = m['line'][m['end']:]
        del m['start'], m['end'], m['line']
        m['objtype'] = 'extended comment'
        m['start_line'] = line_number
        self.ec = dict(m)    # container for extended comment data
        self.ec['text'] = [text]
        self.state_stack.append(self.state)
        self.state = 'extended comment'
        return True

    extended_comment_end_sig_re = re.compile(non_greedy_whitespace
                                                + extended_comment_match
                                                + non_greedy_whitespace
                                                + r'#' + non_greedy_filler
                                                + string_end,
                                                re.IGNORECASE|re.VERBOSE)

    def _is_multiline_end_extended_comment(self, line, line_number):
        m = self._search(self.extended_comment_end_sig_re, line)
        if m is None:
            return False
        text = m['line'][:m['start']]
        self.ec['text'].append(text)
        self.ec['text'] = '\n'.join(self.ec['text'])
        self.ec['end_line'] = line_number
        self.findings.append(dict(self.ec))
        self.state = self.state_stack.pop()
        del self.ec
        return True
    
    def _search(self, regexp, line):
        '''regular expression search of line, returns a match as a dictionary or None'''
        m = regexp.search(line)
        if m is None:
            return None
        # TODO: define a parent key somehow
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
            t = '%s %s %d %d %s' % ('.. ' + '*'*20, 
                                    r['objtype'], 
                                    r['start_line'], 
                                    r['end_line'], 
                                    '*'*20)
            s.append( t )
            s.append( '' )
            s.append( r['text'] )
        return '\n'.join(s)

    def ReST(self):
        """create the ReStructured Text from what has been found"""
        if self.state == 'parsed':
            raise RuntimeWarning, "state = %s, should be 'parsed'" % self.filename
            
        s = []
        declarations = []
        for r in self.findings:
            if r['objtype'] == 'extended comment':
                s.append( '' )
                s.append( '.. %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append(r['text'])
            elif r['objtype'] in ('local', 'global', 'constant'):
                declarations.append(r)      # remember, show this later
            # TODO: other objtypes
        if len(declarations) > 0:
            col_keys = ('text', 'objtype', 'start_line', 'end_line', )
            widths = dict([( key, len(str(key)) ) for key in col_keys])
            for d in declarations:
                widths = dict([( key, max(w, len(str(d[key])))) for key, w in widths.items()])
            separator = " ".join( ["="*widths[key] for key in col_keys] )
            fmt = " ".join( ["%%-%ds"%widths[key] for key in col_keys] )
            s.append( '' )
#            s.append( '.. rubric:: Variable Declarations:' )
            s.append( 'Variable Declarations' )
            s.append( '=====================' )
            s.append( '' )
            s.append( separator )
            s.append( fmt % tuple([str(key) for key in col_keys]) )
            s.append( separator )
            for d in declarations:
                s.append( fmt % tuple([str(d[key]) for key in col_keys]) )
            s.append( separator )
        return '\n'.join(s)


if __name__ == '__main__':
    filelist = [
        '../macros/test-battery.mac',
        '../macros/cdef-examples.mac',
        '../macros/shutter.mac',
    ]
    for item in filelist:
        p = SpecMacrofileParser(item)
        #print p
        print p.ReST()
