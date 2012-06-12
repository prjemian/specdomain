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


class SpecDomain(Domain):
    """SPEC language domain."""
    name = 'spec'
    label = 'SPEC, http://www.certif.com'


# http://sphinx.pocoo.org/ext/tutorial.html#the-setup-function

def setup(app):
    app.add_domain(SpecDomain)
    # http://sphinx.pocoo.org/ext/appapi.html#sphinx.domains.Domain
