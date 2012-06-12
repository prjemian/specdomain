#!/usr/bin/env python

# $Id$

'''
Builds Sphinx documentation
(and provides a way to use the source-code debugger for the process)
'''

import os
import sphinx
import sys


def force_rebuild_all():
    if os.path.exists('_build/doctrees'):
        garbage_list = [
            '_build/doctrees/environment.pickle',
            '_build/doctrees/index.doctree',
            '_build/doctrees/test_doc.doctree',
        ]
        for item in garbage_list:
            if os.path.exists(item):
                os.remove(item)
        os.rmdir('_build/doctrees')


if __name__ == '__main__':
    force_rebuild_all()
    args = [sys.argv[0]] + "-b html -d _build/doctrees . _build/html".split()
    sphinx.main(args)