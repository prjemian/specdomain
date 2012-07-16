#!/usr/bin/env python

# $Id: starter.py 938 2012-06-15 23:10:56Z jemian $

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
    force_rebuild_all()
    args = [sys.argv[0]] + "-b html -d _build/doctrees . _build/html".split()
    sphinx.main(args)
