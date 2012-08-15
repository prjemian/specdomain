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
from pprint import pprint        #@UnusedImport

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


        
extended_comment_block_sig_re = re.compile(
                        string_start
                        + non_greedy_whitespace
                        + extended_comment_marker
                        + r'(' + non_greedy_filler + r')'
                        + extended_comment_marker
                        + non_greedy_filler
                        + string_end, 
                        re.IGNORECASE|re.DOTALL|re.MULTILINE)

variable_description_re = re.compile(
                        string_start
                        + non_greedy_filler
                        + r'#:'
                        + non_greedy_whitespace
                        + r'(' + non_greedy_filler + r')'
                        + non_greedy_whitespace
                        + string_end, 
                        re.IGNORECASE|re.DOTALL|re.MULTILINE)

    
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

arg_list_match = r'(\(' + non_greedy_filler + r'\))?'

spec_macro_declaration_match_re = re.compile(
                        string_start
                        + r'\s*?'                           # optional blank space
                        + r'(r?def)\s'                      # 1: def_type (rdef | def)
                        + non_greedy_whitespace
                        + macro_name_match                  # 2: macro_name
                        + arg_list_match                    # 3: optional arguments
                        + non_greedy_whitespace
                        + '\''                              # start body section
                        + non_greedy_filler_match           # 4: body
                        + '\''                              # end body section
                        + non_greedy_whitespace
                        + r'(#.*?)?'                        # 5: optional comment
                        + string_end
                        , 
                        re.IGNORECASE|re.DOTALL|re.MULTILINE)



args_match_re = re.compile(
                          r'\('
                        + arglist_match                     # 1:  argument list
                        + r'\)', 
                        re.DOTALL)

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
        self.description = ''
        self.clear_description = False
        self.found_first_global_extended_comment = False
    
    def read(self, macrofile):
        """
        load the SPEC macro source code file into an internal buffer (self.buf).
        Also remember the start and end position of each line (self.line_positions).
        
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
        """
        Figure out what can be documented in the file's contents (in self.buf)
        
            each of the list_something() methods returns a 
            list of dictionaries where each dictionary 
            has the keys: objtype, start_line, end_line, and others
        """
        db = self._make_db()        # first, the file parsing
        
        # Build a dict with objecttype for keys and methods for values
        # each method handles that particular spec macro file structure
        handler_method = {
            'cdef': self.handle_other,
            'constant': self.handle_other,
            'def': self.handle_def,
            'descriptive comment': self.handle_descriptive_comment,
            'extended comment': self.handle_extended_comment,
            'function def': self.handle_def,
            'global': self.handle_other,
            'local': self.handle_other,
            'rdef': self.handle_other,
        }
        process_first_list = ('descriptive comment', )
        
        # then analyze what was found
        # proceed line-by-line in order
        # TODO: could override this rule with a sort-order option
        self.findings = []
        self.description = ''
        self.clear_description = False
        self.found_first_global_extended_comment = False
        for linenumber in sorted(db.keys()):
            # Diagnostic line for development only
            #print linenumber, ':', ' '.join(['<%s>' % d['objtype'] for d in db[linenumber]])
            
            # process any descriptive comment first
            for item in db[linenumber]:
                if item['objtype'] in process_first_list:
                    handler_method[item['objtype']](item, db)
            # now process the others
            for item in db[linenumber]:
                if item['objtype'] not in process_first_list:
                    handler_method[item['objtype']](item, db)
            
            if self.clear_description:
                self.description, self.clear_description = '', False
    
    def _make_db(self):
        """build the db dict by parsing for each type of structure"""
        db = {}
        # first, the file parsing
        for func in (self.list_def_macros, 
                     self.list_cdef_macros,
                     self.list_variables,
                     self.list_extended_comments,
                     self.list_descriptive_comments,
                     ):
            for item in func():
                s = item['start_line']
                if s not in db.keys():
                    db[s] = []
                db[s].append(item)
        return db

    def handle_def(self, node, db):
        """document SPEC def structures"""
        # identify all the children of this node
        parent = node['name']
        self.found_first_local_extended_comment = False
        if node.get('comment') is not None:
            node['description'] = node.get('comment').lstrip('#:').strip()
        if len(self.description)>0:
            node['description'] = self.description
        for row in xrange(node['start_line']+1, node['end_line']-1):
            if row in db.keys():
                for item in db[row]:
                    item['parent'] = parent
                    if item['objtype'] == 'extended comment':
                        if not self.found_first_local_extended_comment:
                            # TODO: could override this rule with an option
                            node['description'] = item['text']
                            self.found_first_local_extended_comment = False
        if not node['name'].startswith('_'):
            # TODO: could override this rule with an option
            self.findings.append(node)
        node['summary'] = self._extract_summary(node.get('description', ''))
        self.clear_description = True
    
    def handle_descriptive_comment(self, node, db):
        """document SPEC descriptive comment structures"""
        self.description = node['text']
    
    def handle_extended_comment(self, node, db):
        """document SPEC extended comment structures"""
        #start = node['start_line']
        if node['parent'] == None:
            if not self.found_first_global_extended_comment:
                # TODO: could override this rule with an option
                self.findings.append(node)
                self.found_first_global_extended_comment = True
    
    def handle_other(self, node, db):
        """document SPEC cdef, constant, global, local, and rdef structures"""
        if len(self.description)>0:
            node['description'] = self.description
            node['summary'] = self._extract_summary(self.description)
            self.clear_description = True
        if not node['name'].startswith('_'):
            # TODO: could override this rule with an option
            self.findings.append(node)
    
#    def _handle_ignore(self, node, db):
#        """call this handler to ignore an identified SPEC macro file structure"""
#        pass

    def _extract_summary(self, description):
        """
        return the short summary line from the item description text
        
        The summary line is the first line in the docstring,
        such as the line above.
        
        For our purposes now, we return the first paragraph, 
        if it is not a parameter block such as ``:param var: ...``.
        """
        if len(description) == 0:
            return ''
        text = []
        for line in description.strip().splitlines():
            if len(line.strip()) == 0:
                break
            if not line.strip().startswith(':'):
                text.append(line)
        return ' '.join(text)

    def list_extended_comments(self):
        """
        parse the internal buffer for triple-quoted strings, possibly multiline
        
        Usually, an extended comment is used at the top of a macro file
        to describe the file's contents.  It is also used at the top 
        of a macro definition to describe the macro.  The first line
        of an extended comment for a macro should be a short summary,
        followed by a blank line, then either a parameter list or
        more extensive documentation, as needed.
        """
        items = []
        for mo in extended_comment_block_sig_re.finditer(self.buf):
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

    def list_descriptive_comments(self):
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
        for mo in variable_description_re.finditer(self.buf):
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(1))
            items.append({
                            'start_line': start, 
                            'end_line':   end, 
                            'objtype':    'descriptive comment',
                            'text':       mo.group(1),
                            'parent':     None,
                          })
        return items

    def list_variables(self):
        """
        parse the internal buffer for local, global, and constant variable declarations
        """
        items = []
        for mo in lgc_variable_sig_re.finditer(self.buf):
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(1))
            objtype = mo.group(1)
            content = mo.group(2)
            p = content.find('#')
            if p >= 0:                                      # strip off any comment
                content = content[:p]
            content = re.sub('[,;]', ' ', content)          # replace , or ; with blank space
            if content.find('[') >= 0:
                content = re.sub('\s*?\[', '[', content)    # remove blank space before [
            if objtype in ('constant'):
                name = content.strip().split()[0]
                items.append({
                                'start_line': start, 
                                'end_line':   end, 
                                'objtype':    objtype,
                                'name':       name,
                                'parent':     None,
                              })
            else:
                for var in variable_name_re.finditer(content):
                    name = var.group(1)
                    if len(name) > 0:
                        items.append({
                                        'start_line': start, 
                                        'end_line':   end, 
                                        'objtype':    objtype,
                                        'name':       name,
                                        'parent':     None,
                                      })
        return items

    def list_def_macros(self):
        """
        parse the internal buffer for def and rdef macro declarations
        """
        items = []
        for mo in spec_macro_declaration_match_re.finditer(self.buf):
            objtype = mo.group(1)
            start = self.find_pos_in_line_number(mo.start(1))
            end = self.find_pos_in_line_number(mo.end(4))
            args = mo.group(3)
            # TODO: What if args is multi-line?  flatten.  What if really long?
            if args is not None:
                if len(args)>2:
                    m = args_match_re.search(args)
                    if m is not None:
                        objtype = 'function ' + objtype
                        args = m.group(1)
            d = {
                'start_line': start, 
                'end_line':   end, 
                'objtype':    objtype,
                'name':       mo.group(2),
                'args':       str(args),
                'body':       mo.group(4),
                'comment':    mo.group(5),
                'parent':     None,
            }
            items.append(d)
        return items

    def list_cdef_macros(self):
        """
        parse the internal buffer for cdef macro declarations
        """
        # too complicated for a regular expression, just look for the initial part
        items = []
        for mo in re.finditer('cdef\s*?\(', self.buf):
            # look at each potential cdef declaration
            objtype = 'cdef'
            start = self.find_pos_in_line_number(mo.start())
            s = p = mo.end()                # offset s for start of args
            nesting = 1                     # number of nested parentheses
            sign = {'(': 1, ')': -1}        # increment or decrement
            while nesting > 0 and p < len(self.buf):
                if self.buf[p] in sign.keys():
                    nesting += sign[self.buf[p]]
                p += 1
            e = p
            text = self.buf[s:e-1]    # carve it out, and remove cdef( ... ) wrapping
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
        # TODO: optimize this straight search using a search by bisection
        linenumber = None
        for linenumber, start, end in self.line_positions:
            if start <= pos < end:
                break
        return linenumber
    
    #------------------------ reporting section below ----------------------------------

    def _simple_ReST_renderer(self):
        """create a simple ReStructured Text rendition of the findings"""
        declarations = []       # variables and constants
        macros = []             # def, cdef, and rdef macros
        functions = []          # def and rdef function macros
        s = []
        for r in self.findings:
            # TODO: need to define subsections such as these:
            #    Summary (if present)
            #    Documentation (if present)
            #    Declarations
            #    Tables
            if r['objtype'] == 'extended comment':
                # TODO: apply rules to suppress reporting under certain circumstances
                s.append( '' )
                s.append( '.. %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '' )
                s.append(r['text'])
                s.append( '' )
#                s.append( '-'*10 )
#                s.append( '' )
            elif r['objtype'] in ('def', 'rdef', 'cdef', ):
                # TODO: apply rules to suppress reporting under certain circumstances
                macros.append(r)
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              r['objtype'], 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '.. spec:%s:: %s' % ( r['objtype'], r['name'],) )
                s.append('')
                s.append(' '*4 + '*' + r['objtype'] + ' macro declaration*')
                desc = r.get('description', '')
                if len(desc) > 0:
                    s.append('')
                    for line in desc.splitlines():
                        s.append(' '*4 + line)
                s.append( '' )
            elif r['objtype'] in ('function def', 'function rdef',):
                # TODO: apply rules to suppress reporting under certain circumstances
                functions.append(r)
                objtype = r['objtype'].split()[1]
                s.append( '' )
                s.append( '.. %s %s %s %d %d' % (self.filename, 
                                              objtype, 
                                              r['name'], 
                                              r['start_line'], 
                                              r['end_line']) )
                s.append( '.. spec:%s:: %s(%s)' % ( objtype, r['name'], r['args']) )
                s.append('')
                s.append(' '*4 + '*' + r['objtype'].split()[1] + '() macro function declaration*')
                desc = r.get('description', '')
                if len(desc) > 0:
                    s.append('')
                    for line in desc.splitlines():
                        s.append(' '*4 + line)
                s.append( '' )
            
            # Why document local variables in a global scope?
            elif r['objtype'] in ('global', 'constant'):
                # TODO: apply rules to suppress reporting under certain circumstances
                declarations.append(r)
                if r.get('parent') is None:
                    s.append( '.. spec:%s:: %s' % ( r['objtype'], r['name']) )
                    s.append('')
                    if r['objtype'] in ('constant'):
                        s.append(' '*4 + '*constant declaration*')
                    else:
                        s.append(' '*4 + '*' + r['objtype'] + ' variable declaration*')
                    desc = r.get('description', '')
                    if len(desc) > 0:
                        s.append('')
                        for line in desc.splitlines():
                            s.append(' '*4 + line)
                    s.append( '' )

#        s.append( '-'*10 )
#        s.append( '' )

        s += _report_table('Variable Declarations (%s)' % self.filename, declarations, 
                          ('objtype', 'name', 'start_line', 'summary', ))
        s += _report_table('Macro Declarations (%s)' % self.filename, macros, 
                          ('objtype', 'name', 'start_line', 'end_line', 'summary', ))
        s += _report_table('Function Macro Declarations (%s)' % self.filename, functions, 
                          ('objtype', 'name', 'start_line', 'end_line', 'args', 'summary', ))
        #s += _report_table('Findings from .mac File', self.findings, ('start_line', 'objtype', 'line', 'summary', ))

        return '\n'.join(s)

    def ReST(self, style = 'simple'):
        """create the ReStructured Text from what has been found"""
    
        # allow for additional renderers, selectable by options
        renderer_dict =  {'simple': self._simple_ReST_renderer,}
        if style not in renderer_dict:
            raise RuntimeWarning, "%s renderer not found, using `simple`" % style
        return renderer_dict[style]()


def _report_table(title, itemlist, col_keys = ('objtype', 'start_line', 'end_line', )):
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
            rowdata = [str(d.get(key,'')).strip() for key in col_keys]
            rows.append( tuple(rowdata) )
        last_line = d['start_line']
    return make_rest_table(title, col_keys, rows, '=')


def make_rest_table(title, labels, rows, titlechar = '='):
    """
    build a reST table
    
    :param str title: placed in a section heading above the table
    :param [str] labels: columns labels
    :param [[str]] rows: 2-D grid of data, len(labels) == len(data[i]) for all i
    :param str titlechar: character to use when underlining title as reST section heading
    :returns [str]: each list item is reST
    """
    # this is commented out since it causes a warning when building:
    #  specmacrofileparser.py:docstring of sphinxcontrib.specmacrofileparser.make_rest_table:14: WARNING: Block quote ends without a blank line; unexpected unindent.
    # -----
    #    """
    #    build a reST table
    #        
    #    :param str title: placed in a section heading above the table
    #    :param [str] labels: columns labels
    #    :param [[str]] rows: 2-D grid of data, len(labels) == len(data[i]) for all i
    #    :param str titlechar: character to use when underlining title as reST section heading
    #    :returns [str]: each list item is reST
    #
    #    Example::
    #        
    #        title = 'This is a reST table'
    #        labels = ('name', 'phone', 'email')
    #        rows = [
    #                ['Snoopy',           '12345', 'dog@house'],
    #                ['Red Baron',        '65432', 'fokker@triplane'],
    #                ['Charlie Brown',    '12345', 'main@house'],
    #        ]
    #        print '\n'.join(make_rest_table(title, labels, rows, titlechar='~'))
    #
    #    This results in this reST::
    #    
    #        This is a reST table
    #        ~~~~~~~~~~~~~~~~~~~~
    #        
    #        ============= ===== ===============
    #        name          phone email          
    #        ============= ===== ===============
    #        Snoopy        12345 dog@house      
    #        Red Baron     65432 fokker@triplane
    #        Charlie Brown 12345 main@house     
    #        ============= ===== ===============
    #    
    #    """
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
    s.extend( [fmt % tuple(row) for row in rows] )
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
        #pprint (p.findings)
