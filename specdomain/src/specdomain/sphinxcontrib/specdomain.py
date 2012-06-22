# -*- coding: utf-8 -*-
"""
    sphinxcontrib.specdomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: SPEC domain for Sphinx
    
    Automatically insert ReST-formatted extended comments 
    from SPEC files for macro definitions and variable declarations into
    the Sphinx doctree, thus avoiding duplication between docstrings and documentation
    for those who like elaborate docstrings.

    :copyright: Copyright 2012 by BCDA, Advanced Photon Source, Argonne National Laboratory
    :license: ANL Open Source License, see LICENSE for details.
"""

# http://sphinx.pocoo.org/ext/appapi.html

import os
import re
import string                                           #@UnusedImport
import sys                                              #@UnusedImport

from docutils import nodes                              #@UnusedImport
from docutils.parsers.rst import directives             #@UnusedImport

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _                         #@UnusedImport
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType, Index       #@UnusedImport
from sphinx.util.compat import Directive                #@UnusedImport
from sphinx.util.nodes import make_refnode, nested_parse_with_titles
from sphinx.util.docfields import Field, TypedField
from sphinx.util.docstrings import prepare_docstring    #@UnusedImport

#from docutils.statemachine import ViewList, string2lines
#import sphinx.util.nodes
from sphinx.ext.autodoc import Documenter, bool_option
#from sphinx.util.inspect import getargspec, isdescriptor, safe_getmembers, \
#     safe_getattr, safe_repr
#from sphinx.util.pycompat import base_exception, class_types
from specmacrofileparser import SpecMacrofileParser


# TODO: merge these with specmacrofileparser.py
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
double_quote_string_match   = r'("' + non_greedy_filler + r'")'
word_match                  = r'((?:[a-z_]\w*))'
cdef_match                  = r'(cdef)'
extended_comment_flag       = r'\"\"\"'


spec_macro_sig_re = re.compile(
                               r'''^ ([a-zA-Z_]\w*)         # macro name
                               ''', re.VERBOSE)

spec_func_sig_re = re.compile(word_match + r'\('
                      + r'(' + match_all + r')' 
                      + r'\)', 
                      re.IGNORECASE|re.DOTALL)

spec_cdef_name_sig_re = re.compile(double_quote_string_match, 
                                   re.IGNORECASE|re.DOTALL)


spec_extended_comment_flag_sig_re = re.compile(extended_comment_flag, 
                                               re.IGNORECASE|re.DOTALL)
spec_extended_comment_start_sig_re = re.compile(r'^'
                                                + non_greedy_filler
                                                + extended_comment_flag, 
                                                re.IGNORECASE|re.DOTALL)
spec_extended_comment_block_sig_re = re.compile(r'^'
                                                + non_greedy_filler
                                                + extended_comment_flag
                                                + r'(' + non_greedy_filler + r')'
                                                + extended_comment_flag
                                                + non_greedy_filler
                                                + r'$', 
                                                re.IGNORECASE|re.DOTALL|re.MULTILINE)


class SpecMacroDocumenter(Documenter):
    """
    Document a SPEC macro source code file (autodoc.Documenter subclass)
    
    This code responds to the ReST file directive::
    
        .. autospecmacro:: partial/path/name/somefile.mac
            :displayorder: fileorder
    
    The ``:displayorder`` parameter indicates how the
    contents will be sorted for appearance in the ReST document.
    
        **fileorder** or **file**
            Items will be documented in the order in 
            which they appear in the ``.mac`` file.
        
        **alphabetical** or **alpha**
            Items will be documented in alphabetical order.
    
    .. tip::
        A (near) future enhancement will provide for
        documenting all macro files in a directory, with optional
        recursion into subdirectories.  By default, the code will 
        only document files that match the glob pattern ``*.mac``.
        (This could be defined as a list in the ``conf.py`` file.)
        Such as::
        
           .. spec:directory:: partial/path/name
              :recursion:
              :displayorder: alphabetical
    """

    objtype = 'specmacro'
    member_order = 50
    priority = 0

    option_spec = {
        'displayorder': bool_option,
    }

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        # don't document submodules automatically
        #return isinstance(member, (FunctionType, BuiltinFunctionType))
        r = membername in ('SpecMacroDocumenter', )
        return r
    
    def generate(self, *args, **kw):
        """
        Generate reST for the object given by *self.name*, and possibly for
        its members.

        If *more_content* is given, include that content. If *real_modname* is
        given, use that module name to find attribute docs. If *check_module* is
        True, only generate if the object is defined in the module name it is
        imported from. If *all_members* is True, document all members.
        """
        # now, parse the SPEC macro file
        macrofile = self.parse_name()
        spec = SpecMacrofileParser(macrofile)
        extended_comment = spec.ReST()
        
        # FIXME:
        #     Assume all extended comments contain ReST formatted comments, 
        #     *including initial section titles or transitions*.
        '''
            cdef-examples.mac:7: SEVERE: Unexpected section title.
            
            Examples of SPEC cdef macros
            ==============================
            test-battery.mac:4: SEVERE: Unexpected section title or transition.
            
            ###############################################################################
            test-battery.mac:6: WARNING: Block quote ends without a blank line; unexpected unindent.
            test-battery.mac:6: SEVERE: Unexpected section title or transition.
            
            ###############################################################################
            test-battery.mac:19: SEVERE: Unexpected section title.
            
            common/shutter
            ==============
        '''

        rest = prepare_docstring(extended_comment)

        #self.add_line(u'', '<autodoc>')
        #sig = self.format_signature()
        #self.add_directive_header(sig)
        
        # TODO: Another step should (like for Python) attach source code and provide
        #       links from each to highlighted source code blocks.
        # This works for now.
        self.add_line(u'', '<autodoc>')
        line = 'source code:  :download:`%s <%s>`' % (macrofile, macrofile)
        self.add_line(line, macrofile)
        # TODO: Add each .mac file name to the Index
        
        self.add_line(u'', '<autodoc>')
        for linenumber, line in enumerate(rest):
            self.add_line(line, macrofile, linenumber)
        #self.add_content(rest)
        #self.document_members(all_members)

    def resolve_name(self, modname, parents, path, base):
        if modname is not None:
            self.directive.warn('"::" in autospecmacro name doesn\'t make sense')
        return (path or '') + base, []

    def parse_name(self):
        """Determine what file to parse.
        
        :returns: True if if parsing was successful

        .. Note:: The template method from autodoc sets *self.modname*, *self.objpath*, *self.fullname*,
            *self.args* and *self.retann*.  This is not done here yet.
        """
        ret = self.name
        self.fullname = os.path.abspath(ret)        # TODO: Consider using this
        self.fullname = ret                         # TODO: provisional
        if self.args or self.retann:
            self.directive.warn('signature arguments or return annotation '
                                'given for autospecmacro %s' % self.fullname)
        return ret


class SpecMacroObject(ObjectDescription):
    """
    Description of a SPEC macro definition
    """

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument',
                          'keyword', 'kwarg', 'kwparam'),
                   typerolename='def', typenames=('paramtype', 'type'),
                   can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype',)),
    ]

    def add_target_and_index(self, name, sig, signode):
        targetname = '%s-%s' % (self.objtype, name)
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        indextext = self._get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              targetname, ''))

    def _get_index_text(self, name):
        macro_types = {
            'def':  'SPEC macro definition; %s',
            'rdef': 'SPEC run-time macro definition; %s',
            'cdef': 'SPEC chained macro definition; %s',
        }
        if self.objtype in macro_types:
            return _(macro_types[self.objtype]) % name
        else:
            return ''

    def handle_signature(self, sig, signode):
        # Must be able to match these (without preceding def or rdef)
        #     def macro_name
        #     def macro_name()
        #     def macro_name(arg1, arg2)
        #     rdef macro_name
        #     cdef("macro_name", "content", "groupname", flags)
        m = spec_func_sig_re.match(sig) or spec_macro_sig_re.match(sig)
        if m is None:
            raise ValueError
        arglist = m.groups()
        name = arglist[0]
        args = []
        if len(arglist) > 1:
            args = arglist[1:]
            if name == 'cdef':
                # TODO: need to match complete arg list
                # several different signatures are possible (see cdef-examples.mac)
                # for now, just get the macro name and ignore the arg list
                m = spec_cdef_name_sig_re.match(args[0])
                arglist = m.groups()
                name = arglist[0].strip('"')
                args = ['<<< cdef argument list not handled yet >>>']       # FIXME:
        signode += addnodes.desc_name(name, name)
        if len(args) > 0:
            signode += addnodes.desc_addname(args, args)
        return name


class SpecVariableObject(ObjectDescription):
    """
    Description of a SPEC variable
    """
    
    # TODO: The directive that declares the variable should be the primary (bold) index.
    # TODO: array variables are not handled at all
    # TODO: variables cited by *role* should link back to their *directive* declarations

class SpecXRefRole(XRefRole):
    """ """
    
    def process_link(self, env, refnode, has_explicit_title, title, target):
        key = ":".join((refnode['refdomain'], refnode['reftype']))
        refnode[key] = env.temp_data.get(key)        # key was 'spec:def'
        if not has_explicit_title:
            title = title.lstrip(':')   # only has a meaning for the target
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                colon = title.rfind(':')
                if colon != -1:
                    title = title[colon+1:]
        return title, target

    def result_nodes(self, document, env, node, is_ref):
        # this code adds index entries for each role instance
        if not is_ref:
            return [node], []
        varname = node['reftarget']
        tgtid = 'index-%s' % env.new_serialno('index')
        indexnode = addnodes.index()
        indexnode['entries'] = [
            ('single', varname, tgtid, ''),
            #('single', _('environment variable; %s') % varname, tgtid, ''),
        ]
        targetnode = nodes.target('', '', ids=[tgtid])
        document.note_explicit_target(targetnode)
        return [indexnode, targetnode, node], []


class SpecDomain(Domain):
    """SPEC language domain."""
    
    name = 'spec'
    label = 'SPEC, http://www.certif.com'
    object_types = {    # type of object that a domain can document
        'def':        ObjType(l_('def'),        'def'),
        'rdef':       ObjType(l_('rdef'),       'rdef'),
        'cdef':       ObjType(l_('cdef'),       'cdef'),
        'global':     ObjType(l_('global'),     'global'),
        'local':      ObjType(l_('local'),      'local'),
        'constant':   ObjType(l_('constant'),   'constant'),
        #'specmacro':  ObjType(l_('specmacro'),  'specmacro'),
    }
    directives = {
        'def':          SpecMacroObject,
        'rdef':         SpecMacroObject,
        'cdef':         SpecMacroObject,
        'global':       SpecVariableObject,
        'local':        SpecVariableObject,
        'constant':     SpecVariableObject,
    }
    roles = {
        'def' :     SpecXRefRole(),
        'rdef':     SpecXRefRole(),
        'cdef':     SpecXRefRole(),
        'global':   SpecXRefRole(),
        'local':    SpecXRefRole(),
        'constant': SpecXRefRole(),
    }
    initial_data = {
        'objects': {}, # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for (typ, name), doc in self.data['objects'].items():
            if doc == docname:
                del self.data['objects'][typ, name]

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        objects = self.data['objects']
        objtypes = self.objtypes_for_role(typ)
        for objtype in objtypes:
            if (objtype, target) in objects:
                return make_refnode(builder, fromdocname,
                                    objects[objtype, target],
                                    objtype + '-' + target,
                                    contnode, target + ' ' + objtype)

    def get_objects(self):
        for (typ, name), docname in self.data['objects'].iteritems():
            yield name, name, typ, docname, typ + '-' + name, 1


# http://sphinx.pocoo.org/ext/tutorial.html#the-setup-function

def setup(app):
    app.add_domain(SpecDomain)
    app.add_autodocumenter(SpecMacroDocumenter)
    app.add_config_value('autospecmacrodir_process_subdirs', True, True)
