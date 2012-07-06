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
#double_quote_string_match   = r'("' + non_greedy_filler + r'")'
#prog_name_match             = r'([a-z_]\w*)'
#word_match                  = r'((?:[a-z_]\w*))'
#cdef_match                  = r'(cdef)'
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
    
    Assume macro definitions are not nested (but test for this).
    
    Assume macro files are small enough to load completely in memory.
        
    An additional step would be to parse for:
    * def    (done)
    * cdef    (done)
    * rdef    (done)
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
                for thing in (
                              self._is_function_macro,
                              self._is_def_macro,
                              self._is_cdef_macro,
                              self._is_lgc_variable,
                              self._is_one_line_extended_comment,
                              self._is_multiline_start_extended_comment
                              ):
                    if thing(line, line_number):
                        break
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
            #raise RuntimeWarning, msg
            print msg

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
        del m['start'], m['end']
        if objtype == 'constant':
            if not len(args.split()) == 2:
                print "line_number, args: ", line_number, args
            var, _ = args.split()
            m['name'] = var.rstrip(',')
            self.findings.append(dict(m))
        else:
            # TODO: consider not indexing "global" inside a def
            # TODO: consider not indexing "local" at global level
            #      or leave these decisions for later, including some kind of analyzer
            for var in args.split():
                m['name'] = var.rstrip(',')
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
        line = m['line']
        del m['start'], m['end']
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
        line = m['line']
        text = m['line'][m['end']:]
        del m['start'], m['end']
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

    def _is_def_macro(self, line, line_number):
        m = self._search(self.spec_macro_declaration_match_re, line)
        if m is None:
            return False
        self.ec = dict(m)
        del self.ec['text']
        m = self.spec_macro_declaration_match_re.match(line)
        macrotype, name, args, comment = m.groups()
        self.ec['start_line'] = line_number
        self.ec['end_line'] = line_number       # TODO: consider the multiline definition later
        self.ec['objtype'] = macrotype
        self.ec['name'] = name
        self.ec['args'] = args
        self.ec['comment'] = comment
        self.findings.append(dict(self.ec))
        del self.ec
        return True

    spec_cdef_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'.*?'                    # optional any kind of preceding stuff, was \s*? (optional blank space)
                            + r'(cdef)'                 # 0: cdef
                            + r'\('                     # opening parenthesis
                            + r'(.*?)'                  # 1: args (anything between the parentheses)
                            + r'\)'                     # closing parenthesis
                            + r'.*?'                    # optional any kind of stuff
                            + r'(#.*?)?'                # 2: optional comment with content
                            + r'$'                      # line end
                        )

    def _is_cdef_macro(self, line, line_number):
        m = self._search(self.spec_cdef_declaration_match_re, line)
        if m is None:
            return False
        self.ec = dict(m)
        del self.ec['text']
        m = self.spec_cdef_declaration_match_re.match(line)
        macrotype, args, comment = m.groups()
        name = args.split(',')[0].strip('"')
        self.ec['start_line'] = line_number
        self.ec['end_line'] = line_number       # TODO: consider the multiline definition later
        self.ec['objtype'] = macrotype
        self.ec['name'] = name
        self.ec['args'] = args
        self.ec['comment'] = comment
        self.findings.append(dict(self.ec))
        del self.ec
        return True

    spec_function_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'\s*?'                   # optional blank space
                            + r'(r?def)'                # 0: def_type (rdef | def)
                            + r'\s*?'                   # optional blank space
                            + r'([a-zA-Z_][\w_]*)'      # 1: function_name
                            + r'\s*?'                   # optional blank space
                            + r'\('                     # opening parenthesis
                            + r'(.*?)'                  # 2: args (anything between the parentheses)
                            + r'\)'                     # closing parenthesis
                            + r'\s*?'                   # optional blank space
                            + r'\''                     # open macro content
                            + r'(.*?)'                  # 3: content, optional
                            + r'(#.*?)?'                # 4: optional comment
                            + r'$'                      # line end
                        )

    def _is_function_macro(self, line, line_number):
        m = self._search(self.spec_function_declaration_match_re, line)
        if m is None:
            return False
        self.ec = dict(m)
        del self.ec['text']
        m = self.spec_function_declaration_match_re.match(line)
        macrotype, name, args, content, comment = m.groups()
        self.ec['start_line'] = line_number
        self.ec['end_line'] = line_number       # TODO: consider the multiline definition later
        self.ec['objtype'] = 'function ' + macrotype
        self.ec['name'] = name
        self.ec['args'] = args
        self.ec['content'] = content
        self.ec['comment'] = comment
        self.findings.append(dict(self.ec))
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
        if not self.state == 'parsed':
            raise RuntimeWarning, "state = %s, should be 'parsed'" % self.filename
        return self._simple_ReST_renderer()

    def _simple_ReST_renderer(self):
        """create a simple ReStructured Text rendition of the findings"""
        if not self.state == 'parsed':
            raise RuntimeWarning, "state = %s, should be 'parsed'" % self.filename
            
        declarations = []       # variables and constants
        macros = []             # def, cdef, and rdef macros
        functions = []          # def and rdef function macros
        #title = 'Extended Comments'
        #s = ['', title, '='*len(title), ]
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
            elif r['objtype'] in ('def', 'rdef', 'cdef', ):
                macros.append(r)
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append( '.. rubric:: %s macro declaration' % r['objtype']  )
                s.append( '' )
                #s.append( '.. spec:%s:: %s %s' % ( r['objtype'], r['name'], r['args'],) )
                s.append( '.. spec:%s:: %s' % ( r['objtype'], r['name'],) )
            elif r['objtype'] in ('function def', 'function rdef',):
                # FIXME:  not getting here, such as for kohzuE_cmd()
                functions.append(r)
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append( '.. rubric:: %s macro function declaration' % r['objtype']  )
                s.append( '' )
                s.append( '.. spec:%s:: %s(%s)' % ( r['objtype'], r['name'], r['args']) )
            elif r['objtype'] in ('local', 'global', 'constant'):
                del r['text']
                declarations.append(r)

        s += report_table('Variable Declarations', declarations, ('start_line', 'objtype', 'name', 'line',))
        s += report_table('Macro Declarations', macros, ('start_line', 'name', 'line',))
        s += report_table('Function Macro Declarations', functions)
        #s += report_table('Findings from .mac File', self.findings, ('start_line', 'objtype', 'line',))

        return '\n'.join(s)


def report_table(title, itemlist, col_keys = ('start_line', 'line',)):
    """ 
    return the itemlist as a reST table
    
    :param str title:  section heading above the table
    :param {str,str} itemlist: database (keyed dictionary) to use for table
    :param [str] col_keys: column labels (must be keys in the dictionary)
    :returns [str]: the table (where each list item is a string of reST)
    """
    if len(itemlist) == 0:
        return []
    rows = []
    last_line = None
    for d in itemlist:
        if d['start_line'] != last_line:
            rows.append( tuple([str(d[key]).strip() for key in col_keys]) )
        last_line = d['start_line']
    return make_table(title, col_keys, rows, '=')


def make_table(title, labels, rows, titlechar = '='):
    """
    build a reST table (internal routine)
    
    :param str title: placed in a section heading above the table
    :param [str] labels: columns labels
    :param [[str]] rows: 2-D grid of data, len(labels) == len(data[i]) for all i
    :param str titlechar: character to use when underlining title as reST section heading
    :returns [str]: each list item is reST
    """
    s = []
    if len(rows) == 0:
        return s
    if len(labels) > 0:
        columns = zip(labels, *rows)
    else:
        columns = zip(*rows)
    widths = [max([len(item) for item in row]) for row in columns]
    separator = " ".join( ['='*key for key in widths] )
    fmt = " ".join( '%%-%ds' % key for key in widths )
    s.append( '' )
    s.append( title )
    s.append( titlechar*len(title) )
    s.append( '' )
    s.append( separator )
    if len(labels) > 0:
        s.append( fmt % labels )
        s.append( separator )
    s.extend( fmt % row for row in rows )
    s.append( separator )
    return s


TEST_DIR = os.path.join('..', 'macros')


if __name__ == '__main__':
    filelist = [f for f in sorted(os.listdir(TEST_DIR)) if f.endswith('.mac')]
    for item in filelist:
        filename = os.path.join(TEST_DIR, item)
        print filename
        p = SpecMacrofileParser(filename)
        print p.ReST()
