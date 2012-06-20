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

from docutils.statemachine import ViewList, string2lines
import sphinx.util.nodes


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


class SpecMacroSourceObject(ObjectDescription):
    """
    Document a SPEC macro source code file
    
    This code responds to the ReST file directive::
    
        .. spec:macrofile:: partial/path/name/somefile.mac
            :displayorder: fileorder
    
    The ``:displayorder`` parameter indicates how the
    contents will be sorted for appearance in the ReST document.
    
        **fileorder**, **file**
            Items will be documented in the order in 
            which they appear in the ``.mac`` file.
        
        **alphabetical**, **alpha**
            Items will be documented in alphabetical order.
    
    A (near) future enhancement would be to provide for
    documenting all macro files in a directory, with optional
    recursion into subdirectories.  By default, the code would 
    only document files that match the glob pattern ``*.mac``.
    Such as::
    
       .. spec:directory:: partial/path/name
          :recursion:
          :displayorder: alphabetical
    """
    
    # TODO: work-in-progress
    
    doc_field_types = [
        Field('displayorder', label=l_('Display order'), has_arg=False,
              names=('displayorder', 'synonym')),
    ]

    def add_target_and_index(self, name, sig, signode):
        targetname = '%s-%s' % (self.objtype, name)
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        indextext = sig
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              targetname, ''))

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(sig, sig)
        # TODO: this is the place to parse the SPEC macro source code file named in "sig"
        '''
        Since 2002, SPEC has allowed for triple-quoted strings as extended comments.
        Few, if any, have used them.
        Assume that they will contain ReST formatted comments.
        The first, simplest thing to do is to read the .mac file and only extract
        all the extended comments and add them as nodes to the current document.
        
        An additional step would be to parse for def, cdef, rdef, global, local, const, ...
        Another step would be to attach source code and provide links from each to
        highlighted source code blocks.
        '''
        extended_comments_list = self.parse_macro_file(sig)
        view = ViewList([u'TODO: recognize the ReST formatting in the following extended comment and it needs to be cleaned up'])
        #contentnode = nodes.TextElement()
        node = nodes.paragraph()
        node.document = self.state.document
        self.state.nested_parse(view, 0, signode)
        # TODO: recognize the ReST formatting in the following extended comment and it needs to be cleaned up
        # nodes.TextElement(raw, text)
        # sphinx.directives.__init__.py  ObjectDescription.run() method
        #  Summary:  This does not belong here, in the signature processing part.
        #            Instead, it goes at the directive.run() method.  Where's that here?
#        for extended_comment in extended_comments_list:
#            for line in string2lines(extended_comment):
#                view = ViewList([line])
#                nested_parse_with_titles(self.state, view, signode)
        return sig
    
    def XX_run(self):
        # TODO: recognize the ReST formatting in the following extended comment and it needs to be cleaned up
        # nodes.TextElement(raw, text)
        # sphinx.directives.__init__.py  ObjectDescription.run() method
        #  Summary:  This does not belong here, in the signature processing part.
        #            Instead, it goes at the directive.run() method.  This is the new place!
        pass
    
    def parse_macro_file(self, filename):
        """
        parse the SPEC macro file and return the ReST blocks
        
        :param str filename: name (with optional path) of SPEC macro file
            (The path is relative to the ``.rst`` document.)
        :returns [str]: list of ReST-formatted extended comment blocks (docstrings) from SPEC macro file.
        
        [future] parse more stuff as planned, this is very simplistic for now
        """
        results = []
        if not os.path.exists(filename):
            raise RuntimeError, "could not find: " + filename
        
        buf = open(filename, 'r').read()
        #n = len(buf)
        for node in spec_extended_comment_block_sig_re.finditer(buf):
            #g = node.group()
            #gs = node.groups()
            #s = node.start()
            #e = node.end()
            #t = buf[s:e]
            results.append(node.groups()[0])            # TODO: can we get line number also?
        return results


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
        'def':    ObjType(l_('def'),    'def'),
        'rdef':   ObjType(l_('rdef'),   'rdef'),
        'cdef':   ObjType(l_('cdef'),   'cdef'),
        'global': ObjType(l_('global'), 'global'),
        'local':  ObjType(l_('local'),  'local'),
    }
    directives = {
        'def':          SpecMacroObject,
        'rdef':         SpecMacroObject,
        'cdef':         SpecMacroObject,
        'global':       SpecVariableObject,
        'local':        SpecVariableObject,
        'macrofile':    SpecMacroSourceObject,
    }
    roles = {
        'def' :     SpecXRefRole(),
        'rdef':     SpecXRefRole(),
        'cdef':     SpecXRefRole(),
        'global':   SpecXRefRole(),
        'local':    SpecXRefRole(),
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
    # http://sphinx.pocoo.org/ext/appapi.html#sphinx.domains.Domain
