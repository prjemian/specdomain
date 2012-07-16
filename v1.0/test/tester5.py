'''
Created on Jul 6, 2012

@author: Pete

Correct the parser's match to macro function declarations
'''

import re


barrage = '''
def uascanFindFactor(start center finish numPts exponent minStep) '{                                                                                            
def _usaxs_triangulate (rot,center,dist) '{                                                                                                                     
def uascanStepFunc(x, factor, center, exponent, minStep) '{                                                                                                     
'''

spec_function_declaration_match_re = re.compile(
                              r'^'                      # line start
                            + r'\s*?'                   # optional blank space
                            + r'(r?def)'                # 0: def_type (rdef | def)
                            + r'\s*?'                   # optional blank space
                            + r'([a-zA-Z_][\w_]*)'      # 1: function_name
                            + r'\s*?'                   # optional blank space
                            + r'\('                     # opening parenthesis
                            + r'(.*?)'                  # 2: args (anything between the parentheses)
                            + r'\)'                     # closing parenthesis
                            + r'\s*?'                   # optional blank space
                            + r'\''                     # open macro content
                            + r'(.*?)'                  # 3: content, optional
                            + r'(#.*?)?'                # 4: optional comment
                            + r'$'                      # line end
                        )

if __name__ == '__main__':
    for line in barrage.split('\n'):
        m = spec_function_declaration_match_re.match(line)
        if m is not None:
            print m.groups()