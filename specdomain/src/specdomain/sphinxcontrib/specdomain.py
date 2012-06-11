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


import re
import string

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType, Index
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, TypedField


class SpecDomain(Domain):
    """SPEC language domain."""
    name = 'spec'
    label = 'SPEC'


# http://sphinx.pocoo.org/ext/tutorial.html#the-setup-function

def setup(app):
    app.add_domain(SpecDomain)
    # http://sphinx.pocoo.org/ext/appapi.html#sphinx.domains.Domain
