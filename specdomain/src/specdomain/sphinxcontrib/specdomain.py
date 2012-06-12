# -*- coding: utf-8 -*-
"""
    sphinxcontrib.specdomain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    SPEC domain.

    :copyright: Copyright 2012 by Pete Jemian
    :license: BSD, see LICENSE for details.
"""

# $Id: $

# http://sphinx.pocoo.org/ext/appapi.html


import re                                               #@UnusedImport
import string                                           #@UnusedImport

from docutils import nodes                              #@UnusedImport
from docutils.parsers.rst import directives             #@UnusedImport

from sphinx import addnodes                             #@UnusedImport
from sphinx.roles import XRefRole                       #@UnusedImport
from sphinx.locale import l_, _                         #@UnusedImport
from sphinx.directives import ObjectDescription         #@UnusedImport
from sphinx.domains import Domain, ObjType, Index       #@UnusedImport
from sphinx.util.compat import Directive                #@UnusedImport
from sphinx.util.nodes import make_refnode              #@UnusedImport
from sphinx.util.docfields import Field, TypedField     #@UnusedImport


class SpecObject(ObjectDescription):
    """
    Description of a SPEC object (macro definition or variable).
    """
    def _get_index_text(self, name):
        if self.objtype == 'def':
            return _('%s (SPEC macro)') % name
        elif self.objtype == 'rdef':
            return _('%s (SPEC macro)') % name
        elif self.objtype == 'cdef':
            return _('%s (SPEC global)') % name
        else:
            return ''


class SpecXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['spec:def'] = env.temp_data.get('spec:def')
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


class SpecDomain(Domain):
    """SPEC language domain."""
    name = 'spec'
    label = 'SPEC, http://www.certif.com'
    object_types = {    # type of object that a domain can document
        'def':  ObjType(l_('def'),  'def'),
        'rdef': ObjType(l_('rdef'), 'rdef'),
        'cdef': ObjType(l_('cdef'), 'cdef'),
    }
    directives = {
        'def':          SpecObject,
        'rdef':         SpecObject,
        'cdef':         SpecObject,
    }
    roles = {
        'def' :  SpecXRefRole(),
        'rdef':  SpecXRefRole(),
        'cdef':  SpecXRefRole(),
    }
    #indices = [
    #    SpecMacroIndex,
    #]


# http://sphinx.pocoo.org/ext/tutorial.html#the-setup-function

def setup(app):
    app.add_domain(SpecDomain)
    # http://sphinx.pocoo.org/ext/appapi.html#sphinx.domains.Domain
