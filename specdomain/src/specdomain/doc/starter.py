#!/usr/bin/env python

# $Id$

'''
Builds Sphinx documentation
(and provides a way to use the source-code debugger for the process)
'''

import sphinx, sys

if __name__ == '__main__':
    args = []
    args.append(sys.argv[0])
    args = args + "-b html".split()
    args = args + "-d _build/doctrees .".split()
    args = args + "_build/html".split()
    sphinx.main(args)