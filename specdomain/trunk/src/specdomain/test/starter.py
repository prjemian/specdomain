#!/usr/bin/env python

# $Id$

'''
Builds Sphinx documentation
(and provides a way to use the source-code debugger for the process)
'''

import os
import sphinx
import sys


def force_rebuild_all(parent = '_build'):
    '''
    Delete the pickle file.
    
    :param str parent: path to *build* subdirectory (either ``build`` or ``_build``)
    '''
    pickle_file = parent+'/doctrees/environment.pickle'
    if os.path.exists(pickle_file):
        os.remove(pickle_file)


if __name__ == '__main__':
    builddir, sourcedir = '_build', '.'
#     builddir, sourcedir = 'build', 'source'
#     os.chdir('/home/prjemian/Documents/eclipse/spec/docs')
    force_rebuild_all(builddir)
    opts = "-b html -d %s/doctrees %s %s/html" % (builddir, sourcedir, builddir)
    args = [sys.argv[0]] + opts.split()
    sphinx.main(args)
