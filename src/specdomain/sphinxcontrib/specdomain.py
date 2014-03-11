# -*- coding: utf-8 -*-
"""
    sphinxcontrib.specdomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: SPEC domain for Sphinx
    
    Automatically insert ReST-formatted extended comments 
    from SPEC files for macro definitions and variable declarations into
    the Sphinx doctree, thus avoiding duplication between docstrings and documentation
    for those who like elaborate docstrings.

    :copyright: Copyright 2012-2014 by BCDA, Advanced Photon Source, Argonne National Laboratory
    :license: ANL Open Source License, see LICENSE for details.
"""

# http://sphinx.pocoo.org/ext/appapi.html

import os
import re

from docutils import nodes

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, TypedField
from sphinx.util.docstrings import prepare_docstring

from sphinx.ext.autodoc import Documenter, bool_option
from specmacrofileparser import SpecMacrofileParser


# TODO: merge these with specmacrofileparser.py
match_all                   = r'.*'
non_greedy_filler           = match_all + r'?'
double_quote_string_match   = r'("' + non_greedy_filler + r'")'
word_match                  = r'((?:[a-z_]\w*))'
cdef_match                  = r'(cdef)'


spec_macro_sig_re = re.compile(
                               r'''^ ([a-zA-Z_]\w*)         # macro name
                               ''', re.VERBOSE)

spec_func_sig_re = re.compile(word_match + r'\('
                      + r'(' + match_all + r')' 
                      + r'\)', 
                      re.IGNORECASE|re.DOTALL)

spec_cdef_name_sig_re = re.compile(double_quote_string_match, 
                                   re.IGNORECASE|re.DOTALL)

# this tool is valuable:  http://www.pythonregex.com/
spec_macro_file_re_str = "\w*.mac"  # TRAC #29: can user provide somehow (can't get to it from here if defined in conf.py)?
spec_macro_file_re = re.compile(spec_macro_file_re_str)


def isSpecMacroFile(filename):
    '''is filename a SPEC macro file?'''
    return os.path.isfile(filename) and len(spec_macro_file_re.findall(filename)) > 0


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
            (Default)
        
        **alphabetical** or **alpha**
            Items will be documented in alphabetical order.
            (Not implemented at present.)
    
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
    #: true if the generated content may contain titles
    titles_allowed = True

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
        """
        # now, parse the SPEC macro file
        macrofile = self.parse_name()
        
        # <hack>
        # SPEC macro files are given by paths relative to documentation tree
        # What about absolute paths?  How does Sphinx handle that?
        # macro directory (with the mac file)
        #mdir = os.path.dirname(os.path.abspath(macrofile))
        # source directory (with the rst file)
        sdir = os.path.abspath(os.path.join(self.directive.env.srcdir, self.directive.env.docname))
        # present directory (where the Makefile started this)
        pdir = os.path.abspath(os.getcwd())
        # get the relative path from sdir to pdir (assumes sdir is below pdir)
        # minus one for the .rst doc at the end
        dir_levels = len(sdir.split(os.sep))-len(pdir.split(os.sep))-1
        macrofile_prefix = '../'*dir_levels
        # </hack>

        spec = SpecMacrofileParser(macrofile)
        extended_comment = spec.ReST()
        rest = prepare_docstring(extended_comment)

        #self.add_line(u'', '<autodoc>')
        #sig = self.format_signature()
        #self.add_directive_header(sig)
        
        self.add_line(u'', '<autodoc>')
        self.add_line(u'.. index:: SPEC macro file; %s' % macrofile, '<autodoc>')
        self.add_line(u'.. index:: !%s' % os.path.split(macrofile)[1], '<autodoc>')
        self.add_line(u'', '<autodoc>')
        self.add_line(u'', '<autodoc>')
        title = 'SPEC Macro File: %s' %  macrofile
        self.add_line('@'*len(title), '<autodoc>')
        self.add_line(title, '<autodoc>')
        self.add_line('@'*len(title), '<autodoc>')
        self.add_line(u'', '<autodoc>')
        # TODO: provide links from each to highlighted source code blocks (like Python documenters).
        # This will have to do for now.
        line = 'source code:  :download:`%s <%s>`' % (os.path.basename(macrofile), macrofile_prefix+macrofile)
        self.add_line(line, macrofile)

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
        """
        ret = self.name
        self.fullname = os.path.abspath(ret)
        self.objpath, self.modname = os.path.split(self.fullname)
        self.args = None
        self.retann = None
        if self.args or self.retann:
            self.directive.warn('signature arguments or return annotation '
                                'given for autospecmacro %s' % self.fullname)
        return ret


class SpecDirDocumenter(Documenter):
    """
    Document a directory containing SPEC macro source code files.
    
    This code responds to the ReST file directive::
    
        .. autospecdir:: partial/path/name
    """
    objtype = 'specdir'
    member_order = 50
    priority = 0
    #: true if the generated content may contain titles
    titles_allowed = True
    option_spec = {
        'include_subdirs': bool_option,
    }

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return membername in ('SpecDirDocumenter', )
    
    def generate(self, *args, **kw):
        """
        Look at the named directory and generate reST for the 
        object given by *self.name*, and possibly for its members.
        """
        # now, parse the .mac files in the SPEC directory
        specdir = self.name
#        self.add_line(u'', '<autodoc>')
#        self.add_line(u'directory:\n   ``%s``' % specdir, '<autodoc>')
        macrofiles = []
        if os.path.exists(specdir):
            # TODO: support a user choice for pattern match to the file name (glob v. re)
            # see https://subversion.xray.aps.anl.gov/trac/bcdaext/ticket/29
            for f in sorted(os.listdir(specdir)):
                filename = os.path.join(specdir, f)
                if isSpecMacroFile(filename):
                    # TODO: support the option to include subdirectories (include_subdirs)
                    # TODO: do not add the same SPEC macro file more than once
                    macrofiles.append(filename)
        else:
            self.add_line(u'', '<autodoc>')
            self.add_line(u'Could not find directory: ``%s``' % specdir, '<autodoc>')
        if len(macrofiles) > 0:
            self.add_line(u'', '<autodoc>')
            self.add_line(u'.. rubric:: List of SPEC Macro Files in *%s*' % specdir, '<autodoc>')
            self.add_line(u'', '<autodoc>')
            for filename in macrofiles:
                # Show a bullet list at the top of the page
                # This is an alternative to separate pages for each macro file
                self.add_line(u'* :ref:`%s <%s>`' % (filename, filename), '<autodoc>')
            self.add_line(u'', '<autodoc>')
            self.add_line(u'-'*15, '<autodoc>')         # delimiter
            self.add_line(u'', '<autodoc>')
            for filename in macrofiles:
                self.add_line(u'', '<autodoc>')
                self.add_line(u'.. _%s:' % filename, '<autodoc>')
                self.add_line(u'.. autospecmacro:: %s' % filename, '<autodoc>')
                # TODO: any options?
                self.add_line(u'', '<autodoc>')
                # TODO: suppress delimiter after last file
                self.add_line(u'-'*15, '<autodoc>')         # delimiter between files


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
        targetname = 'macro:%s:%s:%s:%s' % (self.objtype, name, signode.source, str(signode.line))
        signode['ids'].append(targetname)
        self.state.document.note_explicit_target(signode)
        indextext = self._get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext, targetname, ''))
            self.indexnode['entries'].append(('single', sig, targetname, ''))
            # TODO: what if there is more than one file, same name, different path?
            filename = os.path.split(signode.document.current_source)[1]
            if isSpecMacroFile(filename):
                indextext = '%s; %s' % (filename, sig)
                self.indexnode['entries'].append(('single', indextext, targetname, ''))

    macro_types = {
        'def':  'SPEC macro definition; %s',
        'rdef': 'SPEC run-time macro definition; %s',
        'cdef': 'SPEC chained macro definition; %s',
    }

    def _get_index_text(self, name):
        if self.objtype in self.macro_types:
            return _(self.macro_types[self.objtype]) % name
        else:
            return ''

    def handle_signature(self, sig, signode):
        '''return the name of this object from its signature'''
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

    def handle_signature(self, sig, signode):
        '''return the name of this object from its signature'''
        # TODO: Should it match a regular expression?
        # TODO: What if global or local?  
        signode += addnodes.desc_name(sig, sig)
        return sig

    def add_target_and_index(self, name, sig, signode):
        #text = u'! ' + sig      # TODO: How to use emphasized index entry in this context?
        text = name.split()[0]   # when sig = "tth    #: scattering angle"
        targetname = 'var:%s:%s:%s:%s' % (self.objtype, text, signode.source, str(signode.line))
        signode['ids'].append(targetname)
        # TODO: role does not point back to it yet
        # http://sphinx.pocoo.org/markup/misc.html#directive-index
        self.indexnode['entries'].append(('single', text, targetname, ''))
        text = u'SPEC %s variable; %s' % (self.objtype, sig)
        self.indexnode['entries'].append(('single', text, targetname, ''))

class SpecXRefRole(XRefRole):
    """ Cross-reference the roles in specdomain """
    
    def process_link(self, env, refnode, has_explicit_title, title, target):
        """Called after parsing title and target text, and creating the
        reference node (given in *refnode*).  This method can alter the
        reference node and must return a new (or the same) ``(title, target)``
        tuple.
        """
        key = ":".join((refnode['refdomain'], refnode['reftype']))
        value = env.temp_data.get(key)
        refnode[key] = value
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
        """Called before returning the finished nodes.  *node* is the reference
        node if one was created (*is_ref* is then true), else the content node.
        This method can add other nodes and must return a ``(nodes, messages)``
        tuple (the usual return value of a role function).
        """
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
        targetnode = nodes.target(node.rawsource, '', ids=[tgtid])
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
    app.add_autodocumenter(SpecDirDocumenter)
    app.add_config_value('autospecmacrodir_process_subdirs', True, True)
