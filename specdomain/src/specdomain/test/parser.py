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
"""

import os
import re


class SpecMacrofileParser:
    '''
    Parse a SPEC macro file for macro definitions, 
    variable declarations, and extended comments.
    '''

    def __init__(self, macrofile):
        '''
        Constructor
        '''
        self.filename = macrofile
        if not os.path.exists(macrofile):
            raise Exception, "file not found: " + str(macrofile)


if __name__ == '__main__':
    p = SpecMacrofileParser('test-battery.mac')
    p = SpecMacrofileParser('cdef-examples.mac')
    pass
