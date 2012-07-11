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
use by the specdomain for Sphinx.  This parser locates
code blocks in the SPEC macro source code file across multiple lines.

:copyright: Copyright 2012 by BCDA, Advanced Photon Source, Argonne National Laboratory
:license: ANL Open Source License, see LICENSE for details.
"""

import os
import re
from pprint import pprint

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
macro_name                  = r'[a-zA-Z_][\w_]*'
macro_name_match            = r'(' + macro_name + r')'
arglist_match               = r'(' + match_all + r')'
non_greedy_filler_match     = r'(' + non_greedy_filler + r')'
variable_name_match         = r'(@?' + macro_name + r'\[?\]?)'

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
    * def
    * cdef
    * rdef
    * global
    * local
    * constant
    * array
    * ...
    '''
    
    def __init__(self, macrofile):
        self.buf = None
        self.findings = []
        self.filename = None
        self.read(macrofile)
        self.parse_macro_file()
    
    def read(self, macrofile):
        """
        load the SPEC macro source code file into an internal buffer.
        Also remember the start and end position of each line.
        
        :param str filename: name (with optional path) of SPEC macro file
            (The path is relative to the ``.rst`` document.)
        """
        if not os.path.exists(macrofile):
            raise RuntimeError, "file not found: " + macrofile
        self.filename = macrofile
        buf = open(macrofile, 'r').readlines()
        offset = 0
        lines = []
        for linenumber, line in enumerate(buf):
            end = offset+len(line)
            lines.append([linenumber+1, offset, end])
            offset = end
        self.buf = ''.join(buf)
        self.line_positions = lines
    
    def std_read(self, macrofile):
        """
        load the SPEC macro source code file into an internal buffer
        
        :param str filename: name (with optional path) of SPEC macro file
            (The path is relative to the ``.rst`` document.)
        """
        if not os.path.exists(macrofile):
            raise RuntimeError, "file not found: " + macrofile
        self.filename = macrofile
        self.buf = open(macrofile, 'r').read()

    def parse_macro_file(self):
        ext_com = self.find_extended_comments()
        desc_com = self.find_descriptive_comments()
        def_macro = self.find_def_macro()
        cdef_macro = self.find_cdef_macro()
        vars = self.find_variables()
        
        for linenumber in range(len(self.line_positions)):
            # TODO: decide the parent for each item, expect all def are at global scope
            # TODO: decide which macros and variables should not be documented
            # walk through the line numbers in the file
            #  if a def_macro starts, note its name and set the parent field 
            #     of all comments, variables, var_desc, rdef, and cdef within 
            #     its start_line and end_line range
            #  How to handle descriptive comments?
            pass
        
        self.findings = []
        for item in (ext_com, desc_com, def_macro, cdef_macro, vars,):
            if len(item)>0:
                self.findings.extend(item)
        
    extended_comment_block_sig_re = re.compile(
                            string_start
                            + non_greedy_whitespace
                            + extended_comment_marker
                            + r'(' + non_greedy_filler + r')'
                            + extended_comment_marker
                            + non_greedy_filler
                            + string_end, 
                            re.IGNORECASE|re.DOTALL|re.MULTILINE)

    def find_extended_comments(self):
        """
        parse the internal buffer for triple-quoted strings, possibly multiline
        """
        items = []
        for mo in self.extended_comment_block_sig_re.finditer(self.buf):
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(1))
            text = mo.group(1)
            items.append({
                            'start_line': start, 
                            'end_line':   end, 
                            'objtype':    'extended comment',
                            'text':       text,
                            'parent':     None,
                          })
        return items
        
    variable_description_re = re.compile(
                            string_start
                            + non_greedy_filler
                            + r'#:'
                            + non_greedy_whitespace
                            + r'(' + non_greedy_filler + r')'
                            + non_greedy_whitespace
                            + string_end, 
                            re.IGNORECASE|re.DOTALL|re.MULTILINE)

    def find_descriptive_comments(self):
        """
        Descriptive comments are used to document items that cannot contain
        extended comments (triple-quoted strings) such as variable declarations
        or *rdef* or *cdef* macro declarations.  They appear either in-line
        with the declaration or on the preceding line.
        
        Descriptive comment example that documents *tth*, a global variable declaration::
            
            global tth    #: two-theta, the scattering angle
        
        Descriptive comment example that documents *ccdset_shutter*, a *rdef* declaration::
        
            #: clear the ccd shutter handler
            rdef ccdset_shutter ''
        """
        items = []
        for mo in self.variable_description_re.finditer(self.buf):
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(1))
            items.append({
                            'start_line': start, 
                            'end_line':   end, 
                            'objtype':    'variable description',
                            'text':       mo.group(1),
                            'parent':     None,
                          })
        return items
    
    lgc_variable_sig_re = re.compile(
                            r''
                            + string_start
                            + non_greedy_whitespace
                            + r'(local|global|constant)'        # 1: object type
                            + non_greedy_whitespace
                            + r'(' + non_greedy_filler + r')'   # 2: too complicated to parse all at once
                            + string_end
                            , 
                            re.DOTALL
                            |re.MULTILINE
                        )
    
    variable_name_re = re.compile(
                            variable_name_match, 
                            re.IGNORECASE|re.DOTALL|re.MULTILINE
                            )

    def find_variables(self):
        """
        parse the internal buffer for local, global, and constant variable declarations
        """
        items = []
        for mo in self.lgc_variable_sig_re.finditer(self.buf):
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(1))
            objtype = mo.group(1)
            content = mo.group(2)
            p = content.find('#')
            if p >= 0:                              # strip off any comment
                content = content[:p]
            content = re.sub('[,;]', ' ', content)  # replace , or ; with blank space
            if content.find('[') >= 0:
                content = re.sub('\s*?\[', '[', content)  # remove blank space before [
            for var in self.variable_name_re.finditer(content):
                name = var.group(1)
                if len(name) > 0:
                    items.append({
                                    'start_line': start, 
                                    'end_line':   end, 
                                    'objtype':    objtype,
                                    'name':       name,
                                    'parent':     None,
                                    'text':     'FIX in find_variables(self):',
                                  })
        return items

    spec_macro_declaration_match_re = re.compile(
                            string_start
                            + r'\s*?'                           # optional blank space
                            + r'(r?def)'                        # 1: def_type (rdef | def)
                            + non_greedy_whitespace
                            + macro_name_match                  # 2: macro_name
                            + non_greedy_filler_match           # 3: optional arguments
                            + r'\'\{?'                          # start body section
                            + non_greedy_filler_match           # 4: body
                            + r'\}?\''                          # end body section
                            + r'(#.*?)?'                        # 5: optional comment
                            + string_end, 
                            re.IGNORECASE|re.DOTALL|re.MULTILINE)
        
    args_match = re.compile(
                              r'\('
                            + arglist_match                     # 1:  argument list
                            + r'\)', 
                            re.DOTALL)

    def find_def_macro(self):
        """
        parse the internal buffer for def and rdef macro declarations
        """
        items = []
        for mo in self.spec_macro_declaration_match_re.finditer(self.buf):
            objtype = mo.group(1)
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(4))
            args = mo.group(3)
            if len(args)>2:
                m = self.args_match.search(args)
                if m is not None:
                    objtype = 'function ' + objtype
                    args = m.group(1)
            # TODO: What if args is multi-line?  flatten.  What if really long?
            items.append({
                            'start_line': start, 
                            'end_line':   end, 
                            'objtype':    objtype,
                            'name':       mo.group(2),
                            'args':       args,
                            'body':       mo.group(4),
                            'comment':    mo.group(5),
                            'parent':     None,
                          })
        return items

    def find_cdef_macro(self):
        """
        parse the internal buffer for def and rdef macro declarations
        """
        
        # note:  It is not possible to find properly all variations 
        # of the argument list in a cdef declaration using a regular expression,
        # especially across multiple lines.
        
        items = []
        for mo in re.finditer('cdef\(', self.buf):
            # look at each potential cdef declaration
            objtype = 'cdef'
            s = mo.start()
            start = self.find_pos_in_line_number(s)
            p = mo.end()
            nesting = 1                     # number of nested parentheses
            sign = {'(': 1, ')': -1}        # increment or decrement
            while nesting > 0 and p < len(self.buf):
                if self.buf[p] in sign.keys():
                    nesting += sign[self.buf[p]]
                p += 1
            e = p
            text = self.buf[s+5:e-1]    # carve it out, and remove cdef( ... ) wrapping
            end = self.find_pos_in_line_number(e)
            p = text.find(',')
            name = text[:p].strip('"')
            if len(name) == 0:
                name = '<empty name>'
            args = text[p+1:]
            # TODO: parse "args" for content
            # TODO: What if args is multi-line?  convert \n to ;
            #   args = ';'.join(args.splitlines())  # WRONG: This converts string content, as well
            # TODO: What if args is really long?
            items.append({
                            'start_line': start, 
                            'end_line':   end, 
                            'objtype':    objtype,
                            'name':       name,
                            'args':       args,
#                            'body':       mo.group(4),
#                            'comment':    mo.group(5),
                            'parent':     None,
                          })
        return items

    def find_pos_in_line_number(self, pos):
        """
        find the line number that includes *pos*
        
        :param int pos: position in the file
        """
        # straight search
        # TODO: optimize using search by bisection
        linenumber = None
        for linenumber, start, end in self.line_positions:
            if start <= pos < end:
                break
        return linenumber
    
    #------------------------ reporting section below ----------------------------------

    def ReST(self):
        """create the ReStructured Text from what has been found"""
#        if not self.state == 'parsed':
#            raise RuntimeWarning, "state = %s, should be 'parsed'" % self.filename
        return self._simple_ReST_renderer()

    def _simple_ReST_renderer(self):
        """create a simple ReStructured Text rendition of the findings"""
#        if not self.state == 'parsed':
#            raise RuntimeWarning, "state = %s, should be 'parsed'" % self.filename
            
        declarations = []       # variables and constants
        macros = []             # def, cdef, and rdef macros
        functions = []          # def and rdef function macros
        s = []
        for r in self.findings:
            if r['objtype'] == 'extended comment':
                # TODO: apply rules to suppress reporting under certain circumstances
                s.append( '' )
                s.append( '.. %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append(r['text'])
            elif r['objtype'] in ('def', 'rdef', 'cdef', ):
                # TODO: apply rules to suppress reporting under certain circumstances
                macros.append(r)
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                # TODO: make this next be part of the signature display (in specdomain)
                #s.append( '.. rubric:: %s macro declaration' % r['objtype']  )
                s.append( '' )
                s.append( '.. spec:%s:: %s' % ( r['objtype'], r['name'],) )
            elif r['objtype'] in ('function def', 'function rdef',):
                # TODO: apply rules to suppress reporting under certain circumstances
                functions.append(r)
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                #s.append( '.. rubric:: %s macro function declaration' % r['objtype']  )
                s.append( '' )
                s.append( '.. spec:%s:: %s(%s)' % ( r['objtype'], r['name'], r['args']) )
            elif r['objtype'] in ('local', 'global', 'constant'):
                # TODO: apply rules to suppress reporting under certain circumstances
                del r['text']
                declarations.append(r)

        s += report_table('Variable Declarations (%s)' % self.filename, declarations, ('objtype', 'name', 'start_line', ))
        s += report_table('Macro Declarations (%s)' % self.filename, macros, ('objtype', 'name', 'start_line', 'end_line'))
        s += report_table('Function Macro Declarations (%s)' % self.filename, functions, ('objtype', 'name', 'start_line', 'end_line', 'args'))
        #s += report_table('Findings from .mac File', self.findings, ('start_line', 'objtype', 'line',))

        return '\n'.join(s)


def report_table(title, itemlist, col_keys = ('objtype', 'start_line', 'end_line', )):
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
        pprint (p.findings)
