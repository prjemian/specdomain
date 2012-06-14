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
    Delete the *doctrees* subdirectory.
    
    :param str parent: path to *build* subdirectory (either ``build`` or ``_build``)
    '''
    if os.path.exists(parent):
        garbage_list = [
            parent+'/doctrees/environment.pickle',
            parent+'/doctrees/index.doctree',
            parent+'/doctrees/test_doc.doctree',
        ]
        for item in garbage_list:
            if os.path.exists(item):
                os.remove(item)
        os.rmdir(parent+'/doctrees')


if __name__ == '__main__':
    force_rebuild_all()
    args = [sys.argv[0]] + "-b html -d _build/doctrees . _build/html".split()
    sphinx.main(args)
